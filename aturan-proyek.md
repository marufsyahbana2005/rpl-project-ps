Set-Content -Path aturan-proyek.md -Value @"
# Aturan Proyek (Project Rules & Guidelines) - Sistem Manajemen Rental PlayStation (Exito Playbox)

## 1. Stack Teknologi
- **Bahasa & Framework:** Python 3.14 (minimal 3.10), Flask, SQLite.
- **Paket Tambahan:** Penambahan pustaka atau paket eksternal baru hanya dilakukan jika benar-benar dibutuhkan dan terdokumentasi dengan jelas.

## 2. Struktur Folder Proyek
- `app.py`: Titik masuk utama aplikasi (Main entry point Flask).
- `templates/`: Direktori templat antarmuka HTML (Jinja2).
- `static/`: Direktori aset statis (CSS, JavaScript, gambar).
- `tests/`: Direktori unit test dan pengujian otomatis.
- `docs/`: Dokumentasi proyek (termasuk SRS, PRD, dan dokumen elisitasi).

## 3. Konvensi Pengembangan
- **Bahasa & Penamaan:** Komentar kode, pesan antarmuka (*UI messages*), dan pesan *commit* Git menggunakan Bahasa Indonesia yang jelas dan deskriptif.
- **Gaya Penamaan:** Menggunakan *snake_case* untuk fungsi/variabel Python dan *kebab-case* atau *lowercase* untuk nama berkas.
- **Git Workflow:** Menerapkan prinsip *one feature per commit* (satu fitur atau perbaikan per satu kali *commit*).

## 4. Larangan (Prohibitions)
- Menambahkan paket atau dependensi baru tanpa alasan dan persetujuan yang jelas.
- Menyimpan informasi rahasia (*secret keys*, *credentials*) secara langsung di dalam kode sumber (*hardcoded*).
- Mengubah berkas di luar ruang lingkup tugas yang sedang dikerjakan.
- Menghapus atau melemahkan pengujian otomatis (*unit tests*) yang sudah ditetapkan.

## 5. Cara Menjalankan dan Menguji
- **Menjalankan Aplikasi:**
  \`\`\`bash
  python -m venv venv
  source venv/bin/activate  # atau venv\\Scripts\\Activate pada Windows PowerShell
  pip install flask
  python app.py
  \`\`\`
- **Menjalankan Pengujian Otomatis (Kelak):**
  \`\`\`bash
  pytest
  \`\`\`
"@