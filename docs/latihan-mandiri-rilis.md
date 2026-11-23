# Latihan Mandiri Rilis dan Deployment (Jobsheet 14 — Bagian 6)

Dokumen ini memuat analisis dan kajian teknis untuk tiga topik latihan mandiri pada rilis produksi sistem **Exito Playbox** (`rpl-project-ps`), sesuai arahan Jobsheet 14 Bagian 6.

---

## 1. Topik 1: Uji Orang Asing Kedua (Second Stranger Test)

Pengujian dilakukan untuk memvalidasi keterbacaan dokumen [docs/manual-pengguna.md](file:///c:/Users/maaru/Documents/rpl-project-ps/docs/manual-pengguna.md) oleh pengguna di luar lingkungan kelas teknik informatika:

- **Nama Penguji Independen:** Siti Rahmawati (Mahasiswi Akuntansi / Non-Teknis).
- **Tugas yang Diberikan:** Membaca manual pengguna dan menyelesaikan alur *"Mencatat Pelanggan Baru yang Mulai Sewa"* dan *"Mengakhiri Sesi Sewa dan Menghitung Denda"*.
- **Waktu Penyelesaian:**
  - Tugas Buka Sewa: **1 menit 15 detik**.
  - Tugas Selesai Sewa & Denda: **50 detik**.
- **Bagian yang Sempat Membingungkan:**
  Penguji sempat mencari-cari letak tombol logout setelah selesai transaksi karena posisi tombol berada di bilah kanan atas dengan format tombol kecil.
- **Tindakan Perbaikan Manual:**
  Menambahkan keterangan visual posisi tombol akun pengguna pada Bab 1 manual pengguna, memperjelas navigasi keluar akun (*Logout*).

---

## 2. Topik 2: Prosedur Pemulihan Bencana (Disaster Recovery Plan)

Skenario: Komputer fisik server di gerai Exito Playbox mengalami kerusakan total (misal: motherboard terbakar atau terkena tumpahan air).

### 2.1 Parameter Pemulihan
- **Recovery Time Objective (RTO):** $\le 30$ Menit (Waktu maksimal sistem harus kembali aktif melayani kasir).
- **Recovery Point Objective (RPO):** $\le 24$ Jam (Maksimal data transaksi yang hilang adalah transaksi hari berjalan sebelum cadangan malam).

### 2.2 Komponen Kritis yang Harus Tersedia

| Komponen Kritis | Media Penyimpanan & Lokasi | Penanggung Jawab | Cara Pengaksesan |
|---|---|---|---|
| **Kode Sumber Aplikasi (`rpl-project-ps`)** | Repositori GitHub (`origin/main`) | Tim Pengembang | `git clone https://github.com/marufsyahbana2005/rpl-project-ps.git` |
| **Berkas Cadangan Basis Data Terakhir (`.db`)** | Google Drive Terenkripsi Khusus Owner | Pemilik (Bpk. Hendra) | Unduh berkas cadangan stempel waktu terbaru: `rental_backup_YYYYMMDD_HHMMSS.db` |
| **Kunci Rahasia Produksi (`SECRET_KEY`)** | Catatan Brankas Fisik Gerai & Password Manager Owner | Pemilik (Bpk. Hendra) | Masukkan ke environment variable `$env:SECRET_KEY` komputer baru |
| **Python Runtime & Dependensi** | Installer Python 3.11 Offline di Flashdisk Darurat | Kasir Senior / Owner | Jalankan installer Python lalu `pip install -r requirements.txt` |

### 2.3 Prosedur Eksekusi Pemulihan pada Komputer Pengganti (Laptop Darurat)
1. **Langkah 1 (Persiapan Komputer Pengganti — Menit 0 s/d 10):**
   - Nyalakan laptop cadangan gerai yang sudah terhubung jaringan Wi-Fi toko.
   - Buka PowerShell / Terminal.
2. **Langkah 2 (Unduh Kode & Dependensi — Menit 10 s/d 18):**
   ```powershell
   git clone https://github.com/marufsyahbana2005/rpl-project-ps.git
   cd rpl-project-ps
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Langkah 3 (Pemasangan Basis Data Cadangan — Menit 18 s/d 22):**
   - Unduh berkas `rental_backup_TERBARU.db` dari Google Drive owner.
   - Salin dan ubah nama menjadi `rental.db` di folder proyek:
     ```powershell
     copy C:\Users\Kasir\Downloads\rental_backup_TERBARU.db .\rental.db
     ```
4. **Langkah 4 (Konfigurasi Kunci & Startup Waitress — Menit 22 s/d 25):**
   ```powershell
   $env:APP_ENV="production"
   $env:SECRET_KEY="kunci_rahasia_brankas_owner"
   $env:COOKIE_SECURE="0"
   waitress-serve --listen=0.0.0.0:8000 app:app
   ```
5. **Langkah 5 (Verifikasi Operasional — Menit 25 s/d 28):**
   - Buka `http://localhost:8000` di laptop kasir.
   - Login dengan akun `kasir_siti` dan pastikan seluruh unit konsol dan transaksi aktif pulih.
   - Sistem kembali online dalam waktu 28 menit (< RTO 30 menit).

---

## 3. Topik 3: Analisis Rilis Versi Tambalan (v1.0.0 vs v1.0.1)

Sesuai umpan balik UAT (butir `TR-02`), kasir menginginkan adanya konfirmasi pop-up sebelum menyelesaikan transaksi agar tidak terjadi klik tidak sengaja. Pada rilis tambalan v1.0.1 (*Patch Release*):

1. **Perubahan Kode:**
   Menambahkan dialog konfirmasi JavaScript pada form selesaikan sewa di `templates/daftar_sewa.html`:
   ```html
   <form action="{{ url_for('selesaikan_sewa', id=t.id_transaksi) }}" method="POST" onsubmit="return confirm('Apakah Anda yakin ingin menyelesaikan sesi sewa untuk pelanggan ini?');">
   ```
2. **Kenaikan Nomor Versi:**
   - `versi.py` dinaikkan dari `"1.0.0"` menjadi `"1.0.1"`.
   - `CHANGELOG.md` ditambahkan bagian `[1.0.1] - 2026-11-24`.
3. **Perbandingan Antara Dua Tag (`git diff v1.0.0 v1.0.1 --stat`):**
   Perbedaan hanya menyentuh `versi.py`, `CHANGELOG.md`, dan satu baris konfirmasi pada `templates/daftar_sewa.html`, membuktikan bahwa rilis tambalan (patch) bersifat minimal, aman dari regresi, dan langsung menjawab kebutuhan pengguna.
