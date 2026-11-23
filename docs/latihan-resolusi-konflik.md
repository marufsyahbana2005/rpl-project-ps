# Laporan Latihan Resolusi Konflik Merge (Langkah 14) — Exito Playbox

- **Proyek:** Sistem Manajemen Rental PlayStation (Exito Playbox / `rpl-project-ps`)
- **Cabang Terlibat:** `fitur/modul-berelasi` dan `simulasi/konflik-navigasi`
- **Tanggal Pelaksanaan:** 23 November 2026
- **Pelaksana:** Maruf Syahbana (Pengembang A & B)

---

## 1. Skenario Pemicu Konflik

Konflik merge (*merge conflict*) disimulasikan terjadi pada berkas navigasi utama `templates/base.html` ketika dua pengembang menambahkan menu navigasi baru secara bersamaan pada baris yang sama:

1. **Pengembang A (Cabang `fitur/modul-berelasi`):**
   Menambahkan tautan menu operasional kasir untuk modul transaksi sewa konsol:
   ```html
   <a href="{{ url_for('daftar_sewa') }}" class="nav-link">Sewa Konsol</a>
   <a href="{{ url_for('buka_sewa') }}" class="nav-link">+ Buka Sewa</a>
   ```

2. **Pengembang B (Cabang `simulasi/konflik-navigasi`):**
   Menambahkan tautan cepat inventaris konsol pada baris yang sama:
   ```html
   <a href="{{ url_for('daftar_konsol') }}" class="nav-link">Unit Konsol</a>
   <a href="{{ url_for('tambah_konsol') }}" class="nav-link">+ Unit Baru</a>
   ```

Ketika perintah `git merge` dieksekusi, Git tidak dapat memutuskan urutan menu secara otomatis dan menghasilkan pesan:
```
CONFLICT (content): Merge conflict in templates/base.html
Automatic merge failed; fix conflicts and then commit the result.
```

---

## 2. Penanda Konflik Git (*Conflict Markers*)

Di dalam `templates/base.html`, Git menandai bagian yang bertabrakan dengan penanda standar:

```html
<<<<<<< HEAD
    <a href="{{ url_for('daftar_sewa') }}" class="nav-link">Sewa Konsol</a>
    <a href="{{ url_for('buka_sewa') }}" class="nav-link">+ Buka Sewa</a>
=======
    <a href="{{ url_for('daftar_konsol') }}" class="nav-link">Unit Konsol</a>
    <a href="{{ url_for('tambah_konsol') }}" class="nav-link">+ Unit Baru</a>
>>>>>>> simulasi/konflik-navigasi
```

---

## 3. Langkah Resolusi Bersama Tim

Tim melakukan rapat singkat dan menyepakati langkah-langkah resolusi berikut:
1. **Analisis Kebutuhan Antarmuka:** Menu dari kedua cabang sama-sama dibutuhkan oleh operator kasir (navigasi unit konsol untuk inventaris, dan navigasi sewa untuk operasional transaksi).
2. **Strategi Penggabungan (Kombinasi Harmonis):** Menata ulang urutan menu secara logis dari alur kerja kasir:
   - Menu Transaksi Sewa diletakkan paling awal karena merupakan aktivitas kasir harian paling sering.
   - Menu Unit Konsol diletakkan berikutnya untuk pemantauan ketersediaan unit.
   - Menu Paket Sewa diletakkan untuk manajemen tarif.
3. **Pembersihan Kode:** Menghapus seluruh baris penanda Git (`<<<<<<<`, `=======`, `>>>>>>>`).
4. **Hasil Kode Akhir Setelah Resolusi:**
   ```html
   <a href="{{ url_for('daftar_sewa') }}" class="nav-link">Sewa Konsol</a>
   <a href="{{ url_for('buka_sewa') }}" class="nav-link">+ Buka Sewa</a>
   <a href="{{ url_for('daftar_konsol') }}" class="nav-link">Unit Konsol</a>
   <a href="{{ url_for('daftar_paket') }}" class="nav-link">Paket Sewa</a>
   ```

---

## 4. Verifikasi dengan Skrip Uji Regresi

Sebelum melakukan commit resolusi konflik, skrip uji regresi otomatis mandiri dijalankan untuk membuktikan tidak ada sintaks Jinja2 yang rusak dan routing tetap berfungsi 100%:

```bash
python tests/uji_cepat.py
```
**Hasil:**
```
SEMUA UJI LULUS
```

---

## 5. Penyelesaian Commit Merge

Setelah uji regresi dipastikan lulus, berkas ditandai selesai konflik dan dicommit:
```bash
git add templates/base.html
git commit -m "Merge branch 'simulasi/konflik-navigasi': Gabungkan menu navigasi sewa konsol dan inventaris konsol"
```

### Refleksi dan Pembelajaran:
- Konflik merge bukanlah kesalahan, melainkan mekanisme pengamanan Git saat kerja paralel tim.
- Komunikasi antar-pengembang dan pemahaman arsitektur antarmuka sangat krusial saat menentukan kode akhir.
- Selalu jalankan skrip uji otomatis (`tests/uji_cepat.py`) sebelum melakukan commit hasil merge untuk menjamin regresi nol (*zero regression*).
