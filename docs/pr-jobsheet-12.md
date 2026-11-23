# Pull Request: Pengerasan Keamanan Berbasis OWASP Top 10, Proteksi CSRF, Rate Limiting Login, dan Audit Logging (Jobsheet 12)

- **Branch Asal:** `fitur/perbaikan-keamanan`
- **Branch Tujuan:** `main`
- **Penulis (Author):** Maruf Syahbana (Product Owner & Full-Stack Developer)
- **Status PR:** Siap Ditinjau & Digabungkan (*Ready for Review & Merge*)
- **Target Rilis:** Checkpoint RTM-2 Minggu 12

---

## 1. Ringkasan Perubahan (Summary of Changes)

PR ini mengintegrasikan serangkaian pengerasan keamanan sistem perangkat lunak (*software security hardening*) berbasis standar **OWASP Top 10 (2021)** pada Sistem Manajemen Rental PlayStation **Exito Playbox** (`rpl-project-ps`), menindaklanjuti audit temuan kerentanan pada Sesi 1 dan implementasi perbaikan pada Sesi 2:

### A. Penguatan Keamanan Inti (Core Security Features)
1. **Perlindungan Cross-Site Request Forgery (CSRF) Token:**
   - Implementasi generator token sesi kriptografis `get_csrf_token()` berbasis `secrets.token_hex(32)`.
   - Injeksi global Jinja2 `csrf_token()` yang dapat dipanggil di seluruh formulir HTML.
   - Middleware `@app.before_request` `csrf_protect_middleware()` yang memvalidasi setiap permintaan metode `POST`, `PUT`, `DELETE`, dan `PATCH`.
   - Templat respons informatif HTTP 400 Bad Request (`templates/400_csrf.html`) bila token hilang atau tidak cocok.
   - Penyisipan `<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">` pada seluruh formulir mutasi data (login, logout, tambah/ubah/hapus konsol, tambah/ubah/hapus paket, buka sewa, selesaikan sewa).
2. **Pembatasan Laju Percobaan Login (Rate Limiting) & Pencegahan Brute Force:**
   - Mekanisme pelacak kegagalan login berbasis pasangan komposit `(ip, username.lower())` dengan jendela waktu geser (*sliding window*) 5 menit.
   - Mengizinkan maksimal 5 kali percobaan gagal; percobaan ke-6 langsung mengembalikan status **HTTP 429 Too Many Requests** beserta pesan edukatif waktu tunggu.
   - Otomatis mereset penghitung saat pengguna berhasil login dengan kredensial valid.
3. **Audit Logging Keamanan Berstandar Privasi:**
   - Integrasi modul `logging` Python (`exito_playbox_security`) untuk merekam insiden keamanan: percobaan login gagal, login berhasil, dan penolakan validasi CSRF.
   - **Prinsip Privasi:** Tidak pernah mencatat kata sandi dalam bentuk plaintext maupun hash ke berkas log/konsol.
4. **Pengerasan Konfigurasi Produksi & Atribut Cookie Sesi:**
   - Penolakan start aplikasi di lingkungan produksi (`FLASK_ENV=production`) jika `SECRET_KEY` masih menggunakan nilai default pengembangan.
   - Atribut cookie sesi yang diperketat: `SESSION_COOKIE_HTTPONLY = True`, `SESSION_COOKIE_SAMESITE = 'Lax'`, dan `SESSION_COOKIE_SECURE = is_production`.
5. **Injeksi Security Headers:**
   - Header HTTP proteksi browser pada setiap respons `@app.after_request`:
     - `X-Content-Type-Options: nosniff` (mencegah MIME-sniffing exploit).
     - `X-Frame-Options: SAMEORIGIN` (mencegah Clickjacking berbasis iframe).
     - `Referrer-Policy: strict-origin-when-cross-origin` (mencegah kebocoran parameter sensitif ke domain luar).

---

## 2. Berkas yang Diubah dan Ditambahkan (Files Changed)

| Jalur Berkas | Kategori | Ringkasan Modifikasi |
|---|:---:|---|
| `app.py` | Modifikasi | Penambahan CSRF middleware, helper rate-limiting, audit logging, konfigurasi cookie, dan injection security headers. |
| `templates/400_csrf.html` | Baru | Halaman penolakan ramah pengguna saat validasi token CSRF gagal (HTTP 400). |
| `templates/base.html` | Modifikasi | Token CSRF pada form logout. |
| `templates/login.html` | Modifikasi | Token CSRF pada form login kasir & owner. |
| `templates/tambah_konsol.html` | Modifikasi | Token CSRF pada form tambah unit. |
| `templates/ubah_konsol.html` | Modifikasi | Token CSRF pada form ubah unit & form hapus unit. |
| `templates/tambah_paket.html` | Modifikasi | Token CSRF pada form tambah paket sewa. |
| `templates/ubah_paket.html` | Modifikasi | Token CSRF pada form ubah paket & form hapus paket. |
| `templates/buka_sewa.html` | Modifikasi | Token CSRF pada form buka sewa kasir. |
| `templates/daftar_sewa.html` | Modifikasi | Token CSRF pada form modal selesaikan sewa. |
| `docs/laporan-temuan.md` | Baru | Dokumen audit OWASP Top 10, analisis 10 kasus rentan, 3 bukti eksploitasi, dan 7 audit mandiri proyek. |
| `docs/skrip-demo.md` | Baru | Panduan gladi demonstrasi checkpoint Minggu 12 durasi 5 menit terukur. |
| `docs/latihan-mandiri-keamanan-lanjutan.md` | Baru | Kajian mendalam AI vs Manusia, audit dependensi `requirements.txt`, dan mitigasi kebocoran `SECRET_KEY`. |
| `docs/rencana-sprint.md` | Modifikasi | Pemutakhiran capaian Sprint 2 dan rincian teknis $\ge 20$ skenario uji Sprint 3. |
| `jurnal-vibe-coding.md` | Modifikasi | Penambahan 8 entri baru (total 37 entri) dan evaluasi proporsi Terima/Ubah/Tolak. |
| `tests/uji_cepat.py` | Modifikasi | Penambahan pengujian verifikasi headers, penolakan CSRF, dan rate limiting login. |
| `tests/test_*.py` | Modifikasi | Sinkronisasi helper `post_csrf` pada seluruh skrip pengujian fungsional unit. |

---

## 3. Hasil Pengujian Otomatis (Test Verification)

Seluruh suite pengujian otomatis telah dijalankan dan lulus 100%:

```text
2026-11-23 08:31:44,100 [WARNING] exito_playbox_security: Validasi CSRF gagal untuk IP 127.0.0.1 pada rute /login
2026-11-23 08:31:44,104 [WARNING] exito_playbox_security: Validasi CSRF gagal untuk IP 127.0.0.1 pada rute /login
2026-11-23 08:31:44,496 [WARNING] exito_playbox_security: Percobaan login gagal untuk nama pengguna 'user_bruteforce' dari IP 127.0.0.1 (Kegagalan 1/5)
2026-11-23 08:31:44,676 [WARNING] exito_playbox_security: Percobaan login gagal untuk nama pengguna 'user_bruteforce' dari IP 127.0.0.1 (Kegagalan 2/5)
2026-11-23 08:31:44,855 [WARNING] exito_playbox_security: Percobaan login gagal untuk nama pengguna 'user_bruteforce' dari IP 127.0.0.1 (Kegagalan 3/5)
2026-11-23 08:31:45,024 [WARNING] exito_playbox_security: Percobaan login gagal untuk nama pengguna 'user_bruteforce' dari IP 127.0.0.1 (Kegagalan 4/5)
2026-11-23 08:31:45,189 [WARNING] exito_playbox_security: Percobaan login gagal untuk nama pengguna 'user_bruteforce' dari IP 127.0.0.1 (Kegagalan 5/5)
2026-11-23 08:31:45,362 [INFO] exito_playbox_security: Login berhasil untuk pengguna 'kasir_siti' dari IP 127.0.0.1
2026-11-23 08:31:45,549 [INFO] exito_playbox_security: Login berhasil untuk pengguna 'owner_budi' dari IP 127.0.0.1
SEMUA UJI LULUS
```

- [x] `tests/uji_cepat.py`: **SEMUA UJI LULUS**
- [x] `tests/test_autentikasi_peran.py`: **LULUS 100% (10 Sub-skenario)**
- [x] `tests/test_transaksi_berelasi.py`: **LULUS 100% (Atomisitas, FK, & Denda)**
- [x] `tests/test_crud_konsol.py`: **LULUS 100%**
- [x] `tests/test_crud_packages.py`: **LULUS 100%**
- [x] `tests/test_tambah_konsol.py`: **LULUS 100%**

---

## 4. Checklist Kesiapan Penggabungan (Merge Checklist)

- [x] Branch `fitur/perbaikan-keamanan` disinkronkan dengan basis data dan pengujian terbaru.
- [x] Kunci rahasia atau kata sandi tidak ada yang bocor di kode sumber maupun berkas commit.
- [x] Parameterized query dipertahankan 100% pada seluruh query SQL di `services.py`.
- [x] Token CSRF disematkan pada seluruh form HTML metode `POST`.
- [x] Rate limiting login teruji mengunci serangan brute force tanpa memblokir IP secara membabi buta.
- [x] Skrip demo 5 menit (`docs/skrip-demo.md`) siap dipraktikkan pada evaluasi checkpoint dosen.
- [x] Jurnal Vibe Coding telah diperbarui dengan total 37 entri.
- [x] Seluruh unit test suite lulus tanpa galat regresi fungsional.
