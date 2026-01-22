# 🖥️ UI Specifications & UX

## 1. List Views (Tree Views)

### A. Services List
*   **Path:** `Subscription Manager > Services`
*   **Columns:**
    1.  **Name** (Bold)
    2.  **Vendor** (Link to Partner)
    3.  **Client** (Optional, Link to Partner)
    4.  **Type** (Badge)
    5.  **Criticality** (Colored Badge)
    6.  **Status** (Active/Terminated)
    7.  **Next Renewal** (From active subscription)
*   **Default Sort:** `Criticality` (High to Low), then `Next Renewal`.
*   **Search/Filter:**
    *   Search by Name, Vendor, IP.
    *   Filter: `Active Services`, `My Services`.

### B. Vendors List (Standard Odoo View)
*   **Path:** `Subscription Manager > Vendors`
*   **Source:** `res.partner` with filter `supplier_rank > 0`.
*   **Columns:**
    1.  **Name**
    2.  **Phone**
    3.  **Email**
    4.  **City**
    5.  **Country**
*   **Default Sort:** Name (Ascending).

### C. Vendor Bills List (Standard Odoo View)
*   **Path:** `Subscription Manager > Vendor Bills`
*   **Source:** `account.move` with filter `move_type = 'in_invoice'`.
*   **Columns:**
    1.  **Number**
    2.  **Vendor**
    3.  **Bill Date**
    4.  **Due Date**
    5.  **Total**
    6.  **Payment Status** (Paid/Not Paid)
    7.  **Status** (Posted/Draft)

### D. Credentials List
*   **Path:** `Subscription Manager > Credentials`
*   **Restricted Access:** Visible only to `Admin` and `DevOps`.
*   **Columns:**
    1.  **Name**
    2.  **Service** (Link)
    3.  **Type** (Badge: SSH, API, Portal)
    4.  **Username** (Visible)
    5.  **Password/Secret** (Hidden/Stars `***`)
*   **Security:** Password field must use `password` widget to prevent casual shoulder surfing.

### E. Subscriptions List
*   **Path:** `Subscription Manager > Subscriptions`
*   **Columns:**
    1.  **Service**
    2.  **Vendor**
    3.  **Start Date**
    4.  **Next Renewal** (Red if <= 30 days)
    5.  **Days Left** (Integer, computed)
    6.  **Amount** (Monetary)
    7.  **Status** (Badge: Active/Expiring/Expired)
*   **Default Sort:** `Days Left` (Ascending).
*   **Search/Filter:**
    *   Filter: `Expiring Soon` (<= 30 days), `Expired`.
    *   Group By: `Vendor`, `Status`, `Month`.

---

## 2. Kanban Views

### A. Services Kanban
*   **Visual:** Cards representing servers/services.
*   **Card Content:**
    *   **Title:** Service Name.
    *   **Tags:** Criticality, Type.
    *   **Footer:** Vendor Image, Next Renewal Date.
    *   **Color Indicator:** Based on Criticality.

### B. Subscriptions Kanban
*   **Grouped By:** `Status` (Active | Expiring Soon | Expired).
*   **Card Content:**
    *   **Title:** Service Name.
    *   **Body:** Vendor Name, Amount.
    *   **Badge:** Days Left.
*   **Drag & Drop:** Disabled (Status is computed).

---

## 3. Grouping & Filtering Strategy

### Required Groupings
1.  **Group by Vendor:**
    *   *Business Reason:* Finance processes payments per vendor. Helps in batching bills.
2.  **Group by Client:**
    *   *Business Reason:* To identify which client is using the service (e.g. for re-billing reference).
3.  **Group by Criticality:**
    *   *Business Reason:* Managers need to focus on High/Mission Critical services first.
4.  **Group by Status:**
    *   *Business Reason:* Operational triage (what is active vs what is expired).

### Required Filters
1.  **Expiring Soon (<= 30 Days):** Default filter for Finance dashboard.
2.  **Critical Services:** Shows only High/Mission Critical items.
3.  **Missing Bill:** Subscriptions expiring soon but not linked to a Draft/Posted bill.

---

## 4. Tagging & Notes

### Tagging (`sm.service.tag`)
*   **Mechanism:** Standard Odoo `many2many` tags.
*   **Usage:** Flexible categorization not covered by "Type".
*   **Examples:** `Production`, `Staging`, `Internal`, `Project X`, `Promo`.
*   **Behavior:** Colorized tags in List and Kanban views.

### Internal Notes
*   **Field:** `description` (Html field).
*   **Placement:** Tab "Notes" in Service and Subscription forms.
*   **Usage:**
    *   Technical specs (OS version, RAM).
    *   Business decisions ("Do not renew next year").
    *   Manual history log.

---

## 5. Security & Visibility (UI Level)

*   **Credential Tab:**
    *   Visible to: `Admin`, `DevOps`.
    *   Hidden from: `Finance`, `Manager`.
*   **Cost/Amount Fields:**
    *   Visible to: `Admin`, `Finance`, `Manager`.
    *   Hidden from: `DevOps` (Optional, per strict rules).
