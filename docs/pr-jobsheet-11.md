# Pull Request: Fitur Autentikasi, Kontrol Akses Peran (RBAC), dan Antarmuka Responsif (Jobsheet 11)

- **Cabang Sumber:** `fitur/autentikasi`
- **Cabang Tujuan:** `main`
- **Peninjau (Reviewer):** Tim Pengembang Exito Playbox
- **Status:** Approved & Ready to Merge

---

## 1. Ringkasan Perubahan Kode
Pull Request ini mengimplementasikan modul autentikasi dan otorisasi komprehensif untuk sistem manajemen rental PlayStation Exito Playbox:
1. **Penyimpanan Kredensial Aman:** Menghash kata sandi pengguna dengan algoritma modern `scrypt` / `pbkdf2:sha256` ber-salt otomatis via Werkzeug Security. Tersedia modul layanan `create_user()`, `authenticate_user()`, dan skrip CLI interaktif `buat_pengguna.py`.
2. **Rute Login & Logout:**
   - Pesan galat netral identik (*"Nama pengguna atau kata sandi salah"*) untuk meniadakan celah *user enumeration*.
   - Pembersihan sesi menggunakan `session.clear()` sebelum menginisialisasi sesi baru dan saat keluar.
   - Sanitasi query `next` melalui fungsi `is_safe_url()` untuk menangkal celah *Open Redirect*.
   - Rute logout diisolasi hanya menerima metode HTTP `POST`.
3. **Kontrol Akses Berbasis Peran (RBAC):**
   - Decorator `@login_diperlukan` mengalihkan tamu ke halaman login.
   - Decorator `@peran_diperlukan(*roles)` menegakkan otorisasi tingkat server dan mengembalikan HTTP 403 Forbidden bila peran kasir mencoba mengakses modul master (tambah/ubah/hapus konsol dan paket sewa).
   - Templat galat informatif `templates/403.html`.
4. **Antarmuka & Pengalaman Pengguna:**
   - Pemisahan CSS terpusat pada `static/style.css`.
   - Templat `templates/base.html` menyesuaikan menu navigasi dan identitas pengguna sesuai peran yang aktif.
   - Templat `templates/daftar_konsol.html` menyembunyikan tombol kelola untuk peran kasir.
   - Validasi formulir dua lapis (atribut HTML5 + sanitasi server).
5. **Rangkaian Pengujian Otomatis:**
   - Skrip `tests/test_autentikasi_peran.py` mengeksekusi 9 skenario uji autentikasi & peran (Lulus 100%).
   - Skrip `tests/uji_cepat.py` diperluas dengan 6 pengujian baru dan mencetak `"SEMUA UJI LULUS"`.

---

## 2. Penggunaan AI & Refleksi Pengembang
- **Siklus Vibe Coding:** Menghasilkan 9 entri baru (Entri 21–29) pada `jurnal-vibe-coding.md`.
- **Temuan Kritis Terhadap Kode AI (Entri 29):**
  - AI sempat menyarankan enkripsi sederhana/hash cepat `hashlib.sha256()` polos tanpa salt dan hanya menyembunyikan elemen antarmuka di Jinja2.
  - Pengembang mengoreksi dan mewajibkan KDF ber-salt kuat (`generate_password_hash`) serta penegakan otorisasi di tingkat server backend (`@peran_diperlukan`), membuktikan prinsip *human-in-the-loop*.

---

## 3. Daftar Temuan Keamanan yang Ditunda (Untuk Pertemuan 12)
Sesuai dokumen `docs/temuan-keamanan.md`, empat aspek keamanan tingkat lanjut dijadwalkan untuk Sprint 2 (Pertemuan 12):
1. Pembatasan laju percobaan login (*Rate Limiting* / Brute Force Mitigation).
2. Penerapan token CSRF acak tersembunyi pada seluruh formulir POST.
3. Penetapan atribut cookie `HttpOnly`, `SameSite=Lax`, dan `Secure`.
4. Kedaluwarsa otomatis sesi menganggur (*Session Idle Timeout* 30 menit).

---

## 4. Daftar Periksa Peninjauan (Review Checklist)
- [x] Seluruh kode mematuhi arsitektur 3-tier (`app.py`, `services.py`, `models.py`).
- [x] Tidak ada kata sandi teks polos (*plaintext*) di kode maupun basis data.
- [x] Hak akses teruji pada metode GET maupun POST.
- [x] Rangkaian pengujian unit dan regresi mandiri lulus 100% (`python tests/uji_cepat.py`).
