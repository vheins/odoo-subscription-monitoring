# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import AccessError


class Credential(models.Model):
    """Secure credential storage for service access."""
    _name = 'sm.credential'
    _description = 'Service Credential'
    _order = 'service_id, name'

    name = fields.Char(
        string='Credential Name',
        required=True,
        help='Descriptive name for this credential (e.g., Root SSH, Admin Panel)'
    )
    
    service_id = fields.Many2one(
        'sm.service',
        string='Service',
        required=True,
        ondelete='cascade'
    )
    
    credential_type = fields.Selection([
        ('ssh', 'SSH Access'),
        ('portal', 'Vendor Portal'),
        ('api', 'API Key'),
        ('panel', 'Control Panel'),
        ('other', 'Other'),
    ], string='Type', required=True, default='portal')
    
    username = fields.Char(string='Username')
    password = fields.Char(string='Password/Secret')
    url = fields.Char(string='URL/Endpoint')
    port = fields.Char(string='Port')
    
    notes = fields.Text(string='Notes')
    
    # Masked password helper (visible to all as masked)
    password_mask = fields.Char(
        string='Password Mask',
        compute='_compute_password_mask',
        readonly=True,
    )

    # Security: These fields will be restricted via record rules

    @api.depends('password')
    def _compute_password_mask(self):
        for rec in self:
            if rec.password:
                # show fixed-length mask to avoid revealing password length
                rec.password_mask = '••••••'
            else:
                rec.password_mask = ''

    def action_reveal_password(self):
        """Open a reveal wizard showing the plain password and log the reveal action.

        Only users in DevOps or Admin groups are allowed to reveal.
        """
        self.ensure_one()
        allowed = self.env.user.has_group('subscription_monitoring.group_subscription_devops') or self.env.user.has_group('subscription_monitoring.group_subscription_admin')
        if not allowed:
            raise AccessError('You are not allowed to reveal credentials')

        # create audit log
        self.env['sm.credential.access.log'].create({
            'credential_id': self.id,
            'user_id': self.env.user.id,
            'action': 'reveal',
        })

        wizard = self.env['sm.credential.reveal.wizard'].create({'password': self.password or ''})
        return {
            'name': 'Reveal Password',
            'type': 'ir.actions.act_window',
            'res_model': 'sm.credential.reveal.wizard',
            'res_id': wizard.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def rpc_log_copy(self):
        """RPC method used by JS to log a copy action.

        Returns True on success.
        """
        for rec in self:
            # restrict to allowed groups
            if not (self.env.user.has_group('subscription_monitoring.group_subscription_devops') or self.env.user.has_group('subscription_monitoring.group_subscription_admin')):
                raise AccessError('You are not allowed to copy credentials')
            self.env['sm.credential.access.log'].create({
                'credential_id': rec.id,
                'user_id': self.env.user.id,
                'action': 'copy',
            })
        return True
