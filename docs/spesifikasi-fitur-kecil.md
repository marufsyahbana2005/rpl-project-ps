# Spesifikasi Fitur Kecil — Modul CRUD Entitas Pertama: Unit Konsol (`consoles`)

Dokumen ini mendefinisikan rincian 5 fitur kecil (*micro-features*) untuk siklus pengembangan Sesi 1 dan Sesi 2, diturunkan dari dokumen PRD, SRS, dan kamus data.

---

## 1. Penetapan Entitas Pertama
- **Entitas Terpilih:** `consoles` (Unit Konsol PlayStation)
- **Alasan Pemilihan:** Merupakan entitas induk (*master entity*) independen tanpa dependensi kunci asing (*foreign key*) ke tabel lain, serta menjadi fondasi fisik utama operasional rental PlayStation Exito Playbox.
- **Aturan Kamus Data:**
  - `id`: Integer Primary Key Auto-increment.
  - `kode_konsol`: Teks unik, minimal 4 karakter (misal: `PS4-01`, `PS5-02`).
  - `jenis_konsol`: Pilihan terbatas `PS3`, `PS4`, atau `PS5`.
  - `status`: Default `'tersedia'`, nilai valid: `'tersedia'`, `'terpakai'`, `'maintenance'`. Pada form manual ubah konsol, operator hanya dapat beralih antara `'tersedia'` dan `'maintenance'` (karena status `'terpakai'` dikendalikan oleh siklus transaksi sewa).

---

## 2. Tabel Spesifikasi 5 Fitur Kecil (Langkah 2)

| No | Fitur Kecil | Kriteria Penerimaan (dari PRD & Kamus Data) | Kebutuhan Terkait (KF) |
|:--:|---|---|:--:|
| **F1** | **Kerangka Proyek & Inisialisasi Basis Data** | Aplikasi Flask berjalan tanpa galat pada peramban lokal (`http://127.0.0.1:5000`); basis data SQLite (`rental.db`) otomatis dibuat dari `docs/desain/schema.sql` bila berkas belum ada; rute beranda (`/`) otomatis mengalihkan (*redirect*) ke daftar konsol (`/consoles`); kunci rahasia dimuat dari variabel lingkungan. | — |
| **F2** | **Daftar Unit Konsol (`GET /consoles`)** | Menampilkan seluruh unit konsol PlayStation yang tersimpan di basis data dalam format tabel/kartu visual sesuai wireframe `wf-02`/`wf-05`; memuat kolom `kode_konsol`, `jenis_konsol`, dan `status`; menampilkan pesan *"Belum ada unit konsol terdaftar"* bila data kosong; query database berada di lapisan model/service, tidak ada raw SQL di `app.py`. | **KF-04** (Monitoring Ketersediaan Unit) |
| **F3** | **Tambah Unit Konsol (`GET` & `POST /consoles/tambah`)** | Pengguna dapat menambahkan unit konsol baru; input `kode_konsol` dan `jenis_konsol` divalidasi tidak boleh kosong; kode konsol yang sudah terdaftar ditolak dengan pesan peringatan *"Kode konsol sudah ada"*; input yang salah tetap dipertahankan pada form; penyimpanan sukses menerapkan pola *Post-Redirect-Get* (PRG) kembali ke `/consoles` disertai pesan notifikasi keberhasilan. | **KF-01** (Manajemen Unit Konsol) |
| **F4** | **Ubah Unit Konsol (`GET` & `POST /consoles/<id>/ubah`)** | Form ubah memuat data lama unit konsol yang dipilih; pengguna dapat mengubah `kode_konsol`, `jenis_konsol`, dan status operasional (`tersedia` / `maintenance`); mengubah menjadi kode konsol yang sudah dipakai unit lain ditolak; membuka ID yang tidak ada di basis data (misal `/consoles/999/ubah`) menghasilkan respons halaman 404 Not Found yang rapi. | **KF-01** (Manajemen Unit Konsol) |
| **F5** | **Hapus Unit Konsol (`POST /consoles/<id>/hapus`)** | Unit konsol yang belum memiliki riwayat transaksi dapat dihapus dari basis data; penghapusan hanya diproses melalui metode `POST` dengan tombol konfirmasi (akses `GET` tidak menghapus apa pun); unit konsol yang memiliki transaksi sewa tertolak dihapus oleh penegakan integritas referensial (*ON DELETE RESTRICT*) dan memunculkan pesan peringatan jelas tanpa *crash*. | **KF-01** & Integritas Relasi Kamus Data |
