# Peta Bukti Bab 4 (Lampiran B.1) — Exito Playbox

Dokumen ini memetakan rencana penyusunan setiap subbab Bab 4 Laporan Rilis Tugas Mandiri 2 (RTM-2), berkas sumber artefak, jenis bukti pendukung yang ditampilkan, pemilik subbab, dan status pengerjaannya.

---

## Tabel Peta Bukti Subbab 4.1 – 4.6

| Subbab | Judul Subbab | Berkas Sumber Proyek | Bukti yang Ditampilkan | Penanggung Jawab (Pemilik) | Status Bukti |
|:---:|---|---|---|:---:|:---:|
| **4.1** | Lingkungan Pengembangan dan Pengoperasian | `requirements.txt`, `requirements-dev.txt`, `README.md` | • Tabel spesifikasi perangkat keras & lunak<br>• Tabel dependensi pustaka Python berversi pasti<br>• Pernyataan etika dan peran asisten AI | Maruf Syahbana | **Tersedia (Selesai)** |
| **4.2** | Implementasi Fitur Utama | `app.py`, `models.py`, `services.py`, `docs/desain/wireframe/`, `jurnal-vibe-coding.md` | • Diagram struktur proyek 3-tier<br>• 4 Tangkapan layar fitur inti (Dasbor, Buka Sewa, Selesai Denda, Master)<br>• Cuplikan kode terpilih $\le 15$ baris beranotasi alasan arsitektural<br>• 3 Siklus prompt AI representatif | Maruf Syahbana | **Tersedia (Selesai)** |
| **4.3** | Tinjauan Kode dan Keamanan | `docs/laporan-temuan.md`, `app.py` | • Tabel temuan keamanan OWASP Top 10 (A01, A05, A07)<br>• Status remediasi dan commit perbaikan<br>• Cuplikan perbandingan kode sebelum vs sesudah (CSRF & Rate Limiting) | Maruf Syahbana | **Tersedia (Selesai)** |
| **4.4** | Hasil Pengujian dan Evaluasi Cacat | `docs/pengujian/test-case.md`, `docs/pengujian/laporan-cacat.md`, `docs/uat/hasil-uat.md` | • Rekapitulasi 22 test case (BVA, negatif, normal)<br>• Hasil eksekusi 38 uji Pytest (100% Passed)<br>• Tabel penutupan 3 cacat nyata via TDD (D-01 s/d D-03)<br>• Tabel hasil UAT & skor rata-rata SUS 87.5 (Grade A+) | Maruf Syahbana | **Tersedia (Selesai)** |
| **4.5** | Rilis, Penerapan, dan Pemeliharaan | `versi.py`, `CHANGELOG.md`, `cadangkan.py`, `docs/audit-kesiapan-rilis.md` | • Ringkasan rilis Git tag `v1.0.0` & tambalan `v1.0.1`<br>• Parameter WSGI server produksi Waitress<br>• Prosedur pencadangan SQLite & pemulihan bencana | Maruf Syahbana | **Tersedia (Selesai)** |
| **4.6** | Pembahasan dan Refleksi Rekayasa | `jurnal-vibe-coding.md`, `docs/product-backlog.md`, `alat/analisis_jurnal.py` | • Tabel evaluasi pemenuhan seluruh KF dari PRD<br>• Rekapitulasi kuantitatif keputusan Vibe Coding (53 entri log)<br>• Tabel estimasi dampak waktu pengembangan<br>• 3 Keterbatasan sistem & 3 rekomendasi pengembangan | Maruf Syahbana | **Tersedia (Selesai)** |

---

## Catatan Kesiapan Bukti
Seluruh bukti sumber untuk subbab 4.1 sampai 4.6 telah berhasil diproduksi pada Jobsheet 9 sampai Jobsheet 14. Tidak ada subbab yang memiliki status bukti tertunda (*zero pending evidence*).
