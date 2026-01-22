# 🧭 User Journey — Subscription Manager (Concept)

Dokumen ini menjelaskan alur penggunaan sistem oleh setiap role.

**Tujuan:**
- ✅ Menyamakan persepsi
- ✅ Menghindari fitur tidak perlu
- ✅ Memastikan setiap role hanya melihat yang relevan

---

## 👤 ROLE OVERVIEW

| Role | Fokus Utama |
| :--- | :--- |
| **DevOps** | Operasional server & akses teknis |
| **Finance** | Pembayaran vendor & jatuh tempo |
| **Manager / Owner** | Risiko, biaya, dan kontrol |
| **Admin** | Pengelolaan sistem |

---

## 🧑‍💻 1️⃣ User Journey — DevOps

### 🎯 Tujuan DevOps
DevOps ingin memastikan:
1.  Server tidak mati.
2.  Akses selalu tersedia.
3.  Tidak ada kejutan mendadak.

*DevOps tidak fokus ke uang, tapi ke stabilitas sistem.*

### 🔄 Alur DevOps

#### Step 1 — Melihat daftar server
DevOps membuka menu:
> **Subscription Manager → Servers**

Yang ingin langsung terlihat:
- Nama server
- Client (jika ada)
- Vendor
- Status subscription
- Sisa hari

DevOps langsung bisa menjawab:
> “Server mana yang berisiko minggu ini?”

#### Step 2 — Cek detail server
Saat membuka satu server, DevOps melihat:
- IP address
- Region
- OS
- Vendor
- Masa aktif

*Tidak perlu: histori pembayaran, nominal biaya.*

#### Step 3 — Akses credential
Jika perlu maintenance, DevOps membuka:
- SSH credential
- Panel hosting
- API key

**Catatan penting:**
- DevOps hanya melihat credential teknis.
- Tidak melihat credential pembayaran.

#### Step 4 — Server mendekati expired
Jika status: **Expiring Soon**

DevOps bisa:
- Memberi catatan
- Notify finance secara internal

**Tujuan:**
> DevOps tahu risiko lebih awal.

### 🧠 Value untuk DevOps
- ✅ Tidak cari credential ke sana-sini
- ✅ Tidak kaget server mati
- ✅ Bisa planning maintenance

---

## 💰 2️⃣ User Journey — Finance

### 🎯 Tujuan Finance
Finance ingin tahu:
1.  Apa yang harus dibayar.
2.  Kapan harus dibayar.
3.  Berapa nominalnya.

*Finance tidak butuh detail teknis server.*

### 🔄 Alur Finance

#### Step 1 — Melihat daftar subscription
Finance membuka:
> **Subscription Manager → Subscriptions**

Yang ingin terlihat:
- Vendor
- Nama service
- Jatuh tempo
- Sisa hari
- Nominal

Finance langsung tahu:
> “Minggu ini harus bayar apa?”

#### Step 2 — Filter expiring
Finance memfilter:
- Expiring 30 hari
- Expiring 7 hari

**Tujuan:** Menyusun jadwal pembayaran.

#### Step 3 — Melihat vendor
Finance membuka vendor:
- Nama vendor
- Website
- Akun vendor

Finance bisa login vendor untuk melakukan pembayaran.

#### Step 4 — Catat pembayaran
Setelah pembayaran dilakukan, Finance mencatat:
- Tanggal bayar
- Periode yang dibayar
- Nominal
- Bukti pembayaran

**Catatan:**
- Ini bukan accounting.
- Hanya tracking internal.

### 🧠 Value untuk Finance
- ✅ Tidak buka spreadsheet manual
- ✅ Tidak tanya DevOps berkali-kali
- ✅ Jelas kewajiban pembayaran

---

## 👔 3️⃣ User Journey — Manager / Owner

### 🎯 Tujuan Manager
Manager ingin:
1.  Visibilitas
2.  Kontrol
3.  Minim risiko

*Manager tidak ingin detail teknis.*

### 🔄 Alur Manager

#### Step 1 — Melihat dashboard
Manager membuka dashboard dan langsung melihat:
- Total service aktif
- Expiring minggu ini
- Expiring bulan ini
- Total estimasi biaya

**Tujuan:**
> “Apakah ada risiko bisnis hari ini?”

#### Step 2 — Identifikasi risiko
Manager bisa melihat:
- Service berstatus expired
- Service critical

Manager dapat langsung follow-up ke:
- DevOps
- Finance

#### Step 3 — Review biaya
Manager melihat ringkasan:
- Biaya per vendor
- Estimasi bulanan
- Estimasi tahunan

*Tanpa melihat credential.*

### 🧠 Value untuk Manager
- ✅ Tidak reaktif
- ✅ Tidak panik mendadak
- ✅ Bisa ambil keputusan cepat

---

## ⚙️ 4️⃣ User Journey — Admin

### 🎯 Tujuan Admin
Admin bertanggung jawab atas:
- Struktur data
- User & role
- Kebijakan akses

### 🔄 Alur Admin
- Membuat vendor
- Membuat service
- Menentukan role user
- Mengatur siapa melihat apa

*Admin jarang dipakai sehari-hari, namun krusial untuk stabilitas sistem.*

---

## 🔑 Prinsip Penting User Journey
1.  **Setiap role melihat data yang sama, tapi sudut pandang berbeda.**
2.  **Tidak ada role yang melihat informasi tidak relevan.**
3.  **Satu sistem → banyak perspektif.**

---

## 🎯 Outcome User Journey
Jika user journey ini tercapai:
- DevOps fokus ke stabilitas
- Finance fokus ke pembayaran
- Manager fokus ke risiko

*Tanpa saling tanya di chat.*

---

## 📌 Catatan Penutup
Dokumen ini masih **konsep murni**, belum masuk desain teknis atau Odoo.

**Langkah berikutnya:**
1.  Terminologi final
2.  Boundary antar fitur
3.  Baru masuk desain struktur addons
