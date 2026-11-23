# Latihan Mandiri Jobsheet 15 — Analisis Kritis & Kesiapan Sidang
## Sistem Manajemen Rental PlayStation (Exito Playbox)

Dokumen ini memuat hasil pengerjaan tiga paket Latihan Mandiri (Bagian 6) Jobsheet 15 untuk mengasah daya kritis akademis dan kesiapan konseptual menghadapi sidang tugas besar rekayasa perangkat lunak.

---

## Latihan 1: Transformasi Paragraf Deskriptif Menjadi Paragraf Analitis

### Teks Awal (Deskriptif Polos):
> *"Kami mencatat 61 entri pada jurnal vibe coding. Dari 61 entri tersebut, 55 entri berstatus Terima dan 6 entri berstatus Ubah. Tidak ada entri yang Tolak. Kategori galat yang paling banyak adalah logika yaitu sebanyak 5 kali. Waktu yang dihabiskan untuk memperbaiki galat rata-rata adalah 17.5 menit. Galat keamanan membutuhkan waktu paling lama yaitu 25 menit."*

### Teks Hasil Transformasi (Analitis Kritis Akademik):
> *"Dominasi keputusan 'Terima' sebesar 90.2% (55 dari 61 entri) membuktikan bahwa pemberian konteks skema DDL relasional secara eksplisit pada rekayasa prompt berhasil memitigasi halusinasi struktural kecerdasan buatan secara signifikan. Meskipun demikian, keberadaan 9.8% keputusan 'Ubah' merefleksikan keterbatasan inheren model AI dalam mengonseptualisasikan aspek non-fungsional dan aturan bisnis terikat. Fakta empiris bahwa galat keamanan menuntut durasi penanganan terlama (25 menit, berbanding 5 menit pada galat sintaksis) menyingkap fenomena kegagalan senyap (*silent failure*): kode yang digenerasi AI tampak sintaksis valid dan dapat dieksekusi tanpa galat, namun secara tersembunyi melanggar prinsip *least privilege* dan *defense in depth* (seperti pengusulan hash SHA-256 tanpa salt dan otorisasi semu sisi UI). Oleh sebab itu, intervensi pengembang manusia (*human-in-the-loop*) dengan kompetensi audit keamanan berbasis OWASP terbukti menjadi benteng verifikasi yang tak tergantikan guna mentransformasi prototipe buatan AI menjadi perangkat lunak produksi yang handal dan tangguh."*

---

## Latihan 2: Simulasi 5 Pertanyaan Kritis Dewan Penguji & Strategi Jawaban

### Pertanyaan 1 (Integritas Data Transaksional)
> **Dosen Penguji:** *"Pada fungsi pembukaan sewa kasir, bagaimana Anda menjamin bahwa status unit konsol tidak berubah menjadi 'terpakai' jika operasi penambahan baris transaksi sewa tiba-tiba gagal di tengah jalan?"*

- **Strategi Jawaban:** 
  > "Kami menerapkan pola transaksi atomik ACID SQLite menggunakan konteks manajer `with conn:` di berkas `services.py` pada fungsi `create_transaction()`. Kedua operasi mutasi—yakni penyisipan baris ke tabel `transactions` dan pembaruan kolom status pada tabel `consoles`—dieksekusi dalam satu transaksi tunggal. Apabila salah satu kueri memicu galat integritas atau eksepsi Python, blok `with conn:` secara otomatis mengeksekusi *rollback*, membatalkan seluruh perubahan sementara, dan menjamin basis data kembali ke status konsisten sebelumnya tanpa ada status konsol yang tergantung (*orphan state*)."

### Pertanyaan 2 (Arsitektur Keamanan & Otorisasi RBAC)
> **Dosen Penguji:** *"Jika seorang kasir memiliki pengetahuan teknis dan menggunakan Postman atau Curl untuk mengirimkan request penghapusan konsol ke rute `/consoles/<id>/hapus`, bagaimana sistem Anda menahannya?"*

- **Strategi Jawaban:**
  > "Sistem kami menahannya melalui tiga lapisan pertahanan (*defense in depth*). Pertama, rute tersebut diproteksi oleh decorator `@peran_diperlukan('owner')` di sisi server (`app.py`); ketika kasir mengirim token sesi miliknya, server memverifikasi bahwa peran aktifnya adalah `kasir` dan seketika menolak permintaan dengan kode HTTP 403 Forbidden sebelum logika penghapusan disentuh. Kedua, rute hanya menerima metode HTTP `POST` dan mewajibkan token CSRF yang valid; request tanpa header atau payload token CSRF yang cocok akan langsung ditolak dengan HTTP 400 Bad Request oleh middleware `@app.before_request`. Ketiga, pada lapisan basis data, foreign key `ON DELETE RESTRICT` aktif mencegah penghapusan jika konsol pernah memiliki riwayat transaksi."

### Pertanyaan 3 (Strategi Pengujian & Kekuatan Asersi)
> **Dosen Penguji:** *"Banyak pengembang menulis unit test hanya untuk mengejar 'pass' tanpa menguji skenario negatif. Bagaimana Anda membuktikan bahwa rangkaian uji 38 passed pada Pytest Anda benar-benar berkualitas?"*

- **Strategi Jawaban:**
  > "Kualitas rangkaian pengujian kami diverifikasi melalui dua instrumen: pengujian nilai batas (*Boundary Value Analysis*) parametris pada `test_validasi.py` dan pengujian mutasi manual (*mutation testing*). Kami sengaja melakukan mutasi kode sumber—seperti mengubah kondisi ambang batas keterlambatan denda dari `> 5` menjadi `>= 5` atau mengubah operator validasi harga dari `< 0` menjadi `<= 0`. Hasilnya, rangkaian pengujian pytest kami seketika mendeteksi kegagalan (*mutant killed*). Ini membuktikan bahwa asersi uji kami tidak sekadar memeriksa status `200 OK`, melainkan memvalidasi nilai kembalian, efek samping mutasi basis data, dan konten pesan galat spesifik."

### Pertanyaan 4 (Kesiapan Produksi & Skalabilitas WSGI)
> **Dosen Penguji:** *"Mengapa Anda tidak menggunakan server bawaan Flask `app.run()` saat aplikasi digunakan di gerai mitra, dan apa implikasi pemilihan Waitress terhadap performa?"*

- **Strategi Jawaban:**
  > "Server bawaan Flask secara eksplisit didesain oleh pengembangnya hanya untuk lingkungan pengembangan lokal (*single-threaded development server*). Jika dijalankan di gerai riil dengan banyak permintaan simultan (misalnya perenderan daftar transaksi kasir sembari melakukan polling timer konsol), server bawaan akan memblokir antrean request berikutnya, rentan terhadap starvation, dan tidak memiliki penanganan thread pool yang aman. Kami menggunakan **Waitress WSGI Server** versi 3.0.2 dengan alokasi 6 worker threads yang dirancang untuk produksi di sistem operasi Windows. Waitress mengisolasi setiap request dalam thread terpisah, memastikan response time tetap stabil di bawah 50 ms dan mencegah aplikasi lumpuh (*crash*) akibat lonjakan trafik lokal."

### Pertanyaan 5 (Evaluasi Etika & Tanggung Jawab Vibe Coding)
> **Dosen Penguji:** *"Seberapa besar kontribusi AI dalam proyek ini, dan jika ditemukan celah keamanan fatal pada sistem, siapa yang harus bertanggung jawab?"*

- **Strategi Jawaban:**
  > "Berdasarkan jurnal vibe coding kami, AI berkontribusi sebagai akselerator penyusunan draf awal dan perancangan variasi kasus uji. Namun, tanggung jawab penuh 100% atas integritas arsitektur, keabsahan fungsional, dan keamanan sistem berada mutlak pada pengembang manusia (*human-in-the-loop*). Kami telah menyatakan komitmen etika akademik pada Laporan Bab 4 bahwa AI hanyalah kakas bantu. Jika ditemukan celah keamanan, itu adalah kelalaian proses audit pengembang manusia, bukan kesalahan model AI. Sikap akuntabilitas inilah yang kami terapkan melalui audit keamanan OWASP mandiri dan penutupan cacat via TDD."

---

## Latihan 3: Analisis Skenario Uji Otomatis yang Gagal Menangkap Cacat & Usulannya

### Studi Kasus: Deteksi Cacat Keterlambatan Sewa Tepat pada Batas Toleransi (*Grace Period Boundary*)
- **Deskripsi Kerentanan Uji Awal:**
  Pada implementasi awal, pengujian unit yang digenerasi AI untuk fungsi `finish_transaction()` hanya menguji dua titik nilai:
  1. Pengembalian tepat waktu (terlambat 0 menit $\rightarrow$ denda Rp 0).
  2. Pengembalian sangat terlambat (terlambat 60 menit $\rightarrow$ denda Rp 60.000).
- **Kelemahan Pengujian Awal:**
  Uji otomatis awal tidak memvalidasi titik kritis nilai batas (*boundary values*), yaitu tepat pada menit ke-5 (batas akhir masa toleransi gratis) dan menit ke-6 (menit pertama pengenaan denda). Akibatnya, ketika pengembang secara keliru menerapkan logika operator `>= 5` alih-alih `> 5`, pelanggan yang mengembalikan tepat pada menit ke-5 langsung dikenai denda Rp 5.000 secara tidak adil, namun seluruh uji otomatis buatan AI tetap melaporkan *PASSED*.
- **Usulan Perbaikan & Skenario Uji Baru (Parametris Pytest):**
  Uji diperbaiki dengan menyusun skenario batas ketat pada `tests/test_validasi.py`:
  ```python
  @pytest.mark.parametrize("menit_lewat, expected_denda, expected_keterangan", [
      (0, 0, "Tepat waktu"),
      (4, 0, "Dalam batas toleransi"),
      (5, 0, "Tepat pada batas toleransi akhir (grace period 5 menit)"),
      (6, 1000, "Melewati batas toleransi (menit ke-6 kena denda 1 menit x 1000)"),
      (15, 10000, "Melewati batas toleransi (10 menit kena denda x 1000)"),
  ])
  def test_kalkulasi_denda_nilai_batas_presisi(client, sewa_fixture, menit_lewat, expected_denda, expected_keterangan):
      # Simulasi waktu pengembalian presisi
      denda, menit_dihitung = hitung_denda_sewa(sewa_fixture.durasi_paket, menit_lewat)
      assert denda == expected_denda, f"Gagal pada kasus: {expected_keterangan}"
  ```
- **Dampak Kualitas:**
  Pengujian batas ini berhasil membunuh mutasi operator dan menjamin hak finansial pelanggan maupun pemilik rental terlindungi secara presisi sesuai perjanjian sewa.
