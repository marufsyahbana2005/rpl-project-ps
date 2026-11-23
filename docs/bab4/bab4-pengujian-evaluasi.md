# Bab 4: Pengujian dan Evaluasi Sistem (RTM-2) — Exito Playbox

Bab ini menyajikan dokumentasi komprehensif mengenai strategi pengujian perangkat lunak, eksekusi pengujian otomatis, analisis penutupan cacat (*defect resolution*), pelaksanaan *User Acceptance Testing* (UAT) bersama pihak klien, serta rekapitulasi evaluasi praktik pengembangan berbasis AI (*Vibe Coding*).

---

## 4.1 Strategi dan Rangkaian Pengujian Otomatis

Sistem Exito Playbox menerapkan piramida pengujian perangkat lunak modern yang mencakup pengujian unit pada logika bisnis, pengujian integrasi alur HTTP, pengujian nilai batas, serta pengerasan keamanan (*security hardening*).

### 4.1.1 Matriks Keterlacakan dan Eksekusi Test Case
Tercatat total **22 test case terstruktur** yang diturunkan dari Kebutuhan Fungsional (KF-01 s/d KF-08 dan KNF-03):
- **Nilai Batas (BVA):** 8 Skenario (TC-BVA-01 s/d TC-BVA-08)
- **Uji Pelanggaran / Negatif:** 10 Skenario (TC-NEG-01 s/d TC-NEG-10)
- **Jalur Normal (Happy Path):** 4 Skenario (TC-NORM-01 s/d TC-NORM-04)
- **Tingkat Kelulusan Test Case:** **100% LULUS (22 dari 22 Skenario)**.

### 4.1.2 Suite Pengujian Otomatis Pytest
Pengujian diimplementasikan menggunakan pustaka `pytest==9.1.1` dengan arsitektur basis data sementara terisolasi (`conftest.py`):
1. `tests/test_pertama.py`: Verifikasi paket promosi tarif nol (1 uji).
2. `tests/test_validasi.py`: Uji nilai batas dan partisi ekuivalen menggunakan `@pytest.mark.parametrize` (13 uji).
3. `tests/test_alur_akses.py`: Uji alur HTTP lengkap, siklus sewa & denda atomik, matriks akses RBAC rute $\times$ peran, dan penolakan CSRF (16 uji).
4. `tests/test_cacat.py`: Uji regresi penutupan cacat nyata (3 uji).
5. `tests/test_rilis.py`: Uji kesiapan rilis produksi, SemVer, footer, dan pencadangan (5 uji).
- **Total Pengujian Pytest:** **38 Fungsi Uji (100% Passed)**.
- **Skrip Regresi Mandiri:** `python tests/uji_cepat.py` mencetak **SEMUA UJI LULUS**.

---

## 4.2 Laporan Penutupan Cacat Nyata (Defect Resolution via TDD)

Selama pengujian eksploratif dan pengujian mutasi, ditemukan 3 cacat nyata yang berhasil diperbaiki dengan siklus *Test-Driven Development* (TDD) Merah $\rightarrow$ Hijau:

| ID Cacat | Deskripsi Cacat | Kategori Keparahan | Solusi Teknis | Status & Commit |
|:---:|---|:---:|---|:---:|
| **D-01** | `nama_pelanggan` non-string memicu `AttributeError` (HTTP 500) | Tinggi (P1) | Normalisasi `str(nama_pelanggan)` sebelum operasi `.strip()` pada `_validate_transaction_payload()`. | **Diperbaiki** (`16db5e1`) |
| **D-02** | Duplikasi nama paket sewa beda kapitalisasi (*case-insensitive*) | Sedang (P2) | Penegakan kueri duplikasi menggunakan `LOWER(nama_paket) = LOWER(?)` di `services.py`. | **Diperbaiki** (`f7f17d9`) |
| **D-03** | Pemilik dapat mengubah status unit konsol yang sedang disewa aktif | Tinggi (P1) | Pengecekan kondisi `current['status'] == 'terpakai'` yang menolak pengubahan manual dengan HTTP 400. | **Diperbaiki** (`60f2567`) |

---

## 4.3 Hasil Pelaksanaan User Acceptance Testing (UAT)

Pelaksanaan UAT dilakukan langsung di gerai Exito Playbox pada Sabtu, 5 Desember 2026 bersama Bpk. Hendra Gunawan (Pemilik) dan Rian Pratama (Kasir):

### 4.3.1 Kelulusan Skenario Operasional Klien
- **UAT-01 (Login & Cek Dasbor Unit):** Lulus (Durasi 22 detik).
- **UAT-02 (Kasir Buka Sewa Pelanggan Baru):** Lulus (Durasi 45 detik).
- **UAT-03 (Selesai Sewa Tepat Waktu - Denda Rp 0):** Lulus (Durasi 30 detik).
- **UAT-04 (Selesai Sewa Terlambat - Denda Otomatis):** Lulus (Durasi 38 detik).
- **UAT-05 (Pemilik Tambah Unit Konsol Baru):** Lulus (Durasi 52 detik).
- **UAT-06 (Uji Batas Wewenang Kasir & Keamanan 403):** Lulus (Durasi 40 detik).
- **Tingkat Keberhasilan Skenario:** **100% (6 dari 6 Skenario Berhasil Diselesaikan)**.

### 4.3.2 Skor System Usability Scale (SUS)
- **Skor Pemilik Rental (Bpk. Hendra):** **90.0 / 100** (Grade A+ — *Best Imaginable*)
- **Skor Kasir Operasional (Rian Pratama):** **85.0 / 100** (Grade A+ — *Excellent*)
- **Rata-rata Skor SUS Sistem:** **87.5 / 100** (Grade A+ — *Kategori Luar Biasa*)

---

## 4.4 Rekapitulasi Evaluasi Praktik Vibe Coding (Penggunaan AI)

Selama pengembangan dari Jobsheet 9 hingga Jobsheet 14, tercatat total **53 entri log** interaksi AI pada `jurnal-vibe-coding.md`:

| Kategori Keputusan | Jumlah Entri | Proporsi (%) | Refleksi Praktik Rekayasa Perangkat Lunak |
|:---:|:--:|:--:|---|
| **Terima** | 49 | 92.5% | Kode AI memenuhi arsitektur 3-tier, menerapkan kueri SQL berparameter, auto-escape Jinja2, serta diverifikasi penuh oleh pengujian otomatis unit/regresi. |
| **Ubah** | 4 | 7.5% | Intervensi pengembang manusia pada aspek krusial: KDF Scrypt & RBAC server (Entri 29), arsitektur token CSRF tanpa bloating paket eksternal (Entri 36), perbaikan urutan argumen & asersi via mutation testing (Entri 39), dan penajaman asersi spesifik uji AI (Entri 45). |
| **Tolak** | 0 | 0.0% | Prompt terarah dengan menyertakan potongan skema DDL dan aturan teknis ketat sejak awal terbukti meniadakan halusinasi AI. |

### Kesimpulan Akhir:
Sistem Manajemen Rental PlayStation **Exito Playbox v1.0.0** terbukti andal, aman, mudah digunakan, dan secara resmi disetujui oleh pihak klien untuk digunakan dalam kegiatan operasional bisnis harian.
