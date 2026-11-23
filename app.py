"""
app.py — Titik Masuk Utama Aplikasi Web Flask Exito Playbox
Mengelola inisialisasi aplikasi, routing antarmuka, dan penanganan permintaan HTTP.
Mencakup:
- Entitas Pertama: consoles (Unit Konsol)
- Entitas Kedua: packages (Paket Sewa)
- Entitas Berelasi & Transaksi: transactions (Sesi Sewa Konsol) — Jobsheet 10
"""

import os
from functools import wraps
from flask import Flask, redirect, url_for, render_template, request, flash, session
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
    create_user,
    authenticate_user,
    get_user_by_id,
    get_user_by_username,
)

# Inisialisasi Aplikasi Flask
app = Flask(__name__)

# Konfigurasi Kunci Rahasia dari Variabel Lingkungan
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "exito-playbox-dev-secret-key-2026-rentalsecure"
)
app.config["DATABASE_NAME"] = os.environ.get("DATABASE_NAME", "rental.db")


# ============================================================================
# HELPER AUTENTIKASI, KEAMANAN REDIRECT, & DECORATOR OTORISASI (JOBSHEET 11)
# ============================================================================

def is_safe_url(target):
    """
    Langkah 4 (Siklus 2): Memastikan parameter next hanya mengarah ke rute internal.
    Hanya diterima bila dimulai '/' dan bukan '//' atau '/\\'.
    Mencegah celah Open Redirect ke domain luar situs.
    """
    if not target:
        return False
    if target.startswith("/") and not target.startswith("//") and not target.startswith("/\\"):
        return True
    return False


def login_diperlukan(f):
    """
    Langkah 5 (Siklus 3): Pengaman rute untuk mewajibkan login.
    Mengarahkan tamu yang belum login ke /login?next=<rute_tujuan>.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            next_url = request.full_path if request.query_string else request.path
            if next_url.endswith("?"):
                next_url = next_url[:-1]
            return redirect(url_for("login", next=next_url))
        return f(*args, **kwargs)
    return decorated_function


def peran_diperlukan(*peran_diizinkan):
    """
    Langkah 5 (Siklus 3): Decorator otorisasi berbasis peran (RBAC).
    - Jika tamu -> dialihkan ke login dengan query next.
    - Jika peran pengguna tidak ada dalam daftar peran_diizinkan -> mengembalikan HTTP 403 Forbidden.
    Berlaku seragam untuk permintaan GET maupun POST.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get("user_id"):
                next_url = request.full_path if request.query_string else request.path
                if next_url.endswith("?"):
                    next_url = next_url[:-1]
                return redirect(url_for("login", next=next_url))
            user_role = session.get("role")
            if user_role not in peran_diizinkan:
                return (
                    render_template(
                        "403.html",
                        message=f"Peran Anda saat ini ('{user_role}') tidak memiliki izin otorisasi untuk mengakses fitur ini.",
                    ),
                    403,
                )
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.context_processor
def inject_user_context():
    """
    Menyuntikkan identitas dan peran pengguna aktif ke semua templat Jinja2.
    """
    return {
        "current_user_id": session.get("user_id"),
        "current_username": session.get("username"),
        "current_role": session.get("role"),
    }


# ============================================================================
# RUTE AUTENTIKASI: LOGIN & LOGOUT (JOBSHEET 11)
# ============================================================================

@app.route("/")
def index():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    return redirect(url_for("daftar_sewa"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Langkah 4 (Siklus 2): Halaman dan aksi masuk sistem.
    - Menolak user enumeration (pesan galat netral identik).
    - session.clear() sebelum sesi diisi.
    - Memvalidasi parameter next (anti open-redirect).
    """
    if session.get("user_id"):
        return redirect(url_for("daftar_sewa"))

    next_page = request.args.get("next") or request.form.get("next") or ""
    error = None
    username = ""

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user, error_msg = authenticate_user(
            username=username,
            password=password,
            db_name=app.config["DATABASE_NAME"],
        )

        if user:
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]

            flash(
                f"Selamat datang kembali, {user['username']}! Anda berhasil masuk sebagai {user['role'].upper()}.",
                "success",
            )

            if is_safe_url(next_page):
                return redirect(next_page)
            return redirect(url_for("daftar_sewa"))
        else:
            error = error_msg

    return render_template(
        "login.html", error=error, username=username, next_page=next_page
    )


@app.route("/logout", methods=["POST"])
def logout():
    """
    Langkah 4 (Siklus 2): Aksi keluar sistem.
    Hanya menerima metode POST guna mencegah serangan logout paksa via CSRF pre-fetch.
    """
    session.clear()
    flash("Anda telah keluar dari sistem secara aman.", "info")
    return redirect(url_for("login"))


# ============================================================================
# 1. RUTE ENTITAS PERTAMA: CONSOLES (UNIT KONSOL)
# ============================================================================

@app.route("/consoles")
@login_diperlukan
def daftar_konsol():
    consoles = get_all_consoles(app.config["DATABASE_NAME"])
    return render_template("daftar_konsol.html", consoles=consoles)


@app.route("/consoles/tambah", methods=["GET", "POST"])
@peran_diperlukan("owner")
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
@peran_diperlukan("owner")
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
@peran_diperlukan("owner")
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
@peran_diperlukan("owner")
def daftar_paket():
    packages = get_all_packages(app.config["DATABASE_NAME"])
    return render_template("daftar_paket.html", packages=packages)


@app.route("/packages/tambah", methods=["GET", "POST"])
@peran_diperlukan("owner")
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
@peran_diperlukan("owner")
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
@peran_diperlukan("owner")
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
@login_diperlukan
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
@login_diperlukan
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

        # Gunakan ID kasir yang sedang login di sesi
        aktif_user_id = session.get("user_id", 1)

        success, errors, new_trx_id = create_transaction(
            nama_pelanggan=data["nama_pelanggan"],
            console_id=data["console_id"],
            package_id=data["package_id"],
            status_bayar=data["status_bayar"],
            user_id=aktif_user_id,
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
@login_diperlukan
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


# Penangan Galat 403 Forbidden
@app.errorhandler(403)
def forbidden_error(e):
    return (
        render_template(
            "403.html",
            message="Akses Ditolak: Anda tidak memiliki izin otorisasi untuk membuka rute ini.",
        ),
        403,
    )


# Penangan Galat 404 Not Found
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
