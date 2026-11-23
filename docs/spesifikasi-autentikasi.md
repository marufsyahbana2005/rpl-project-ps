# Spesifikasi Fitur Autentikasi dan Matriks Akses (Jobsheet 11) — Exito Playbox

Dokumen ini mendefinisikan matriks kontrol akses berbasis peran (*Role-Based Access Control* / RBAC) dan rincian kriteria penerimaan untuk modul autentikasi dan otorisasi sistem Exito Playbox (`rpl-project-ps`).

---

## 1. Matriks Hak Akses Pengguna

Sistem memiliki dua peran (*role*) terdaftar dalam tabel `users`:
1. **Kasir (`kasir`):** Bertanggung jawab atas pencatatan operasional sewa konsol harian dan penagihan biaya rental.
2. **Pemilik (`owner`):** Memiliki hak administratif penuh untuk mengelola inventaris unit konsol, menentukan tarif paket sewa, dan melihat laporan bisnis.

Tamu (*guest*) adalah setiap entitas yang belum melakukan login sesi ke dalam sistem.

| Halaman / Aksi | Metode HTTP | Rute URL | Tamu | Kasir | Pemilik (`owner`) |
|---|:--:|---|:--:|:--:|:--:|
| **Halaman Login** | GET, POST | `/login` | ✓ (Diizinkan) | ✓ (Dialihkan ke beranda jika sudah aktif) | ✓ (Dialihkan ke beranda jika sudah aktif) |
| **Proses Logout** | POST | `/logout` | login (401/Redirect) | ✓ (Diizinkan) | ✓ (Diizinkan) |
| **Halaman Utama / Beranda** | GET | `/` | login | ✓ (Redirect ke `/sewa`) | ✓ (Redirect ke `/sewa`) |
| **Daftar Sewa Konsol** | GET | `/sewa` | login | ✓ (Diizinkan) | ✓ (Diizinkan) |
| **Buka Sesi Sewa Baru** | GET, POST | `/sewa/buka` | login | ✓ (Diizinkan) | ✓ (Diizinkan) |
| **Selesaikan Sesi Sewa & Denda** | POST | `/sewa/<id>/selesai` | login | ✓ (Diizinkan) | ✓ (Diizinkan) |
| **Daftar Unit Konsol** | GET | `/consoles` | login | ✓ (Hanya melihat inventaris) | ✓ (Akses penuh) |
| **Tambah Unit Konsol Baru** | GET, POST | `/consoles/tambah` | login | ✗ (403 Forbidden) | ✓ (Diizinkan) |
| **Ubah Data Unit Konsol** | GET, POST | `/consoles/<id>/ubah` | login | ✗ (403 Forbidden) | ✓ (Diizinkan) |
| **Hapus Unit Konsol** | POST | `/consoles/<id>/hapus` | login | ✗ (403 Forbidden) | ✓ (Diizinkan) |
| **Daftar Paket Sewa** | GET | `/packages` | login | ✗ (403 Forbidden) | ✓ (Diizinkan) |
| **Tambah Paket Sewa** | GET, POST | `/packages/tambah` | login | ✗ (403 Forbidden) | ✓ (Diizinkan) |
| **Ubah Paket Sewa** | GET, POST | `/packages/<id>/ubah` | login | ✗ (403 Forbidden) | ✓ (Diizinkan) |
| **Hapus Paket Sewa** | POST | `/packages/<id>/hapus` | login | ✗ (403 Forbidden) | ✓ (Diizinkan) |

*Keterangan Simbol:*
- **✓:** Diizinkan mengakses dan mengeksekusi aksi.
- **✗ (403):** Akses ditolak dengan status HTTP 403 Forbidden (Peran tidak memiliki otorisasi).
- **login:** Tamu belum terautentikasi dan otomatis dialihkan ke `/login?next=<rute_tujuan>`.

---

## 2. Tabel Fitur Kecil Autentikasi (H1 s/d H5)

| No | Fitur Kecil | Kriteria Penerimaan | Pelaksana |
|:--:|---|---|:--:|
| **H1** | **Akun Awal dan Hash Kata Sandi** | 1. Kata sandi di-hash menggunakan algoritma ber-salt modern (`scrypt` / `pbkdf2:sha256`) via Werkzeug Security.<br/>2. Dilarang menggunakan MD5, SHA-256 polos, plaintext, atau *hardcoded credentials* pada kode sumber.<br/>3. Tersedia skrip `buat_pengguna.py` untuk pembuatan akun ter-hash dari terminal. | Maruf Syahbana |
| **H2** | **Login dan Logout Aman** | 1. Pesan galat netral dan identik untuk username salah maupun password salah: *"Nama pengguna atau kata sandi salah."* (Mencegah *user enumeration*).<br/>2. Memanggil `session.clear()` sebelum menginisialisasi sesi baru.<br/>3. Sesi server hanya menyimpan: `user_id`, `username`, `role`.<br/>4. Logout hanya menerima metode `POST` untuk mencegah serangan CSRF via *pre-fetching* tag gambar/link.<br/>5. Parameter `next` diverifikasi ketat (wajib berawalan `/` dan bukan `//`) untuk menangkal celah *Open Redirect*. | Maruf Syahbana |
| **H3** | **Pembatasan Hak Akses (RBAC)** | 1. Decorator `@login_diperlukan` mengalihkan tamu ke `/login?next=...`.<br/>2. Decorator `@peran_diperlukan(*roles)` mengembalikan respons HTTP 403 Forbidden jika peran tidak sesuai.<br/>3. Tersedia halaman `templates/403.html` yang menjelaskan penyebab penolakan dan menyediakan tautan kembali.<br/>4. Penegakan peran berlaku identik pada metode HTTP `GET` dan `POST`. | Maruf Syahbana |
| **H4** | **Antarmuka Responsif & Dinamis** | 1. Templat induk `templates/base.html` menampilkan menu sesuai peran yang aktif (Kasir tidak melihat tombol Tambah/Ubah/Hapus Konsol dan menu Paket Sewa).<br/>2. Navbar memuat identitas pengguna dan badge peran (`Kasir` / `Pemilik`).<br/>3. Tombol Logout terpasang di navbar sebagai formulir POST ringkas.<br/>4. Halaman login `templates/login.html` selaras dengan wireframe `wf-01` dan memiliki styling konsisten pada `static/style.css`. | Maruf Syahbana |
| **H5** | **Validasi Masukan Dua Lapis** | 1. Formulir login dan kelola data menerapkan atribut HTML5 (`required`, `type`, `min`, `maxlength`, `autocomplete`).<br/>2. Validasi sisi server (`services.py`) tetap berjalan penuh meskipun validasi browser dilewati lewat alat pengembang.<br/>3. Nilai isian formulir tetap dipertahankan saat validasi server gagal (kecuali password). | Maruf Syahbana |
