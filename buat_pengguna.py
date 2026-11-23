"""
buat_pengguna.py — Skrip CLI Pembuatan Pengguna Awal Ber-hash (Langkah 3 / Jobsheet 11)
Mengelola pembuatan akun pengguna dengan kata sandi ter-hash secara aman
tanpa menyimpan kata sandi plaintext di basis data maupun kode sumber.
"""

import os
import sys
import getpass
import argparse

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from models import init_db
from services import create_user, get_user_by_username


def main():
    parser = argparse.ArgumentParser(description="Buat akun pengguna baru Exito Playbox.")
    parser.add_argument("--username", "-u", help="Nama pengguna (username)")
    parser.add_argument("--role", "-r", choices=["kasir", "owner"], help="Peran pengguna (kasir / owner)")
    parser.add_argument("--password", "-p", help="Kata sandi pengguna (opsional, jika tidak diisi akan diminta lewat prompt interaktif)")
    parser.add_argument("--db", help="Nama file basis data SQLite", default="rental.db")
    args = parser.parse_args()

    db_name = os.environ.get("DATABASE_NAME", args.db)
    init_db(db_name)

    print("==================================================")
    print(" EXITO PLAYBOX — PEMBUATAN AKUN PENGGUNA TER-HASH ")
    print("==================================================")

    # 1. Input Username
    username = args.username
    if not username:
        username = input("Masukkan nama pengguna (username): ").strip().lower()

    # Cek duplikasi sebelum meminta password
    existing = get_user_by_username(username, db_name=db_name)
    if existing:
        print(f"[GALAT] Nama pengguna '{username}' sudah terdaftar dengan peran '{existing['role']}'.")
        sys.exit(1)

    # 2. Input Role
    role = args.role
    if not role:
        while True:
            r = input("Pilih peran [1 = kasir, 2 = owner]: ").strip()
            if r in ("1", "kasir"):
                role = "kasir"
                break
            elif r in ("2", "owner"):
                role = "owner"
                break
            print("Pilihan peran tidak valid. Masukkan 1 untuk kasir atau 2 untuk owner.")

    # 3. Input Password (aman dengan getpass jika tidak ada di argumen)
    password = args.password
    if not password:
        while True:
            p1 = getpass.getpass("Masukkan kata sandi (minimal 6 karakter): ")
            p2 = getpass.getpass("Konfirmasi kata sandi: ")
            if p1 != p2:
                print("[GALAT] Konfirmasi kata sandi tidak cocok. Silakan coba lagi.")
                continue
            if len(p1) < 6:
                print("[GALAT] Kata sandi minimal 6 karakter. Silakan coba lagi.")
                continue
            password = p1
            break

    # 4. Simpan Pengguna dengan Kata Sandi Ter-hash
    success, errors, new_id = create_user(
        username=username,
        password=password,
        role=role,
        db_name=db_name,
    )

    if success:
        print("\n--------------------------------------------------")
        print(f"[SUKSES] Akun #{new_id} untuk '{username}' ({role.upper()}) berhasil dibuat!")
        print("Kata sandi berhasil di-hash menggunakan algoritma ber-salt modern.")
        print("--------------------------------------------------")
    else:
        print("\n[GALAT PEMBUATAN PENGGUNA]")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
