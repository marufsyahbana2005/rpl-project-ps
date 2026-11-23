# Daftar Periksa Audit Kesiapan Rilis (Lampiran B) — Exito Playbox v1.0.0

Dokumen ini memuat hasil audit kesiapan rilis (*Release Readiness Audit*) untuk rilis resmi versi **v1.0.0** Sistem Manajemen Rental PlayStation **Exito Playbox** (`rpl-project-ps`).

---

## 1. Hasil Eksekusi Tiga Pemeriksaan Wajib Terminal Git

| No | Perintah Pemeriksaan Git | Hasil Eksekusi | Status | Catatan / Tindakan |
|:---:|---|---|:---:|---|
| **1** | `git ls-files "*.db" ".env"` | *(Output kosong)* | **LULUS** | Tidak ada file basis data SQLite riil maupun file environment sensitif yang terlacak oleh Git. |
| **2** | `git grep -nI "SECRET_KEY"` | Hanya merujuk pada pengambilan aman `os.environ.get("SECRET_KEY")` di `app.py` dan dokumentasi. | **LULUS** | Tidak ada kunci rahasia (*hardcoded secret key*) atau kredensial yang tertanam di kode sumber. |
| **3** | `git log --all --oneline -- "*.db" ".env"` | *(Output kosong)* | **LULUS** | Tidak ada jejak berkas `.db` maupun `.env` yang pernah ter-commit di seluruh riwayat repositori Git. |

---

## 2. Tabel Daftar Periksa Kesiapan Rilis (Lampiran B)

| Kategori | Butir Periksa | Status | Bukti & Keterangan |
|---|---|:---:|---|
| **Konfigurasi** | Basis data mendukung variabel lingkungan `TOKO_DB` | **LULUS** | Diatur pada `models.py` dan `app.py` dengan fallback aman. |
| **Konfigurasi** | Kunci rahasia `SECRET_KEY` tidak diketik di kode | **LULUS** | Membaca dari `os.environ.get("SECRET_KEY")`. Startup ditolak di mode produksi jika kunci kosong. |
| **Konfigurasi** | Mode produksi (`APP_ENV=production` / `FLASK_ENV=production`) menolak start tanpa `SECRET_KEY` | **LULUS** | `RuntimeError` dilempar dengan pesan jelas jika kunci produksi tidak disetel. |
| **Konfigurasi** | Cookie sesi aman (`HttpOnly`, `SameSite=Lax`, `COOKIE_SECURE`) | **LULUS** | Diatur otomatis pada konfigurasi sesi `app.py`. |
| **Keamanan** | Seluruh query SQL berparameter (Anti-SQLi) | **LULUS** | 100% kueri di `services.py` memakai placeholder `?`. |
| **Keamanan** | Seluruh form mutasi POST terproteksi Token CSRF | **LULUS** | Middleware `@app.before_request` memvalidasi CSRF token dengan penolakan HTTP 400. |
| **Keamanan** | Rate limiting login aktif (anti brute-force) | **LULUS** | 5 kegagalan per 5 menit $\rightarrow$ percobaan ke-6 mengembalikan status HTTP 429. |
| **Penomoran Versi** | Berkas `versi.py` mendefinisikan `__version__ = "1.0.0"` | **LULUS** | `versi.py` terpasang dan nomor versi ditampilkan di footer halaman web. |
| **Pencadangan** | Skrip `cadangkan.py` berfungsi via SQLite Backup API | **LULUS** | Berkas cadangan terstempel waktu otomatis terbentuk pada folder `cadangan/`. |
| **Repositori** | `.gitignore` mengecualikan `.env`, `*.db`, dan `cadangan/` | **LULUS** | Terdaftar lengkap pada baris `.gitignore`. |
| **Ketergantungan** | `requirements.txt` memuat versi pasti seluruh paket | **LULUS** | Memuat Flask, Werkzeug, Jinja2, dan server produksi `waitress==3.0.2`. |
| **Pengujian** | Seluruh unit test suite dan uji rilis lulus 100% | **LULUS** | `pytest -q tests` (33+ uji) dan `python tests/uji_cepat.py` lulus hijau. |
| **Dokumentasi** | CHANGELOG.md, README.md, dan Manual Pengguna lengkap | **LULUS** | Terdokumentasi lengkap dengan panduan instalasi dan pemulihan bencana. |

---

## 3. Kesimpulan Audit

Seluruh butir pemeriksaan kesiapan rilis telah terpenuhi (**100% LULUS**). Repositori berada dalam kondisi aman, bersih dari data sensitif, dan siap untuk tahap deployment server produksi.
