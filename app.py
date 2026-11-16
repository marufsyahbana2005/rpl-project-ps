"""
app.py — Titik Masuk Utama Aplikasi Web Flask Exito Playbox
Mengelola inisialisasi aplikasi, routing antarmuka, dan penanganan permintaan HTTP.
"""

import os
from flask import Flask, redirect, url_for, render_template, request, flash
from models import init_db
from services import get_all_consoles, create_console, get_console_by_id

# Inisialisasi Aplikasi Flask
app = Flask(__name__)

# Konfigurasi Kunci Rahasia dari Variabel Lingkungan
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "exito-playbox-dev-secret-key-2026-rentalsecure"
)
app.config["DATABASE_NAME"] = os.environ.get("DATABASE_NAME", "rental.db")


# Rute Beranda (Redirect ke Entitas Utama: /consoles)
@app.route("/")
def index():
    """
    Rute beranda utama yang mengalihkan pengguna langsung
    ke halaman daftar unit konsol (/consoles).
    """
    return redirect(url_for("daftar_konsol"))


# Rute Daftar Konsol (Siklus 2)
@app.route("/consoles")
def daftar_konsol():
    """
    Halaman utama daftar unit konsol PlayStation.
    Seluruh kueri data ditangani oleh lapisan services.
    """
    consoles = get_all_consoles(app.config["DATABASE_NAME"])
    return render_template("daftar_konsol.html", consoles=consoles)


# Rute Tambah Konsol (Siklus 3: Form & Validasi Input)
@app.route("/consoles/tambah", methods=["GET", "POST"])
def tambah_konsol():
    """
    Form dan eksekusi penambahan unit konsol baru.
    Menerapkan validasi input dan pola Post-Redirect-Get (PRG).
    """
    errors = []
    data = {}

    if request.method == "POST":
        data = {
            "kode_konsol": request.form.get("kode_konsol", ""),
            "jenis_konsol": request.form.get("jenis_konsol", "PS4"),
        }

        success, errors, new_id = create_console(
            kode_konsol=data["kode_konsol"],
            jenis_konsol=data["jenis_konsol"],
            db_name=app.config["DATABASE_NAME"],
        )

        if success:
            flash(
                f"Unit konsol '{data['kode_konsol'].strip().upper()}' berhasil ditambahkan ke inventaris!",
                "success",
            )
            return redirect(url_for("daftar_konsol"))

    return render_template("tambah_konsol.html", errors=errors, data=data)


if __name__ == "__main__":
    init_db(app.config["DATABASE_NAME"])
    app.run(host="127.0.0.1", port=5000, debug=True)
