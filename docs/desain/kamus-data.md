# Kamus Data (Data Dictionary) — Exito Playbox

Kamus data ini mendefinisikan struktur fisik seluruh tabel hasil normalisasi 3NF untuk implementasi pada basis data **SQLite**, yang telah diselaraskan dengan hasil **Konfirmasi Aturan Data dengan Klien (Langkah 14)**.

---

## 1. Tabel `users`
Menyimpan data akun pengguna (Kasir/Operator dan Owner) untuk otentikasi serta pembatasan hak akses.

| Nama Kolom | Tipe Data | Wajib (NOT NULL) | Kunci | Aturan Nilai / Constraints | Sumber KF / Konfirmasi |
|---|---|---|---|---|---|
| `id` | `INTEGER` | Ya | **PK** | Auto-increment (`PRIMARY KEY AUTOINCREMENT`) | KF-01 |
| `username` | `TEXT` | Ya | **UNIQUE** | Unik, minimal 4 karakter, tanpa spasi | KF-01 |
| `password_hash` | `TEXT` | Ya | - | Hasil hashing kata sandi (Werkzeug/Bcrypt) | KF-01 |
| `role` | `TEXT` | Ya | - | Nilai valid: `'kasir'` atau `'owner'` (`CHECK`) | KF-01 |
| `is_active` | `INTEGER` | Ya | - | Default `1`; nilai valid: `0` (nonaktif) atau `1` (aktif) (`CHECK`). *(Tandai: **[DITAMBAHKAN HASIL KONFIRMASI Q1]** Akun kasir yang berhenti dinonaktifkan tanpa hard-delete agar audit transaksi tetap utuh)* | Konfirmasi Q1 |

---

## 2. Tabel `consoles`
Menyimpan inventaris unit PlayStation beserta status operasional terkini di lokasi rental.

| Nama Kolom | Tipe Data | Wajib (NOT NULL) | Kunci | Aturan Nilai / Constraints | Sumber KF / Konfirmasi |
|---|---|---|---|---|---|
| `id` | `INTEGER` | Ya | **PK** | Auto-increment (`PRIMARY KEY AUTOINCREMENT`) | KF-04 |
| `kode_konsol` | `TEXT` | Ya | **UNIQUE** | Unik, format kode unit (misal: `'PS4-01'`, `'PS5-02'`) | KF-04 |
| `jenis_konsol` | `TEXT` | Ya | - | Nilai valid: `'PS3'`, `'PS4'`, atau `'PS5'` (`CHECK`). *(Tandai: **[DIKONFIRMASI Q4]** Klien menegaskan saat ini hanya melayani 3 tipe konsol tersebut)* | KF-04, Konfirmasi Q4 |
| `status` | `TEXT` | Ya | - | Default `'tersedia'`; nilai valid: `'tersedia'`, `'terpakai'`, `'maintenance'`. *(Tandai: **[DIKONFIRMASI Q3 & Q5]** Konsol rusak beralih ke `'maintenance'` tanpa dihapus; konsol `'terpakai'` tidak boleh disewa ganda)* | KF-04, KF-05, Konfirmasi Q3, Q5 |

---

## 3. Tabel `packages`
Menyimpan daftar paket durasi penyewaan dan tarif resmi yang berlaku di rental.

| Nama Kolom | Tipe Data | Wajib (NOT NULL) | Kunci | Aturan Nilai / Constraints | Sumber KF / Konfirmasi |
|---|---|---|---|---|---|
| `id` | `INTEGER` | Ya | **PK** | Auto-increment (`PRIMARY KEY AUTOINCREMENT`) | KF-02 |
| `nama_paket` | `TEXT` | Ya | **UNIQUE** | Unik (misal: `'PS4 Reguler 1 Jam'`, `'PS5 Hemat 2 Jam'`) | KF-02 |
| `jenis_konsol` | `TEXT` | Ya | - | Nilai valid: `'PS3'`, `'PS4'`, `'PS5'` (`CHECK`). *(Tandai: **[DITAMBAHKAN HASIL KONFIRMASI Q7]** Mengakomodasi perbedaan tarif sewa berdasarkan tipe konsol PlayStation)* | Konfirmasi Q7 |
| `durasi_menit` | `INTEGER` | Ya | - | Harus lebih besar dari 0 (`durasi_menit > 0`) | KF-02 |
| `harga` | `INTEGER` | Ya | - | Dalam Rupiah, tidak boleh negatif (`harga >= 0`). Nilai `0` diperbolehkan khusus promo/hadiah. *(Tandai: **[DIKONFIRMASI Q6 & Q8]** Tarif flat resmi, dilarang tawar-menawar bebas antarpelanggan)* | KF-02, Konfirmasi Q6, Q8 |
| `is_active` | `INTEGER` | Ya | - | Default `1`; nilai valid: `0` (kedaluwarsa/arsip) atau `1` (aktif) (`CHECK`). *(Tandai: **[DITAMBAHKAN HASIL KONFIRMASI Q9]** Paket promo lama diarsipkan tanpa menghapus histori transaksi)* | Konfirmasi Q9 |

---

## 4. Tabel `transactions`
Menyimpan catatan transaksi penyewaan unit konsol oleh pelanggan yang diproses oleh kasir.

| Nama Kolom | Tipe Data | Wajib (NOT NULL) | Kunci | Aturan Nilai / Constraints | Sumber KF / Konfirmasi |
|---|---|---|---|---|---|
| `id` | `INTEGER` | Ya | **PK** | Auto-increment (`PRIMARY KEY AUTOINCREMENT`) | KF-02, KF-08 |
| `nama_pelanggan` | `TEXT` | Ya | - | Minimal 2 karakter, nama panggilan/pengenal pelanggan di tempat rental. *(Tandai: **[DITAMBAHKAN HASIL KONFIRMASI Q10]** Mencegah kekeliruan unit sewa saat kondisi rental ramai)* | Konfirmasi Q10 |
| `user_id` | `INTEGER` | Ya | **FK** | Merujuk ke `users(id)` (`ON DELETE RESTRICT`) | KF-01, KF-02 |
| `console_id` | `INTEGER` | Ya | **FK** | Merujuk ke `consoles(id)` (`ON DELETE RESTRICT`) | KF-02, KF-04 |
| `package_id` | `INTEGER` | Ya | **FK** | Merujuk ke `packages(id)` (`ON DELETE RESTRICT`) | KF-02 |
| `waktu_mulai` | `DATETIME` | Ya | - | Format ISO-8601 (`YYYY-MM-DD HH:MM:SS`) | KF-02 |
| `waktu_selesai` | `DATETIME` | Tidak | - | Format ISO-8601; bernilai `NULL` selama sesi sewa masih berjalan | KF-02, KF-03 |
| `status_bayar` | `TEXT` | Ya | - | Default `'open_bill'`; nilai valid diperluas: `'lunas'`, `'open_bill'`, atau `'batal'` (`CHECK`). *(Tandai: **[DIUBAH HASIL KONFIRMASI Q11]** Penambahan opsi `'batal'` untuk penanganan pembatalan sewa darurat < 5 menit)* | KF-08, Konfirmasi Q11 |

> **Catatan Retensi Data Transaksi [DIKONFIRMASI Q12]:**  
> Data transaksi bersifat permanen untuk audit keuangan minimal 3-5 tahun (*No Hard Delete*). Seluruh relasi kunci asing ke tabel master menggunakan aturan `ON DELETE RESTRICT`.

---

## 5. Tabel `fines`
Menyimpan rincian denda keterlambatan (*overtime*) apabila waktu penghentian sewa melebihi durasi paket.

| Nama Kolom | Tipe Data | Wajib (NOT NULL) | Kunci | Aturan Nilai / Constraints | Sumber KF / Konfirmasi |
|---|---|---|---|---|---|
| `id` | `INTEGER` | Ya | **PK** | Auto-increment (`PRIMARY KEY AUTOINCREMENT`) | KF-03 |
| `transaction_id` | `INTEGER` | Ya | **FK, UNIQUE** | Merujuk ke `transactions(id)` (`ON DELETE CASCADE`); unik untuk relasi `1:1` | KF-03 |
| `menit_terlambat` | `INTEGER` | Ya | - | Akumulasi keterlambatan dalam menit (`menit_terlambat >= 0`). *(Tandai: **[DIKONFIRMASI Q13]** Terdapat grace period 5 menit; jika `<= 5` menit, denda tetap Rp 0)* | KF-03, Konfirmasi Q13 |
| `biaya_denda` | `INTEGER` | Ya | - | Nominal denda dalam Rupiah (`biaya_denda >= 0`). *(Tandai: **[DIKONFIRMASI Q14]** Denda boleh bernilai 0 bila mendapat pembebasan/kompensasi dari kasir/pemilik)* | KF-03, Konfirmasi Q14 |

---

## 6. Daftar Perubahan dan Penyesuaian Kamus Data (Hasil Konfirmasi Klien - Langkah 14)

Berikut adalah rekapitulasi penyesuaian kolom dan batasan (*constraints*) pada kamus data sebagai tindak lanjut langsung dari hasil konfirmasi aturan data bersama pihak klien:

| No | Tabel Terkait | Nama Kolom / Batasan | Sifat Perubahan | Keterangan & Alasan Bisnis Klien |
|:--:|---|---|:--:|---|
| 1 | `users` | `is_active` | **Penambahan Kolom Baru** | Ditambahkan tipe `INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1))`. Kasir yang berhenti dinonaktifkan statusnya agar tidak bisa login, tanpa menghapus riwayat transaksi lampau. |
| 2 | `packages` | `jenis_konsol` | **Penambahan Kolom Baru** | Ditambahkan tipe `TEXT NOT NULL CHECK (jenis_konsol IN ('PS3', 'PS4', 'PS5'))`. Tarif sewa berbeda antarkonsol sehingga paket wajib terikat pada jenis unit tertentu. |
| 3 | `packages` | `is_active` | **Penambahan Kolom Baru** | Ditambahkan tipe `INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1))`. Paket sewa promo lama yang kedaluwarsa dinonaktifkan (arsip) tanpa merusak integritas foreign key transaksi lampau. |
| 4 | `transactions` | `nama_pelanggan` | **Penambahan Kolom Baru** | Ditambahkan tipe `TEXT NOT NULL`. Kasir wajib menginput nama pelanggan saat sesi rental dibuka agar mempermudah identifikasi pelanggan di ruang rental saat ramai. |
| 5 | `transactions` | `status_bayar` | **Pembaruan Batasan (Constraint)** | Batasan diubah dari `CHECK (status_bayar IN ('lunas', 'open_bill'))` menjadi `CHECK (status_bayar IN ('lunas', 'open_bill', 'batal'))` untuk menangani pembatalan sewa darurat (misal: listrik padam < 5 menit pertama). |
| 6 | `consoles` | Kebijakan Delete | **Penegasan Aturan Integritas** | Ditegaskan batasan `ON DELETE RESTRICT`. Unit konsol fisik tidak boleh dihapus jika memiliki riwayat transaksi; unit rusak cukup dialihkan status operasionalnya ke `'maintenance'`. |
| 7 | `fines` | Logika Bisnis Denda | **Penegasan Aturan Validasi** | Ditegaskan aturan toleransi (*grace period*) 5 menit (keterlambatan $\le 5$ menit menghasilkan denda Rp 0). Kolom denda tetap mendukung nilai `0` untuk kompensasi/toleransi kasir. |
| 8 | Seluruh Basis Data | Kebijakan Retensi | **Penetapan Aturan Penyimpanan** | Data transaksi disimpan permanen (minimal 3–5 tahun untuk audit pembukuan). Sistem tidak mengizinkan aksi *hard delete* pada data transaksional. |
