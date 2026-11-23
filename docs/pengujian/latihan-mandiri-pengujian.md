# Latihan Mandiri Pengujian Perangkat Lunak (Jobsheet 13 — Bagian 6)

Dokumen ini memuat analisis dan kajian teknis untuk tiga butir latihan mandiri pengujian perangkat lunak sistem **Exito Playbox** (`rpl-project-ps`), sesuai panduan Jobsheet 13 Bagian 6.

---

## 1. Analisis Pengujian Mutasi (*Mutation Testing Analysis*)

Pengujian mutasi (*Mutation Testing*) dilakukan dengan menyuntikkan kesalahan buatan (*fault injection/mutants*) pada kode sumber untuk mengevaluasi apakah rangkaian pengujian (*test suite*) yang ada mampu mendeteksi cacat tersebut (*killing the mutants*). Jika suatu mutasi lolos tanpa ada pengujian yang gagal (*mutant survives*), hal ini menandakan adanya celah pengujian (*test gap*).

Berikut analisis 3 fungsi utama pada `services.py` dan `models.py`, masing-masing dengan 2 mutasi berbeda:

### 1.1 Fungsi 1: `services.create_console()`
- **Tujuan Fungsi:** Memvalidasi dan menambahkan unit konsol baru (panjang kode $\ge 4$, jenis valid PS3/PS4/PS5, status valid).
- **Mutasi A (Ubah Operator Relasional):**
  - *Kode Asli:* `elif len(kode_clean) < 4:` (baris 74)
  - *Mutasi:* `elif len(kode_clean) <= 4:`
  - *Dampak Perilaku:* Kode konsol pas 4 karakter (misal: `"PS41"`) yang seharusnya valid akan ditolak karena panjangnya $\le 4$.
  - *Hasil Uji:* **Tertangkap (*Killed*)** oleh `tests/test_validasi.py::test_validasi_nilai_batas_kode_konsol[PS41-PS4-True-None]`. Pengujian gagal dengan `assert False is True`.
- **Mutasi B (Hapus Pemeriksaan Jenis Konsol):**
  - *Kode Asli:* `if jenis_clean not in ("PS3", "PS4", "PS5"): errors.append(...)`
  - *Mutasi:* Hapus blok kondisional pemeriksaan jenis (`pass`).
  - *Dampak Perilaku:* Jenis konsol tidak valid seperti `"XBOX"` atau `"NINTENDO"` akan lolos dan tersimpan ke basis data.
  - *Hasil Uji:* **Tertangkap (*Killed*)** oleh `tests/test_validasi.py::test_validasi_nilai_batas_kode_konsol[XB-01-XBOX-False-Jenis konsol tidak valid]`. Pengujian gagal karena `sukses` bernilai `True`.

---

### 1.2 Fungsi 2: `services.create_package()`
- **Tujuan Fungsi:** Memvalidasi durasi $>0$ menit dan tarif harga $\ge 0$ Rupiah sebelum menyimpan paket sewa.
- **Mutasi A (Ubah Batas Durasi):**
  - *Kode Asli:* `if durasi_val <= 0:` (baris 261)
  - *Mutasi:* `if durasi_val < 0:`
  - *Dampak Perilaku:* Paket sewa berdurasi `0` menit diperbolehkan tersimpan di sistem.
  - *Hasil Uji:* **Tertangkap (*Killed*)** oleh `tests/test_validasi.py::test_validasi_nilai_batas_durasi_paket[Paket Nol Menit-0-10000-False-lebih besar dari 0 menit]`.
- **Mutasi B (Ubah Batas Bawah Harga Negatif):**
  - *Kode Asli:* `if harga_val < 0:` (baris 268)
  - *Mutasi:* `if harga_val <= 0:`
  - *Dampak Perilaku:* Paket promosi gratis dengan harga Rp `0` akan ditolak oleh sistem.
  - *Hasil Uji:* **Tertangkap (*Killed*)** oleh `tests/test_pertama.py` dan `tests/test_validasi.py::test_validasi_nilai_batas_harga_paket[Paket Promo Gratis-60-0-True-None]`.

---

### 1.3 Fungsi 3: `models.get_db_connection()`
- **Tujuan Fungsi:** Membuka koneksi SQLite dan menegakkan integritas referensial foreign key (`PRAGMA foreign_keys = ON;`).
- **Mutasi A (Hapus Penegakan Foreign Key):**
  - *Kode Asli:* `conn.execute("PRAGMA foreign_keys = ON;")` (baris 22)
  - *Mutasi:* Komentari atau hapus baris `conn.execute("PRAGMA foreign_keys = ON;")`.
  - *Dampak Perilaku:* SQLite secara baku tidak memeriksa integritas foreign key; penghapusan data induk yang sedang dirujuk transaksi anak tidak akan diblokir oleh SQLite engine.
  - *Hasil Uji:* **Tertangkap (*Killed*)** oleh `tests/test_transaksi_berelasi.py` (Langkah 6: Uji Proteksi FK) dan `tests/test_crud_konsol.py::F5-3`.
- **Mutasi B (Ubah Row Factory):**
  - *Kode Asli:* `conn.row_factory = sqlite3.Row` (baris 20)
  - *Mutasi:* Hapus baris pengaturan `row_factory` sehingga mengembalikan tuple standar alih-alih objek berbasis nama.
  - *Dampak Perilaku:* Seluruh pengaksesan kolom berbasis nama (misal: `row["status"]`, `row["kode_konsol"]`) akan melempar `TypeError: tuple indices must be integers or slices, not str`.
  - *Hasil Uji:* **Tertangkap (*Killed*)** seketika oleh seluruh fungsi pengujian integrasi dan alur HTTP.

---

## 2. Analisis Nilai Batas Kolom `stok_minimum` (Kapasitas Rental) dan `nama_pengguna`

Berdasarkan kamus data dan aturan bisnis sistem rental Exito Playbox:

### 2.1 Kolom `stok_minimum` / Kapasitas Unit Rental (`kapasitas_unit` / `stok_minimum`)
- **Aturan Kamus Data:** Jumlah unit konsol operasional minimal yang harus tersedia di gerai rental. Bertipe Integer, rentang yang sah adalah antara $1$ sampai dengan $50$ unit konsol.
- **Tabel Partisi dan 6 Nilai Batas:**

| Nilai Uji | Kategori Partisi | Jenis Nilai Batas | Hasil yang Diharapkan Menurut Kamus Data |
|:---:|---|---|---|
| `0` | Invalid (Di bawah batas minimal) | Batas atas daerah tidak valid | **Ditolak**: "Stok/kapasitas minimum harus lebih besar dari 0 unit." |
| `1` | Valid (Batas bawah minimum) | Batas bawah daerah valid | **Diterima**: Kuota minimum tervalidasi 1 unit. |
| `2` | Valid (Nilai normal bawah) | Tepat di atas batas bawah | **Diterima**: Kuota minimum tersimpan 2 unit. |
| `49` | Valid (Nilai normal atas) | Tepat di bawah batas atas | **Diterima**: Kuota minimum tersimpan 49 unit. |
| `50` | Valid (Batas atas maksimum) | Batas atas daerah valid | **Diterima**: Kuota maksimum tervalidasi 50 unit. |
| `51` | Invalid (Di atas batas maksimal) | Batas bawah daerah tidak valid | **Ditolak**: "Stok/kapasitas unit melebihi kapasitas fisik gerai (maks. 50)." |

---

### 2.2 Kolom `nama_pengguna` (`username`)
- **Aturan Kamus Data:** Karakter alfanumerik (huruf kecil dan angka), panjang antara $3$ sampai dengan $20$ karakter, tidak boleh mengandung spasi atau karakter khusus.
- **Tabel Partisi dan 6 Nilai Batas:**

| Nilai Uji | Panjang Karakter | Kategori Partisi | Hasil yang Diharapkan Menurut Kamus Data |
|:---:|:---:|---|---|
| `"ab"` | 2 karakter | Invalid (Terlalu pendek) | **Ditolak**: "Nama pengguna minimal 3 karakter." |
| `"abc"` | 3 karakter | Valid (Batas bawah) | **Diterima**: Nama pengguna valid dan terdaftar. |
| `"abcd"` | 4 karakter | Valid (Normal bawah) | **Diterima**: Nama pengguna valid. |
| `"kasir_budi_sukses_1"` | 19 karakter | Valid (Normal atas) | **Diterima**: Nama pengguna valid. |
| `"kasir_budi_sukses_12"` | 20 karakter | Valid (Batas atas) | **Diterima**: Nama pengguna 20 karakter tersimpan. |
| `"kasir_budi_sukses_123"`| 21 karakter | Invalid (Terlalu panjang) | **Ditolak**: "Nama pengguna maksimal 20 karakter." |

---

## 3. Cacat vs Permintaan Perubahan: Nama Barang/Konsol Berbeda Huruf Besar-Kecil

### Kasus:
Dua nama konsol/paket/barang yang hanya berbeda huruf besar-kecil (contoh: `"Semen"` dan `"semen"`, atau `"Paket Malam"` dan `"paket malam"`) dapat didaftarkan bersamaan ke dalam sistem.

### 3.1 Dua Kemungkinan Keputusan Klien:

#### Keputusan Opsi A: Diklasifikasikan sebagai **CACAT (Defect)**
- **Perspektif Klien:**
  Klien (pemilik rental/toko) menganggap bahwa secara entitas bisnis di dunia nyata, `"Semen"` dan `"semen"` adalah barang dagangan yang persis sama. Membiarkan keduanya tersimpan akan memecah data stok fisik menjadi dua baris terpisah, membingungkan kasir saat transaksi penjualan, dan mengacaukan pembukuan omset.
- **Tindakan Perbaikan:**
  Ubah kueri pengecekan duplikasi pada service layer dan DDL SQLite untuk menegakkan keunikan case-insensitive:
  ```sql
  SELECT id FROM items WHERE LOWER(nama_barang) = LOWER(?);
  -- atau pada skema DDL:
  CREATE TABLE items (
      nama_barang TEXT NOT NULL UNIQUE COLLATE NOCASE
  );
  ```
- **Rancangan Pengujian pytest untuk Opsi A:**
  ```python
  def test_opsi_a_nama_duplikat_beda_kapitalisasi_ditolak(test_db):
      create_item("Semen", db_name=test_db)
      sukses, errors, _ = create_item("semen", db_name=test_db)
      assert sukses is False
      assert any("sudah digunakan" in err for err in errors)
  ```

---

#### Keputusan Opsi B: Diklasifikasikan sebagai **PERMINTAAN PERUBAHAN (Change Request) / Fitur Sah**
- **Perspektif Klien:**
  Klien menyatakan bahwa dalam industri tertentu (misal: kode part manufaktur, serial number unit, atau barang impor), kapitalisasi huruf memiliki arti pembeda yang disengaja (misal: `"Semen"` adalah brand dagang semen instan, sedangkan `"semen"` adalah bahan curah kiloan). Oleh karena itu, perilaku case-sensitive saat ini dianggap telah sesuai dengan spesifikasi awal (*as-is*), dan penggabungan keduanya memerlukan perubahan aturan bisnis (*business rule change*).
- **Tindakan Perbaikan:**
  Sistem tetap mempertahankan pembedaan case-sensitive, namun menambahkan fitur pembantu berupa pesan peringatan konfirmasi (*confirmation warning prompt*) pada formulir:
  *"Peringatan: Terdapat nama serupa 'Semen'. Apakah Anda yakin ini barang yang berbeda?"*.
- **Rancangan Pengujian pytest untuk Opsi B:**
  ```python
  def test_opsi_b_nama_beda_kapitalisasi_diizinkan_sebagai_entitas_terpisah(test_db):
      ok1, _, id1 = create_item("Semen", db_name=test_db)
      ok2, _, id2 = create_item("semen", db_name=test_db)
      assert ok1 is True
      assert ok2 is True
      assert id1 != id2
      # Pastikan keduanya memiliki baris tersendiri di basis data
      items = get_all_items(db_name=test_db)
      names = [it["nama_barang"] for it in items]
      assert "Semen" in names and "semen" in names
  ```
