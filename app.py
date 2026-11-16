"""
app.py — Titik Masuk Utama Aplikasi Web Flask Exito Playbox
Mengelola inisialisasi aplikasi, routing antarmuka, dan penanganan permintaan HTTP.
"""

import os
from flask import Flask, redirect, url_for, render_template, request, flash
from models import init_db
from services import (
    get_all_consoles,
    create_console,
    get_console_by_id,
    update_console,
    delete_console,
)

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


# Rute Ubah Konsol (Siklus 4: Form Ubah & Validasi)
@app.route("/consoles/<int:id>/ubah", methods=["GET", "POST"])
def ubah_konsol(id):
    """
    Form dan penanganan pembaruan data unit konsol (F4).
    Jika ID tidak ditemukan, menghasilkan respons 404 Not Found.
    """
    console = get_console_by_id(id, app.config["DATABASE_NAME"])
    if not console:
        return (
            render_template(
                "404.html",
                message=f"Unit konsol dengan ID #{id} tidak ditemukan di sistem.",
            ),
            404,
        )

    errors = []
    if request.method == "POST":
        kode_konsol = request.form.get("kode_konsol", "")
        jenis_konsol = request.form.get("jenis_konsol", "")
        status = request.form.get("status", "tersedia")

        success, errors, status_code = update_console(
            console_id=id,
            kode_konsol=kode_konsol,
            jenis_konsol=jenis_konsol,
            status=status,
            db_name=app.config["DATABASE_NAME"],
        )

        if success:
            flash(
                f"Data unit konsol '{kode_konsol.strip().upper()}' berhasil diperbarui!",
                "success",
            )
            return redirect(url_for("daftar_konsol"))

        # Jika terdapat galat, kembalikan data yang diketik kasir
        form_data = {
            "id": id,
            "kode_konsol": kode_konsol,
            "jenis_konsol": jenis_konsol,
            "status": status,
        }
        return (
            render_template(
                "ubah_konsol.html", console=form_data, errors=errors
            ),
            status_code,
        )

    return render_template("ubah_konsol.html", console=console, errors=errors)


# Rute Hapus Konsol (Siklus 5: Proteksi POST & Foreign Key)
@app.route("/consoles/<int:id>/hapus", methods=["POST"])
def hapus_konsol(id):
    """
    Eksekusi penghapusan unit konsol (F5).
    Hanya menerima metode POST. Jika unit memiliki riwayat transaksi sewa,
    penghapusan ditolak tanpa menyebabkan crash aplikasi.
    """
    success, message, status_code = delete_console(
        id, app.config["DATABASE_NAME"]
    )
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    return redirect(url_for("daftar_konsol"))


# Penangan Galat 404
@app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html",
            message="Halaman atau entitas data yang Anda tuju tidak ditemukan.",
        ),
        404,
    )


if __name__ == "__main__":
    init_db(app.config["DATABASE_NAME"])
    app.run(host="127.0.0.1", port=5000, debug=True)
