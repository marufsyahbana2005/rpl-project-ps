# Skrip Gladi Demo Checkpoint 5 Menit — Exito Playbox (Minggu 12)

Dokumen ini memuat skenario panduan teknis dan alur demonstrasi berdurasi ketat **5 menit (300 detik)** untuk evaluasi *Checkpoint RTM-2 (Minggu 12)* Sistem Manajemen Rental PlayStation **Exito Playbox**.

---

## 1. Lembar Informasi & Persiapan Gladi Demo

- **Nama Proyek:** Exito Playbox (Sistem Manajemen Rental PlayStation)
- **Presenter / Demonstrator:** Maruf Syahbana (Product Owner & Full-Stack Developer)
- **Alokasi Waktu:** Tepat 5 Menit (300 Detik) + Sesi Tanya Jawab Dosen Evaluator
- **Branch Kerja:** `main` (telah digabungkan dari `fitur/perbaikan-keamanan`)
- **Perlengkapan yang Disiapkan Sebelum Demo:**
  1. Terminal 1: Aplikasi Flask berjalan di `http://127.0.0.1:5000` (`python app.py`).
  2. Terminal 2: Siap di direktori proyek untuk eksekusi `python tests/uji_cepat.py` dan inspeksi SQLite.
  3. Browser Web: Terbuka pada tab *Incognito/Private Window* pada alamat `http://127.0.0.1:5000`.
  4. Akun Uji yang Digunakan:
     - **Kasir:** `kasir_siti` / kata sandi: `KasirSiti#2026`
     - **Pemilik (Owner):** `owner_budi` / kata sandi: `OwnerBudi#2026`
     - **Akun Brute-force:** `user_bruteforce` / sembarang kata sandi salah

---

## 2. Tabel Runtutan Waktu (Timeline) Demo 5 Menit

| Menit / Detik | Segmen Demonstrasi | Aktor / Peran | Aksi Utama & Narasi Teknis | Hasil yang Ditampilkan |
|:---:|---|---|---|---|
| **00:00 – 01:00**<br>*(60 dtk)* | **Segmen 1:** Akses Tamu & Autentikasi Kasir | Tamu $\rightarrow$ Kasir | 1. Buka `http://127.0.0.1:5000/sewa` sebagai tamu.<br>2. Jelaskan pengalihan otomatis ke `/login?next=%2Fsewa`.<br>3. Masuk dengan akun `kasir_siti`.<br>4. Perlihatkan navbar dinamis kasir. | • Terlempar ke login.<br>• Login sukses dengan pesan flash selamat datang.<br>• Menu hanya memuat: *Sewa Konsol*, *Buka Sewa*, dan *Daftar Unit Konsol*. |
| **01:00 – 02:00**<br>*(60 dtk)* | **Segmen 2:** Transaksi Buka Sewa & Atomisitas | Kasir (`kasir_siti`) | 1. Klik menu **Buka Sewa**.<br>2. Pilih unit `PS4-01` dan paket `Reguler 1 Jam`.<br>3. Masukkan nama pelanggan `Rian Pratama`.<br>4. Klik Simpan Sewa.<br>5. Buka tab Daftar Unit Konsol. | • Transaksi sewa baru tercatat status `open_bill`.<br>• Unit `PS4-01` otomatis berubah status menjadi badge merah `terpakai`.<br>• Tidak bisa disewa pelanggan lain. |
| **02:00 – 03:00**<br>*(60 dtk)* | **Segmen 3:** Pembuktian Keamanan (403 RBAC & 429 Rate Limiting) | Kasir & Penyerang Simulasi | 1. Kasir mencoba mengetik URL pemilik: `/packages` atau `/consoles/tambah`.<br>2. Tunjukkan halaman penolakan HTTP 403 Forbidden.<br>3. Logout kasir.<br>4. Masukkan password salah 5 kali berturut-turut untuk `user_bruteforce`.<br>5. Percobaan ke-6 ditolak HTTP 429 Too Many Requests. | • Muncul halaman `403.html` informatif tanpa kebocoran stack trace.<br>• Pesan kesalahan login identik (anti user enumeration).<br>• HTTP 429 aktif: "Terlalu banyak percobaan login gagal. Silakan tunggu 5 menit." |
| **03:00 – 04:00**<br>*(60 dtk)* | **Segmen 4:** Penghentian Sewa, Denda, & Hak Akses Owner | Kasir $\rightarrow$ Pemilik (`owner_budi`) | 1. Login kembali sebagai `kasir_siti`.<br>2. Pada transaksi pelanggan, klik tombol **Selesaikan Sewa**.<br>3. Tunjukkan kalkulasi denda otomatis jika melebihi batas waktu sewa.<br>4. Logout kasir $\rightarrow$ Login sebagai `owner_budi`.<br>5. Tunjukkan menu penuh Owner. | • Status transaksi menjadi `lunas`, unit konsol kembali `tersedia`.<br>• Muncul badge denda jika ada keterlambatan.<br>• Owner memiliki akses penuh ke menu Master Unit Konsol dan Paket Sewa. |
| **04:00 – 05:00**<br>*(60 dtk)* | **Segmen 5:** Audit Kriptografi SQLite & Eksekusi Skrip Uji Cepat | Pengembang / Evaluator | 1. Buka Terminal 2, jalankan kueri SQLite `SELECT username, role, substr(password_hash, 1, 25) FROM users;`.<br>2. Perlihatkan kata sandi ter-hash scrypt ber-salt unik.<br>3. Jalankan `python tests/uji_cepat.py`.<br>4. Tunjukkan seluruh uji lulus seketika. | • Tidak ada password plaintext di basis data.<br>• Terminal mencetak log audit keamanan.<br>• Output akhir: `"SEMUA UJI LULUS"` tercetak hijau tanpa galat. |

---

## 3. Naskah Verbal Presenter (Script per Menit)

### Menit 00:00 – 01:00: Pembukaan & Alur Autentikasi Kasir
> *"Selamat pagi Bapak/Ibu evaluator. Hari ini saya mendemonstrasikan sistem Exito Playbox yang telah diperkeras dengan standar keamanan OWASP Top 10.*
>
> *Pertama, jika saya mengakses rute internal `/sewa` sebagai tamu tanpa login, sistem segera mengarahkan saya ke halaman login dengan query `next` yang telah disanitasi dari bahaya Open Redirect.*
>
> *Sekarang saya login menggunakan akun kasir `kasir_siti`. Perhatikan bahwa sistem menerapkan Role-Based Access Control pada antarmuka: kasir hanya diberikan akses menu operasional sewa harian dan daftar inventaris tanpa kemampuan mengubah master paket atau menghapus konsol."*

### Menit 01:00 – 02:00: Alur Transaksi Buka Sewa & Atomisitas Database
> *"Kedua, kasir mencatat sewa baru untuk pelanggan 'Rian Pratama' pada konsol PS4-01 dengan paket 1 jam. Saat form dikirimkan, sistem menggunakan transaksi atomik SQLite:*
>
> *Data sewa berhasil disimpan dan secara bersamaan unit PS4-01 otomatis berubah status menjadi 'terpakai'. Konsol ini tidak akan muncul lagi di dropdown pilihan kasir lain sehingga bentrok penyewaan ganda mustahil terjadi."*

### Menit 02:00 – 03:00: Uji Ketahanan Keamanan (RBAC 403 & Rate Limiting 429)
> *"Ketiga, kita buktikan pertahanan keamanan berlapis:*
>
> *Apabila kasir nakal memanipulasi URL browser menuju rute khusus pemilik di `/packages` atau mengirim request hapus data, decorator otorisasi server segera menolaknya dengan kode HTTP 403 Forbidden.*
>
> *Selanjutnya, saya simulasikan serangan brute force login. Ketika seseorang mencoba memasukkan kata sandi salah sebanyak 5 kali berturut-turut, sistem mencatat audit log keamanan dan pada percobaan ke-6, IP penyerang dikunci dengan status HTTP 429 Too Many Requests selama 5 menit."*

### Menit 03:00 – 04:00: Penghentian Sewa, Denda, & Login Pemilik (Owner)
> *"Keempat, kasir mengakhiri sesi sewa pelanggan. Sistem secara otomatis menghitung durasi aktual terhadap paket sewa. Bila terjadi keterlambatan melebihi batas toleransi, denda Rp 1.000 per menit otomatis dihitung dan dicatat pada tabel fines, sementara unit konsol langsung kembali berstatus 'tersedia'.*
>
> *Sekarang kita beralih masuk sebagai peran Pemilik `owner_budi`. Menu navigasi berubah dinamis menampilkan modul Paket Sewa dan aksi modifikasi unit konsol yang sebelumnya terlarang bagi kasir."*

### Menit 04:00 – 05:00: Verifikasi Kriptografi & Uji Regresi Mandiri
> *"Kelima, kita periksa bukti integritas di lapisan data. Di database SQLite, seluruh kata sandi tersimpan sebagai hash scrypt dengan salt acak unik. Tidak ada teks sandi asli yang disimpan maupun dicatat di log aplikasi.*
>
> *Sebagai penutup, saya jalankan skrip uji regresi otomatis mandiri `python tests/uji_cepat.py`. Seluruh pengujian modul, validasi CSRF token, batas brute-force, dan atomisitas multi-tabel lulus 100% dengan mencetak 'SEMUA UJI LULUS'. Sistem siap memasuki Sprint 3. Terima kasih."*

---

## 4. Rencana Kontinjensi & Mitigasi Kendala Demo (Glitch Protection)

| Potensi Kendala | Penyebab Kemungkinan | Solusi Cepat Saat Demo Live |
|---|---|---|
| **Akun Terkunci 429 sebelum giliran demo** | Pengujian brute-force sebelumnya masih berada dalam jendela waktu 5 menit. | Jalankan skrip reset memori atau restart cepat server Flask: `python app.py` (kamus memori rate-limiter akan ter-reset instan). |
| **Port 5000 terpakai (Address already in use)** | Ada instance Flask latar belakang yang belum mati. | Matikan proses lewat PowerShell: `Get-Process python \| Stop-Process -Force` lalu jalankan kembali `python app.py`. |
| **Data uji berantakan atau kotor** | Pengujian manual berulang mengubah status unit konsol. | Jalankan `python models.py` atau `python buat_pengguna.py` untuk menginisialisasi ulang database sewa bersih dengan data benih awal (*clean seed data*). |
| **CSRF Error 400 saat klik tombol** | Form di-submit dari tab lama sebelum token sesi diperbarui. | Refresh halaman formulir (`F5`) agar token CSRF baru disuntikkan ke elemen formulir tersembunyi. |

---

## 5. Ringkasan Kesiapan Checkpoint

- [x] Skenario demo teruji tepat 5 menit tanpa interupsi.
- [x] Data seed akun uji (`kasir_siti` dan `owner_budi`) siap pakai.
- [x] Respon HTTP 403, 400 (CSRF), dan 429 (Rate Limit) terverifikasi berjalan mulus.
- [x] Skrip `tests/uji_cepat.py` terbukti mencetak `"SEMUA UJI LULUS"` secara konsisten.
