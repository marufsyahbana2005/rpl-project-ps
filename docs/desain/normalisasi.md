# Normalisasi Basis Data — Exito Playbox

## 1. Bentuk Tak Ternormalisasi (UNF - Unnormalized Form)
Data mentah diambil dari **Nota Transaksi Manual Rental PS**, di mana seluruh rincian kasir, unit konsol, paket durasi, transaksi sewa, dan denda dicatat dalam satu lembar gabungan yang mengandung pengulangan data (*repeating groups*).

**Tabel UNF (`nota_rental_mentah`):**
| id_nota | kasir_username | kasir_role | kode_konsol | jenis_konsol | status_konsol | nama_paket | durasi_menit | harga_paket | waktu_mulai | waktu_selesai | status_bayar | menit_terlambat | biaya_denda |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TRX-01 | kasir_andi | kasir | PS4-01 | PS4 | terpakai | Paket 2 Jam | 120 | 16000 | 2026-11-14 10:00 | 2026-11-14 12:30 | lunas | 30 | 4000 |
| TRX-02 | kasir_andi | kasir | PS5-01 | PS5 | terpakai | Paket 1 Jam | 60 | 12000 | 2026-11-14 11:00 | 2026-11-14 12:00 | lunas | 0 | 0 |

---

## 2. Bentuk Normal Pertama (1NF - First Normal Form)
**Syarat 1NF:** Setiap sel bernilai atomik (tunggal), tidak ada atribut berulang (*repeating groups*), dan memiliki *Primary Key* yang unik.

**Masalah yang Diperbaiki:**
- Memastikan seluruh kolom waktu (`waktu_mulai`, `waktu_selesai`), rincian nominal (`harga_paket`, `biaya_denda`), dan identitas entitas dipisah menjadi atribut atomik tunggal.
- Menetapkan `id_nota` sebagai *Primary Key* sementara untuk mengidentifikasi setiap baris transaksi secara unik.

**Struktur 1NF:**
`nota_rental_1nf` (**`id_nota`**, `kasir_username`, `kasir_role`, `kode_konsol`, `jenis_konsol`, `status_konsol`, `nama_paket`, `durasi_menit`, `harga_paket`, `waktu_mulai`, `waktu_selesai`, `status_bayar`, `menit_terlambat`, `biaya_denda`)

---

## 3. Bentuk Normal Kedua (2NF - Second Normal Form)
**Syarat 2NF:** Sudah memenuhi 1NF dan tidak ada ketergantungan parsial (*partial dependency*) terhadap kunci utama, serta memisahkan entitas master yang berdiri sendiri agar tidak terjadi anomali pembaruan (*update anomaly*).

**Masalah yang Diperbaiki:**
- Data master pengguna (`kasir_username`, `kasir_role`), data unit konsol (`kode_konsol`, `jenis_konsol`, `status_konsol`), dan data master paket (`nama_paket`, `durasi_menit`, `harga_paket`) tidak bergantung pada transaksi tunggal, melainkan berdiri sendiri sebagai entitas independen. Jika harga paket atau status konsol berubah, cukup diperbarui di satu tabel master tanpa mengubah seluruh riwayat transaksi.
- Memecah tabel menjadi entitas master dan transaksional dengan *Primary Key* `id` otomatis (*auto-increment*).

**Struktur 2NF:**
1. **`users`** (**`id`**, `username`, `password_hash`, `role`)
2. **`consoles`** (**`id`**, `kode_konsol`, `jenis_konsol`, `status`)
3. **`packages`** (**`id`**, `nama_paket`, `durasi_menit`, `harga`)
4. **`transactions_2nf`** (**`id`**, `user_id`, `console_id`, `package_id`, `waktu_mulai`, `waktu_selesai`, `status_bayar`, `menit_terlambat`, `biaya_denda`)

---

## 4. Bentuk Normal Ketiga (3NF - Third Normal Form)
**Syarat 3NF:** Sudah memenuhi 2NF dan tidak ada ketergantungan transitif (*transitive dependency*), di mana atribut non-kunci bergantung pada atribut non-kunci lainnya.

**Masalah yang Diperbaiki:**
- Pada `transactions_2nf`, atribut `biaya_denda` dan `menit_terlambat` hanya muncul apabila transaksi mengalami keterlambatan (*overtime*) dan nilainya bergantung secara transitif pada evaluasi waktu keterlambatan, bukan langsung pada identitas awal transaksi. Menyimpannya di tabel utama menyebabkan banyak nilai kosong/nol (`NULL`/`0`) pada transaksi tepat waktu.
- Memisahkan pencatatan denda ke dalam tabel **`fines`** yang berelasi `1 : 1` (opsional) dengan **`transactions`**, serta menghapus atribut turunan yang dapat dikalkulasi sistem.

**Struktur Final 3NF (Selaras dengan ERD):**
1. **`users`** (**`id`**, `username`, `password_hash`, `role`)
2. **`consoles`** (**`id`**, `kode_konsol`, `jenis_konsol`, `status`)
3. **`packages`** (**`id`**, `nama_paket`, `durasi_menit`, `harga`)
4. **`transactions`** (**`id`**, `user_id` [FK], `console_id` [FK], `package_id` [FK], `waktu_mulai`, `waktu_selesai`, `status_bayar`)
5. **`fines`** (**`id`**, `transaction_id` [FK], `menit_terlambat`, `biaya_denda`)