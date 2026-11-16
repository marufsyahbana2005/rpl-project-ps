"""
app.py — Titik Masuk Utama Aplikasi Web Flask Exito Playbox
Mengelola inisialisasi aplikasi, routing antarmuka, dan penanganan permintaan HTTP.
"""

import os
from flask import Flask, redirect, url_for, render_template, request, flash
from models import init_db
from services import get_all_consoles

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


# Rute Tambah Konsol (Placeholder Kerangka Awal)
@app.route("/consoles/tambah", methods=["GET", "POST"])
def tambah_konsol():
    """
    Form penambahan unit konsol baru.
    """
    return render_template("tambah_konsol.html", errors=[], data={})


if __name__ == "__main__":
    # Inisialisasi basis data dari schema.sql saat aplikasi pertama kali dijalankan
    init_db(app.config["DATABASE_NAME"])
    # Jalankan server pengembangan Flask
    app.run(host="127.0.0.1", port=5000, debug=True)
