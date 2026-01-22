# 🔄 Workflow Lifecycle — Subscription Manager

Dokumen ini menjelaskan alur hidup (lifecycle) sebuah service dan subscription sejak dibuat hingga dihentikan.

**Tujuan:**
- ✅ Menyamakan pemahaman alur kerja
- ✅ Menjadi dasar validasi sistem
- ✅ Mencegah kebingungan status

---

## 🎯 Prinsip Workflow
1.  **Semua perubahan mengikuti alur.**
2.  **Status tidak boleh lompat.**
3.  **Status utama ditentukan sistem**, bukan user.
4.  **Histori tidak pernah dihapus.**

---

## 🧩 Objek yang Terlibat
- Service
- Subscription
- Payment Record
- Reminder

*Workflow difokuskan pada Subscription, karena subscription menentukan risiko.*

---

## 🟢 FASE 1 — Service Creation
**Trigger:** Admin / DevOps membuat service baru.

**Yang terjadi:**
- Service tercatat di sistem.
- Status service: `Active`
- Belum memiliki subscription.

**Catatan:**
- Service belum dianggap aman.
- Service wajib memiliki subscription untuk aktif penuh.

---

## 📄 FASE 2 — Subscription Created
**Trigger:** Admin / Finance membuat subscription.

**Yang terjadi:**
- Subscription terhubung ke service.
- Sistem mencatat:
    - Tanggal mulai
    - Interval pembayaran
    - Nominal
- **Status awal Subscription:** `Active`

---

## ⏱️ FASE 3 — Running Period
**Kondisi:** Subscription masih dalam masa aktif.

**Sistem melakukan:**
- Perhitungan sisa hari otomatis.
- Monitoring harian.

**Status:**
- 🟢 `Active`

---

## ⚠️ FASE 4 — Expiring Soon
**Trigger:** Sisa hari ≤ threshold (misal 30 hari).

**Yang terjadi:**
- Status berubah menjadi `Expiring Soon`.
- Reminder otomatis dibuat.

**Tujuan:** Memberi waktu cukup untuk proses pembayaran.

---

## 🔔 FASE 5 — Reminder Cycle
Reminder berjalan bertahap:
- H-30
- H-14
- H-7
- H-3

**Reminder dikirim ke:**
- Finance
- DevOps (jika critical)

---

## 💰 FASE 6 — Payment Recorded
**Trigger:** Finance melakukan pembayaran.

**Yang terjadi:**
- Payment record dibuat.
- Subscription diperpanjang.
- Periode baru dimulai.

**Status kembali:**
- 🟢 `Active`

*Histori lama tetap tersimpan.*

---

## 🔴 FASE 7 — Expired
**Trigger:** Tanggal jatuh tempo terlewati.

**Yang terjadi:**
- Status berubah menjadi `Expired`.
- Reminder bersifat urgent.

**Catatan:**
- Sistem tidak otomatis mematikan service.
- Tapi menandai risiko sangat tinggi.

---

## 🚫 FASE 8 — Termination
**Trigger:**
- Service tidak lagi digunakan.
- Diputus secara bisnis.

**Yang terjadi:**
- Service status diubah ke `Terminated`.
- Subscription dihentikan.
- Tidak ada reminder lagi.

*Histori tetap tersimpan.*

---

## 🔁 RINGKASAN FLOW

**Main Flow:**
Service Created ↓ Subscription Created ↓ Active ↓ Expiring Soon ↓ (Reminder Cycle) ↓ Renewed → **kembali Active**

**Alternatif:**
Expired ↓ Terminated

---

## ⚠️ Aturan Penting Workflow
- User tidak boleh set status manual.
- Status ditentukan sistem.
- Renewal hanya melalui payment record.
- Tidak ada delete histori.

---

## 🧠 Filosofi Workflow
Workflow ini dibuat untuk:
1.  Mencegah human error.
2.  Menjaga konsistensi data.
3.  Memudahkan audit.
4.  Memastikan tidak ada layanan terlupakan.

---

## 📌 Catatan Penutup
Dokumen ini menjadi **acuan utama** saat:
1.  Membuat validasi.
2.  Membuat automation.
3.  Membuat cron job.
4.  Membuat status logic.

**Setelah workflow ini disepakati, sistem dianggap siap masuk desain teknis.**
