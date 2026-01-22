# Odoo Subscription Manager

A comprehensive monitoring system for infrastructure subscriptions (VPS, domains, SSL certificates, etc.) that prevents service downtime due to missed payments.

## Features

### Core Features
- **Service Inventory Management**: Track all your infrastructure services in one place
- **Subscription Lifecycle Tracking**: Monitor billing cycles and renewal dates automatically
- **Vendor Bill Integration**: Integrates with Odoo Accounting for payment tracking
- **Automated Reminders**: Get notified at H-30, H-14, H-7, and H-3 days before expiry
- **Risk-Based Criticality**: Prioritize services based on business impact
- **Secure Credential Storage**: Store access credentials with role-based visibility

### Role-Based Access Control
- **Admin**: Full access to all features
- **DevOps**: Manage services and view credentials, read-only on financial data
- **Finance**: Manage subscriptions and vendor bills, no access to technical credentials
- **Manager**: Read-only strategic overview, no access to credentials

## Installation

### Prerequisites
- Odoo Community 19.0 or higher
- Accounting module enabled

### Installation Steps

1. **Clone or download this repository** to your Odoo addons directory:
   ```bash
   cd /path/to/odoo/addons
   git clone https://github.com/vheins/odoo-subscription-monitoring.git
   ```

2. **Restart Odoo** server:
   ```bash
   odoo-bin -c /path/to/odoo.conf
   ```

3. **Update Apps List**:
   - Go to Apps menu in Odoo
   - Click "Update Apps List"

4. **Install the module**:
   - Search for "Subscription Manager"
   - Click "Install"

## Quick Start

### 1. Configure Criticality Levels
Go to: **Subscription Manager > Configuration > Criticality Levels**
- Default levels are pre-configured (Low, Medium, High, Mission Critical)
- Customize alert days based on your needs

### 2. Add Vendors
Go to: **Subscription Manager > Vendors**
- Create or link existing vendor partners
- Add contact information and portal URLs

### 3. Create Services
Go to: **Subscription Manager > Services**
- Add your infrastructure services (VPS, domains, etc.)
- Assign vendor and criticality level
- Add technical details (IP address, hostname)

### 4. Setup Subscriptions
Go to: **Subscription Manager > Subscriptions**
- Create subscription contracts for each service
- Set billing interval (monthly, quarterly, annual)
- Define renewal dates and amounts

### 5. Link Vendor Bills
When you receive and create vendor bills in Odoo Accounting:
- Link them to the corresponding subscription
- When marked as "Paid", the subscription automatically renews

## Usage

### For DevOps
- Monitor service health and expiry dates
- Access technical credentials securely
- Receive alerts for critical services approaching expiry

### For Finance
- View all upcoming payment obligations
- Process vendor bills and payments
- Track payment history and renewal cycles

### For Managers
- View dashboard for strategic overview
- Monitor risk exposure
- Track infrastructure costs

## Module Structure

```
odoo-subscription-monitoring/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── criticality.py      # Risk levels
│   ├── service.py          # Service inventory
│   ├── subscription.py     # Subscription contracts
│   └── credential.py       # Access credentials
├── views/
│   ├── menu_views.xml
│   ├── criticality_views.xml
│   ├── service_views.xml
│   ├── subscription_views.xml
│   ├── credential_views.xml
│   └── dashboard_views.xml
├── security/
│   ├── security_groups.xml # User groups
│   ├── ir.model.access.csv # Access rights
│   └── security_rules.xml  # Record rules
└── data/
    ├── criticality_data.xml # Default data
    └── cron_data.xml        # Scheduled jobs
```

## Key Principles

1. **Accounting is Single Source of Truth**: All payment data comes from Odoo Accounting
2. **No Manual Renewals**: Subscriptions only renew when vendor bills are marked as paid
3. **Principle of Least Privilege**: Users only see data relevant to their role
4. **Audit Trail**: All changes are tracked and logged

## Workflow

1. Service is created and linked to a vendor
2. Subscription is created with billing details
3. System monitors and sends automated reminders
4. Finance creates vendor bill in Odoo Accounting
5. Finance processes payment
6. When bill is marked "Paid", subscription automatically renews
7. Process repeats for next billing cycle

## Support

For issues, questions, or contributions, please visit the GitHub repository:
https://github.com/vheins/odoo-subscription-monitoring

## License

LGPL-3

## Credits

Developed for Odoo Community 19.0

