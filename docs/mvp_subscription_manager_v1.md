# 🎯 MVP — Subscription Manager v1 (Concept Only)

## 📄 Pendahuluan
Dokumen ini mendefinisikan cakupan minimum (Minimum Viable Product - MVP) untuk addons Odoo Subscription Manager.

**Tujuan Utama:**
- ✅ Mencegah lupa pembayaran layanan hosting & infrastruktur.
- ✅ Memberikan visibilitas risiko ke DevOps, Finance, dan Manager.

---

## 🧭 Prinsip MVP
Fokus utama adalah pada **monitoring & awareness**, bukan otomasi pembayaran.

- Tidak masuk ke ranah accounting.
- Tidak masuk ke billing client.
- Tidak mencoba menggantikan tools DevOps yang sudah ada.

**Pertanyaan Kunci:**
MVP harus bisa menjawab satu pertanyaan penting:
> “Apa saja layanan yang berisiko mati karena belum dibayar?”

---

## ✅ Scope MVP v1 (WAJIB ADA)

### 1️⃣ Registry Service / Server
Sistem harus berfungsi sebagai **Inventory** terpusat untuk menyimpan daftar layanan yang dikelola.

**Contoh Layanan:**
- VPS / Dedicated Server
- Cloud Instance (AWS, GCP, Azure, dll)
- Domain Name
- SSL Certificates
- Email Hosting (Google Workspace, Zoho, dll)

**Atribut Service (Minimal):**
- **Nama Service**: Identitas layanan.
- **Vendor Penyedia**: Siapa yang menyediakan layanan.
- **Client**: (Opsional) Referensi jika layanan ini untuk client tertentu.
- **Jenis Layanan**: Kategorisasi tipe service.
- **Status**: `Aktif`, `Suspend`, `Terminate`.

**Tujuan:**
Memiliki satu daftar terpusat untuk semua resource perusahaan.

### 2️⃣ Subscription / Masa Aktif
Setiap service wajib memiliki informasi masa berlaku untuk perhitungan jatuh tempo.

**Informasi Inti:**
- **Tanggal Mulai**: Kapan layanan diaktifkan.
- **Interval Pembayaran**: Periode tagihan.
    - `1` = Bulanan
    - `3` = Triwulan
    - `6` = Semester
    - `12` = Tahunan
    - *Custom*: Bebas sesuai kebutuhan vendor.
- **Nominal Pembayaran**: Berapa biaya per interval.
- **Mata Uang**: Currency yang digunakan (IDR, USD, dll).

**Tujuan:**
Sistem dapat menghitung kapan tanggal jatuh tempo berikutnya secara otomatis.

### 3️⃣ Status Otomatis Subscription
Sistem harus mampu memberikan indikator visual status secara otomatis berdasarkan sisa waktu.

**Status & Logika:**
- 🟢 **Active**: Masa aktif aman.
- 🟡 **Expiring Soon**: `≤ 30 hari` menuju jatuh tempo (Configurable).
- 🔴 **Expired**: `≤ 0 hari` (Sudah lewat jatuh tempo).

**Tujuan:**
User langsung tahu kondisi kesehatan layanan tanpa perlu menghitung tanggal secara manual.

### 4️⃣ Reminder & Alert Dasar
Fitur pengingat internal untuk memastikan tidak ada pembayaran yang terlewat (Tanpa integrasi notifikasi eksternal kompleks di V1).

**Mekanisme:**
- Notifikasi di Odoo (Inbox/Tray).
- Activity Reminder (To-Do List Odoo).

**Trigger Default:**
- H-30 (Persiapan budgeting)
- H-14 (Review)
- H-7 (Proses pembayaran)
- H-3 (Urgent)
- Expired (Critical)

**Tujuan:**
Menghilangkan alasan "lupa" bayar.

### 5️⃣ Vendor Management
Sistem menyimpan daftar vendor hosting/layanan sebagai entitas terpisah.

**Informasi Dasar:**
- Nama Vendor
- Website / Portal URL
- Catatan Tambahan

**Tujuan:**
Mengelompokkan service berdasarkan penyedia untuk kemudahan manajemen tagihan.

### 6️⃣ Credential Repository (Basic)
Penyimpanan credential terpusat yang aman.

**Jenis Credential:**
- Vendor Portal Login
- SSH Server Access
- API Keys / Secrets

**Keamanan:**
- **Restricted Access**: Credential hanya dapat dilihat oleh role tertentu (misal: DevOps, Admin).
- Tidak semua user bisa mengakses field ini.

**Tujuan:**
Efisiensi akses, menghindari pencarian credential di chat history atau file excel yang tidak aman.

### 7️⃣ Role & Akses Dasar (ACL)
Pembagian hak akses untuk keamanan data.

**Definisi Role:**
1.  **Admin**: Akses penuh (Read/Write/Delete/Configure).
2.  **DevOps**:
    - Melihat daftar server/service.
    - **Bisa** melihat credential teknis (SSH, API).
3.  **Finance**:
    - Melihat subscription & tanggal jatuh tempo.
    - Melihat nominal biaya.
    - **Tidak bisa** melihat credential teknis (SSH hidden).
4.  **Viewer / Manager**: Read-only akses untuk monitoring.

**Tujuan:**
Informasi aman, terstruktur, dan tidak bocor ke pihak yang tidak berkepentingan.

### 8️⃣ Dashboard Sederhana
Halaman utama untuk tinjauan cepat (Helicopter View).

**Metrik Kunci:**
- Total Service Aktif
- Jumlah Service Expiring (30 hari ke depan)
- Jumlah Service Expired
- Total Estimasi Biaya (Bulanan / Tahunan)

**Tujuan:**
Manajemen bisa melihat risiko dan proyeksi biaya dalam satu layar.

---

## ❌ OUT OF SCOPE (TIDAK MASUK MVP)
Hal-hal berikut sengaja **tidak dimasukkan** ke versi 1 untuk menjaga kesederhanaan dan kecepatan rilis:

- ❌ Pembuatan Invoice ke Client (Re-billing).
- ❌ Integrasi modul Accounting Odoo.
- ❌ Auto Payment ke Vendor (Kartu Kredit/Bank).
- ❌ Integrasi API Vendor (Cek status server real-time).
- ❌ Forecast AI.
- ❌ Notifikasi Telegram / WhatsApp.
- ❌ Struktur Multi-company yang kompleks.

*Fitur di atas disimpan untuk roadmap v2 / v3.*

---

## 🎯 Outcome yang Diharapkan
Setelah MVP berjalan, tim diharapkan dapat:
1.  Mengetahui inventaris lengkap layanan yang dikelola.
2.  Mengetahui layanan mana yang mendekati jatuh tempo.
3.  Mengurangi risiko server mati karena masalah administrasi.
4.  Mempermudah koordinasi antara tim DevOps & Finance.
5.  Meningkatkan kontrol terhadap biaya infrastruktur IT.

---

## 🧠 Indikator Keberhasilan (Success Metrics)
MVP dianggap sukses jika:
- ✅ **Zero Downtime** akibat lupa bayar.
- ✅ **Traceability**: Semua server bisa ditelusuri vendor & masa aktifnya.
- ✅ **Visibility**: Finance tahu jadwal pembayaran minggu ini tanpa tanya DevOps.
- ✅ **Risk Awareness**: DevOps tahu server mana yang berisiko expired.

---

## 📌 Catatan Penutup
Dokumen ini murni **konsep bisnis**, belum masuk ke ranah desain teknis Odoo.

**Langkah Selanjutnya:**
1.  Penyusunan User Journey per role.
2.  Finalisasi Terminologi.
3.  Desain Teknis & Struktur Addons (Data Model).
