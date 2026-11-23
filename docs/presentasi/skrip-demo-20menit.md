# Panduan Operasional & Skrip Live Demo 20 Menit
## Exito Playbox PlayStation Rental Management System

Panduan ini digunakan oleh tim pengembang sebagai lembar panduan eksekusi teknis selama gladi bersih dan pelaksanaan demonstrasi ujian akhir tugas besar di hadapan dewan penguji.

---

## 1. Lembar Alokasi Waktu Gladi Bersih (Total 20 Menit)

| Segmen | Menit | Aktivitas Utama | Perlengkapan & Layar | Target Waktu Riil |
|:---:|:---:|---|---|:---:|
| **1** | 00:00 – 03:00 | Pembukaan, Latar Belakang Mitra, dan Nilai Tambah Sistem | Layar Salindia 1–3 | 2m 50s |
| **2** | 03:00 – 06:00 | Paparan Arsitektur 3-Tier, Kontrol Akses (RBAC), dan OWASP | Layar Salindia 4–6 | 2m 55s |
| **3** | 06:00 – 09:00 | Strategi Pengujian Otomatis Pytest, Penutupan Cacat TDD, & UAT | Layar Salindia 7–9 | 2m 45s |
| **4** | 09:00 – 15:00 | **Live Demo Aplikasi di Server Produksi Waitress (4 Skenario)** | Peramban & Terminal | 5m 40s |
| **5** | 15:00 – 17:30 | Analisis Evaluasi Jurnal Vibe Coding & Dampak Waktu Galat AI | Layar Salindia 10 | 2m 20s |
| **6** | 17:30 – 20:00 | Keterbatasan Teknis, Rekomendasi Masa Depan, & Penutup | Layar Salindia 11–13 | 2m 15s |
| **TOTAL** | **20:00** | **Seluruh Sesi Demonstrasi & Presentasi Selesai Tepat Waktu** | - | **19m 45s (PAS)** |

---

## 2. Skenario Langkah demi Langkah Live Demo (Segmen 4: 09:00 – 15:00)

### Skenario A: Startup Runner Produksi & Verifikasi Lingkungan (1 Menit)
1. **Perintah Terminal:**
   ```bash
   python jalankan.py
   ```
2. **Poin yang Dijelaskan ke Penguji:**
   - Tunjukkan bahwa server menggunakan **Waitress WSGI** dengan 6 threads, bukan development server Flask.
   - Buktikan bahwa server terhubung ke basis data `instance/rental_ps.db` dan environment `FLASK_ENV=production`.

### Skenario B: Demonstrasi Keamanan Otentikasi & RBAC (1.5 Menit)
1. **Buka Browser:** Kunjungi `http://127.0.0.1:8000/login`.
2. **Uji Negatif (Brute-Force & Netralitas Pesan):**
   - Masukkan username sembarang `admin_palsu` dan password salah.
   - Tunjukkan pesan galat: *"Nama pengguna atau kata sandi salah."* (pesan netral anti-enumerasi akun).
3. **Uji Otorisasi Peran Kasir:**
   - Login dengan akun kasir: `kasir_andi` / `Kasir123!`.
   - Perhatikan menu atas: hanya ada menu "Konsol" dan "Sewa". Menu "Kelola Paket" dan menu administratif disembunyikan.
   - Ketik manual URL terlarang di address bar: `http://127.0.0.1:8000/packages`.
   - Tunjukkan respons ramah: **HTTP 403 Forbidden** (halaman akses ditolak).

### Skenario C: Demonstrasi Transaksi Atomik Multi-Tabel (1.5 Menit)
1. **Buka Menu Sewa:** Klik tombol "Buka Sewa" (`/sewa/buka`).
2. **Pilihan Entitas Induk Berelasi:**
   - Tunjukkan bahwa dropdown hanya menampilkan konsol yang saat ini berstatus `'tersedia'`.
   - Pilih konsol `PS4-01`, nama pelanggan `Budi Santoso`, dan pilih `Paket Reguler 2 Jam`.
3. **Eksekusi Pembukaan:**
   - Klik "Buka Sewa".
   - Tunjukkan bahwa secara atomik sistem mencatat baris transaksi baru, dan saat kembali ke menu Konsol, unit `PS4-01` seketika berubah status menjadi **Terpakai** dengan indikator badge warna merah.

### Skenario D: Demonstrasi Penyelesaian Sewa, Denda, & Otomasi Cadangan (2 Menit)
1. **Selesaikan Transaksi Sewa:**
   - Masuk ke `/sewa`, klik tombol "Selesaikan Sewa" pada baris transaksi aktif.
   - Sistem memvalidasi waktu: jika sewa melebihi batas durasi paket di atas toleransi 5 menit, rincian menit keterlambatan dan denda Rp 1.000/menit muncul otomatis di layar.
   - Kasir menekan konfirmasi bayar lunas. Status konsol `PS4-01` seketika kembali pulih menjadi **Tersedia** (badge hijau).
2. **Uji Eksekusi Skrip Uji & Pencadangan di Terminal:**
   ```bash
   python tests/uji_cepat.py
   python cadangkan.py
   ```
   - Tunjukkan output: *"SEMUA UJI LULUS!"* (7 modul keamanan lolos) dalam 1 detik.
   - Tunjukkan berkas baru `backups/rental_ps_backup_YYYYMMDD_HHMMSS.db` tercipta via Online Backup API.

---

## 3. Checklist Kesiapan Teknis Ruang Sidang
- [x] Laptop terhubung ke sumber daya listrik (adaptor terpasang).
- [x] Basis data pengujian telah di-seed dengan data awal bersih (`python -c "from app import create_app; from models import init_db; init_db(create_app())"`).
- [x] Port 8000 bebas dan siap digunakan oleh Waitress.
- [x] Akun uji siap: `kasir_andi` (role kasir) dan `owner_hendra` (role owner).
- [x] File slide PDF / Markdown terbuka pada tab peramban terpisah.
