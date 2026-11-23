# Simulasi Tanya Jawab Teknis dan Modifikasi Kode Tanpa Bantuan AI
## Sistem Manajemen Rental PlayStation (Exito Playbox)

Dokumen ini mencatat pelaksanaan simulasi ujian akhir: sesi tanya jawab teknis mendalam dan uji keterampilan live-coding (*live modification*) mandiri tanpa ketergantungan pada kakas kecerdasan buatan (*AI assistant*).

---

## Bagian 1: Simulasi Tanya Jawab Teknis Mendalam Tanpa AI

- **Peserta Simulasi:** Maruf Syahbana (Pengembang / Teruji)
- **Peran Penguji:** Simulasi Dewan Penguji Ujian Akhir RPL
- **Aturan Sesi:** Teruji menjawab secara lisan tanpa membuka internet, tanpa generator AI, dan merujuk langsung pada nama berkas, fungsi, dan arsitektur kode proyek.

### Pertanyaan 1: Arsitektur Data & Kueri Relasional
> **Penguji:** *"Di mana persisnya letak kueri JOIN multi-tabel dalam proyek Anda? Mengapa kueri tersebut tidak ditaruh langsung di Controller `app.py`, dan bagaimana Anda menangani kasus jika unit konsol atau paket yang berelasi telah dihapus?"*

**Jawaban Pengembang (Lisan Tanpa AI):**
> "Kueri SQL JOIN multi-tabel diisolasi secara terpusat pada lapisan Service di berkas `services.py`, tepatnya pada fungsi `get_all_transactions()`. Kueri ini menggabungkan tabel `transactions t` dengan `consoles c ON t.console_id = c.id`, `packages p ON t.package_id = p.id`, dan `users u ON t.user_id = u.id` menggunakan klausa `LEFT JOIN`.
> Alasan arsitekturalnya adalah pemisahan tanggung jawab (*Separation of Concerns*). Berkas `app.py` bertindak sebagai Controller yang hanya bertugas menangani protokol HTTP, memvalidasi form request, mengelola sesi, dan merender templat. Jika raw SQL ditaruh di `app.py`, pengujian unit lapisan bisnis akan sangat sulit dilakukan tanpa memicu lingkungan HTTP web server.
> Terkait penanganan data relasi yang dihapus, pertama, skema basis data kami menerapkan batasan kunci asing `ON DELETE RESTRICT` pada tabel konsol dan paket yang memiliki riwayat sewa di `transactions`, sehingga kasir atau pemilik tidak dapat menghapus entitas induk yang masih memiliki relasi sewa aktif. Kedua, dengan klausul `LEFT JOIN`, apabila terjadi ketidakteraturan data historis lama, kolom relasi akan bernilai `NULL` dan templat Jinja2 kami memiliki penanganan nilai default seperti `t.kode_konsol or 'Konsol Dihapus'` sehingga perenderan antarmuka tidak pernah *crash* dengan eksepsi *NoneType*."

---

### Pertanyaan 2: Arsitektur Server Produksi
> **Penguji:** *"Mengapa Anda memilih Waitress sebagai WSGI runner di produksi dan bukan Gunicorn atau uWSGI? Bagaimana cara kerja konfigurasi multithreading-nya?"*

**Jawaban Pengembang (Lisan Tanpa AI):**
> "Pemilihan Waitress WSGI didasarkan pada lingkungan operasional riil gerai mitra Exito Playbox. Mesin kasir utama mitra menggunakan sistem operasi Windows 10/11 Home Edition. Gunicorn dan uWSGI dibangun di atas arsitektur model proses UNIX (`fork()`) yang tidak didukung secara native pada subsistem proses Windows. Memaksakan Gunicorn di Windows akan menimbulkan instabilitas proses atau memerlukan dependensi WSL yang memperberat mesin kasir berdaya rendah.
> Sebaliknya, Waitress adalah server WSGI murni (*pure-Python*) yang dirancang khusus memiliki portabilitas penuh lintas platform (Windows dan Linux) dengan arsitektur asynchronous I/O multi-threaded. Pada berkas `jalankan.py`, kami mengonfigurasi Waitress melalui pemanggilan fungsi `serve(app, host=host, port=port, threads=6)`. Konfigurasi 6 thread ini memungkinkan server melayani hingga 6 permintaan kasir konkuren secara simultan (misalnya perenderan daftar sewa, pembaruan timer via polling, dan permintaan pencadangan) tanpa saling memblokir (*non-blocking concurrent workers*)."

---

### Pertanyaan 3: Mekanisme Keamanan CSRF Tanpa Dependensi Pihak Ketiga
> **Penguji:** *"Bagaimana cara kerja token CSRF yang Anda buat sendiri? Di mana token tersebut dibangkitkan, disimpan, divalidasi, dan mengapa Anda tidak menggunakan ekstensi `Flask-WTF`?"*

**Jawaban Pengembang (Lisan Tanpa AI):**
> "Mekanisme proteksi CSRF kami dirancang berbasis sesi dengan generator mandiri di `app.py`. Kami tidak menggunakan `Flask-WTF` karena alasan efisiensi: kami ingin menghindari *dependency bloat* dan menjaga aplikasi seringan mungkin untuk mesin kasir tanpa mengorbankan keamanan.
> Cara kerjanya terdiri dari empat tahap terpadu:
> 1. **Pembangkitan Token:** Fungsi `get_csrf_token()` memanfaatkan modul kriptografi native Python `secrets.token_hex(32)`. Saat kasir membuka sesi web, token dibangkitkan dan disimpan ke dalam objek `session['_csrf_token']`.
> 2. **Injeksi Templat:** Token didaftarkan sebagai fungsi konteks global Jinja2 via `@app.context_processor`, sehingga seluruh templat dapat menyisipkan tag `<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">` pada setiap formulir mutasi POST.
> 3. **Validasi Middleware:** Pada hook `@app.before_request`, sistem memeriksa metode HTTP. Jika permintaan menggunakan metode `POST`, `PUT`, `DELETE`, atau `PATCH`, middleware mengambil nilai `csrf_token` dari form payload atau HTTP header `X-CSRFToken` dan mencocokkannya dengan `session.get('_csrf_token')` menggunakan perbandingan waktu konstan `secrets.compare_digest()`.
> 4. **Penolakan:** Apabila token tidak dikirim, kosong, atau tidak cocok, server segera memutus pemrosesan dan mengembalikan kode status HTTP 400 Bad Request dengan templat halaman peringatan `400_csrf.html`."

---

## Bagian 2: Simulasi Tugas Modifikasi Kode Mandiri Tanpa AI ($\le 10$ Menit)

Untuk membuktikan penguasaan kode mandiri pengembang tanpa bantuan AI, dilakukan satu simulasi tugas modifikasi riil pada basis kode sistem.

### Spesifikasi Tugas Modifikasi:
> *"Tambahkan batasan durasi minimal baru pada form tambah paket sewa (`tambah_paket.html` & `services.py`): Durasi paket tidak boleh kurang dari 30 menit. Jika pengguna memasukkan durasi antara 1 s/d 29 menit, tolak dengan pesan galat ramah: 'Durasi paket minimal adalah 30 menit'. Pastikan seluruh pengujian regresi tetap lulus 100%!"*

### Pelaksanaan & Log Modifikasi Mandiri:
- **Waktu Mulai:** 10:40:00
- **Langkah 1 (Lapisan Validasi Logika Bisnis):** Membuka `services.py` pada fungsi `create_package()`. Menambahkan pengecekan:
  ```python
  if durasi_menit < 30:
      return False, "Durasi paket minimal adalah 30 menit."
  ```
- **Langkah 2 (Lapisan Presentasi Formulir):** Membuka `templates/tambah_paket.html`. Mengubah atribut HTML5 input durasi menjadi:
  ```html
  <input type="number" name="durasi_menit" min="30" step="15" required class="form-control">
  ```
- **Langkah 3 (Penyesuaian Uji Batas Otomatis):** Membuka berkas uji `tests/test_validasi.py` dan `tests/test_crud_packages.py` untuk memastikan nilai batas uji disesuaikan dari $< 0$ ke $< 30$.
- **Langkah 4 (Verifikasi Regresi):** Menjalankan skrip `pytest -q tests` dan `python tests/uji_cepat.py` di terminal.
- **Waktu Selesai:** 10:47:15
- **Total Waktu yang Dihabiskan:** **7 menit 15 detik** (Di bawah batas ambang 10 menit).

### Hasil Pengujian Pasca-Modifikasi:
```text
============================== test session starts ==============================
collected 38 items
......................................                                   [100%]
38 passed in 1.48s
============================== 38 passed in 1.48s ===============================

[*] Menjalankan verifikasi cepat uji_cepat.py...
[OK] SEC-PS-01: CSRF Protection aktif
[OK] SEC-PS-02: Rate Limiting aktif
[OK] SEC-PS-03: Security Headers terpasang
[OK] SEC-PS-04: Cookie Flags aman
[OK] Modul Transaksi & Integritas Relasional Konsisten
============================================================
SEMUA UJI LULUS! Sistem berjalan stabil tanpa regresi.
============================================================
```

### Kesimpulan Simulasi:
Pengembang mampu memodifikasi logika bisnis, antarmuka formulir, dan menyesuaikan rangkaian uji otomatis dalam waktu 7 menit 15 detik secara mandiri tanpa galat sintaksis maupun regresi sistem. Hal ini membuktikan penguasaan arsitektur kode 100% berada pada pengembang manusia (*human control*).
