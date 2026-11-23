# Laporan Pembahasan Latihan Mandiri & Bahan Kuis 2 (Jobsheet 11) — Exito Playbox

Dokumen ini memuat analisis teknis mendalam terhadap 3 topik Latihan Mandiri Keamanan Web serta rangkuman materi persiapan Kuis 2 LMS.

---

## 1. Analisis Latihan Mandiri 1: Kelemahan Hash Cepat (`hashlib.sha256`) vs KDF Ber-Salt (`generate_password_hash`)

### Skenario Kode Hash Lemah:
```python
import hashlib

def hash_lemah(password):
    return hashlib.sha256(password.encode()).hexdigest()
```

### Dua Kelemahan Fatal Dibandingkan `generate_password_hash`:
1. **Ketiadaan Garam Kriptografis (*No Salt / Deterministic Output*):**
   - Fungsi `hashlib.sha256()` polos menghasilkan nilai heksadesimal yang identik untuk kata sandi yang sama.
   - **Dampak Serangan:** Penyerang dapat menggunakan tabel pencarian terkomputasi sebelumnya (*Rainbow Tables*) untuk membalikkan jutaan hash kata sandi menjadi teks asli dalam hitungan detik.
   - **Perbandingan Werkzeug:** `generate_password_hash()` secara otomatis menyisipkan *salt* acak unik (misal: 16 byte acak) untuk setiap kata sandi, sehingga dua pengguna dengan kata sandi "rahasia123" akan memiliki nilai hash yang sama sekali berbeda di basis data.
2. **Terlalu Cepat (*High Throughput / Low Computational Cost*):**
   - SHA-256 dirancang untuk integritas berkas dan penandatanganan cepat, mampu mengeksekusi miliaran operasi per detik pada kartu grafis (GPU) modern.
   - **Dampak Serangan:** Penyerang dapat melakukan serangan tebak kata sandi (*offline brute-force attack*) hingga $> 10^{9}$ percobaan per detik.
   - **Perbandingan Werkzeug:** Menggunakan fungsi derivasi kunci (*Key Derivation Function* / KDF) lambat seperti `scrypt` atau `PBKDF2-HMAC-SHA256` dengan faktor peregangan (*work factor / cost factor*). Algoritma ini membutuhkan memori dan CPU signifikan, membatasi kemampuan penyerang menjadi hanya beberapa ratus tebakan per detik.

---

## 2. Analisis Latihan Mandiri 2: Bahaya Hanya Menyembunyikan Tautan Antarmuka (*Security through Obscurity*)

### Skenario Masalah:
Pengembang hanya menyembunyikan tombol `[Hapus]` atau menu `[Paket Sewa]` di templat Jinja2:
```html
<!-- Cacat Keamanan: Hanya menyembunyikan tombol di HTML -->
{% if current_role == 'owner' %}
    <form action="/consoles/1/hapus" method="POST">
        <button type="submit">Hapus</button>
    </form>
{% endif %}
```
Namun di `app.py`, decorator `@peran_diperlukan('owner')` tidak dipasang pada rute:
```python
# Cacat: Tidak ada penjagaan peran di server
@app.route("/consoles/<int:id>/hapus", methods=["POST"])
@login_diperlukan
def hapus_konsol(id):
    delete_console(id)
    return redirect(url_for('daftar_konsol'))
```

### Eksploitasi oleh Peran Terbatas:
Meskipun tombol hapus tidak terlihat di browser kasir:
1. Kasir dapat membuka DevTools browser (F12) atau menggunakan alat HTTP seperti Postman / cURL.
2. Kasir mengirim permintaan langsung:
   ```bash
   curl -X POST http://localhost:5000/consoles/1/hapus -b "session=..."
   ```
3. Server memproses penghapusan karena server hanya memeriksa status login, bukan peran!

### Solusi Perbaikan (Pertahanan Berlapis):
Penegakan otorisasi **wajib selalu berada di lapisan server backend**:
```python
@app.route("/consoles/<int:id>/hapus", methods=["POST"])
@peran_diperlukan("owner") # Mengembalikan HTTP 403 Forbidden bila kasir mencoba mengirim POST
def hapus_konsol(id):
    ...
```

---

## 3. Analisis Latihan Mandiri 3: Celah *Open Redirect* dan Mekanisme Penangkalnya

### Skenario Kerentanan:
Pada sistem autentikasi tanpa validasi parameter `next`:
```python
# Cacat: Mengalihkan langsung tanpa sanitasi
@app.route("/login", methods=["POST"])
def login():
    ...
    next_page = request.args.get("next")
    return redirect(next_page) # Penyerang mengirim: /login?next=https://jahat.example
```

### Bahaya Eksploitasi:
1. Penyerang menyebarkan tautan phishing: `https://exitoplaybox.com/login?next=https://jahat.example/fake-portal`.
2. Korban melihat domain asli `exitoplaybox.com`, merasa aman, dan memasukkan kredensial.
3. Setelah login berhasil, peramban otomatis mengalihkan korban keluar ke `jahat.example` yang tampilannya dipalsukan untuk mencuri informasi kartu kredit atau mengunduh malware.

### Solusi dan Kode Pencegah:
Fungsi `is_safe_url(target)` memastikan nilai `next` hanya merujuk ke jalur lokal internal:
```python
def is_safe_url(target):
    if not target:
        return False
    # Wajib diawali '/' dan dilarang '//' (skema relatif) atau '/\' (bypass Windows)
    if target.startswith("/") and not target.startswith("//") and not target.startswith("/\\"):
        return True
    return False
```
Telah diverifikasi lewat uji otomatis `test_autentikasi_peran.py` (TC-4): masukan `https://jahat.example` dinetralkan dan dialihkan ke `/sewa`.

---

## 4. Rangkuman Materi Kunci Kuis 2 LMS

1. **Autentikasi vs Otorisasi:**
   - *Autentikasi:* "Siapakah Anda?" (Pembuktian identitas lewat username dan password).
   - *Otorisasi:* "Apa yang boleh Anda lakukan?" (Pemeriksaan izin akses fitur berdasarkan peran/RBAC).
2. **Karakteristik Hash Kriptografis Aman:**
   - Bersifat satu arah (*one-way*), tahan benturan (*collision-resistant*), memiliki efek longsor (*avalanche effect*), dan ber-salt unik acak.
3. **Manajemen Sesi:**
   - Sesi disimpan di sisi server (atau di-enkripsi dalam cookie yang ditandatangani secara kriptografis menggunakan `SECRET_KEY`).
   - Selalu panggil `session.clear()` sebelum menginisialisasi sesi baru guna mencegah *Session Fixation Attack*.
4. **Prinsip Least Privilege:**
   - Setiap pengguna hanya diberikan hak akses minimum yang mutlak diperlukan untuk menyelesaikan tugas operasionalnya. Kasir hanya berhak mengelola sewa, bukan mengubah struktur inventaris atau tarif rental.
