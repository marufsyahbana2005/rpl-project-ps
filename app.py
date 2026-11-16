"""
app.py — Titik Masuk Utama Aplikasi Web Flask Exito Playbox
Mengelola inisialisasi aplikasi, routing antarmuka, dan penanganan permintaan HTTP.
Mencakup modul entitas pertama (consoles) dan entitas kedua (packages).
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
    get_all_packages,
    create_package,
    get_package_by_id,
    update_package,
    delete_package,
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
    return redirect(url_for("daftar_konsol"))


# ============================================================================
# RUTE ENTITAS PERTAMA: CONSOLES (UNIT KONSOL)
# ============================================================================

@app.route("/consoles")
def daftar_konsol():
    consoles = get_all_consoles(app.config["DATABASE_NAME"])
    return render_template("daftar_konsol.html", consoles=consoles)


@app.route("/consoles/tambah", methods=["GET", "POST"])
def tambah_konsol():
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


@app.route("/consoles/<int:id>/ubah", methods=["GET", "POST"])
def ubah_konsol(id):
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


@app.route("/consoles/<int:id>/hapus", methods=["POST"])
def hapus_konsol(id):
    success, message, status_code = delete_console(
        id, app.config["DATABASE_NAME"]
    )
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    return redirect(url_for("daftar_konsol"))


# ============================================================================
# RUTE ENTITAS KEDUA: PACKAGES (PAKET SEWA RENTAL) — LANGKAH 14
# ============================================================================

@app.route("/packages")
def daftar_paket():
    packages = get_all_packages(app.config["DATABASE_NAME"])
    return render_template("daftar_paket.html", packages=packages)


@app.route("/packages/tambah", methods=["GET", "POST"])
def tambah_paket():
    errors = []
    data = {}

    if request.method == "POST":
        data = {
            "nama_paket": request.form.get("nama_paket", ""),
            "jenis_konsol": request.form.get("jenis_konsol", "PS4"),
            "durasi_menit": request.form.get("durasi_menit", ""),
            "harga": request.form.get("harga", ""),
            "is_active": 1 if request.form.get("is_active") == "1" else 0,
        }

        success, errors, new_id = create_package(
            nama_paket=data["nama_paket"],
            jenis_konsol=data["jenis_konsol"],
            durasi_menit=data["durasi_menit"],
            harga=data["harga"],
            is_active=data["is_active"],
            db_name=app.config["DATABASE_NAME"],
        )

        if success:
            flash(
                f"Paket sewa '{data['nama_paket'].strip()}' berhasil ditambahkan!",
                "success",
            )
            return redirect(url_for("daftar_paket"))

    return render_template("tambah_paket.html", errors=errors, data=data)


@app.route("/packages/<int:id>/ubah", methods=["GET", "POST"])
def ubah_paket(id):
    package = get_package_by_id(id, app.config["DATABASE_NAME"])
    if not package:
        return (
            render_template(
                "404.html",
                message=f"Paket sewa dengan ID #{id} tidak ditemukan.",
            ),
            404,
        )

    errors = []
    if request.method == "POST":
        nama_paket = request.form.get("nama_paket", "")
        jenis_konsol = request.form.get("jenis_konsol", "")
        durasi_menit = request.form.get("durasi_menit", "")
        harga = request.form.get("harga", "")
        is_active = 1 if request.form.get("is_active") == "1" else 0

        success, errors, status_code = update_package(
            package_id=id,
            nama_paket=nama_paket,
            jenis_konsol=jenis_konsol,
            durasi_menit=durasi_menit,
            harga=harga,
            is_active=is_active,
            db_name=app.config["DATABASE_NAME"],
        )

        if success:
            flash(
                f"Paket sewa '{nama_paket.strip()}' berhasil diperbarui!",
                "success",
            )
            return redirect(url_for("daftar_paket"))

        form_data = {
            "id": id,
            "nama_paket": nama_paket,
            "jenis_konsol": jenis_konsol,
            "durasi_menit": durasi_menit,
            "harga": harga,
            "is_active": is_active,
        }
        return (
            render_template(
                "ubah_paket.html", package=form_data, errors=errors
            ),
            status_code,
        )

    return render_template("ubah_paket.html", package=package, errors=errors)


@app.route("/packages/<int:id>/hapus", methods=["POST"])
def hapus_paket(id):
    success, message, status_code = delete_package(
        id, app.config["DATABASE_NAME"]
    )
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    return redirect(url_for("daftar_paket"))


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
