-- Aktifkan penegakan Foreign Key di SQLite
PRAGMA foreign_keys = ON;

-- 1. Tabel users (Akun Kasir dan Pemilik)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('kasir', 'owner')),
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)) -- [Hasil Konfirmasi Q1]
);

-- 2. Tabel consoles (Unit Konsol PlayStation)
CREATE TABLE IF NOT EXISTS consoles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kode_konsol TEXT NOT NULL UNIQUE,
    jenis_konsol TEXT NOT NULL CHECK (jenis_konsol IN ('PS3', 'PS4', 'PS5')),
    status TEXT NOT NULL DEFAULT 'tersedia' CHECK (status IN ('tersedia', 'terpakai', 'maintenance'))
);

-- 3. Tabel packages (Paket Sewa Rental)
CREATE TABLE IF NOT EXISTS packages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_paket TEXT NOT NULL UNIQUE,
    jenis_konsol TEXT NOT NULL DEFAULT 'PS4' CHECK (jenis_konsol IN ('PS3', 'PS4', 'PS5')), -- [Hasil Konfirmasi Q7]
    durasi_menit INTEGER NOT NULL CHECK (durasi_menit > 0),
    harga INTEGER NOT NULL CHECK (harga >= 0),
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)) -- [Hasil Konfirmasi Q9]
);

-- 4. Tabel transactions (Pencatatan Transaksi Sewa)
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_pelanggan TEXT NOT NULL DEFAULT 'Pelanggan', -- [Hasil Konfirmasi Q10]
    user_id INTEGER NOT NULL,
    console_id INTEGER NOT NULL,
    package_id INTEGER NOT NULL,
    waktu_mulai DATETIME NOT NULL,
    waktu_selesai DATETIME,
    status_bayar TEXT NOT NULL DEFAULT 'open_bill' CHECK (status_bayar IN ('lunas', 'open_bill', 'batal')), -- [Hasil Konfirmasi Q11]
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT,
    FOREIGN KEY (console_id) REFERENCES consoles(id) ON DELETE RESTRICT,
    FOREIGN KEY (package_id) REFERENCES packages(id) ON DELETE RESTRICT
);

-- 5. Tabel fines (Denda Keterlambatan Sewa)
CREATE TABLE IF NOT EXISTS fines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id INTEGER NOT NULL UNIQUE,
    menit_terlambat INTEGER NOT NULL CHECK (menit_terlambat >= 0),
    biaya_denda INTEGER NOT NULL CHECK (biaya_denda >= 0),
    FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE CASCADE
);
