# Jurnal Vibe Coding — Exito Playbox

- **Nama Pengembang:** Maruf Syahbana
- **Peran:** Product Owner, Scrum Master, & Full-Stack Developer
- **Proyek:** Sistem Manajemen Rental PlayStation (Exito Playbox / `rpl-project-ps`)
- **Repositori:** https://github.com/marufsyahbana2005/rpl-project-ps

---

## Tabel Log Catatan Penggunaan AI (Lampiran D.1)

| No | Tanggal / Waktu | Siklus / Fitur | Ringkasan Prompt | Hasil AI | Keputusan | Alasan Keputusan & Refleksi |
|:--:|---|---|---|---|:--:|---|
| **1** | 16/11/2026 11:35 | **[Siklus 1] Kerangka Proyek & Inisialisasi Basis Data (F1)** | Membuat kerangka proyek Flask: `app.py`, `models.py` (PRAGMA foreign_keys = ON, `init_db` dari `schema.sql`), `services.py`, dan `templates/base.html`. Rute `/` mengalihkan ke `/consoles`. | Berkas `app.py`, `models.py`, `services.py`, dan templat `base.html` terbentuk. Basis data `rental.db` terinisialisasi otomatis dengan 5 tabel lengkap tanpa galat. | **Terima** | Kode bersih, modular (3-tier), kunci rahasia membaca `os.environ`, dan berhasil diuji dengan `test_client()` (HTTP 302 -> 200). |
| **2** | 16/11/2026 11:40 | **[Siklus 2] Daftar Unit Konsol (F2)** | Menampilkan daftar konsol via fungsi `get_all_consoles()` pada `services.py` tanpa raw SQL di `app.py`. Format tabel memuat kode, jenis, badge status warna, aksi ubah, dan keadaan data kosong. | Fungsi service dan rute `/consoles` berhasil dibuat. Templat `daftar_konsol.html` menampilkan 5 unit konsol awal dengan badge status rapi. | **Terima** | Memenuhi pemisahan logika (SoC), tabel responsif sesuai wireframe, dan uji `test_client()` memvalidasi 5 unit konsol ter-render. |

---

## Pedoman Pengambilan Keputusan (Terima / Ubah / Tolak)
1. **Terima:** Kode memenuhi spesifikasi PRD, mengikuti skema basis data SQLite, menerapkan prinsip keamanan (SQL berparameter, pencegahan XSS via Jinja2), dan berjalan tanpa galat.
2. **Ubah:** Kode memiliki logika dasar yang benar namun memerlukan penyesuaian (misal: gaya penamaan, struktur arsitektur 3-tier, atau validasi nilai batas).
3. **Tolak:** Kode menghasilkan ketergantungan paket baru yang dilarang, membocorkan kredensial, merusak skema basis data, atau menggunakan *hard-coded secret keys*.
