"""
app.py — Titik Masuk Utama Aplikasi Web Flask Exito Playbox
Mengelola inisialisasi aplikasi, routing antarmuka, dan penanganan permintaan HTTP.
Mencakup:
- Entitas Pertama: consoles (Unit Konsol)
- Entitas Kedua: packages (Paket Sewa)
- Entitas Berelasi & Transaksi: transactions (Sesi Sewa Konsol) — Jobsheet 10
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
    get_available_consoles,
    get_all_packages,
    create_package,
    get_package_by_id,
    update_package,
    delete_package,
    get_active_packages,
    get_all_transactions,
    get_transaction_by_id,
    create_transaction,
    finish_transaction,
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
# 1. RUTE ENTITAS PERTAMA: CONSOLES (UNIT KONSOL)
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
# 2. RUTE ENTITAS KEDUA: PACKAGES (PAKET SEWA RENTAL)
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


# ============================================================================
# 3. RUTE ENTITAS BERELASI: TRANSACTIONS (SESI SEWA KONSOL) — JOBSHEET 10
# ============================================================================

@app.route("/sewa")
def daftar_sewa():
    """
    Langkah 3 (Siklus 1): Daftar Transaksi Sewa dengan JOIN ke consoles & packages.
    Langkah 9 & 10: Pencarian (q) dan Penyaringan (status_bayar, jenis_konsol).
    """
    query_q = request.args.get("q", "").strip()
    filter_status = request.args.get("status_bayar", "").strip()
    filter_jenis = request.args.get("jenis_konsol", "").strip()

    transactions = get_all_transactions(
        q=query_q,
        status_bayar=filter_status,
        jenis_konsol=filter_jenis,
        db_name=app.config["DATABASE_NAME"],
    )

    return render_template(
        "daftar_sewa.html",
        transactions=transactions,
        query_q=query_q,
        filter_status=filter_status,
        filter_jenis=filter_jenis,
    )


@app.route("/sewa/buka", methods=["GET", "POST"])
def buka_sewa():
    """
    Langkah 4 & 5 (Siklus 2 & 3): Form Tambah dengan Pilihan Induk & Transaksi Atomik Multi-Tabel.
    """
    errors = []
    data = {}

    if request.method == "POST":
        data = {
            "nama_pelanggan": request.form.get("nama_pelanggan", ""),
            "console_id": request.form.get("console_id", ""),
            "package_id": request.form.get("package_id", ""),
            "status_bayar": request.form.get("status_bayar", "open_bill"),
        }

        success, errors, new_trx_id = create_transaction(
            nama_pelanggan=data["nama_pelanggan"],
            console_id=data["console_id"],
            package_id=data["package_id"],
            status_bayar=data["status_bayar"],
            user_id=1,  # Kasir aktif default
            db_name=app.config["DATABASE_NAME"],
        )

        if success:
            flash(
                f"Sesi sewa untuk '{data['nama_pelanggan'].strip()}' berhasil dibuka! Unit konsol kini berstatus TERPAKAI.",
                "success",
            )
            return redirect(url_for("daftar_sewa"))

    available_consoles = get_available_consoles(app.config["DATABASE_NAME"])
    active_packages = get_active_packages(app.config["DATABASE_NAME"])

    return render_template(
        "buka_sewa.html",
        errors=errors,
        data=data,
        available_consoles=available_consoles,
        active_packages=active_packages,
    )


@app.route("/sewa/<int:id>/selesai", methods=["POST"])
def selesaikan_sewa(id):
    """
    Tugas Lanjutan (Langkah 16): Penghentian Sesi Sewa Kasir.
    Mengubah status transaksi menjadi lunas, konsol menjadi tersedia,
    dan mencatat denda keterlambatan jika ada.
    """
    success, message, status_code = finish_transaction(
        transaction_id=id,
        db_name=app.config["DATABASE_NAME"],
    )
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    return redirect(url_for("daftar_sewa"))


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
