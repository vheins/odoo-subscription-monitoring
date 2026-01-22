# -*- coding: utf-8 -*-

from odoo import models, fields, api


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
    
    # Security: These fields will be restricted via record rules
