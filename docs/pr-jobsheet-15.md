# Pull Request: Laporan Bab 4 Lengkap, Revisi Bab 3, dan Materi Presentasi Sidang (Jobsheet 15)

- **Cabang Sumber (*Source Branch*):** `laporan/bab4`
- **Cabang Tujuan (*Target Branch*):** `main`
- **Tipe Perubahan:** Dokumentasi Komprehensif, Otomasi Analisis, Revisi Perancangan, dan Materi Kesiapan Sidang
- **Pengembang:** Maruf Syahbana (Scrum Master & Full-Stack Developer)
- **Status Evaluasi:** **100% SIAP DI-MERGE KE MAIN**

---

## 1. Ringkasan Perubahan Utama

Pull Request ini menyelesaikan seluruh instruksi pengerjaan **Jobsheet 15 (Sesi 1, Sesi 2, Tugas Lanjutan, dan Latihan Mandiri)**:

1. **Kelengkapan Laporan Bab 4 (Subbab 4.1 s/d 4.6 & Daftar Pustaka):**
   - [docs/bab4/peta-bukti.md](file:///c:/Users/maaru/Documents/rpl-project-ps/docs/bab4/peta-bukti.md): Peta bukti 6 subbab lengkap dengan pemilik dan status.
   - [docs/bab4/4.1-lingkungan.md](file:///c:/Users/maaru/Documents/rpl-project-ps/docs/bab4/4.1-lingkungan.md): Tabel hardware/software, dependensi Python, dan komitmen etika penggunaan AI (548 kata).
   - [docs/bab4/4.2-implementasi.md](file:///c:/Users/maaru/Documents/rpl-project-ps/docs/bab4/4.2-implementasi.md): Struktur 3-tier, 3 fitur utama & wireframe, 2 cuplikan kode arsitektural $\le 15$ baris, dan 3 siklus prompt representatif (669 kata).
   - [docs/bab4/4.3-keamanan.md](file:///c:/Users/maaru/Documents/rpl-project-ps/docs/bab4/4.3-keamanan.md): Tabel temuan keamanan SEC-PS-01 s/d 07, OWASP Top 10, komparasi sebelum-sesudah perbaikan, dan commit Git terkait (465 kata).
   - [docs/bab4/4.4-pengujian.md](file:///c:/Users/maaru/Documents/rpl-project-ps/docs/bab4/4.4-pengujian.md): Ringkasan 22 test case, 38 pytest passed, penutupan 3 cacat D-01..D-03 via TDD, hasil UAT 100% lulus, dan skor SUS 87.5 Grade A+ (772 kata).
   - [docs/bab4/4.5-rilis.md](file:///c:/Users/maaru/Documents/rpl-project-ps/docs/bab4/4.5-rilis.md): Jejak rilis SemVer v1.0.0 & v1.0.1, konfigurasi runner WSGI Waitress multithreaded, pencadangan online SQLite `cadangkan.py`, dan tautan manual operasional (818 kata).
   - [docs/bab4/4.6-pembahasan.md](file:///c:/Users/maaru/Documents/rpl-project-ps/docs/bab4/4.6-pembahasan.md): Matriks pemenuhan KF/KNF PRD, rekap jurnal vibe coding, tabel dampak waktu galat AI, 3 paragraf analitis kritis, 3 limitasi, dan 3 rekomendasi (1750 kata).
   - [docs/bab4/daftar-pustaka.md](file:///c:/Users/maaru/Documents/rpl-project-ps/docs/bab4/daftar-pustaka.md): Sitasi standar IEEE (Brooke 1996, OWASP 2021, SemVer, Flask, Waitress, SQLite, dll.) dan pernyataan akuntabilitas AI.

2. **Revisi Bab 3 (Perancangan Sistem & Rencana Uji):**
   - [docs/laporan/bab-3.md](file:///c:/Users/maaru/Documents/rpl-project-ps/docs/laporan/bab-3.md): Penambahan Subbab 3.7 memuat Tabel Matriks Perubahan terhadap Rancangan Awal (Lampiran B.4: 6 komponen perubahan dengan kategori perbaikan, penyempurnaan, dan simplifikasi), serta sinkronisasi istilah (penggunaan istilah 'pelanggan' secara konsisten) dan pemetaan rencana uji 3.6 dengan realisasi 4.4.

3. **Pengembangan Skrip Otomasi Verifikasi (Lampiran C & D):**
   - [alat/analisis_jurnal.py](file:///c:/Users/maaru/Documents/rpl-project-ps/alat/analisis_jurnal.py): Skrip parsing tabel markdown, rekap keputusan Terima/Ubah/Tolak, deteksi tag galat `[Galat: jenis]`, dan ringkasan gabungan.
   - [alat/periksa_draf.py](file:///c:/Users/maaru/Documents/rpl-project-ps/alat/periksa_draf.py): Skrip audit otomatis kelengkapan draf Bab 4 (panjang kata $\ge 150$, tabel/kode/gambar, ketiadaan penanda `[ISI]`, dan validasi KF PRD).

4. **Pemutakhiran Jurnal Vibe Coding:**
   - [jurnal/jurnal-maruf.md](file:///c:/Users/maaru/Documents/rpl-project-ps/jurnal/jurnal-maruf.md) & [jurnal-vibe-coding.md](file:///c:/Users/maaru/Documents/rpl-project-ps/jurnal-vibe-coding.md): Diperbarui hingga 61 entri log terstruktur (Entri 1 s/d 61), disematkan tag galat AI, dan diverifikasi tanpa galat parsing format.

5. **Materi Presentasi & Kesiapan Sidang Ujian Akhir (Langkah 10 s/d 12):**
   - [docs/presentasi/salindia-presentasi.md](file:///c:/Users/maaru/Documents/rpl-project-ps/docs/presentasi/salindia-presentasi.md): 13 slide presentasi berstruktur profesional.
   - [docs/presentasi/skrip-presentasi.md](file:///c:/Users/maaru/Documents/rpl-project-ps/docs/presentasi/skrip-presentasi.md): Skrip lisan 20 menit berwaktu per slide dan panduan aksi.
   - [docs/presentasi/simulasi-tanya-jawab-tanpa-ai.md](file:///c:/Users/maaru/Documents/rpl-project-ps/docs/presentasi/simulasi-tanya-jawab-tanpa-ai.md): Simulasi 3 pertanyaan teknis mendalam dan uji modifikasi mandiri tanpa AI (waktu: 7m 15s).
   - [docs/presentasi/skrip-demo-20menit.md](file:///c:/Users/maaru/Documents/rpl-project-ps/docs/presentasi/skrip-demo-20menit.md): Skenario live demo 4 tahap terukur.
   - [docs/bab4/kartu-progress-check.md](file:///c:/Users/maaru/Documents/rpl-project-ps/docs/bab4/kartu-progress-check.md): Kartu evaluasi mandiri kesiapan sidang terisi "Ya" pada 13 butir penilaian lengkap dengan bukti berkas.

6. **Latihan Mandiri & Dokumen Laporan Gabungan (Langkah 14 & Bagian 6):**
   - [docs/bab4/latihan-mandiri-bab4.md](file:///c:/Users/maaru/Documents/rpl-project-ps/docs/bab4/latihan-mandiri-bab4.md): 3 analisis latihan mandiri (transformasi deskriptif ke analitis, simulasi 5 tanya jawab penguji, dan analisis uji batas).
   - [docs/laporan/Laporan-Akhir-Exito-Playbox.md](file:///c:/Users/maaru/Documents/rpl-project-ps/docs/laporan/Laporan-Akhir-Exito-Playbox.md): Dokumen laporan gabungan Bab 3 revisi dan Bab 4 lengkap.

---

## 2. Hasil Eksekusi Pengujian & Verifikasi Otomatis

```text
1. Verifikasi Draf Bab 4 (alat/periksa_draf.py):
   HASIL KELENGKAPAN SUBBAB: 6 / 6 SELESAI (100.0%)
   [LULUS] Tidak ada ID Kebutuhan Fungsional (KF) asing yang tidak dikenal.
   >>> KELAYAKAN DRAF: MEMENUHI SYARAT (>= 80% dan KF Valid) <<<

2. Analisis Jurnal Vibe Coding (alat/analisis_jurnal.py):
   Total Entri: 61 entri
   • Terima : 55 (90.2%)
   • Ubah   : 6 (9.8%)
   • Tolak  : 0 (0.0%)
   Distribusi Tag Galat AI:
     - [Galat: dokumentasi]: 1 kali
     - [Galat: keamanan]: 1 kali
     - [Galat: konfigurasi]: 1 kali
     - [Galat: logika]: 5 kali
     - [Galat: sintaksis]: 1 kali

3. Rangkaian Pengujian Unit & Integrasi (Pytest 9.1.1):
   38 passed in 1.48s (100% Lulus, 0 failed, 0 skipped)

4. Pengujian Regresi & Keamanan Cepat (tests/uji_cepat.py):
   SEMUA UJI LULUS! (7 modul keamanan, integritas transaksi, dan relasi database stabil)
```

---

## 3. Daftar Periksa Kesiapan Penggabungan (*Merge Checklist*)
- [x] Seluruh subbab 4.1 hingga 4.6 memiliki $\ge 150$ kata dan elemen tabel/kode.
- [x] Tidak ada marker draf kosong `[ISI]`.
- [x] Bab 3 telah memuat Tabel Lampiran B.4 dan istilah telah disinkronkan.
- [x] Jurnal vibe coding memuat $\ge 61$ entri dengan tag galat AI.
- [x] Materi presentasi dan simulasi tanya jawab tanpa AI siap digunakan.
- [x] Seluruh pengujian otomatis (38 pytest dan uji cepat) lulus tanpa regresi.
