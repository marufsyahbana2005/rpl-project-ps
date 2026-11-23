# Pull Request: Test Case, Uji Otomatis Pytest, Penutupan 3 Cacat, dan Rencana UAT (Jobsheet 13)

- **Branch Asal:** `fitur/pengujian`
- **Branch Tujuan:** `main`
- **Penulis (Author):** Maruf Syahbana (Product Owner & Full-Stack Developer)
- **Status PR:** Siap Ditinjau & Digabungkan (*Ready for Review & Merge*)
- **Target Rilis:** RTM-2 Sprint 3 (Persiapan UAT & Rilis v1.0)

---

## 1. Ringkasan Perubahan (Summary of Changes)

PR ini mengintegrasikan kerangka pengujian otomatis terstandar berbasis **Pytest**, perancangan test case komprehensif, penutupan 3 cacat nyata melalui siklus TDD merah $\rightarrow$ hijau, serta penyusunan rencana *User Acceptance Testing* (UAT) untuk Sistem Manajemen Rental PlayStation **Exito Playbox** (`rpl-project-ps`):

### A. Kerangka & Rangkaian Uji Otomatis Pytest
1. **Pemasangan & Konfigurasi Pytest (`pytest==9.1.1`):**
   - Penambahan dependensi pengujian pada `requirements-dev.txt`.
   - Penyusunan `tests/conftest.py` yang menyediakan isolasi basis data sementara (`exito_pytest_temp.db`), seed pengguna uji (`kasir_siti` & `owner_budi`), dan helper transmisi token CSRF (`post_csrf`).
   - Uji pertama verifikasi basis data sementara pada `tests/test_pertama.py`.
2. **Matriks Keterlacakan & 22 Test Case (`docs/pengujian/test-case.md`):**
   - Matriks pemetaan kebutuhan fungsional (`KF-01` s/d `KF-08` dan `KNF-03`) terhadap kriteria penerimaan.
   - Perancangan 22 skenario test case berbasis Partisi Ekuivalen dan Analisis Nilai Batas (BVA):
     - **8 Kasus Nilai Batas (BVA):** Harga 0 vs -1, durasi 0 vs 1 mnt, denda 5 vs 6 mnt, kode konsol 3 vs 4 char.
     - **10 Kasus Uji Pelanggaran / Negatif:** Kode konsol kosong/duplikat, jenis konsol dilarang, input transaksi kosong, pelanggaran hak akses kasir HTTP 403, penolakan CSRF HTTP 400, dan rate limiting login HTTP 429.
     - **4 Kasus Jalur Normal (Happy Path):** Tambah konsol owner, buka sewa kasir, selesai sewa tepat waktu, dan dasbor filter transaksi.
3. **Uji Validasi Parametris (`tests/test_validasi.py`):**
   - 13 kasus uji spesifikasi nilai batas menggunakan decorator `@pytest.mark.parametrize`.
4. **Uji Alur HTTP & Matriks Akses Peran (`tests/test_alur_akses.py`):**
   - 16 skenario pengujian tingkat alur:
     (a) Alur operasional master konsol hingga tampil di daftar.
     (b) Siklus transaksi sewa konsol atomik, penghentian sewa, dan pencatatan denda.
     (c) Matriks otorisasi rute $\times$ peran (Tamu, Kasir, Owner).
     (d) Penolakan permintaan POST tanpa CSRF token atau token palsu (HTTP 400).

---

## 2. Penutupan Cacat Nyata (Defects Closed via TDD Merah $\rightarrow$ Hijau)

Tiga cacat nyata yang ditemukan melalui uji eksploratif telah ditutup melalui TDD dan verifikasi regresi pada `tests/test_cacat.py`:

| ID Cacat | Deskripsi Cacat | Commit Perbaikan | Status Pengujian |
|:---:|---|:---:|:---:|
| **D-01** | Penanganan masukan non-string pada `nama_pelanggan` memicu `AttributeError` (HTTP 500) | `16db5e1` | **LULUS (Green)** |
| **D-02** | Duplikasi nama paket sewa berbeda huruf besar-kecil (*case-insensitive bypass*) | `f7f17d9` | **LULUS (Green)** |
| **D-03** | Pemilik dapat mengubah status unit konsol yang sedang disewa aktif (`terpakai`) | `60f2567` | **LULUS (Green)** |

Dokumentasi detail tersimpan pada `docs/pengujian/laporan-cacat.md`.

---

## 3. Rencana User Acceptance Testing (UAT)

- Dokumen `docs/pengujian/rencana-uat.md` memuat 6 skenario alur kerja operasional bahasa awam klien.
- Jadwal pelaksanaan UAT disepakati resmi: **Sabtu, 5 Desember 2026, pukul 10.00 – 12.00 WIB** di gerai Exito Playbox bersama Bpk. Hendra Gunawan (Owner) dan Rian Pratama (Kasir).
- Lingkungan uji karangan (`rental_uat.db`) dan data seed telah disiapkan.

---

## 4. Hasil Verifikasi Pengujian (Test Results)

```text
============================= test session starts =============================
platform win32 -- Python 3.14.0a4, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Users\maaru\Documents\rpl-project-ps
collected 33 items

tests/test_pertama.py .                                                  [  3%]
tests/test_validasi.py .............                                     [ 42%]
tests/test_alur_akses.py ................                                [ 90%]
tests/test_cacat.py ...                                                  [100%]

============================== 33 passed in 4.04s ==============================
SEMUA UJI LULUS (python tests/uji_cepat.py)
```

- **Total Uji Pytest:** **33 Fungsi Uji (100% LULUS)**
- **Skrip Regresi Cepat:** **SEMUA UJI LULUS**
- **Kebutuhan Fungsional Tanpa Uji:** **0 Kebutuhan (100% Tercakup)**

---

## 5. Checklist Kesiapan Penggabungan (Merge Checklist)

- [x] Rangkaian pytest (`pytest -q tests`) lulus 100% (33 passed).
- [x] Skrip regresi mandiri (`python tests/uji_cepat.py`) mencetak "SEMUA UJI LULUS".
- [x] Seluruh 3 cacat terbukti ditutup dengan uji merah $\rightarrow$ hijau dan commit terpisah.
- [x] Dokumen test case (`test-case.md`), laporan cacat (`laporan-cacat.md`), rencana UAT (`rencana-uat.md`), dan latihan mandiri (`latihan-mandiri-pengujian.md`) tersusun lengkap.
- [x] Jurnal Vibe Coding diperbarui dengan 8 entri baru (total 45 entri).
- [x] Tidak ada regresi fungsional atau kebocoran data pada cabang utama.
