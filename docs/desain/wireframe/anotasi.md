# Anotasi Wireframe dan Penerapan Prinsip Antarmuka — Exito Playbox

Dokumen ini memuat anotasi terperinci untuk seluruh elemen wireframe antarmuka sistem Exito Playbox (`wf-01` sampai `wf-07`), pemetaan pesan galat skenario use case, serta dokumentasi penerapan prinsip antarmuka dan catatan sebelum-sesudah perbaikan rancangan.

---

## 1. Tabel Anotasi Elemen Antarmuka per Halaman

### 1.1 Halaman Login (`wf-01-login.png`)
| No | Elemen | Data / Aksi | Aturan / Pesan | Prinsip Antarmuka |
|:--:|---|---|---|---|
| **1** | Judul & Konteks Halaman | Teks judul: "Masuk ke Sistem" | Memberikan identitas jelas bahwa pengguna sedang berada di gerbang autentikasi. | Kejelasan & Keterbacaan |
| **2** | Alert Box Pesan Galat | Area notifikasi status kesalahan | Muncul bila kredensial tidak cocok atau akun nonaktif: `"[!] Username atau password salah!"` | Umpan Balik Segera |
| **3** | Input Isian Username | `users.username` (Teks) | Minimal 4 karakter, tanpa spasi, karakter huruf kecil & angka saja. | Pencegahan Galat |
| **4** | Input Isian Password | `users.password_hash` (Password mask) | Disamarkan dengan bullet (`••••••`), wajib diisi (tidak boleh kosong). | Keamanan & Pencegahan Galat |
| **5** | Tombol Aksi "Masuk" | Aksi POST otentikasi | Tombol dengan warna aksen utama (Biru). Mengarahkan ke Beranda (`wf-02`) jika sukses. | Konsistensi Aksi Utama |

---

### 1.2 Dasbor Pemantauan Unit & Timer (`wf-02-dasbor-utama.png`)
| No | Elemen | Data / Aksi | Aturan / Pesan | Prinsip Antarmuka |
|:--:|---|---|---|---|
| **1** | Bar Navigasi & Identitas | Menu global, peran aktif & logout | Menampilkan peran pengguna `[Kasir (Andi)]` dan tombol keluar. Konsisten di semua halaman. | Konsistensi Antarmuka |
| **2** | Judul & Keterangan Dasbor | Teks judul & indikator polling | Menjelaskan fungsi dasbor pemantauan konsol dan interval polling sinkronisasi 10 detik. | Kejelasan & Transparansi |
| **3** | Kartu Ringkasan Status Unit | Penghitung unit: Tersedia, Terpakai, Maintenance | Menampilkan rekapitulasi cepat status unit PlayStation menggunakan kode warna standar (Hijau, Merah, Kuning). | Pengenalan Visual Cepat |
| **4** | Kartu Unit "Tersedia" | `consoles.kode_konsol`, `jenis_konsol`, status | Tombol hijau `[+] Mulai Sewa` hanya aktif jika unit benar-benar kosong/tersedia. | Pembatasan Aksi & Pencegahan Galat |
| **5** | Kartu Unit "Terpakai" & Timer | `transactions.nama_pelanggan`, countdown timer | Timer bergerak mundur *real-time*. Tombol merah `[v] Selesaikan & Bayar` membuka form kasir. | Umpan Balik Kontinu |
| **6** | Indikator Overtime Denda | Status Kuning `OVERTIME`, waktu keterlambatan | Menandai sesi sewa yang telah melewati paket durasi dengan teks keterlambatan yang kontras. | Visibilitas Status Sistem |
| **7** | Banner Sinkronisasi Polling | Timestamp sinkronisasi terakhir | Informasi waktu terakhir data diperbarui otomatis dari server: `"Terakhir sinkron: 10:15:30 WIB"`. | Umpan Balik Sistem |

---

### 1.3 Form Pembukaan Sewa Konsol (`wf-03-buka-sewa.png`)
| No | Elemen | Data / Aksi | Aturan / Pesan | Prinsip Antarmuka |
|:--:|---|---|---|---|
| **1** | Banner Galat Validasi | Pesan peringatan kesalahan input | Muncul jika kolom wajib kosong saat submit: `"[!] Validasi Gagal: Nama pelanggan wajib diisi minimal 2 karakter!"` (Pengecualian UC-01 3b). | Umpan Balik & Pencegahan Galat |
| **2** | Display Unit Terpilih | `consoles.kode_konsol`, `jenis_konsol` | Terkunci (*read-only*), menjamin kasir tidak salah membuka sewa pada konsol yang sedang dipakai orang lain. | Pencegahan Galat |
| **3** | Input Nama Pelanggan | `transactions.nama_pelanggan` (Teks) | Wajib diisi, minimal 2 karakter, nama panggilan pengenal pelanggan di tempat rental. | Pencegahan Galat |
| **4** | Dropdown Paket Sewa | `packages.nama_paket`, `durasi_menit`, `harga` | Hanya menampilkan daftar paket aktif (`is_active = 1`) yang sesuai dengan tipe konsol unit terpilih (PS3/PS4/PS5). | Pencegahan Galat & Efisiensi |
| **5** | Radio Metode Pembayaran | `transactions.status_bayar` | Pilihan: `(o) Open Bill` (bayar saat selesai) atau `( ) Bayar Lunas` (bayar di depan). Disertai estimasi waktu selesai. | Fleksibilitas Operasional |
| **6** | Tombol Simpan & Batal | Aksi simpan sewa / batalkan form | Tombol hijau `Mulai Sewa` untuk eksekusi, tombol abu-abu `Batal` untuk kembali ke dasbor tanpa perubahan. | Kontrol Pengguna & Jalan Keluar |

---

### 1.4 Penghentian Sewa & Kelola Denda (`wf-04-selesai-sewa-denda.png`)
| No | Elemen | Data / Aksi | Aturan / Pesan | Prinsip Antarmuka |
|:--:|---|---|---|---|
| **1** | Alert Deteksi Overtime | Notifikasi keterlambatan & kalkulasi denda | Muncul otomatis jika `waktu_selesai - waktu_mulai > durasi_paket + 5 menit`: `"[!] TERDETEKSI OVERTIME: Terlambat 18 menit... Denda: Rp 4.000"` (Pengecualian UC-02 2b). | Umpan Balik Transparan |
| **2** | Identitas Transaksi | Nomor nota `#TRX-20261116-004` | Menampilkan nomor transaksi unik yang sedang diselesaikan untuk verifikasi kasir. | Kejelasan Informasi |
| **3** | Tabel Rincian Biaya | Paket sewa, biaya denda, durasi terpakai | Rincian transparan antara tarif pokok sewa dengan biaya denda keterlambatan. | Keterbacaan Finansial |
| **4** | Baris Total Tagihan Akhir | Total Rupiah (`packages.harga` + `fines.biaya_denda`) | Ditampilkan dengan ukuran huruf besar dan warna primer kontras agar kasir dan penyewa tidak salah membaca nominal. | Penegasan Informasi Kritis |
| **5** | Tombol "Konfirmasi Bayar" | Aksi penyelesaian sewa | Menutup transaksi menjadi `'lunas'`, membebaskan status konsol kembali ke `'tersedia'`. | Umpan Balik Keberhasilan |
| **6** | Tombol "Batalkan Sewa" | Aksi pembatalan transaksi khusus | Mengubah status transaksi ke `'batal'` (kasus listrik padam < 5 menit awal). Konsol langsung dibebaskan tanpa denda. | Penanganan Kondisi Khusus |

---

### 1.5 Kelola Unit Konsol & Paket Sewa (`wf-05-kelola-master.png` — Khusus Pemilik)
| No | Elemen | Data / Aksi | Aturan / Pesan | Prinsip Antarmuka |
|:--:|---|---|---|---|
| **1** | Alert Notifikasi Sukses | Konfirmasi keberhasilan perubahan | Muncul setelah update status: `"[v] Berhasil: Status operasional unit PS3-02 berhasil diperbarui menjadi Maintenance."` | Umpan Balik Positif |
| **2** | Judul Tabel Master Konsol | Informasi total unit terdaftar (8 unit) | Menjelaskan cakupan seluruh inventaris fisik konsol rental. | Kejelasan Informasi |
| **3** | Tabel Unit & Aksi Status | `consoles.kode_konsol`, `jenis_konsol`, status | Tombol aksi `[Ubah Status]` (Tersedia $\leftrightarrow$ Maintenance). Tidak ada tombol *Hard Delete* untuk menjaga integritas data. | Pencegahan Kerusakan Data |
| **4** | Judul Tabel Master Paket | Daftar paket aktif & tarif resmi | Menampilkan seluruh opsi durasi sewa yang tersedia bagi kasir. | Konsistensi |
| **5** | Tabel Paket & Status Aktif | `packages.nama_paket`, `jenis_konsol`, `harga`, `is_active` | Paket lama yang kedaluwarsa berstatus "Nonaktif" sehingga tidak muncul di form kasir namun tetap tersimpan di riwayat. | Pencegahan Galat |
| **6** | Tombol Tambah Master Baru | Aksi `[+] Tambah Konsol` & `[+] Buat Paket` | Tombol biru terstandar untuk membuka form penambahan master baru. | Konsistensi Aksi |

---

### 1.6 Penelusuran Riwayat Transaksi (`wf-06-riwayat-transaksi.png`)
| No | Elemen | Data / Aksi | Aturan / Pesan | Prinsip Antarmuka |
|:--:|---|---|---|---|
| **1** | Filter & Bar Pencarian | Input pencarian nama pelanggan & tanggal | Pencarian instan berdasarkan nama pelanggan atau filter tanggal transaksi tertentu. | Kemudahan Pencarian Data |
| **2** | Header Tabel Riwayat | Kolom data transaksi lengkap | Menyajikan kolom: ID Nota, Pelanggan, Unit, Paket, Waktu Mulai-Selesai, Denda, Total, Status. | Keterbacaan Tabel |
| **3** | Badge Status Pembayaran | `transactions.status_bayar` | Label visual berwarna: Hijau (`Lunas`), Kuning (`Open Bill`), Merah (`Batal`). | Pembedaan Status Visual |
| **4** | Kontrol Paginasi Data | Navigasi halaman `[< Sebelumnya] [1] [2] [Berikutnya >]` | Membatasi tampilan 5-10 baris per halaman agar performa render data cepat dan tidak membebani layar. | Efisiensi Antarmuka |

---

### 1.7 Laporan Rekapitulasi Pendapatan (`wf-07-laporan-pendapatan.png` — Khusus Pemilik)
| No | Elemen | Data / Aksi | Aturan / Pesan | Prinsip Antarmuka |
|:--:|---|---|---|---|
| **1** | Filter Periode Rentang Tanggal | Input tanggal mulai s/d tanggal selesai | Pemilik dapat memilih tanggal custom atau memilih tombol jalan pintas (*shortcut*): "Hari Ini", "Minggu Ini", "Bulan Ini". | Fleksibilitas Pengguna |
| **2** | Tiga Kartu Metrik Omset | Omset Paket, Omset Denda, Omset Bersih | Tampilan *high-level* angka pendapatan kotor, denda, dan total penerimaan bersih dengan angka format Rupiah besar. | Keterbacaan Eksekutif |
| **3** | Tabel Kontribusi per Unit Konsol | `consoles.kode_konsol`, sesi sewa, jam, omset | Rincian kontribusi omset per unit konsol untuk membantu pemilik mengevaluasi unit konsol terlaris. | Kebutuhan Analisis Bisnis |
| **4** | Baris Ringkasan Total | Akumulasi total sesi, durasi jam, dan uang | Memverifikasi kecocokan antara rincian tabel per unit dengan kartu metrik omset di atasnya. | Integritas Informasi |

---

## 2. Pemeriksaan Terhadap Prinsip Antarmuka (Bagian 2.3)

1. **Konsistensi Navigasi dan Elemen:**
   - Seluruh halaman (`wf-02` hingga `wf-07`) memiliki *Top Navigation Bar* yang identik: warna latar gelap `#0F172A`, logo "EXITO PLAYBOX" di kiri, menu navigasi utama di tengah, dan indikator pengguna aktif di kanan.
   - Tombol aksi utama (*primary/success*) konsisten menggunakan warna hijau/biru dengan label teks aksi yang diawali tanda bantu visual (`[+]`, `[v]`, `[>]`).
   - Tombol pembatalan/kembali konsisten berada di sisi kanan atau menggunakan warna netral abu-abu.

2. **Umpan Balik Segera (*Immediate Feedback*):**
   - Setiap kondisi galat atau peringatan validasi (`wf-01`, `wf-03`, `wf-04`) memiliki kontainer pesan bertanda `[!]` dengan batas garis merah/kuning dan teks deskriptif yang menjelaskan letak kesalahan.
   - Setiap aksi modifikasi status sukses (`wf-05`) langsung menampilkan pesan notifikasi hijau bertanda `[v]`.
   - Dasbor pemantauan (`wf-02`) menampilkan timestamp terakhir sinkronisasi polling data otomatis.

3. **Pencegahan Galat (*Error Prevention*):**
   - Pemilihan unit pada form buka sewa (`wf-03`) bersifat terkunci (*read-only*) dari unit yang dipilih pada dasbor, mencegah kasir salah memilih unit konsol yang sedang terpakai.
   - Pilihan paket sewa menggunakan *dropdown* yang telah disaring otomatis berdasarkan jenis konsol unit terpilih (paket PS3 hanya muncul untuk unit PS3, paket PS5 hanya untuk unit PS5).
   - Kasir tidak dapat mengetikkan nominal denda secara sembarangan; denda dihitung otomatis oleh sistem pada `wf-04` sesuai aturan *grace period* 5 menit dan tarif proporsional.

4. **Keterbacaan dan Kejelasan Istilah:**
   - Seluruh istilah menggunakan bahasa Indonesia yang lugas dan dipahami oleh kasir rental ("Buka Sewa", "Selesaikan & Bayar", "Tersedia", "Terpakai", "Maintenance", "Lunas", "Batal").
   - Nominal uang selalu ditulis dengan pemisah ribuan standar Rupiah (`Rp 24.000`).

---

## 3. Catatan Perbaikan Rancangan Sebelum vs Sesudah Penerapan Prinsip

Berikut adalah dokumentasi evaluasi dan perbaikan rancangan sebelum dan sesudah penerapan prinsip desain antarmuka:

| No | Komponen Antarmuka | Rancangan Sebelum Evaluasi Prinsip | Rancangan Sesudah Perbaikan Prinsip | Alasan Perbaikan & Prinsip yang Diterapkan |
|:--:|---|---|---|---|
| **1** | **Form Buka Sewa (`wf-03`): Input Durasi & Tarif** | Kasir mengetik durasi sewa (angka menit bebas) dan mengetik nominal rupiah sewa secara manual di kotak teks. | Input durasi dan nominal diganti menjadi **Dropdown Paket Sewa Resmi** yang terikat langsung dengan tipe unit konsol (`packages.nama_paket`). | **Prinsip: Pencegahan Galat (*Error Prevention*)**<br>Mencegah kasir salah memasukkan nilai angka negatif, salah ketik durasi, atau memanipulasi harga sewa secara sepihak. |
| **2** | **Kelola Master (`wf-05`): Tombol Hapus Konsol Rusak** | Terdapat tombol merah `[Hapus Konsol]` yang melakukan *hard-delete* baris konsol dari database. | Tombol `[Hapus Konsol]` dihilangkan dan diganti dengan tombol **`[Ubah Status: Maintenance]`**. | **Prinsip: Integritas Data & Proteksi Sistem**<br>Menghapus konsol fisik yang memiliki riwayat transaksi akan memicu error integritas (*foreign key restriction*) dan merusak audit trail laporan keuangan lampau. |
| **3** | **Selesai Sewa (`wf-04`): Deteksi & Perhitungan Denda** | Kasir menghitung kelebihan jam di kepala lalu mengetikkan nominal denda ke kolom tagihan tanpa rincian. | Sistem secara otomatis membandingkan waktu selesai dengan durasi paket, menerapkan **toleransi 5 menit (*grace period*)**, lalu menampilkan **Banner Alert Denda Overtime** dan rincian tabel biaya terpisah. | **Prinsip: Umpan Balik Segera & Transparansi Informasi**<br>Menghilangkan perdebatan antara kasir dan pelanggan mengenai perhitungan denda serta memberikan keadilan waktu *save game*. |
| **4** | **Navigasi Global: Menu Laporan Keuangan** | Menu "Laporan Omset" dan "Kelola Unit" terlihat dan dapat diklik oleh semua pengguna termasuk kasir biasa. | Menu "Laporan Omset" dan "Kelola Unit & Paket" **diberi label khusus Pemilik** dan disembunyikan/dibatasi hak aksesnya (*role-based authorization*) saat login sebagai kasir. | **Prinsip: Pembatasan Hak Akses & Keamanan Sistem**<br>Mencegah kebocoran data rahasia omset keuangan bisnis kepada pihak staf operasional biasa. |
