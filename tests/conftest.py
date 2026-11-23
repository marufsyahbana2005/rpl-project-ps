"""
conftest.py — Konfigurasi Fixture Pytest untuk Pengujian Exito Playbox (Jobsheet 13)
Menyediakan basis data sementara, akun uji (kasir & owner), dan helper pengiriman token CSRF.
"""

import os
import sys
import tempfile
import pytest

# Pastikan path modul induk dapat diimpor
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from models import init_db
from services import create_user, create_console, create_package


@pytest.fixture(scope="session")
def test_db_path():
    """Membuat jalur basis data sementara yang terisolasi untuk sesi pengujian."""
    temp_dir = tempfile.gettempdir()
    db_path = os.path.join(temp_dir, "exito_pytest_temp.db")
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except Exception:
            pass

    # Inisialisasi skema tabel lengkap
    init_db(db_path)

    # Seed data pengguna uji
    create_user("kasir_siti", "KasirSiti#2026", "kasir", db_name=db_path)
    create_user("owner_budi", "OwnerBudi#2026", "owner", db_name=db_path)

    yield db_path

    # Pembersihan setelah seluruh sesi uji selesai
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except Exception:
            pass


@pytest.fixture
def app_instance(test_db_path):
    """Mengembalikan instance Flask yang dikonfigurasi untuk pengujian."""
    app.config["TESTING"] = True
    app.config["DATABASE_NAME"] = test_db_path
    app.config["WTF_CSRF_ENABLED"] = False
    return app


@pytest.fixture
def client(app_instance):
    """Klien pengujian Flask untuk pengguna anonim (tamu)."""
    return app_instance.test_client()


@pytest.fixture
def post_csrf():
    """Helper untuk mengirim permintaan POST lengkap dengan token CSRF."""
    def _post(c, url, data=None, **kwargs):
        payload = dict(data or {})
        with c.session_transaction() as sess:
            if "_csrf_token" not in sess:
                sess["_csrf_token"] = "pytest_secure_token_12345"
            token = sess["_csrf_token"]
        payload["csrf_token"] = token
        return c.post(url, data=payload, **kwargs)
    return _post


@pytest.fixture
def kasir_client(app_instance):
    """Klien pengujian Flask yang telah masuk sebagai peran kasir."""
    c = app_instance.test_client()
    with c.session_transaction() as sess:
        sess["user_id"] = 1
        sess["username"] = "kasir_siti"
        sess["role"] = "kasir"
        sess["_csrf_token"] = "pytest_secure_token_12345"
    return c


@pytest.fixture
def owner_client(app_instance):
    """Klien pengujian Flask yang telah masuk sebagai peran owner."""
    c = app_instance.test_client()
    with c.session_transaction() as sess:
        sess["user_id"] = 2
        sess["username"] = "owner_budi"
        sess["role"] = "owner"
        sess["_csrf_token"] = "pytest_secure_token_12345"
    return c
