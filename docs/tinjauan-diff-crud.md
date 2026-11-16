# Tinjauan Diff Modul CRUD Entitas Pertama (Langkah 11) — Exito Playbox

Dokumen ini mencatat evaluasi baris-demi-baris terhadap seluruh perubahan kode modul CRUD unit konsol (`consoles`) pada branch `fitur/kerangka` dibandingkan dengan branch `main`.

---

## 1. Tabel Temuan Tinjauan Kode (Lampiran C)

| No | Temuan Masalah / Usulan Perbaikan | Kategori | Tindakan yang Diambil | Alasan Keputusan |
|:--:|---|:--:|---|---|
| **1** | **Pencegahan Penghapusan Data via GET:**<br>Rute `/consoles/<id>/hapus` tidak boleh dieksekusi melalui permintaan `GET` untuk mencegah penghapusan data secara tidak sengaja oleh web crawler atau klik tautan peramban. | **Keamanan** | **Diperbaiki Sekarang:** Mengunci dekorator rute menjadi `methods=['POST']` di `app.py` dan menambahkan konfirmasi JavaScript `confirm()` pada form tombol hapus di `ubah_konsol.html`. | Mencegah celah keamanan penghapusan tidak disengaja. Akses `GET` menghasilkan respons standar HTTP 405 Method Not Allowed. |
| **2** | **Pembatasan Status Operasional Manual:**<br>Pada form ubah unit, kasir/pemilik tidak boleh mengubah status unit secara bebas menjadi `'terpakai'` dari antarmuka master. | **Kesesuaian Bisnis** | **Diperbaiki Sekarang:** Pilihan dropdown status di `ubah_konsol.html` dan validasi `services.py` dibatasi hanya untuk nilai `'tersedia'` dan `'maintenance'`. | Status `'terpakai'` hanya boleh diatur secara atomik oleh sistem saat kasir membuka transaksi sewa pada modul billing kasir. |
| **3** | **Pemisahan Kueri SQL dari Lapisan Routing:**<br>Seluruh pemanggilan basis data SQLite wajib berada di `services.py` dan `models.py`, tidak boleh ada baris raw SQL di dalam `app.py`. | **Keterbacaan & Arsitektur** | **Diperbaiki Sekarang:** Fungsi `get_all_consoles()`, `create_console()`, `get_console_by_id()`, `update_console()`, dan `delete_console()` sepenuhnya didelegasikan ke `services.py`. | Menjaga prinsip arsitektur 3-tier (*Separation of Concerns*), memudahkan pengujian otomatis independen tanpa bergantung pada server web Flask. |
| **4** | **Pencatatan Audit Trail Log Akses:**<br>Perlu ditambahkan pencatatan riwayat siapa pengguna kasir/owner yang mengubah status konsol ke file log sistem. | **Keamanan** | **Dicatat untuk Minggu 12:** Dicatat dalam backlog peninjauan keamanan dan logging audit (*Sprint 4 / Minggu 12*). | Fokus siklus saat ini adalah validitas CRUD dasar dan penegakan integritas data entitas pertama. |

---

## 2. Penjelasan Alur Permintaan (*Request Lifecycle*)
1. **Peramban (*Browser*):** Pengguna menavigasi ke URL `http://127.0.0.1:5000/consoles`.
2. **Routing (*Controller* `app.py`):** Fungsi `daftar_konsol()` menangkap permintaan HTTP GET.
3. **Layanan Bisnis (*`services.py`*):** Fungsi `get_all_consoles()` dipanggil untuk meminta data seluruh unit konsol.
4. **Model & Basis Data (*`models.py` & SQLite*):** Koneksi dibuka dengan `PRAGMA foreign_keys = ON;`, kueri berparameter dieksekusi, data diambil sebagai objek `sqlite3.Row`, dan koneksi ditutup secara aman dalam blok `finally`.
5. **Templat Mesin (*Jinja2*):** Data daftar konsol diteruskan ke templat `daftar_konsol.html` yang mewarisi `base.html`, meng-escape variabel secara otomatis untuk mencegah XSS, dan merender HTML utuh kembali ke peramban.
