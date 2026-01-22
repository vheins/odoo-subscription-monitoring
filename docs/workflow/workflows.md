# 🔄 Workflows — Subscription Manager

## 1. Subscription Lifecycle
This workflow defines the state transitions of a subscription, driven by time and payment events.

```mermaid
stateDiagram-v2
    [*] --> Active: Created

    state Active {
        [*] --> Running
        Running --> ExpiringSoon: Days Left <= 30
    }

    state ExpiringSoon {
        [*] --> Alerting
        Alerting --> Expired: Days Left <= 0
        Alerting --> Renewed: Bill Paid
    }

    state Expired {
        [*] --> Overdue
        Overdue --> Terminated: Service Stopped
        Overdue --> Renewed: Late Payment
    }

    Renewed --> Active: New Period Starts
    Terminated --> [*]

    note right of Alerting
        Triggers ir.activity:
        H-30, H-14, H-7, H-3
    end note
```

### Key Rules
*   **Automatic Transitions:** `Active` → `Expiring Soon` → `Expired` are driven purely by time (cron jobs).
*   **Manual/Event Transitions:** `Renewed` is triggered by a Payment event. `Terminated` is a manual decision.

---

## 2. Vendor Bill & Renewal Flow
This flowchart details how the Accounting module triggers a subscription renewal.

```mermaid
flowchart TD
    subgraph "Subscription Manager"
        Sub[Subscription: Expiring Soon]
    end

    subgraph "Odoo Accounting"
        BillDraft[Vendor Bill: Draft]
        BillPosted[Vendor Bill: Posted]
        Payment[Payment Registered]
        BillPaid[Vendor Bill: Paid]
    end

    %% Flow
    Sub -- "Finance creates Bill" --> BillDraft
    BillDraft -- "Finance Validates" --> BillPosted
    BillPosted -- "Finance Pays" --> Payment
    Payment -- "Reconciliation" --> BillPaid

    %% Feedback Loop
    BillPaid -- "Trigger Renewal" --> Sub

    %% Logic
    Sub -- "Update Date & Hist." --> Sub

    %% Styling
    classDef acc fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef sub fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px;

    class BillDraft,BillPosted,Payment,BillPaid acc;
    class Sub sub;
```

### Integration Logic
1.  **Manual-First:** The Vendor Bill is typically created manually by Finance based on the Vendor's invoice.
2.  **Linking:** The Bill must be linked to the `sm.subscription` record (Many2one).
3.  **Trigger:** The Subscription Manager listens for the `account.move` state change to `paid`.
4.  **Action:** Upon `paid` status, the Subscription logic adds the billing interval to the `next_renewal_date`.
