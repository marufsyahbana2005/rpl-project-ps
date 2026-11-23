"""
test_rilis.py — Uji Otomatis Kesiapan Rilis Produksi (Jobsheet 14 / Lampiran C.4)
Memverifikasi nomor versi SemVer, tampilan footer, skrip pencadangan SQLite,
dukungan variabel TOKO_DB, dan penolakan start tanpa SECRET_KEY di mode produksi.
"""

import os
import re
import sqlite3
import subprocess
import pytest
from versi import __version__
from cadangkan import backup_database


def test_versi_semver():
    """Memverifikasi bahwa versi aplikasi mengikuti kaidah Semantic Versioning (x.y.z)."""
    assert isinstance(__version__, str)
    assert re.match(r"^\d+\.\d+\.\d+$", __version__) is not None
    assert __version__ == "1.0.0"


def test_tampilan_versi_pada_footer(client):
    """Memverifikasi bahwa nomor versi aplikasi tampil di footer halaman HTML."""
    res = client.get("/login")
    assert res.status_code == 200
    assert f"v{__version__}" in res.text


def test_skrip_cadangkan_database(test_db_path, tmp_path):
    """Memverifikasi bahwa fungsi backup_database menghasilkan berkas SQLite valid."""
    backup_dir = str(tmp_path / "backup_test")
    backup_file = backup_database(source_db=test_db_path, backup_dir=backup_dir)

    assert os.path.exists(backup_file)
    assert os.path.getsize(backup_file) > 0

    # Pastikan file hasil cadangan dapat dibuka sebagai SQLite yang valid
    conn = sqlite3.connect(backup_file)
    try:
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        table_names = [t[0] for t in tables]
        assert "consoles" in table_names
        assert "packages" in table_names
        assert "transactions" in table_names
    finally:
        conn.close()


def test_toko_db_env_variable(monkeypatch, tmp_path):
    """Memverifikasi bahwa variabel lingkungan TOKO_DB dihormati oleh models."""
    custom_db = str(tmp_path / "custom_toko.db")
    monkeypatch.setenv("TOKO_DB", custom_db)

    # Impor ulang models dalam konteks environment baru
    import importlib
    import models
    importlib.reload(models)

    assert models.DATABASE_NAME == custom_db


def test_produksi_menolak_start_tanpa_secret_key(monkeypatch):
    """Memverifikasi bahwa startup aplikasi gagal jika APP_ENV=production dan SECRET_KEY kosong."""
    import importlib
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.delenv("SECRET_KEY", raising=False)

    with pytest.raises(RuntimeError) as exc_info:
        import app
        importlib.reload(app)

    assert "tanpa variabel lingkungan SECRET_KEY" in str(exc_info.value)
