# Kamus Data (Data Dictionary) — Exito Playbox

Kamus data ini mendefinisikan struktur fisik seluruh tabel hasil normalisasi 3NF untuk implementasi pada basis data **SQLite**.

---

## 1. Tabel `users`
Menyimpan data akun pengguna (Kasir/Operator dan Owner) untuk otentikasi serta pembatasan hak akses.

| Nama Kolom | Tipe Data | Wajib (NOT NULL) | Kunci | Aturan Nilai / Constraints | Sumber KF |
|---|---|---|---|---|---|
| `id` | `INTEGER` | Ya | **PK** | Auto-increment (`PRIMARY KEY AUTOINCREMENT`) | KF-01 |
| `username` | `TEXT` | Ya | **UNIQUE** | Unik, minimal 4 karakter, tanpa spasi | KF-01 |
| `password_hash` | `TEXT` | Ya | - | Hasil hashing kata sandi (Werkzeug/Bcrypt) | KF-01 |
| `role` | `TEXT` | Ya | - | Nilai valid: `'kasir'` atau `'owner'` (`CHECK`) | KF-01 |

---

## 2. Tabel `consoles`
Menyimpan inventaris unit PlayStation beserta status operasional terkini di lokasi rental.

| Nama Kolom | Tipe Data | Wajib (NOT NULL) | Kunci | Aturan Nilai / Constraints | Sumber KF |
|---|---|---|---|---|---|
| `id` | `INTEGER` | Ya | **PK** | Auto-increment (`PRIMARY KEY AUTOINCREMENT`) | KF-04 |
| `kode_konsol` | `TEXT` | Ya | **UNIQUE** | Unik, format kode unit (misal: `'PS4-01'`, `'PS5-02'`) | KF-04 |
| `jenis_konsol` | `TEXT` | Ya | - | Nilai valid: `'PS3'`, `'PS4'`, atau `'PS5'` (`CHECK`) | KF-04 |
| `status` | `TEXT` | Ya | - | Default `'tersedia'`; nilai valid: `'tersedia'`, `'terpakai'`, `'maintenance'` | KF-04, KF-05 |

---

## 3. Tabel `packages`
Menyimpan daftar paket durasi penyewaan dan tarif resmi yang berlaku.

| Nama Kolom | Tipe Data | Wajib (NOT NULL) | Kunci | Aturan Nilai / Constraints | Sumber KF |
|---|---|---|---|---|---|
| `id` | `INTEGER` | Ya | **PK** | Auto-increment (`PRIMARY KEY AUTOINCREMENT`) | KF-02 |
| `nama_paket` | `TEXT` | Ya | **UNIQUE** | Unik (misal: `'Reguler 1 Jam'`, `'Paket Malam'`) | KF-02 |
| `durasi_menit` | `INTEGER` | Ya | - | Harus lebih besar dari 0 (`durasi_menit > 0`) | KF-02 |
| `harga` | `INTEGER` | Ya | - | Dalam Rupiah, tidak boleh negatif (`harga >= 0`) | KF-02 |

---

## 4. Tabel `transactions`
Menyimpan catatan transaksi penyewaan unit konsol oleh pelanggan yang diproses oleh kasir.

| Nama Kolom | Tipe Data | Wajib (NOT NULL) | Kunci | Aturan Nilai / Constraints | Sumber KF |
|---|---|---|---|---|---|
| `id` | `INTEGER` | Ya | **PK** | Auto-increment (`PRIMARY KEY AUTOINCREMENT`) | KF-02, KF-08 |
| `user_id` | `INTEGER` | Ya | **FK** | Merujuk ke `users(id)` (`ON DELETE RESTRICT`) | KF-01, KF-02 |
| `console_id` | `INTEGER` | Ya | **FK** | Merujuk ke `consoles(id)` (`ON DELETE RESTRICT`) | KF-02, KF-04 |
| `package_id` | `INTEGER` | Ya | **FK** | Merujuk ke `packages(id)` (`ON DELETE RESTRICT`) | KF-02 |
| `waktu_mulai` | `DATETIME` | Ya | - | Format ISO-8601 (`YYYY-MM-DD HH:MM:SS`) | KF-02 |
| `waktu_selesai` | `DATETIME` | Tidak | - | Format ISO-8601; bernilai `NULL` selama sesi sewa masih berjalan | KF-02, KF-03 |
| `status_bayar` | `TEXT` | Ya | - | Default `'open_bill'`; nilai valid: `'lunas'` atau `'open_bill'` | KF-08 |

---

## 5. Tabel `fines`
Menyimpan rincian denda keterlambatan (*overtime*) apabila waktu penghentian sewa melebihi durasi paket.

| Nama Kolom | Tipe Data | Wajib (NOT NULL) | Kunci | Aturan Nilai / Constraints | Sumber KF |
|---|---|---|---|---|---|
| `id` | `INTEGER` | Ya | **PK** | Auto-increment (`PRIMARY KEY AUTOINCREMENT`) | KF-03 |
| `transaction_id` | `INTEGER` | Ya | **FK, UNIQUE** | Merujuk ke `transactions(id)` (`ON DELETE CASCADE`); unik untuk relasi `1:1` | KF-03 |
| `menit_terlambat` | `INTEGER` | Ya | - | Akumulasi keterlambatan dalam menit (`menit_terlambat >= 0`) | KF-03 |
| `biaya_denda` | `INTEGER` | Ya | - | Nominal denda dalam Rupiah (`biaya_denda >= 0`) | KF-03 |