# Pull Request: Rilis Produksi v1.0.0: Konfigurasi Waitress, Pencadangan SQLite, Dokumentasi, dan Hasil UAT (Jobsheet 14)

- **Branch Asal:** `rilis/v1.0.0`
- **Branch Tujuan:** `main`
- **Penulis (Author):** Maruf Syahbana (Product Owner & Full-Stack Developer)
- **Status PR:** Siap Ditinjau & Digabungkan (*Ready for Review & Merge*)
- **Target Rilis:** Rilis Resmi Produksi **v1.0.0** (RTM-2 Selesai 100%)

---

## 1. Ringkasan Perubahan (Summary of Changes)

PR ini memfinalisasi seluruh persiapan rilis produksi versi **v1.0.0** untuk Sistem Manajemen Rental PlayStation **Exito Playbox** (`rpl-project-ps`), menindaklanjuti audit kesiapan rilis, konfigurasi server produksi, dokumentasi pengguna, dan pengujian penerimaan pengguna (*User Acceptance Testing*):

### A. Konfigurasi Rilis, Lingkungan, dan Kriptografi
1. **Nomor Versi SemVer & Tampilan Footer:**
   - Pembuatan modul `versi.py` yang mendefinisikan `__version__ = "1.0.0"`.
   - Injeksi global `app_version` ke Jinja2 context processor dan tampilan nomor versi pada footer `templates/base.html`.
2. **Fleksibilitas Direktori Basis Data (`TOKO_DB`):**
   - Mendukung konfigurasi variabel lingkungan `TOKO_DB` pada `models.py` dan `app.py`.
3. **Pencadangan Mandiri SQLite (`cadangkan.py`):**
   - Implementasi skrip pencadangan menggunakan *SQLite Online Backup API* (`conn.backup`) yang menghasilkan berkas stempel waktu di folder `cadangan/`.
   - Folder `cadangan/` dikecualikan dari Git melalui `.gitignore`.
4. **Server WSGI Produksi Waitress (`waitress==3.0.2`):**
   - Integrasi server produksi Waitress berkecepatan tinggi.
   - Penolakan startup (`RuntimeError`) pada mode `APP_ENV=production` jika `SECRET_KEY` tidak dikonfigurasi di environment.
   - Dukungan penyesuaian `COOKIE_SECURE=0` untuk akses jaringan LAN toko lokal tanpa HTTPS.
5. **Rangkaian Pengujian Rilis (`tests/test_rilis.py`):**
   - 5 pengujian otomatis memvalidasi SemVer, footer, integritas file cadangan SQLite, variabel `TOKO_DB`, dan penolakan start tanpa `SECRET_KEY`.
   - Total uji Pytest meningkat menjadi **38 fungsi uji (100% Passed)**.

### B. Dokumentasi Pengguna & Hasil UAT Klien
1. **Catatan Perubahan (`CHANGELOG.md`):** Disusun rapi mengikuti format *Keep a Changelog* (Fitur yang Ditambahkan, Diperbaiki, dan Keamanan).
2. **README Komprehensif (`README.md`):** Panduan instalasi cepat, konfigurasi environment, migrasi akun awal, instruksi waitress, prosedur backup/recovery, dan catatan uji orang asing (*stranger test*).
3. **Manual Pengguna Bergambar (`docs/manual-pengguna.md`):** Panduan operasional non-teknis kasir dan pemilik dilengkapi langkah bernomor, rujukan wireframe, dan tabel pemecahan masalah (*troubleshooting*).
4. **Pelaksanaan UAT & Kuesioner SUS (`docs/uat/hasil-uat.md`):**
   - 6 skenario operasional diuji langsung oleh Bpk. Hendra (Owner) dan Rian Pratama (Kasir) dengan **kelulusan 100%**.
   - Perhitungan skor SUS menggunakan `docs/uat/hitung_sus.py`: skor rata-rata **87.5 / 100** (**Grade A+ / Best Imaginable**).
   - Penandatanganan resmi berita acara penerimaan sistem oleh Bpk. Hendra.
5. **Bahan Laporan Bab 4 (`docs/bab4/bab4-pengujian-evaluasi.md`):** Rekapitulasi akademik test case, penutupan cacat, hasil UAT, dan evaluasi praktik vibe coding.
6. **Latihan Mandiri Rilis (`docs/latihan-mandiri-rilis.md`):** Uji orang asing kedua, rencana pemulihan bencana (*Disaster Recovery* RTO 30 mnt), dan analisis versi tambalan.

---

## 2. Hasil Verifikasi Pengujian

```text
============================= test session starts =============================
platform win32 -- Python 3.14.0a4, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Users\maaru\Documents\rpl-project-ps
collected 38 items

tests/test_pertama.py .                                                  [  2%]
tests/test_validasi.py .............                                     [ 36%]
tests/test_alur_akses.py ................                                [ 78%]
tests/test_cacat.py ...                                                  [ 86%]
tests/test_rilis.py .....                                                [100%]

============================== 38 passed in 3.93s ==============================
SEMUA UJI LULUS (python tests/uji_cepat.py)
```

- [x] Pytest Suite: **38 passed in 3.93s**
- [x] Uji Regresi Mandiri: **SEMUA UJI LULUS**
- [x] Tiga Pemeriksaan Git: **LULUS (Tidak ada .db/.env terlacak dan tidak ada rahasia di kode)**

---

## 3. Checklist Kesiapan Penggabungan & Rilis (Merge Checklist)

- [x] Branch `rilis/v1.0.0` bersih dan sinkron dengan `main`.
- [x] Seluruh 38 pengujian otomatis lulus 100%.
- [x] Skrip `cadangkan.py` teruji sukses mencadangkan dan memulihkan basis data.
- [x] Server Waitress teruji berjalan normal dan menolak start tanpa `SECRET_KEY` di produksi.
- [x] Berita acara persetujuan UAT telah ditandatangani oleh klien (Bpk. Hendra).
- [x] Jurnal Vibe Coding telah dimutakhirkan (53 entri log).
- [x] Siap digabungkan ke `main` dan diberi tag Git `v1.0.0`.
