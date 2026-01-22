# 🗂️ Information Architecture — Subscription Manager

Dokumen ini menjelaskan struktur menu, navigasi, dan tampilan informasi.

**Tujuan utama:**
- ✅ UI tidak membingungkan
- ✅ Setiap role hanya melihat yang relevan
- ✅ Addons terasa rapi dan enterprise

---

## 🎯 Prinsip Information Architecture
1.  **Menu tidak boleh terlalu dalam.**
2.  **Menu disusun berdasarkan cara orang berpikir**, bukan struktur database.
3.  **Role menentukan apa yang terlihat.**
4.  **Informasi penting harus terlihat cepat.**

---

## 🧭 Struktur Menu Utama

**Menu utama:**
> **Subscription Manager**

**Di dalamnya:**
1.  Dashboard
2.  Services
3.  Subscriptions
4.  Vendors
5.  Credentials
6.  Payments
7.  Reports
8.  Configuration

---

## 📊 1️⃣ Dashboard
**Tujuan:** Memberikan gambaran kondisi sistem dalam **10 detik**.

**Informasi yang tampil:**
- Total service aktif
- Expiring dalam 30 hari
- Expiring dalam 7 hari
- Service expired
- Estimasi biaya bulan ini

**Catatan UI:**
- Tidak ada tombol edit
- Read-only
- Visual indikator warna (aman / warning / risiko)

---

## 🖥️ 2️⃣ Services
**Tujuan:** Daftar semua resource yang dikelola.

**Tampilan list:**
- Nama service
- Jenis service
- Vendor
- Client (opsional)
- Criticality
- Status subscription
- Days left

**Detail service:**
- Informasi umum
- Subscription aktif
- Credential terkait
- Catatan

**Akses:**
- **DevOps:** Full view
- **Finance:** View terbatas
- **Manager:** Read-only

---

## 📄 3️⃣ Subscriptions
**Tujuan:** Melihat semua kewajiban pembayaran.

**Tampilan list:**
- Service
- Vendor
- Interval pembayaran
- Next renewal date
- Days left
- Nominal

**Filter penting:**
- Expiring 30 hari
- Expiring 7 hari
- Vendor
- Criticality

**Akses:**
- **Finance:** Utama
- **DevOps:** Read-only

---

## 🏢 4️⃣ Vendors
**Tujuan:** Manajemen penyedia layanan.

**Informasi:**
- Nama vendor
- Website
- Daftar service
- Catatan

**Akses:**
- **Admin**
- **Finance**

---

## 🔐 5️⃣ Credentials
**Tujuan:** Penyimpanan akses terpusat.

**Tampilan:**
- Nama credential
- Tipe (SSH / Vendor / API)
- Service terkait

**Catatan penting:**
- Tidak ditampilkan di menu semua role
- Bisa disembunyikan sepenuhnya dari Manager

---

## 💰 6️⃣ Payments
**Tujuan:** Mencatat histori pembayaran.

**Tampilan:**
- Subscription
- Vendor
- Tanggal bayar
- Periode
- Nominal
- Bukti pembayaran

**Akses:**
- **Finance**
- **Admin**

---

## 📈 7️⃣ Reports
**Tujuan:** Ringkasan manajemen.

**Contoh laporan:**
- Biaya per vendor
- Biaya per bulan
- Service paling mahal
- Service critical

**Akses:**
- **Manager**
- **Admin**

---

## ⚙️ 8️⃣ Configuration
**Tujuan:** Pengaturan sistem.

**Isi:**
- Master criticality
- Reminder rule
- Role mapping

**Akses:**
- **Admin only**

---

## 👥 Role-Based Visibility

| Menu | Admin | DevOps | Finance | Manager |
| :--- | :---: | :---: | :---: | :---: |
| **Dashboard** | ✅ | ✅ | ✅ | ✅ |
| **Services** | ✅ | ✅ | 👁️ | 👁️ |
| **Subscriptions** | ✅ | 👁️ | ✅ | 👁️ |
| **Vendors** | ✅ | ❌ | ✅ | 👁️ |
| **Credentials** | ✅ | ✅ | ❌ | ❌ |
| **Payments** | ✅ | ❌ | ✅ | ❌ |
| **Reports** | ✅ | ❌ | ❌ | ✅ |
| **Configuration** | ✅ | ❌ | ❌ | ❌ |

*(Keterangan: 👁️ = read-only, ❌ = hidden)*

---

## 🧠 Prinsip Navigasi
- Semua menu bisa diakses **maksimal 2 klik**.
- Tidak ada menu tersembunyi penting.
- **Dashboard** selalu menjadi landing page.

---

## 🎯 Outcome Information Architecture
Dengan struktur ini:
- **DevOps** cepat ke server
- **Finance** cepat ke pembayaran
- **Manager** cepat ke risiko
- **Admin** mudah mengatur sistem

---

## 📌 Catatan Penutup
Dokumen ini adalah **jembatan terakhir** sebelum desain teknis Odoo 19.

Setelah ini, barulah masuk ke:
1.  Struktur models
2.  Menu XML
3.  Security groups
4.  Workflow teknis

**Namun konsep bisnisnya sudah dianggap final.**
