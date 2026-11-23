# Spesifikasi Fitur Kecil — Modul Berelasi & Transaksi: Sesi Sewa (`transactions`)

Dokumen ini mendefinisikan spesifikasi fitur modul berelasi (*foreign key relationships*), transaksi multi-tabel atomik, pencarian, dan penyaringan pada Sistem Manajemen Rental PlayStation (Exito Playbox).

---

## 1. Penetapan Entitas Berelasi
- **Entitas Berelasi:** `transactions` (Pencatatan Transaksi Sewa Konsol)
- **Tabel Induk yang Dirujuk (*Foreign Keys*):**
  1. `consoles` (`console_id` $\rightarrow$ `consoles.id` ON DELETE RESTRICT): Unit PlayStation fisik yang disewa.
  2. `packages` (`package_id` $\rightarrow$ `packages.id` ON DELETE RESTRICT): Paket durasi dan tarif sewa yang dipilih.
  3. `users` (`user_id` $\rightarrow$ `users.id` ON DELETE RESTRICT): Kasir/operator yang memproses transaksi.
- **Relasi & Dampak Atomik (Dua Tabel Berubah Bersama):**
  Saat kasir membuka sesi sewa baru:
  1. Baris baru ditambahkan ke tabel `transactions` dengan `waktu_mulai = CURRENT_TIMESTAMP`, `status_bayar = 'open_bill'` (atau `'lunas'`).
  2. Status unit pada tabel `consoles` berubah dari `'tersedia'` menjadi `'terpakai'`.
  *Kedua operasi wajib dieksekusi dalam satu transaksi atomik (`with conn:` / `BEGIN TRANSACTION` $\rightarrow$ `COMMIT`). Kegagalan salah satu operasi otomatis memicu pembatalan penuh (rollback).*

---

## 2. Tabel Spesifikasi 4 Fitur Kecil (Langkah 2)

| No | Fitur Kecil | Kriteria Penerimaan (dari PRD, SRS, & Kamus Data) | Pelaksana |
|:--:|---|---|:--:|
| **G1** | **Daftar Transaksi Sewa dengan JOIN (`GET /sewa`)** | Menampilkan daftar sesi sewa lengkap dengan data dari tabel induk hasil kueri `JOIN`: kode konsol dan tipe konsol (`consoles`), nama paket dan tarif (`packages`), nama kasir (`users`), serta identitas `nama_pelanggan`, waktu mulai sewa, dan badge status pembayaran (`lunas` / `open_bill` / `batal`). Kueri menggunakan alias kolom yang jelas, dan menampilkan keadaan *"Belum ada transaksi sewa yang tercatat"* bila data kosong. | Maruf Syahbana |
| **G2** | **Tambah Sesi Sewa dengan Pilihan Induk (`GET & POST /sewa/buka`)** | Form pembukaan sewa menyajikan pilihan dropdown (`<select>`) konsol yang berstatus `'tersedia'` dan paket sewa yang berstatus aktif (`is_active = 1`). Kasir wajib memasukkan `nama_pelanggan` (minimal 2 karakter). Masukan tanpa memilih konsol/paket atau ID induk 999 ditolak dengan pesan peringatan jelas tanpa *crash* halaman. Menerapkan pola *Post-Redirect-Get* (PRG). | Maruf Syahbana |
| **G3** | **Dampak pada Tabel Lain (Transaksi Atomik Multi-Tabel)** | Saat sesi sewa disimpan, penambahan baris ke `transactions` dan pembaruan `consoles.status = 'terpakai'` dieksekusi dalam satu blok transaksi basis data. Terbukti atomik: bila transaksi berhasil, status konsol berubah dan baris sewa bertambah; bila gagal (misal konsol sudah tidak tersedia / FK invalid), tidak ada data parsial tertinggal. | Maruf Syahbana |
| **G4** | **Pencarian dan Penyaringan Data Sewa (Sesi 2)** | Menyediakan pencarian nama pelanggan atau kode konsol menggunakan parameter `GET /sewa?q=...` dengan kueri `LIKE ?` berparameter dan escape karakter khusus (`%` dan `_`). Dapat dikombinasikan dengan penyaring `status_bayar` (`?q=budi&status=open_bill`). Aman dari manipulasi injeksi SQL. | Maruf Syahbana |
