# 🧱 Boundary & Rules — Subscription Manager

Dokumen ini mendefinisikan aturan main sistem.

**Tujuan utama:**
- ✅ Mencegah kekacauan data
- ✅ Menentukan batas tanggung jawab
- ✅ Menghindari konflik antar role
- ✅ Menjadi dasar validasi sistem

---

## 🎯 Prinsip Umum
1.  **Sistem ini bersifat monitoring & kontrol risiko**, bukan eksekusi pembayaran.
2.  Data bersifat **jangka panjang dan sensitif**.
3.  Perubahan data harus dapat dipertanggungjawabkan.
4.  Tidak semua hal boleh diedit semua role.

---

## 🔐 1️⃣ Aturan Akses Data

### 1.1 Prinsip dasar
- Semua user melihat objek yang sama.
- Tetapi hak akses berbeda.

### 1.2 Akses per role

| Role | Hak Akses | Larangan |
| :--- | :--- | :--- |
| **Admin** | • Boleh membuat<br>• Boleh mengubah<br>• Boleh menghapus<br>• Boleh mengatur role | - |
| **DevOps** | • Boleh melihat service & server<br>• Boleh melihat credential teknis | • Tidak boleh melihat nominal pembayaran<br>• Tidak boleh menghapus subscription |
| **Finance** | • Boleh melihat subscription<br>• Boleh melihat nominal<br>• Boleh mencatat payment record | • Tidak boleh melihat credential teknis |
| **Manager / Viewer** | • Read-only | • Tidak boleh edit<br>• Tidak boleh melihat credential |

---

## 🧩 2️⃣ Aturan Service

### 2.1 Pembuatan service
- Service hanya boleh dibuat oleh:
    - **Admin**
    - (opsional) **DevOps**
- Service wajib memiliki:
    - Vendor
    - Minimal satu subscription
- **Tidak boleh ada service tanpa subscription.**

### 2.2 Penghapusan service
- Service tidak boleh dihapus jika:
    - Pernah memiliki subscription.
    - Pernah memiliki payment record.
- **Alternatif:** Status diubah menjadi `terminated`.
- **Tujuan:** Histori tetap aman.

---

## 📄 3️⃣ Aturan Subscription

### 3.1 Hubungan
- Satu service hanya memiliki **satu subscription aktif**.
- Subscription lama menjadi histori.

### 3.2 Edit subscription
- **Yang boleh diedit:**
    - Nominal
    - Interval pembayaran
    - Criticality
- **Yang tidak boleh diedit setelah aktif:**
    - Start date
- **Jika salah input:** Buat subscription baru.

### 3.3 Status subscription
- Status ditentukan oleh sistem:
    - `Active`
    - `Expiring Soon`
    - `Expired`
- **User tidak boleh mengubah status manual.**

---

## 🔁 4️⃣ Aturan Renewal
- Renewal terjadi ketika: **Finance mencatat payment record**.
- Setelah renewal:
    - Periode subscription maju.
    - Histori lama tetap tersimpan.
- **Renewal tidak otomatis ke vendor.**

---

## 💰 5️⃣ Aturan Payment Record
- Payment record:
    - Hanya bisa dibuat oleh **Finance** atau **Admin**.
    - **Tidak boleh dihapus.**
    - Hanya boleh dikoreksi dengan record baru.
- **Tujuan:** Menjaga audit trail.

---

## 🔐 6️⃣ Aturan Credential

### 6.1 Prinsip
- Credential adalah data paling sensitif.
- **Aturan:**
    - Tidak boleh ditampilkan ke semua role.
    - Tidak boleh diekspor massal.

### 6.2 Edit credential
- Hanya **Admin** dan **DevOps**.
- **Finance tidak boleh melihat SSH.**

---

## ⚠️ 7️⃣ Aturan Criticality
- Criticality ditentukan saat service dibuat.
- Digunakan untuk:
    - Prioritas reminder
    - Prioritas dashboard
- **Criticality tidak mempengaruhi nominal.**

---

## 🔔 8️⃣ Aturan Reminder
- Reminder bersifat:
    - Otomatis
    - **Tidak bisa dimatikan per user**
- **Tujuan:** Mencegah human error.

---

## 🚫 9️⃣ Hal yang Tidak Dilakukan Sistem
Sistem tidak akan:
- ❌ Melakukan pembayaran otomatis
- ❌ Menghubungi API vendor
- ❌ Membuat invoice client
- ❌ Mencatat jurnal accounting

---

## 🧠 10️⃣ Filosofi Boundary
Jika muncul pertanyaan:
> “Apakah fitur ini perlu?”

Maka jawabannya harus mengacu ke:
> "Apakah ini membantu mencegah layanan mati karena lupa bayar?"

**Jika tidak → tidak masuk scope.**

---

## 📌 Catatan Penutup
Dokumen ini menjadi aturan tetap sistem sebelum masuk ke desain teknis.

**Perubahan boundary hanya boleh dilakukan jika ada kebutuhan bisnis baru.**
