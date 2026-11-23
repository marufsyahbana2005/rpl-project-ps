# Exito Playbox — Sistem Manajemen Rental PlayStation

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask Version](https://img.shields.io/badge/flask-3.1.3-green.svg)](https://flask.palletsprojects.com/)
[![Waitress Production](https://img.shields.io/badge/WSGI-Waitress%203.0.2-orange.svg)](https://docs.pylonsproject.org/projects/waitress/)
[![Pytest Suite](https://img.shields.io/badge/tests-38%20passed-brightgreen.svg)](tests/)
[![Security Standards](https://img.shields.io/badge/OWASP-Top%2010%20Hardened-blueviolet.svg)](docs/laporan-temuan.md)
[![Release Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](CHANGELOG.md)

**Exito Playbox** adalah aplikasi web manajemen persewaan PlayStation modern berbasis Python Flask dan SQLite. Sistem ini dirancang untuk mempermudah operasional gerai rental game: mencatat sesi bermain pelanggan, mengontrol ketersediaan unit konsol secara visual dan atomik, mengkalkulasi tarif dan denda keterlambatan secara otomatis, serta mengamankan hak akses pengguna berbasis peran (*Role-Based Access Control*).

---

## 1. Prasyarat Sistem (Prerequisites)

- **Sistem Operasi:** Windows 10/11, Linux (Ubuntu 20.04+), atau macOS (Monterey+).
- **Python:** Versi 3.10 atau lebih baru (`python --version`).
- **Git:** Versi 2.30 atau lebih baru.
- **Peramban Web:** Google Chrome, Mozilla Firefox, Microsoft Edge, atau Safari modern.

---

## 2. Panduan Instalasi Cepat (Quick Start)

### 2.1 Kloning Repositori & Persiapan Lingkungan Virtual
Buka terminal / PowerShell, lalu jalankan:

```powershell
# 1. Kloning repositori
git clone https://github.com/marufsyahbana2005/rpl-project-ps.git
cd rpl-project-ps

# 2. Buat lingkungan virtual Python
python -m venv .venv

# 3. Aktifkan lingkungan virtual
# Windows PowerShell:
.venv\Scripts\activate
# Linux / macOS:
source .venv/bin/activate

# 4. Pasang seluruh dependensi produksi
pip install -r requirements.txt

# (Opsional) Pasang dependensi pengujian untuk developer:
pip install -r requirements-dev.txt
```

---

## 3. Konfigurasi Variabel Lingkungan (Environment Variables)

Aplikasi mendukung konfigurasi fleksibel melalui variabel lingkungan OS:

| Variabel Lingkungan | Nilai Default | Keterangan & Aturan Penggunaan |
|---|:---:|---|
| `TOKO_DB` | `rental.db` | Jalur berkas basis data SQLite yang digunakan aplikasi. |
| `SECRET_KEY` | *(Random dev key)* | **Wajib disetel pada mode produksi!** Kunci kriptografi penandatangan cookie sesi. |
| `APP_ENV` | `development` | Pilihan: `development` (mode lokal) atau `production` (mode produksi ketat). |
| `COOKIE_SECURE` | `1` *(jika produksi)* | Setel `COOKIE_SECURE=0` bila server dijalankan di jaringan lokal tertutup tanpa sertifikat SSL/HTTPS (HTTP biasa). |

---

## 4. Inisialisasi Basis Data & Akun Awal

Sistem secara otomatis menginisialisasi skema tabel SQLite dari `docs/desain/schema.sql` saat pertama kali dijalankan. Untuk mendaftarkan akun Kasir dan Pemilik pertama kali:

```powershell
python buat_pengguna.py
```
*Ikuti petunjuk di terminal untuk memasukkan nama pengguna, kata sandi, dan memilih peran (`kasir` atau `owner`).*

---

## 5. Menjalankan Aplikasi

### 5.1 Mode Pengembangan (Development Server)
Cocok untuk pengembangan dan pengujian lokal cepat:
```powershell
python app.py
```
Aplikasi dapat dibuka pada alamat: [http://127.0.0.1:5000](http://127.0.0.1:5000).

### 5.2 Mode Produksi Resmi (Waitress WSGI Server)
Gunakan server produksi WSGI **Waitress** yang berkinerja tinggi dan stabil:

1. Buat kunci rahasia berkekuatan tinggi:
   ```powershell
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
2. Atur variabel lingkungan produksi (PowerShell Windows):
   ```powershell
   $env:APP_ENV="production"
   $env:SECRET_KEY="kunci_rahasia_hasil_generasi_di_atas"
   $env:COOKIE_SECURE="0"   # Setel 0 jika akses jaringan toko belum memakai HTTPS
   ```
3. Jalankan server Waitress:
   ```powershell
   # Hanya akses komputer lokal:
   waitress-serve --listen=127.0.0.1:8000 app:app

   # Akses dari komputer kasir lain di jaringan toko tertutup:
   waitress-serve --listen=0.0.0.0:8000 app:app
   ```
   *Buka peramban pada alamat `http://localhost:8000` atau `http://[IP_KOMPUTER_SERVER]:8000`.*

> [!IMPORTANT]
> Pada mode produksi (`APP_ENV=production`), aplikasi akan **menolak berjalan (throw RuntimeError)** jika variabel `SECRET_KEY` tidak disetel di environment!

---

## 6. Prosedur Pencadangan & Pemulihan Basis Data (Backup & Recovery)

### 6.1 Prosedur Pencadangan Rutin
Jalankan skrip pencadangan mandiri:
```powershell
python cadangkan.py
```
Skrip memanfaatkan *SQLite Online Backup API* yang menjamin konsistensi data transaksi tanpa perlu mematikan aplikasi. Berkas cadangan otomatis disimpan pada folder `cadangan/` dengan nama stempel waktu, contoh: `cadangan/rental_backup_20261123_093055.db`.

- **Frekuensi Rekomendasi:** 1 kali setiap hari sebelum tutup gerai operasional (pukul 23.00 WIB).
- **Lokasi Simpan Cadangan Tambahan:** Salin berkas folder `cadangan/` ke flashdisk eksternal atau Google Drive khusus pemilik rental.
- **Penanggung Jawab:** Kasir shift malam didampingi Pemilik Rental.

### 6.2 Prosedur Pemulihan Basis Data (Disaster Recovery)
Bila terjadi kerusakan data atau komputer kasir mengalami kendala:
1. Hentikan proses aplikasi Flask / Waitress (`Ctrl + C`).
2. Tentukan berkas cadangan terakhir yang masih sehat dari folder `cadangan/`.
3. Salin dan ganti berkas basis data aktif:
   ```powershell
   copy cadangan\rental_backup_TERAKHIR.db rental.db
   ```
4. Jalankan kembali aplikasi:
   ```powershell
   waitress-serve --listen=127.0.0.1:8000 app:app
   ```
5. Periksa integritas data transaksi terakhir di menu **Daftar Sewa**.

---

## 7. Eksekusi Pengujian Otomatis

Seluruh rangkaian pengujian unit, pengujian alur, matriks akses otorisasi, penolakan CSRF, rate-limiting, dan pengujian rilis dapat dijalankan dengan perintah:

```powershell
# Menjalankan seluruh rangkaian pytest (38 fungsi uji)
python -m pytest -q tests

# Menjalankan skrip verifikasi regresi cepat mandiri
python tests/uji_cepat.py
```

---

## 8. Catatan Hasil Uji Orang Asing (Stranger Test)

Dokumentasi uji keterbacaan panduan instalasi oleh pihak independen:
- **Nama Penguji Independen:** David Kurniawan (Pengembang Sistem Rental Mobil / Rekan Mahasiswa).
- **Lingkungan Uji:** Komputer laptop Windows 11 bersih dengan folder dan virtual environment baru tanpa riwayat setup sebelumnya.
- **Hasil Pengujian:**
  - Penguji berhasil mengkloning, membuat `.venv`, memasang dependensi dari `requirements.txt`, dan menjalankan server hingga halaman login.
  - **Catatan Masukan:** Penguji sempat bingung ketika server produksi Waitress langsung tertutup dengan pesan galat `RuntimeError: KRITIS: Aplikasi menolak berjalan pada mode produksi tanpa variabel lingkungan SECRET_KEY!`.
  - **Tindakan Perbaikan:** Ditambahkan kotak peringatan *[!IMPORTANT]* pada Bagian 5.2 README yang menjelaskan bahwa perintah `export` / `$env:SECRET_KEY` wajib dijalankan sebelum memulai `waitress-serve`. Setelah diperbaiki, penguji berhasil login 100%.

---

## 9. Lisensi & Hak Cipta

Dikembangkan oleh **Tim Pengembang Exito Playbox** (Maruf Syahbana) untuk memenuhi tugas besar Rekayasa Perangkat Lunak 2026. Hak cipta dilindungi undang-undang.
