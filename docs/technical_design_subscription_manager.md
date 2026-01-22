# 🧩 Desain Teknis Addons — Subscription Manager (Odoo Community 19)

Dokumen ini menjelaskan desain teknis tingkat tinggi berdasarkan seluruh konsep yang telah disepakati.

**Tujuan:**
- ✅ Menjadi blueprint implementasi
- ✅ Menjaga agar tidak keluar dari arsitektur Odoo
- ✅ Mencegah model redundant

---

## 🎯 Prinsip Teknis
1.  **Gunakan model Odoo core sebagai master data.**
2.  Addons hanya menambah **model bisnis unik**.
3.  **Tidak mengubah alur accounting.**
4.  Semua integrasi bersifat **relasional**, bukan duplikasi.

---

## 🧩 Daftar Model yang DIGUNAKAN

### Model Odoo Core (digunakan langsung)
| Model | Fungsi |
| :--- | :--- |
| `res.partner` | Vendor & Client |
| `res.currency` | Mata uang |
| `account.move` | Vendor Bill |
| `account.payment` | Payment |
| `ir.activity` | Reminder |
| `res.users` | User |

*Model ini tidak dibuat ulang.*

---

## 🧱 Model Custom (Subscription Manager)
Hanya model berikut yang dibuat:

| Model | Tujuan |
| :--- | :--- |
| `sm.service` | Service / resource |
| `sm.subscription` | Kontrak pembayaran |
| `sm.credential` | Credential akses |
| `sm.criticality` | Tingkat risiko |

---

## 🖥️ sm.service (Service)

### Fungsi
Mewakili resource nyata yang digunakan.

### Relasi
- Vendor → `res.partner`
- Client → `res.partner` (opsional)
- Subscription aktif → `sm.subscription`
- Credential → `sm.credential`

### Data yang disimpan
- Nama service
- Tipe service
- Vendor
- Client
- Criticality
- Status operasional

**Tidak menyimpan data keuangan.**

---

## 📄 sm.subscription (Subscription)

### Fungsi
Mengelola masa aktif & kewajiban pembayaran.

### Relasi
- Service → `sm.service`
- Vendor → `res.partner`
- Vendor Bill → `account.move`
- Currency → `res.currency`

### Data yang disimpan
- Billing interval (bulan)
- Estimasi biaya
- Tanggal mulai
- Next renewal date
- Status (computed)

**Status ditentukan sistem.**

---

## 💰 Integrasi Vendor Bill

### Sumber kebenaran
`account.move` (type: vendor bill)

### Peran Subscription Manager
- Link ke vendor bill
- Membaca status pembayaran

### Aturan
- Bill **paid** → Subscription **renewed**
- Bill **unpaid** → Subscription tetap **expiring**

**Addon tidak menyentuh jurnal.**

---

## 🔐 sm.credential (Credential)

### Fungsi
Menyimpan akses teknis.

### Relasi
- Service → `sm.service`

### Catatan
- Tidak terhubung ke accounting.
- Akses dibatasi group.

---

## ⚠️ sm.criticality (Criticality)

### Fungsi
Menentukan tingkat risiko.

### Digunakan untuk:
- Dashboard
- Prioritas reminder

### Nilai contoh:
- Low
- Medium
- High
- Mission Critical

---

## 🔔 Reminder System

### Menggunakan:
`ir.activity`

### Flow:
1.  Cron harian cek subscription.
2.  Jika mendekati jatuh tempo.
3.  Buat activity otomatis.

**Tidak membuat sistem notifikasi sendiri.**

---

## 📊 Dashboard

### Menggunakan view bawaan Odoo:
- Kanban
- Graph
- Pivot

### Sumber data:
- `sm.subscription`
- `sm.service`

**Tidak membuat engine reporting baru.**

---

## 🔐 Security Group

| Group | Akses |
| :--- | :--- |
| **Subscription Admin** | Full |
| **DevOps** | Service + Credential |
| **Finance** | Subscription + Vendor Bill |
| **Manager** | Read-only |

*Akses field sensitif dibatasi.*

---

## 🗂️ Struktur Menu

**Subscription Manager**
1.  Dashboard
2.  Services
3.  Subscriptions
4.  Vendors (`res.partner` filtered)
5.  Vendor Bills (`account.move` filtered)
6.  Credentials
7.  Reports
8.  Configuration

*Menu tampil berdasarkan role.*

---

## 🔄 Workflow Teknis
1.  Service dibuat.
2.  Subscription dibuat.
3.  Sistem monitoring berjalan.
4.  Vendor bill dibuat (manual / otomatis).
5.  Bill dibayar.
6.  Subscription diperpanjang otomatis.

---

## 🚫 Yang Tidak Dibuat
- ❌ Model invoice
- ❌ Model payment
- ❌ Model vendor
- ❌ Model currency
- ❌ Payment automation

---

## 🧠 Final Architecture
`Odoo Core` ↑ **Subscription Manager** (monitoring & risk) ↑ `Infrastructure & DevOps`

**Accounting tetap menjadi pemilik keuangan.**

---

## 📌 Dokumen ini menjadi pedoman implementasi teknis resmi.
Setelah ini:
1.  Developer bisa mulai coding.
2.  Struktur addons bisa dibuat.
3.  Estimasi waktu bisa dihitung.

**Tanpa perlu mengubah konsep lagi.**
