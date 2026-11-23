# Catatan Perubahan (Changelog) — Exito Playbox

Format penulisan catatan perubahan ini mengikuti panduan [Keep a Changelog](https://keepachangelog.com/id/1.0.0/) dan mematuhi prinsip [Semantic Versioning](https://semver.org/lang/id/).

---

## [1.0.1] — 2026-11-24

Rilis tambalan (*patch release*) menindaklanjuti umpan balik pengujian penerimaan pengguna (UAT) butir `TR-02`.

### Diperbaiki (Fixed)
- Penyempurnaan pesan konfirmasi visual (*JavaScript confirmation prompt*) saat kasir menyelesaikan sesi sewa untuk mencegah penghentian transaksi sewa tidak sengaja: *"Apakah Anda yakin ingin menyelesaikan sesi sewa pelanggan '...'? Unit konsol akan otomatis kembali berstatus TERSEDIA."*
- Peningkatan kejelasan label aksi operasional pada tabel transaksi aktif.

---

## [1.0.0] — 2026-11-23

Rilis versi produksi perdana (**v1.0.0**) Sistem Manajemen Rental PlayStation **Exito Playbox** (`rpl-project-ps`). Sistem dirancang untuk membantu operasional rental dalam pencatatan sewa, pemantauan status konsol, kalkulasi tarif dan denda, serta pengamanan hak akses pengguna.

### Ditambahkan (Added)
- **Modul Master Unit Konsol (`consoles`):** Pencatatan inventaris konsol (PS3, PS4, PS5) dengan kode unik ($\ge 4$ char), badge status visual (tersedia, terpakai, maintenance), serta pembatasan hak hapus jika terkait transaksi (*ON DELETE RESTRICT*).
- **Modul Master Paket Sewa (`packages`):** Pengelolaan paket sewa jam (nama paket, jenis konsol, durasi menit, harga sewa) dengan validasi durasi $>0$ menit dan harga $\ge 0$.
- **Modul Transaksi Sewa Berelasi (`transactions`):** Pembukaan sesi sewa kasir dengan kueri JOIN multi-tabel, transaksi atomik pembaruan status unit menjadi `'terpakai'`, pencarian nama pelanggan berparameter (anti-SQLi), dan penyaringan multi-kriteria (`status_bayar` dan `jenis_konsol`).
- **Modul Penghentian Sewa & Denda (`fines`):** Penghentian transaksi sewa, pemulihan status konsol menjadi `'tersedia'`, dan kalkulasi otomatis denda keterlambatan (toleransi 5 menit, Rp 1.000 / menit kelebihan waktu).
- **Autentikasi & Role-Based Access Control (RBAC):**
  - Penyimpanan kata sandi aman berbasis *Scrypt* dengan salt acak unik.
  - Decorator otorisasi server `@login_diperlukan` dan `@peran_diperlukan('kasir', 'owner')`.
  - Halaman galat 403 Forbidden informatif dan pesan login identik (anti user enumeration).
- **Pengerasan Keamanan OWASP Top 10:**
  - Perlindungan Cross-Site Request Forgery (CSRF) pada seluruh form `POST` dengan middleware penolakan HTTP 400 (`templates/400_csrf.html`).
  - Pembatasan laju login (*Rate Limiting*) maksimal 5 kegagalan per 5 menit $\rightarrow$ percobaan ke-6 mengembalikan status HTTP 429 Too Many Requests.
  - Audit logging keamanan privasi (tanpa mencatat password plaintext).
  - Security headers HTTP (`X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `Referrer-Policy: strict-origin-when-cross-origin`).
  - Atribut cookie sesi aman (`HttpOnly`, `SameSite=Lax`, dan `COOKIE_SECURE`).
- **Infrastruktur Rilis & Produksi:**
  - Berkas penomoran versi [versi.py](file:///c:/Users/maaru/Documents/rpl-project-ps/versi.py) dan penayangan versi di kaki halaman templat.
  - Skrip pencadangan mandiri [cadangkan.py](file:///c:/Users/maaru/Documents/rpl-project-ps/cadangkan.py) menggunakan SQLite Online Backup API.
  - Dukungan server produksi berkinerja tinggi WSGI **Waitress** (`waitress==3.0.2`).
  - Dukungan variabel lingkungan `TOKO_DB` untuk fleksibilitas direktori basis data.
  - Rangkaian pengujian otomatis komprehensif (38 fungsi uji Pytest dan skrip regresi mandiri `tests/uji_cepat.py`).

### Diperbaiki (Fixed)
- **`D-01`**: Penanganan masukan non-string pada parameter `nama_pelanggan` transaksi kini dinormalisasi secara aman menjadi string tanpa memicu `AttributeError` (HTTP 500).
- **`D-02`**: Validasi keunikan nama paket sewa diperketat menggunakan perbandingan *case-insensitive* (`LOWER(nama_paket) = LOWER(?)`) sehingga mencegah duplikasi semantik.
- **`D-03`**: Penolakan pengubahan status manual unit konsol yang sedang berada dalam sesi sewa aktif (`current['status'] == 'terpakai'`) dengan respons HTTP 400 ramah.
- Pencegahan serangan *Open Redirect* pada parameter `next` URL login via sanitasi fungsi helper `is_safe_url()`.

### Keamanan (Security)
- Larangan *startup* aplikasi di lingkungan produksi (`APP_ENV=production` atau `FLASK_ENV=production`) jika variabel lingkungan `SECRET_KEY` tidak disetel (menghilangkan ketergantungan pada *fallback secret key*).
- Penghapusan seluruh kredensial dan berkas basis data dari riwayat pelacakan Git melalui konfigurasi [.gitignore](file:///c:/Users/maaru/Documents/rpl-project-ps/.gitignore).
