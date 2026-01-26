# -*- coding: utf-8 -*-
{
    'name': 'Subscription Manager',
    'version': '17.0.1.0.0',
    'category': 'Services',
    'summary': 'Monitor and manage infrastructure subscriptions and prevent service downtime',
    'description': """
Subscription Manager
====================
A comprehensive monitoring system for infrastructure subscriptions (VPS, domains, SSL, etc.)
that prevents service downtime due to missed payments.

Key Features:
* Service inventory management
* Subscription lifecycle tracking
* Vendor bill integration
* Automated reminders (H-30, H-14, H-7, H-3)
* Role-based access control (Admin, DevOps, Finance, Manager)
* Secure credential storage
* Risk-based criticality levels

This module integrates with Odoo Accounting module to use vendor bills as the single
source of truth for payments, ensuring proper audit trails and financial control.
    """,
    'author': 'Muhammad Rheza Alfin',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'account',
        'mail',
    ],
    'data': [
        # Security
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'security/security_rules.xml',
        
        # Data
        'data/criticality_data.xml',
        'data/cron_data.xml',
        
        # Views
        'views/dashboard_views.xml',
        'views/criticality_views.xml',
        'views/service_views.xml',
        'views/subscription_views.xml',
        'views/credential_views.xml',
        'views/menu_views.xml',
        # Reveal wizard removed
    ],
    'images': [
        'static/description/icon.png',
        'static/description/icon.svg',
    ],
    'assets': {
        'web.assets_backend': [
            # copy_password asset removed
        ],
    },
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
