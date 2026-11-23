# Kartu Progress Check Kesiapan Sidang Tugas Besar RPL (Lampiran B.5)
## Proyek: Exito Playbox PlayStation Rental Management System

- **Nama Pengembang:** Maruf Syahbana
- **NIM / Peran:** 2024xx / Scrum Master, Full-Stack Developer, QA Engineer
- **Mitra Usaha:** Exito Playbox Rental PS (Bpk. Hendra)
- **Cabang Git:** `laporan/bab4` (menuju `main`)
- **Versi Rilis Saat Ini:** v1.0.1 (Production Ready)

---

## Tabel Penilaian Mandiri Kesiapan Ujian Akhir

| No | Butir Penilaian Mandiri | Status | Bukti Nyata & Lokasi Artefak |
|:---:|---|:---:|---|
| **1** | Seluruh Kebutuhan Fungsional (KF) berstatus *Must* dan *Should* dari PRD telah selesai diimplementasikan. | **Ya** | Matriks Pemenuhan PRD pada [docs/bab4/4.6-pembahasan.md](file:///c:/Users/maaru/Documents/rpl-project-ps/docs/bab4/4.6-pembahasan.md#L14-L30) (KF-01 s/d KF-08 terpenuhi 100%). |
| **2** | Seluruh pengujian otomatis unit dan integrasi lolos 100% tanpa ada yang sengaja dilewati (*skipped*). | **Ya** | Pytest 9.1.1 menghasilkan 38 skenario *passed* pada [tests/](file:///c:/Users/maaru/Documents/rpl-project-ps/tests/) dan `tests/uji_cepat.py` berstatus SEMUA UJI LULUS. |
| **3** | Pengerasan keamanan OWASP Top 10 telah diterapkan dan diverifikasi melalui audit mandiri. | **Ya** | Dokumen [docs/bab4/4.3-keamanan.md](file:///c:/Users/maaru/Documents/rpl-project-ps/docs/bab4/4.3-keamanan.md) memetakan 7 temuan keamanan (SEC-PS-01 s/d 07) beserta commit perbaikannya. |
| **4** | Tiga cacat perangkat lunak telah diselesaikan menggunakan pendekatan Test-Driven Development (TDD). | **Ya** | Penutupan Cacat D-01 (commit `16db5e1`), D-02 (commit `f7f17d9`), dan D-03 (commit `60f2567`) terdokumentasi di [docs/bab4/4.4-pengujian.md](file:///c:/Users/maaru/Documents/rpl-project-ps/docs/bab4/4.4-pengujian.md#L45-L65). |
| **5** | Uji Keberterimaan Pengguna (UAT) telah dilaksanakan bersama mitra nyata dengan hasil terukur. | **Ya** | UAT bersama Bpk. Hendra dan kasir rental menghasilkan tingkat kelulusan 100% skenario dan skor SUS 87.5 Grade A+ di [docs/bab4/4.4-pengujian.md](file:///c:/Users/maaru/Documents/rpl-project-ps/docs/bab4/4.4-pengujian.md#L68-L95). |
| **6** | Aplikasi siap dijalankan pada server produksi WSGI berstandar industri (bukan server development bawaan). | **Ya** | Konfigurasi multi-threaded WSGI runner Waitress pada [jalankan.py](file:///c:/Users/maaru/Documents/rpl-project-ps/jalankan.py) dan panduan rilis di [docs/bab4/4.5-rilis.md](file:///c:/Users/maaru/Documents/rpl-project-ps/docs/bab4/4.5-rilis.md). |
| **7** | Mekanisme pencadangan data *online* tanpa downtime telah tersedia dan teruji. | **Ya** | Skrip utilitas [cadangkan.py](file:///c:/Users/maaru/Documents/rpl-project-ps/cadangkan.py) berbasis SQLite Online Backup API dan direktori snapshot `backups/`. |
| **8** | Laporan Bab 4 lengkap (Subbab 4.1 hingga 4.6), setiap subbab $\ge 150$ kata, memuat tabel/kode, dan tanpa marker `[ISI]`. | **Ya** | Lolos 100% pada verifikasi otomatis [alat/periksa_draf.py](file:///c:/Users/maaru/Documents/rpl-project-ps/alat/periksa_draf.py) (6 dari 6 subbab berstatus SELESAI). |
| **9** | Bab 3 telah direvisi dengan menambahkan tabel perubahan rancangan awal dan sinkronisasi istilah. | **Ya** | Subbab 3.7 pada [docs/laporan/bab-3.md](file:///c:/Users/maaru/Documents/rpl-project-ps/docs/laporan/bab-3.md#L140-L165) memuat Matriks Perubahan Lampiran B.4. |
| **10** | Jurnal vibe coding terisi lengkap ($\ge 61$ entri log) dengan tag galat AI dan analisis kuantitatif. | **Ya** | Berkas [jurnal-vibe-coding.md](file:///c:/Users/maaru/Documents/rpl-project-ps/jurnal-vibe-coding.md) memuat 61 entri log terverifikasi via [alat/analisis_jurnal.py](file:///c:/Users/maaru/Documents/rpl-project-ps/alat/analisis_jurnal.py). |
| **11** | Materi presentasi lengkap: salindia 12–14 slide, skrip lisan berwaktu 20 menit, dan skenario demo terukur. | **Ya** | Berkas [docs/presentasi/salindia-presentasi.md](file:///c:/Users/maaru/Documents/rpl-project-ps/docs/presentasi/salindia-presentasi.md) (13 slides), [docs/presentasi/skrip-presentasi.md](file:///c:/Users/maaru/Documents/rpl-project-ps/docs/presentasi/skrip-presentasi.md), dan [docs/presentasi/skrip-demo-20menit.md](file:///c:/Users/maaru/Documents/rpl-project-ps/docs/presentasi/skrip-demo-20menit.md). |
| **12** | Simulasi tanya jawab mendalam dan tugas modifikasi mandiri tanpa bantuan AI telah diselesaikan $\le 10$ menit. | **Ya** | Dokumentasi pada [docs/presentasi/simulasi-tanya-jawab-tanpa-ai.md](file:///c:/Users/maaru/Documents/rpl-project-ps/docs/presentasi/simulasi-tanya-jawab-tanpa-ai.md) (waktu modifikasi riil: 7 menit 15 detik, uji lulus 100%). |
| **13** | Repositori bersih dari file basis data rahasia (`.env`, `*.db`) dan bebas dari kredensial hard-coded. | **Ya** | Audit `git ls-files "*.db" ".env"` bersih dan `contoh.env` tersedia sebagai cetak biru konfigurasi aman. |

---

## Kesimpulan Evaluasi Kesiapan:
**SIAP MENGIKUTI SIDANG UJIAN AKHIR TUGAS BESAR REKAYASA PERANGKAT LUNAK.**
Seluruh artefak teknis, dokumentasi akademis, rangkaian uji otomatis, dan persiapan materi demonstrasi telah lengkap 100% sesuai panduan Jobsheet 15.
