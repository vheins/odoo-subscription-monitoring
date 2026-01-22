# 🧭 Mapping Konsep Subscription Manager → Odoo Community 19

Dokumen ini memetakan konsep bisnis yang sudah disepakati ke model & fitur bawaan Odoo 19 Community.

**Tujuan utama:**
- ✅ Menghindari model redundant
- ✅ Menggunakan Odoo core sebagai single source of truth
- ✅ Menjaga kompatibilitas jangka panjang

---

## 🎯 Prinsip Arsitektur
1.  **Jangan menduplikasi data master Odoo.**
2.  **Gunakan model Odoo core sebagai sumber utama.**
3.  Addons Subscription Manager hanya menambahkan layer kontrol & monitoring.
4.  **Accounting tetap menjadi pemilik data finansial.**

---

## 🧩 Mapping Utama

| Konsep Bisnis | Odoo Model | Keterangan |
| :--- | :--- | :--- |
| **Vendor** | `res.partner` | `supplier_rank > 0` |
| **Client** | `res.partner` | `customer_rank > 0` |
| **Mata uang** | `res.currency` | Native Odoo |
| **Vendor Bill** | `account.move` | `move_type = 'in_invoice'` |
| **Payment** | `account.payment` | Native accounting |
| **Pajak** | `account.tax` | Tidak disentuh |

---

## 🖥️ Service

### Konsep
Service adalah resource nyata yang bisa mati jika tidak dibayar.

### Odoo Core
❌ **Tidak tersedia**

### Keputusan
✅ **Dibuat sebagai model custom**

**Service menyimpan:**
- Nama service
- Jenis (VPS, domain, SSL, dll)
- Vendor (`res.partner`)
- Client (`res.partner`, opsional)
- Criticality
- Status operasional

**Service TIDAK menyimpan:**
- Payment
- Invoice
- Jurnal

---

## 📄 Subscription

### Konsep
Kontrak pembayaran berulang atas satu service.

### Odoo Core
❌ **Tidak tersedia di Community**
*(Subscription module hanya ada di Enterprise)*

### Keputusan
✅ **Model custom**

**Subscription menyimpan:**
- Service
- Vendor (`res.partner`)
- Billing interval (bulan)
- Estimasi nominal
- Next renewal date

**Subscription TIDAK menyimpan:**
- Status pembayaran
- Jurnal
- Tax

---

## 💰 Vendor Bill Integration

### Odoo Model
`account.move` (`in_invoice`)

### Peran Vendor Bill
**Vendor bill menjadi sumber kebenaran pembayaran.**

**Subscription Manager:**
- Dapat membuat draft vendor bill (opsional)
- Membaca status bill

**Logika bisnis:**
- Bill paid → Subscription dianggap **renewed**
- Bill unpaid → Tetap **expiring**

**Addon tidak mencatat pembayaran sendiri.**

---

## 🔁 Renewal Concept
**Renewal terjadi ketika:** Vendor bill sudah `paid`.

**Sistem:**
1.  Membaca vendor bill.
2.  Menghitung periode berikutnya.
3.  Memperbarui subscription.

**Tidak ada renewal manual tanpa bill.**

---

## 🔐 Credential

### Konsep
Data akses operasional.

### Odoo Core
❌ **Tidak tersedia**

### Keputusan
✅ **Model custom**

**Credential:**
- Terkait ke service.
- Tidak terkait ke accounting.
- Akses dibatasi per role.

---

## ⚠️ Criticality

### Konsep
Tingkat risiko jika service mati.

### Odoo Core
❌ **Tidak tersedia**

### Keputusan
✅ **Model custom**

**Digunakan untuk:**
- Prioritas reminder.
- Highlight dashboard.

---

## 🔔 Reminder & Activity

### Odoo Core
`ir.activity`

### Keputusan
✅ **Gunakan activity native**

**Subscription Manager hanya:**
- Membuat activity otomatis.
- Menentukan siapa penerimanya.

**Tidak membuat sistem notifikasi sendiri.**

---

## 📊 Dashboard & Reporting

### Odoo Core
- Graph View
- Pivot View
- Kanban

### Keputusan
✅ **Reuse semua view bawaan**

**Data sumber:**
- Subscription
- Vendor Bill

**Tidak membuat reporting engine baru.**

---

## 🧠 Single Source of Truth

| Data | Pemilik |
| :--- | :--- |
| **Vendor** | `res.partner` |
| **Client** | `res.partner` |
| **Invoice** | Accounting |
| **Payment** | Accounting |
| **Currency** | Odoo Core |
| **Service** | Subscription Manager |
| **Subscription** | Subscription Manager |

---

## 🚫 Yang DILARANG Dibuat
- ❌ Model vendor baru
- ❌ Model client baru
- ❌ Model currency
- ❌ Model payment
- ❌ Model invoice

**Semua ini wajib memakai Odoo core.**

---

## 🧭 Posisi Addons dalam Odoo
Subscription Manager berada di tengah:

`Infrastructure` ←→ **Subscription Manager** ←→ `Accounting`

**Bukan menggantikan salah satunya.**

---

## 🎯 Manfaat Mapping Ini
- ✅ Aman upgrade Odoo
- ✅ Minim konflik modul
- ✅ Finance tetap pakai accounting standar
- ✅ DevOps dapat visibilitas
- ✅ Manager dapat kontrol risiko

---

## 📌 Catatan Penutup
Dokumen ini menjadi **blueprint arsitektur final** sebelum masuk desain teknis.
