# 🗄️ Entity Relationship Diagram (ERD)

## 1. Data Model Overview
The data model is built to minimize redundancy with Odoo Core. Custom models (`sm.*`) are used only when no suitable standard model exists.

```mermaid
erDiagram
    %% Core Odoo Models
    res_partner ||--|{ sm_service : "Vendor for"
    res_partner ||--|{ sm_service : "Client for"
    res_partner ||--|{ sm_subscription : "Vendor for"
    account_move ||--|| sm_subscription : "Links to (Last Bill)"
    res_currency ||--|{ sm_subscription : "Currency"

    %% Custom Models
    sm_service ||--|{ sm_subscription : "Has History"
    sm_service ||--|| sm_subscription : "Current Active"
    sm_service ||--|{ sm_credential : "Has Access"
    sm_criticality ||--|{ sm_service : "Defines Risk"

    %% Entity Definitions
    sm_service {
        string name
        selection type "VPS/Domain/SSL"
        selection state "Active/Terminated"
    }

    sm_subscription {
        date date_start
        date next_renewal_date
        integer billing_interval "Months"
        float amount
        selection state "Active/Expiring/Expired"
    }

    sm_credential {
        string name
        string username
        string password_encrypted
        selection type "SSH/Portal/API"
    }

    sm_criticality {
        string name
        integer level
        string color
    }
```

---

## 2. Entity Specifications

### `sm.service` (Service Registry)
*   **Description:** The central inventory item being monitored.
*   **Key Relationships:**
    *   `partner_id`: Many2one to `res.partner` (Vendor).
    *   `client_id`: Many2one to `res.partner` (Client/Customer) - *Optional*.
    *   `subscription_ids`: One2many to `sm.subscription` (History).
    *   `credential_ids`: One2many to `sm.credential`.
    *   `criticality_id`: Many2one to `sm.criticality`.

### `sm.subscription` (Subscription Contract)
*   **Description:** Represents the billing cycle and financial obligation.
*   **Key Fields:**
    *   `date_start`: Date.
    *   `next_renewal_date`: Date (Computed/Editable).
    *   `billing_interval`: Integer (Months).
    *   `amount`: Float (Estimated cost).
    *   `state`: Selection (Active, Expiring Soon, Expired) - *Computed*.
*   **Key Relationships:**
    *   `service_id`: Many2one to `sm.service`.
    *   `last_bill_id`: Many2one to `account.move` (Latest linked bill).

### `sm.credential` (Access Repository)
*   **Description:** Secure storage for technical access details.
*   **Security:** Field-level security rules applied (Hidden from Finance/Manager).
*   **Key Fields:**
    *   `type`: Selection (SSH, Portal, API Key).
    *   `secret`: Char (Encrypted/Password widget).

### `sm.criticality` (Risk Level)
*   **Description:** Configurable risk levels for prioritization.
*   **Fields:** `name` (e.g., "Mission Critical"), `alert_days` (default reminder threshold).
