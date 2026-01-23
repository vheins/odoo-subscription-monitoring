# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class Subscription(models.Model):
    """Subscription contract model for managing billing cycles."""
    _name = 'sm.subscription'
    _description = 'Subscription'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'next_renewal_date, id'

    name = fields.Char(
        string='Reference',
        compute='_compute_name',
        store=True
    )
    
    # Core Relationships
    service_id = fields.Many2one(
        'sm.service',
        string='Service',
        required=True,
        ondelete='cascade',
        tracking=True
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Vendor',
        required=True,
        domain=[('supplier_rank', '>', 0)],
        tracking=True
    )
    
    # Billing Information
    date_start = fields.Date(
        string='Start Date',
        required=True,
        default=fields.Date.today,
        tracking=True,
        help='Date when this subscription period started'
    )
    billing_interval = fields.Integer(
        string='Billing Interval (Months)',
        required=True,
        default=12,
        tracking=True,
        help='Payment cycle in months (1=Monthly, 3=Quarterly, 6=Semi-Annual, 12=Annual)'
    )
    next_renewal_date = fields.Date(
        string='Next Renewal Date',
        required=True,
        tracking=True,
        help='Next payment due date'
    )
    
    # Financial
    amount = fields.Monetary(
        string='Amount',
        required=True,
        tracking=True,
        help='Estimated cost per billing interval'
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True,
        default=lambda self: self.env.company.currency_id
    )
    
    # Vendor Bill Integration
    last_bill_id = fields.Many2one(
        'account.move',
        string='Last Vendor Bill',
        domain=[('move_type', '=', 'in_invoice')],
        tracking=True,
        help='Link to the latest vendor bill for this subscription'
    )
    bill_state = fields.Selection(
        related='last_bill_id.state',
        string='Bill Status',
        store=True
    )
    payment_state = fields.Selection(
        related='last_bill_id.payment_state',
        string='Payment Status',
        store=True
    )
    
    # Status (Computed)
    state = fields.Selection([
        ('active', 'Active'),
        ('expiring_soon', 'Expiring Soon'),
        ('expired', 'Expired'),
    ], string='Status', compute='_compute_state', store=True, tracking=True)
    
    days_left = fields.Integer(
        string='Days Left',
        compute='_compute_days_left',
        store=True
    )
    
    # Notes
    description = fields.Html(string='Notes')
    
    @api.model_create_multi
    def create(self, vals_list):
        """Override create to compute next_renewal_date if not provided."""
        for vals in vals_list:
            if 'next_renewal_date' not in vals and 'date_start' in vals and 'billing_interval' in vals:
                date_start = fields.Date.to_date(vals['date_start'])
                billing_interval = vals['billing_interval']
                vals['next_renewal_date'] = date_start + relativedelta(months=billing_interval)
        return super(Subscription, self).create(vals_list)
    
    @api.depends('service_id', 'partner_id')
    def _compute_name(self):
        """Generate subscription reference name."""
        for sub in self:
            if sub.service_id and sub.partner_id:
                sub.name = f"{sub.service_id.name} - {sub.partner_id.name}"
            else:
                sub.name = "New Subscription"
    
    @api.onchange('date_start', 'billing_interval')
    def _onchange_compute_next_renewal_date(self):
        """Calculate initial next renewal date when creating subscription."""
        for sub in self:
            if sub.date_start and sub.billing_interval and not sub.next_renewal_date:
                sub.next_renewal_date = sub.date_start + relativedelta(months=sub.billing_interval)
    
    def renew_subscription(self):
        """Renew subscription by extending the next renewal date.
        This should be called when a vendor bill is marked as paid.
        """
        self.ensure_one()
        if self.next_renewal_date and self.billing_interval:
            new_renewal_date = self.next_renewal_date + relativedelta(months=self.billing_interval)
            self.write({
                'next_renewal_date': new_renewal_date,
            })
            self.message_post(
                body=f"Subscription renewed. New renewal date: {new_renewal_date}",
                subject="Subscription Renewed"
            )
            return True
        return False
    
    @api.depends('next_renewal_date')
    def _compute_days_left(self):
        """Calculate days remaining until renewal."""
        today = date.today()
        for sub in self:
            if sub.next_renewal_date:
                delta = sub.next_renewal_date - today
                sub.days_left = delta.days
            else:
                sub.days_left = 0
    
    @api.depends('days_left', 'criticality_id.alert_days')
    def _compute_state(self):
        """Compute subscription state based on days left."""
        for sub in self:
            if sub.days_left <= 0:
                sub.state = 'expired'
            elif sub.days_left <= (sub.service_id.criticality_id.alert_days or 30):
                sub.state = 'expiring_soon'
            else:
                sub.state = 'active'
    
    # Related fields for easier access
    criticality_id = fields.Many2one(
        related='service_id.criticality_id',
        string='Criticality',
        store=True
    )
    
    @api.model
    def _cron_check_expiring_subscriptions(self):
        """Cron job to check subscriptions and create reminders."""
        today = date.today()
        reminder_days = [30, 14, 7, 3]
        
        for days in reminder_days:
            target_date = today + timedelta(days=days)
            subscriptions = self.search([
                ('next_renewal_date', '=', target_date),
                ('state', 'in', ['active', 'expiring_soon'])
            ])
            
            for sub in subscriptions:
                self._create_renewal_reminder(sub, days)
        
        # Also check expired subscriptions
        expired_subs = self.search([
            ('state', '=', 'expired')
        ])
        for sub in expired_subs:
            self._create_urgent_reminder(sub)
    
    def _create_renewal_reminder(self, subscription, days_before):
        """Create activity reminder for renewal."""
        # Find Finance users
        finance_group = self.env.ref('subscription_monitoring.group_subscription_finance', raise_if_not_found=False)
        if not finance_group:
            return
        
        user_ids = finance_group.users.ids
        if not user_ids:
            user_ids = [self.env.user.id]
        
        activity_type = self.env.ref('mail.mail_activity_data_todo', raise_if_not_found=False)
        
        for user_id in user_ids:
            # Check if activity already exists
            existing = self.env['mail.activity'].search([
                ('res_model', '=', 'sm.subscription'),
                ('res_id', '=', subscription.id),
                ('user_id', '=', user_id),
                ('activity_type_id', '=', activity_type.id if activity_type else False),
                ('date_deadline', '=', subscription.next_renewal_date),
            ], limit=1)
            
            if not existing:
                self.env['mail.activity'].create({
                    'res_model': 'sm.subscription',
                    'res_id': subscription.id,
                    'activity_type_id': activity_type.id if activity_type else False,
                    'summary': f'Subscription Renewal in {days_before} days',
                    'note': f'Service: {subscription.service_id.name}<br/>'
                           f'Vendor: {subscription.partner_id.name}<br/>'
                           f'Amount: {subscription.amount} {subscription.currency_id.name}<br/>'
                           f'Due Date: {subscription.next_renewal_date}',
                    'user_id': user_id,
                    'date_deadline': subscription.next_renewal_date,
                })
    
    def _create_urgent_reminder(self, subscription):
        """Create urgent activity for expired subscription."""
        finance_group = self.env.ref('subscription_monitoring.group_subscription_finance', raise_if_not_found=False)
        if not finance_group:
            return
        
        user_ids = finance_group.users.ids
        if not user_ids:
            user_ids = [self.env.user.id]
        
        activity_type = self.env.ref('mail.mail_activity_data_warning', raise_if_not_found=False)
        
        for user_id in user_ids:
            existing = self.env['mail.activity'].search([
                ('res_model', '=', 'sm.subscription'),
                ('res_id', '=', subscription.id),
                ('user_id', '=', user_id),
                ('state', '!=', 'done'),
            ], limit=1)
            
            if not existing:
                self.env['mail.activity'].create({
                    'res_model': 'sm.subscription',
                    'res_id': subscription.id,
                    'activity_type_id': activity_type.id if activity_type else False,
                    'summary': f'URGENT: Subscription Expired - {subscription.service_id.name}',
                    'note': f'Service: {subscription.service_id.name}<br/>'
                           f'Vendor: {subscription.partner_id.name}<br/>'
                           f'Expired: {subscription.next_renewal_date}<br/>'
                           f'Days Overdue: {abs(subscription.days_left)}',
                    'user_id': user_id,
                    'date_deadline': date.today(),
                })


class AccountMove(models.Model):
    """Extend account.move to trigger subscription renewal when bill is paid."""
    _inherit = 'account.move'
    
    subscription_ids = fields.One2many(
        'sm.subscription',
        'last_bill_id',
        string='Related Subscriptions',
        help='Subscriptions linked to this vendor bill'
    )
    
    def action_post(self):
        """Override to check for subscription renewal when bill is paid."""
        res = super(AccountMove, self).action_post()
        # Check if this is a paid vendor bill with linked subscriptions
        for move in self:
            if move.move_type == 'in_invoice' and move.payment_state == 'paid':
                for subscription in move.subscription_ids:
                    subscription.renew_subscription()
        return res
    
    def _write(self, vals):
        """Override write to detect when payment_state changes to paid."""
        res = super(AccountMove, self)._write(vals)
        if 'payment_state' in vals and vals['payment_state'] == 'paid':
            for move in self:
                if move.move_type == 'in_invoice':
                    for subscription in move.subscription_ids:
                        subscription.renew_subscription()
        return res

