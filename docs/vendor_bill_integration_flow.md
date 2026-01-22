# 💰 Flow Integrasi Vendor Bill — Subscription Manager × Odoo Accounting 19

Dokumen ini menjelaskan alur terbaik (**best practice**) integrasi antara:
1.  **Subscription Manager** (monitoring & risk)
2.  **Odoo Accounting Community 19** (pembayaran & pencatatan keuangan)

**Tujuan utama:**
- ✅ Tidak duplikasi fungsi accounting
- ✅ Finance tetap nyaman
- ✅ Subscription otomatis mengikuti status pembayaran

---

## 🎯 Prinsip Utama
1.  **Accounting adalah single source of truth** untuk pembayaran.
2.  **Subscription Manager tidak mencatat uang.**
3.  **Renewal hanya sah jika vendor bill sudah dibayar.**
4.  Sistem harus fleksibel (**manual-first**).

---

## 🧩 Aktor yang Terlibat

| Role | Peran |
| :--- | :--- |
| **DevOps** | Menjaga service tetap hidup |
| **Finance** | Membuat & membayar vendor bill |
| **Subscription Manager** | Monitoring & linking |
| **Accounting** | Validasi finansial |

---

## 🧭 OVERVIEW FLOW
Service ↓ Subscription ↓ Vendor Bill (Draft) ↓ Vendor Bill (Posted) ↓ Payment ↓ Bill Paid ↓ **Subscription Renewed**

---

## 🟢 FLOW 1 — Manual Vendor Bill (RECOMMENDED v1)
*Ini flow paling aman dan realistis.*

### Step 1 — Subscription mendekati jatuh tempo
**Kondisi:** H-30 / H-14 / H-7
**Yang terjadi:**
- Subscription status = `Expiring Soon`
- Activity dibuat ke Finance

### Step 2 — Finance membuat Vendor Bill
Finance membuka: **Accounting → Vendor Bills**
Membuat bill dengan:
- Vendor = partner yang sama
- Tanggal bill
- Nominal sesuai subscription

**Subscription Manager:**
- Tidak membuat bill
- Hanya menunggu link

### Step 3 — Link Vendor Bill ke Subscription
Finance atau Admin:
1.  Memilih subscription
2.  Mengaitkan vendor bill

**Tujuan:** Sistem tahu bill ini untuk subscription apa.

### Step 4 — Bill diposting
**Status bill:** `Draft` → `Posted`
**Subscription masih:** `Expiring` (Karena belum dibayar)

### Step 5 — Payment dilakukan
Finance melakukan: **Register Payment**
Accounting memproses:
- Journal
- Rekonsiliasi

### Step 6 — Bill Paid
Saat bill berstatus: **Paid**
**Maka:**
- Subscription otomatis dianggap **renewed**
- Periode subscription maju
- Status kembali `Active`

---

## 🟡 FLOW 2 — Semi Otomatis (Optional)
*Digunakan jika tim ingin lebih cepat.*

**Mekanisme:**
Subscription Manager dapat **generate draft vendor bill**.

**Namun:**
- Finance tetap review
- Finance tetap post

**Keuntungan:** Mengurangi input manual.
**Risiko:** Harus disiplin validasi.

---

## 🔴 FLOW 3 — Full Otomatis (TIDAK DISARANKAN v1)
*Contoh: Auto create bill & auto renew.*

**Risiko:**
- Salah nominal
- Salah vendor
- Sulit audit

❌ **Tidak disarankan untuk Community v1.**

---

## 🧠 Status Subscription vs Vendor Bill

| Vendor Bill Status | Dampak ke Subscription |
| :--- | :--- |
| **Tidak ada bill** | Expiring |
| **Draft** | Expiring |
| **Posted** | Expiring |
| **Paid** | Renewed → **Active** |

*Hanya Paid yang valid.*

---

## 🔐 Boundary Responsibility

| Area | Pemilik |
| :--- | :--- |
| **Nominal** | Finance |
| **Pajak** | Accounting |
| **Journal** | Accounting |
| **Renewal logic** | Subscription Manager |
| **Risk monitoring** | Subscription Manager |

---

## ⚠️ Aturan Penting
1.  **Subscription tidak boleh renewed manual.**
2.  **Renewal hanya via vendor bill paid.**
3.  **Jika bill dibatalkan → renewal dibatalkan.**
4.  **Subscription Manager hanya membaca status.**

---

## 📊 Dampak ke Dashboard
Dashboard dapat menampilkan:
- Subscription expiring tanpa bill
- Subscription dengan bill unpaid
- Subscription paid

Manager bisa melihat:
> “Yang belum dibayar itu yang mana?”

---

## 🎯 Manfaat Flow Ini
- ✅ Finance tetap kerja dengan cara Odoo standar
- ✅ Tidak ada double input
- ✅ Audit aman
- ✅ Developer tidak bikin accounting palsu

---

## 🧠 Filosofi Akhir
> **Subscription Manager bukan sistem uang.**

Ia adalah sistem **kesadaran & kontrol risiko**.
Uang tetap milik Accounting.

---

## 📌 Catatan Penutup
Dokumen ini menjadi **acuan wajib** integrasi Accounting.

Setelah ini:
1.  Implementasi teknis aman.
2.  Konflik antar modul minimal.
3.  Finance & DevOps bisa jalan bareng.

*Tanpa saling menyalahkan 😄*
