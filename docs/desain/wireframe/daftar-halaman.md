# Daftar Halaman Antarmuka — Exito Playbox

Dokumen ini memetakan seluruh kebutuhan halaman antarmuka pengguna (*User Interface*) yang diturunkan langsung dari dokumen Skenario Use Case (`docs/uml/skenario-use-case.md`) dan Kamus Data (`docs/desain/kamus-data.md`).

---

## Tabel Pemetaan Halaman dari Use Case (Langkah 2)

| No | Kode / Nama Halaman | Use Case Terkait | Aktor Pengguna | Data yang Ditampilkan (Merujuk Kamus Data) |
|:--:|---|---|---|---|
| 1 | **wf-01-login**<br>Halaman Masuk (Login) | Autentikasi Pengguna (Prasyarat Sistem) | Kasir, Pemilik (Owner) | `users.username`, `users.password_hash` (input password), `users.role`, `users.is_active`, pesan galat kredensial salah / akun dinonaktifkan. |
| 2 | **wf-02-dasbor-utama**<br>Dasbor Pemantauan Unit & Timer | **UC-03:** Pantau Ketersediaan Unit (Must)<br>**UC-01:** Inisiasi Catat Sewa (Must) | Kasir, Pemilik (Owner) | `consoles.kode_konsol`, `consoles.jenis_konsol`, `consoles.status` (Tersedia / Terpakai / Maintenance), `transactions.nama_pelanggan`, sisa waktu sewa (*real-time countdown timer*), status polling sinkronisasi. |
| 3 | **wf-03-buka-sewa**<br>Form Pembukaan Sewa Konsol | **UC-01:** Catat Transaksi Sewa (Must) | Kasir | `consoles.kode_konsol`, `consoles.jenis_konsol`, `transactions.nama_pelanggan`, daftar `packages.nama_paket`, `packages.durasi_menit`, `packages.harga`, `transactions.waktu_mulai`, estimasi selesai, `transactions.status_bayar` (`'open_bill'` / `'lunas'`). |
| 4 | **wf-04-selesai-sewa-denda**<br>Penghentian Sewa & Kelola Denda | **UC-02:** Kelola Penghentian dan Denda (Should) | Kasir | `transactions.id`, `transactions.nama_pelanggan`, `consoles.kode_konsol`, `packages.nama_paket`, `transactions.waktu_mulai`, `transactions.waktu_selesai`, durasi terpakai, `fines.menit_terlambat`, `fines.biaya_denda`, total tagihan (`packages.harga` + `fines.biaya_denda`), `transactions.status_bayar` (`'lunas'` / `'batal'`). |
| 5 | **wf-05-kelola-master**<br>Manajemen Konsol & Paket (Khusus Pemilik) | Pengelolaan Entitas Master Unit & Paket | Pemilik (Owner) | `consoles.id`, `consoles.kode_konsol`, `consoles.jenis_konsol`, `consoles.status`, `packages.id`, `packages.nama_paket`, `packages.jenis_konsol`, `packages.durasi_menit`, `packages.harga`, `packages.is_active`, modal tambah/ubah status konsol/paket. |
| 6 | **wf-06-riwayat-transaksi**<br>Penelusuran Riwayat Transaksi | **UC-05:** Telusuri Riwayat Transaksi (Should) | Pemilik (Owner), Kasir | `transactions.id`, `transactions.nama_pelanggan`, `consoles.kode_konsol`, `packages.nama_paket`, `transactions.waktu_mulai`, `transactions.waktu_selesai`, `fines.menit_terlambat`, `fines.biaya_denda`, `transactions.status_bayar`, filter pencarian nama pelanggan/tanggal, paginasi data. |
| 7 | **wf-07-laporan-pendapatan**<br>Rekapitulasi Omset & Laporan (Khusus Pemilik) | **UC-04:** Lihat Laporan Pendapatan (Must) | Pemilik (Owner) | Filter rentang tanggal (`transactions.waktu_mulai`), total omset sewa paket (`packages.harga`), total pendapatan denda (`fines.biaya_denda`), total penerimaan bersih, jumlah transaksi, rincian omset per unit konsol (`consoles.kode_konsol`, `consoles.jenis_konsol`). |

---

## Verifikasi Ketercakupan Kebutuhan
- **Minimal 6 Halaman:** Terpenuhi (tersedia 7 halaman spesifik).
- **Ketercakupan Use Case Must:**
  - *UC-01 (Catat Transaksi Sewa):* Dilayani oleh `wf-02` (tombol inisiasi) dan `wf-03` (form transaksi).
  - *UC-03 (Pantau Ketersediaan Unit):* Dilayani oleh `wf-02` (dasbor utama).
  - *UC-04 (Lihat Laporan Pendapatan):* Dilayani oleh `wf-07` (laporan omset).
- **Ketercakupan Use Case Should:**
  - *UC-02 (Kelola Penghentian dan Denda):* Dilayani oleh `wf-04`.
  - *UC-05 (Telusuri Riwayat Transaksi):* Dilayani oleh `wf-06`.
- **Kolom Data:** Seluruh kolom yang ditampilkan merujuk langsung pada kolom kamus data normalisasi 3NF hasil konfirmasi klien.
