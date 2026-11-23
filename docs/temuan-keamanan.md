# Laporan Tinjauan Diff Keamanan Autentikasi & Otorisasi (Jobsheet 11) — Exito Playbox

Dokumen ini memuat hasil audit keamanan independen terhadap implementasi fitur login, penanganan sesi, dan pembatasan peran (*Role-Based Access Control*) pada sistem Exito Playbox.

---

## 1. Daftar Periksa Keamanan Autentikasi dan Otorisasi (Lampiran C.2)

| No | Aspek Keamanan | Kondisi Saat Ini | Status Evaluasi | Catatan / Pembuktian |
|:--:|---|---|:--:|---|
| **1** | **Penyimpanan Kata Sandi** | Menggunakan algoritma hash ber-salt modern `scrypt` / `pbkdf2:sha256` via Werkzeug. Dilarang plaintext, MD5, atau SHA-256 polos. | **LULUS (Aman)** | Diverifikasi lewat kueri basis data: awalan hash `scrypt:32768:8:1$...`, salt acak berbeda untuk setiap akun. |
| **2** | **Pencegahan Enumerasi Pengguna** | Pesan galat saat login bernilai netral identik (*"Nama pengguna atau kata sandi salah."*). | **LULUS (Aman)** | Uji TC-2 dan TC-3 membuktikan respons server sama persis saat password salah maupun username tidak ditemukan. |
| **3** | **Manajemen Siklus Sesi** | Pemanggilan `session.clear()` sebelum menginisialisasi sesi baru dan saat logout. | **LULUS (Aman)** | Mencegah serangan fiksasi sesi (*Session Fixation*). Sesi hanya menyimpan `user_id`, `username`, dan `role`. |
| **4** | **Metode Logout** | Rute `/logout` diproteksi hanya menerima metode `POST`. | **LULUS (Aman)** | Akses `GET /logout` mengembalikan `HTTP 405 Method Not Allowed`, mencegah logout paksa via *pre-fetching* peramban. |
| **5** | **Pencegahan Celah Open Redirect** | Parameter `next` diverifikasi ketat (wajib diawali `/` dan bukan `//` atau `/\\`). | **LULUS (Aman)** | Masukan `https://jahat.example` ditolak dan dialihkan kembali ke rute internal aman (`/sewa`). |
| **6** | **Penegakan Hak Akses di Server** | Decorator `@login_diperlukan` dan `@peran_diperlukan` dipasang pada seluruh rute backend (GET & POST). | **LULUS (Aman)** | Kasir yang memanipulasi form / cURL untuk POST `/consoles/<id>/hapus` terblokir HTTP 403 Forbidden. |

---

## 2. Tabel Temuan Keamanan & Tindakan Perbaikan (≥ 3 Temuan)

Berikut adalah daftar temuan kelemahan keamanan yang diidentifikasi dari diff kode, tindakan mitigasi yang telah dilakukan, serta butir yang ditunda untuk diselesaikan pada **Pertemuan 12 (Audit & Hardening Keamanan Menyeluruh)**:

| No | Area / Komponen | Kategori Temuan | Tingkat Risiko | Tindakan Hari Ini | Rencana Penyelesaian Pertemuan 12 |
|:--:|---|---|:--:|---|---|
| **1** | **Rute `/login`** | Belum ada mekanisme pembatasan frekuensi percobaan masuk (*Rate Limiting* / *Brute Force Protection*). | **Sedang (Medium)** | Menerapkan pesan galat netral untuk memperlambat analisis penyerang. | Menerapkan ekstensi `Flask-Limiter` atau penghitung percobaan gagal berbasis IP/akun (maksimal 5 kali salah per 15 menit). |
| **2** | **Semua Form POST** | Perlindungan terhadap Pemalsuan Permintaan Lintas Situs (*Cross-Site Request Forgery* / CSRF) belum menggunakan token acak per form. | **Sedang (Medium)** | Mengunci rute mutasi data hanya menerima metode HTTP `POST` dan mewajibkan otentikasi sesi aktif. | Mengintegrasikan `Flask-WTF` / `CSRFProtect` untuk menghasilkan token CSRF tersembunyi pada setiap formulir POST. |
| **3** | **Konfigurasi Cookie Sesi** | Atribut cookie keamanan (*HttpOnly*, *Secure*, dan *SameSite*) masih menggunakan nilai bawaan Flask. | **Rendah (Low)** | Membaca `SECRET_KEY` dari variabel lingkungan OS untuk penandatanganan kriptografis cookie. | Menetapkan konfigurasi cookie pada `app.py`: `SESSION_COOKIE_HTTPONLY = True`, `SESSION_COOKIE_SAMESITE = 'Lax'`, dan `SESSION_COOKIE_SECURE = True` (saat HTTPS aktif). |
| **4** | **Durasi Sesi Aktif** | Sesi pengguna belum memiliki waktu kedaluwarsa otomatis saat idle (*Session Idle Timeout*). | **Rendah (Low)** | Menyediakan tombol logout jelas pada navbar yang langsung mengeksekusi `session.clear()`. | Mengaktifkan `PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)` agar sesi kadaluwarsa otomatis jika kasir meninggalkan komputer kasir tanpa logout. |

---

## 3. Kesimpulan Tinjauan Diff

Implementasi autentikasi dan otorisasi Jobsheet 11 telah memenuhi seluruh standar dasar keamanan web:
- Tidak ada kata sandi yang disimpan dalam bentuk teks polos (*plaintext*) maupun di dalam kode sumber repositori Git.
- Penjagaan peran ditegakkan pada tingkat server (*server-side enforcement*), bukan sekadar menyembunyikan elemen visual antarmuka.
- Empat temuan keamanan terdaftar di atas telah didokumentasikan secara rapi dan dipetakan sebagai butir backlog prioritas pada Sprint 2 / Pertemuan 12.
