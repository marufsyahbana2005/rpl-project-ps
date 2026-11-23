# Tinjauan Diff Modul Berelasi & Transaksi Multi-Tabel (Langkah 7) — Exito Playbox

Dokumen ini mendokumentasikan hasil tinjauan kode terhadap implementasi relasi foreign key antara `transactions`, `consoles`, `packages`, dan `users`, serta verifikasi transaksi atomik multi-tabel pada branch `fitur/modul-berelasi`.

---

## 1. Verifikasi Tiga Pertanyaan Relasi Kritis
1. **Apakah perubahan dua tabel berada dalam satu transaksi atomik?**  
   **YA.** Pada fungsi `create_transaction()` di `services.py`, operasi penambahan baris ke tabel `transactions` dan pembaruan `consoles.status = 'terpakai'` dibungkus di dalam satu blok transaksi `with conn:`. Jika salah satu kueri gagal (misal pelanggaran foreign key atau kegagalan disk), SQLite secara otomatis membatalkan seluruh operasi (*automatic rollback*).
2. **Apakah ada query di luar models.py dan services.py?**  
   **TIDAK ADA.** Seluruh kueri SQL (termasuk JOIN multi-tabel, kueri berparameter, dan pembaharuan status) 100% diisolasi pada `services.py`. Berkas `app.py` murni berfungsi sebagai pengatur alur (*routing controller*), pembacaan parameter request, dan penyaji templat HTML (*view*).
3. **Apakah kolom status konsol hanya berubah lewat transaksi sewa yang sah?**  
   **YA.** Status `'terpakai'` hanya dapat diaktifkan melalui fungsi `create_transaction()` saat kasir membuka sesi sewa. Form manual ubah unit konsol (`/consoles/<id>/ubah`) secara ketat membatasi pilihan hanya antara `'tersedia'` dan `'maintenance'`, sehingga kasir tidak dapat secara sengaja atau tidak sengaja mengubah status menjadi terpakai tanpa membuka transaksi sewa nyata.

---

## 2. Tabel Temuan dan Tindakan (Lampiran C)

| No | Temuan Masalah / Usulan Perbaikan | Kategori | Tindakan yang Diambil | Alasan Keputusan |
|:--:|---|:--:|---|---|
| **1** | **Pencegahan Kueri Wildcard Liar pada Pencarian:**<br>Pengguna yang menginput karakter `%` atau `_` pada kotak pencarian dapat memicu pencocokan liar (*wildcard match*) yang menampilkan seluruh data. | **Keamanan & Akurasi** | **Diperbaiki:** Menambahkan sanitasi string escape: `.replace('%', '\\%').replace('_', '\\_')` dan menggunakan sintaks SQL `LIKE ? ESCAPE '\\'`. | Memastikan karakter persen dan garis bawah dicari secara harfiah (*literal match*) dan mencegah kebocoran data. |
| **2** | **Proteksi Validasi Induk Konsol yang Sedang Terpakai:**<br>Kasir yang membuka dua tab browser bersamaan berpotensi menyewa konsol yang sama dua kali (*race condition*). | **Kesesuaian Bisnis** | **Diperbaiki:** Pada `create_transaction()`, sistem memeriksa ulang `status = 'tersedia'` tepat di dalam transaksi basis data sebelum melakukan insert dan update status. | Menjamin konsol yang sedang terpakai tidak pernah bisa disewa ganda (*double booking prevention*). |
| **3** | **Penanganan ID Induk Invalid (ID 999):**<br>Bila pengguna mengirim form dengan ID konsol atau paket yang direkayasa manual melalui inspect element, sistem harus menolak secara ramah. | **Pencegahan Galat** | **Diperbaiki:** Ditambahkan validasi keberadaan entitas induk (`console` dan `package`) sebelum transaksi dieksekusi. | Menghindari tampilan crash basis data (*OperationalError*) dan menyajikan pesan peringatan yang informatif. |
