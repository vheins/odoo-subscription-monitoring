# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Service(models.Model):
    """Service/Resource inventory model."""
    _name = 'sm.service'
    _description = 'Service'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(
        string='Service Name',
        required=True,
        tracking=True,
        help='Name of the service (e.g., VPS Production, Domain company.com)'
    )
    
    # Service Type
    service_type = fields.Selection([
        ('vps', 'VPS'),
        ('dedicated', 'Dedicated Server'),
        ('cloud', 'Cloud Instance'),
        ('domain', 'Domain Name'),
        ('ssl', 'SSL Certificate'),
        ('email', 'Email Hosting'),
        ('storage', 'Storage/Backup'),
        ('cdn', 'CDN'),
        ('other', 'Other'),
    ], string='Service Type', required=True, default='vps', tracking=True)
    
    # Relationships to res.partner
    partner_id = fields.Many2one(
        'res.partner',
        string='Vendor',
        required=True,
        domain=[('supplier_rank', '>', 0)],
        tracking=True,
        help='Vendor providing this service'
    )
    client_id = fields.Many2one(
        'res.partner',
        string='Client',
        domain=[('customer_rank', '>', 0)],
        tracking=True,
        help='Client/Customer using this service (optional)'
    )
    
    # Operational Status
    state = fields.Selection([
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('terminated', 'Terminated'),
    ], string='Status', default='active', required=True, tracking=True)
    
    # Criticality
    criticality_id = fields.Many2one(
        'sm.criticality',
        string='Criticality',
        required=True,
        tracking=True,
        help='Risk level if this service goes down'
    )
    
    # Technical Details
    ip_address = fields.Char(string='IP Address')
    hostname = fields.Char(string='Hostname')
    location = fields.Char(string='Location/Region')
    
    # Relationships to other models
    subscription_ids = fields.One2many(
        'sm.subscription',
        'service_id',
        string='Subscription History'
    )
    active_subscription_id = fields.Many2one(
        'sm.subscription',
        string='Active Subscription',
        compute='_compute_active_subscription',
        store=True
    )
    credential_ids = fields.One2many(
        'sm.credential',
        'service_id',
        string='Credentials'
    )

    # Dashboard counters
    subscriptions_count = fields.Integer(string='Subscriptions Count', compute='_compute_counts')
    vendor_bills_count = fields.Integer(string='Vendor Bills', compute='_compute_counts')
    vendor_bills_amount = fields.Monetary(string='Vendor Bills Amount', compute='_compute_counts', currency_field='company_currency_id')
    company_currency_id = fields.Many2one('res.currency', string='Company Currency', default=lambda self: self.env.company.currency_id)
    
    # Computed fields for display
    next_renewal_date = fields.Date(
        string='Next Renewal',
        related='active_subscription_id.next_renewal_date',
        store=True
    )
    days_left = fields.Integer(
        string='Days Left',
        related='active_subscription_id.days_left',
        store=True
    )
    subscription_state = fields.Selection(
        string='Subscription Status',
        related='active_subscription_id.state',
        store=True
    )
    
    # Notes
    description = fields.Html(string='Notes')
    
    # Tags
    tag_ids = fields.Many2many(
        'sm.service.tag',
        string='Tags',
        help='Flexible categorization tags'
    )
    
    @api.depends('subscription_ids', 'subscription_ids.state')
    def _compute_active_subscription(self):
        """Find the currently active subscription."""
        for service in self:
            active_subs = service.subscription_ids.filtered(
                lambda s: s.state in ['active', 'expiring_soon']
            )
            service.active_subscription_id = active_subs[0] if active_subs else False

    def action_add_subscription(self):
        """Open a new subscription form pre-filled with this service.

        Returns an action opening `sm.subscription` form in a modal with
        `default_service_id` set so the user can quickly create a subscription.
        """
        self.ensure_one()
        return {
            'name': 'Add Subscription',
            'type': 'ir.actions.act_window',
            'res_model': 'sm.subscription',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_service_id': self.id,
                'default_partner_id': self.partner_id.id if self.partner_id else False,
            },
        }

    def action_view_subscriptions(self):
        self.ensure_one()
        action = self.env.ref('subscription_monitoring.action_sm_subscription').read()[0]
        action.update({
            'domain': [('service_id', '=', self.id)],
        })
        return action

    def action_view_vendor_bills(self):
        """Open vendor bills related to this service via subscriptions."""
        self.ensure_one()
        # collect related bill ids from subscriptions
        bill_ids = self.mapped('subscription_ids.last_bill_id').ids
        action = self.env.ref('account.action_move_in_invoice_type').read()[0]
        action.update({
            'domain': [('id', 'in', bill_ids)],
        })
        return action

    @api.depends('subscription_ids', 'subscription_ids.last_bill_id')
    def _compute_counts(self):
        for service in self:
            subs = service.subscription_ids
            service.subscriptions_count = len(subs)
            bills = subs.mapped('last_bill_id')
            service.vendor_bills_count = len(bills)
            total = sum(bill.amount_total or 0.0 for bill in bills)
            service.vendor_bills_amount = total


class ServiceTag(models.Model):
    """Tags for flexible service categorization."""
    _name = 'sm.service.tag'
    _description = 'Service Tag'
    
    name = fields.Char(string='Tag Name', required=True, translate=True)
    color = fields.Integer(string='Color Index', default=0)
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Tag name must be unique!'),
    ]
