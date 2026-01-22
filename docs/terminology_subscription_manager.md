# 📘 Terminologi Final — Subscription Manager

Dokumen ini menetapkan istilah resmi (**single source of truth**) yang digunakan di seluruh sistem.

**Tujuan utama:**
- ✅ Menghindari istilah ambigu
- ✅ Menyamakan bahasa DevOps, Finance, dan Manager
- ✅ Menjadi acuan sebelum desain teknis & UI

---

## 🎯 Prinsip Terminologi
1.  **Satu konsep = satu istilah**
2.  **Tidak ada istilah ganda** untuk hal yang sama
3.  **Nama harus mudah dipahami** non-teknis
4.  **Istilah mencerminkan fungsi bisnis**

---

## 🧩 DAFTAR TERMINOLOGI FINAL

### 1️⃣ Vendor
**Definisi:** Pihak ketiga yang menyediakan layanan dan menerima pembayaran dari perusahaan.

**Contoh:**
- AWS
- DigitalOcean
- Google Cloud
- Niagahoster
- Rumahweb
- Cloudflare

**Catatan penting:**
- Vendor ≠ Client
- Vendor adalah pihak yang kita bayar

### 2️⃣ Service
**Definisi:** Satu unit layanan yang dibeli dari vendor.

Service adalah objek utama yang bisa:
- Aktif
- Suspend
- Expired

**Contoh Service:**
- VPS Production
- Domain company.com
- SSL Wildcard
- Email Hosting
- Cloud Instance

**Catatan:**
- Service adalah sesuatu yang bisa mati jika tidak dibayar

### 3️⃣ Server (Subtype dari Service)
**Definisi:** Service yang bersifat komputasi / infrastruktur.

**Contoh:**
- VPS
- Dedicated Server
- Cloud VM

**Catatan:**
- Tidak semua service adalah server
- Tapi semua server adalah service
- *(UI boleh menampilkan "Server" agar familiar bagi DevOps)*

### 4️⃣ Subscription
**Definisi:** Kontrak pembayaran berulang untuk satu service.

Subscription menjawab pertanyaan:
- Kapan mulai?
- Interval berapa bulan?
- Kapan jatuh tempo berikutnya?
- Berapa biaya?

**Contoh:**
- VPS dibayar tiap 6 bulan
- Domain dibayar tahunan

**Catatan:**
- Subscription ≠ Invoice
- Subscription adalah kewajiban berulang

### 5️⃣ Billing Interval
**Definisi:** Jarak waktu antar pembayaran.

**Dinyatakan dalam:**
- Jumlah bulan

**Contoh:**
- 1 bulan → Bulanan
- 3 bulan → Triwulan
- 6 bulan → 6 Bulanan
- 12 bulan → Tahunan

**Catatan:**
- Disimpan sebagai angka
- UI boleh menampilkan label

### 6️⃣ Renewal / Perpanjangan
**Definisi:** Aktivitas memperpanjang masa aktif subscription.

Renewal terjadi ketika:
- Pembayaran berhasil
- Periode baru dimulai

**Catatan:**
- Renewal bisa manual
- Tidak otomatis ke vendor (di MVP)

### 7️⃣ Payment Record
**Definisi:** Catatan internal bahwa suatu subscription telah dibayar.

**Digunakan untuk:**
- Tracking
- Audit internal
- Histori

**Bukan:**
- Invoice
- Jurnal accounting

### 8️⃣ Credential
**Definisi:** Informasi akses ke service atau vendor.

**Jenis:**
- Vendor portal login
- SSH
- API key
- Panel hosting

**Catatan penting:**
- Credential adalah data sensitif
- Akses dibatasi per role

### 9️⃣ Client (Opsional)
**Definisi:** Pihak yang menggunakan service (end customer).

**Digunakan hanya untuk:**
- Referensi
- Klasifikasi

**Catatan:**
- Client tidak melakukan pembayaran di sistem ini
- Tidak ada invoice ke client

### 🔟 Status Subscription
**Status standar:**
- **Active** → Masih aman
- **Expiring Soon** → Mendekati jatuh tempo
- **Expired** → Melewati jatuh tempo

*Status ditentukan otomatis oleh sistem.*

### 1️⃣1️⃣ Criticality (Tingkat Risiko)
**Definisi:** Dampak bisnis jika service mati.

**Level:**
- **Low** (Staging, testing)
- **Medium** (Internal)
- **High** (Production non-core)
- **Mission Critical** (Core business)

**Digunakan untuk:**
- Prioritas reminder
- Prioritas pembayaran

### 1️⃣2️⃣ Reminder
**Definisi:** Notifikasi internal terkait jatuh tempo.

**Contoh:**
- H-30
- H-14
- H-7
- H-3
- Expired

**Reminder bersifat:**
- Internal
- Preventif

---

## 🚫 ISTILAH YANG TIDAK DIGUNAKAN
Untuk menghindari kebingungan, istilah berikut **tidak digunakan**:

- ❌ **Invoice** (karena bukan billing client)
- ❌ **Billing Client**
- ❌ **Accounting**
- ❌ **Payment Gateway**
- ❌ **Auto debit**

---

## 🎯 Manfaat Terminologi Final
Dengan terminologi ini:
1.  Diskusi bisnis lebih cepat
2.  Developer tidak salah tafsir
3.  UI lebih konsisten
4.  Dokumentasi lebih rapi

Dokumen ini menjadi:
> **Acuan wajib sebelum desain teknis dan implementasi Odoo**

---

## 📌 Catatan Penutup
Dokumen ini bersifat **final secara konsep**.

Perubahan istilah hanya boleh dilakukan jika:
1.  Ada kebutuhan bisnis baru
2.  Disetujui semua stakeholder
