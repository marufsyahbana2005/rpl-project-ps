# Daftar User Story

## US-01 Pencatatan Transaksi Sewa Unit
Sebagai **Kasir Rental**, saya ingin **memulai dan menghentikan durasi sewa konsol via sistem** agar **biaya sewa terkalkulasi secara otomatis dan akurat**.

**Kriteria Penerimaan:**
- **Given** konsol dalam status *Tersedia*, **When** kasir memilih paket jam dan mengklik *Mulai Sewa*, **Then** status konsol berubah menjadi *Terpakai* dan timer durasi berjalan.
- **Given** transaksi sewa sedang berjalan, **When** waktu habis atau penghentian diproses, **Then** sistem menghitung total biaya sesuai tarif per jam dan membebaskan status konsol.

*Sumber:* Catatan wawancara No. 1 & 2 [Asumsi: Tidak]

---

## US-02 Monitoring Ketersediaan Unit Konsol
Sebagai **Operator Rental**, saya ingin **melihat dasbor status ketersediaan semua unit PS** agar **dapat mengalokasikan pelanggan yang datang dengan cepat**.

**Kriteria Penerimaan:**
- **Given** pengguna berada di halaman dasbor utama, **When** halaman dimuat, **Then** sistem menampilkan seluruh unit konsol beserta indikator warna statusnya (Hijau = Kosong, Merah = Terpakai).

*Sumber:* Catatan wawancara Analisis No. 2 [Asumsi: Tidak]

---

## US-03 Rekapitulasi Laporan Pendapatan Harian
Sebagai **Pemilik Rental**, saya ingin **menerima laporan rekapitulasi pendapatan harian** agar **dapat memantau omset bisnis tanpa menghitung nota fisik**.

**Kriteria Penerimaan:**
- **Given** pemilik membuka halaman Laporan, **When** memilih filter tanggal harian, **Then** sistem menampilkan total pendapatan, jumlah transaksi, dan ringkasan penyewaan per unit.

*Sumber:* Catatan wawancara No. 3 [Asumsi: Ya]
