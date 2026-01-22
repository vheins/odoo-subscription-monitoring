# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Criticality(models.Model):
    """Risk level model for prioritizing services."""
    _name = 'sm.criticality'
    _description = 'Service Criticality Level'
    _order = 'level desc, name'

    name = fields.Char(
        string='Name',
        required=True,
        translate=True,
        help='Criticality level name (e.g., Mission Critical, High, Medium, Low)'
    )
    level = fields.Integer(
        string='Priority Level',
        required=True,
        default=1,
        help='Numeric priority level (higher = more critical)'
    )
    alert_days = fields.Integer(
        string='Default Alert Days',
        default=30,
        help='Default number of days before expiry to start sending reminders'
    )
    color = fields.Integer(
        string='Color Index',
        default=0,
        help='Color for UI display'
    )
    description = fields.Text(
        string='Description',
        help='Description of what this criticality level means'
    )
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Criticality name must be unique!'),
    ]
