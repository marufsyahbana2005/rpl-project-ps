# Keputusan Revisi Rancangan Pasca Design Review (Langkah 12) — Exito Playbox

Dokumen ini memuat tindak lanjut keputusan perbaikan rancangan antarmuka dan rencana pengujian setelah menerima masukan dari sesi penelaahan silang (*design review*).

---

## 1. Tabel Keputusan Masukan Penelaah

| No | Masukan Penelaah | Keputusan | Tindak Lanjut Perubahan / Alasan Keputusan |
|:--:|---|:--:|---|
| **1** | **Dialog Konfirmasi Pembatalan Sewa:**<br>Berikan dialog konfirmasi (*modal confirmation popup*) sebelum kasir membatalkan transaksi pada `wf-04` agar tidak terjadi salah klik (*accidental click*). | **TERIMA** | **Perubahan:** Menambahkan dialog konfirmasi modal pada alur penghentian sewa di `wf-04` dan memperbarui dokumen anotasi antarmuka (`docs/desain/wireframe/anotasi.md` Bagian 1.4 nomor 6). Kasir wajib mengonfirmasi alasan pembatalan (misal: listrik padam / kendala mesin) sebelum transaksi ditandai `'batal'`. |
| **2** | **Indikator Visual Berkedip & Suara Timer Habis:**<br>Tambahkan efek visual berkedip dan notifikasi suara saat timer sewa habis di `wf-02` agar kasir cepat tanggap di jam sibuk. | **TERIMA** | **Perubahan:** Menambahkan spesifikasi umpan balik multimedia pada anotasi `wf-02`: saat timer mencapai 00:00:00, kartu konsol memicu animasi berkedip (*pulsing border*) dan notifikasi audio browser singkat. Skenario uji ditambahkan ke `rencana-uji.md`. |
| **3** | **Penambahan Fitur Cetak Struk Kertas Mini:**<br>Sediakan tombol opsi cetak struk thermal 58mm untuk pelanggan walk-in. | **TANYA KLIEN / DITUNDA** | **Alasan:** Klien (Bpk. Hendra) pada elisitasi awal menyatakan bahwa nota transaksi di rental Exito Playbox umumnya bersifat *paperless* dan pelanggan jarang meminta struk fisik. Fitur ini dicatat sebagai usulan *enhancement* masa depan (*Backlog Sprint 4*) setelah dikonfirmasi lebih lanjut ke pihak pemilik. |
| **4** | **Ketahanan Timer saat Jaringan Terputus:**<br>Pertanyaan mengenai keakuratan timer di sisi server jika jaringan browser kasir sempat putus. | **TERIMA** | **Perubahan:** Menambahkan penegasan arsitektural pada dokumen pengujian: timer sewa dihitung berdasarkan selisih waktu server (`CURRENT_TIMESTAMP - waktu_mulai`), bukan berdasarkan timer JavaScript di browser kasir. Sehingga meskipun browser kasir sempat ditutup/terputus, durasi dan denda di database tetap 100% presisi. |

---

## 2. Pembaruan Dokumen Terdampak
1. **`docs/desain/wireframe/anotasi.md`:**  
   - Ditambahkan keterangan dialog modal konfirmasi pada tombol pembatalan sewa (`wf-04`).
   - Ditambahkan catatan efek visual berkedip (*pulsing border*) saat status konsol beralih ke `OVERTIME` (`wf-02`).
2. **`docs/pengujian/rencana-uji.md`:**  
   - Ditambahkan kasus uji verifikasi integritas timer berbasis waktu server (*server-side time calculation*).

---

## 3. Catatan Jurnal Vibe Coding (Pelajaran dari Tinjauan)
> **Pelajaran Penting dari Sesi Design Review:**  
> *"Desain antarmuka yang baik bukan hanya tentang tata letak tombol yang rapi, melainkan tentang memahami dinamika stres dan beban kerja pengguna di dunia nyata. Di ruang rental PlayStation yang ramai dengan suara game dan antrean pelanggan, kasir sangat rentan melakukan salah klik atau melewatkan perubahan teks kecil di layar. Oleh karena itu, proteksi aksi kritis (seperti tombol pembatalan sewa) wajib dilindungi oleh dialog konfirmasi, dan status kritis (seperti waktu sewa habis) membutuhkan penguatan umpan balik visual dan audio yang mencolok."*
