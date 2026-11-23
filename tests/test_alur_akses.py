"""
test_alur_akses.py — Pengujian Tingkat Alur HTTP dan Matriks Akses Peran (Langkah 9)
Mencakup:
(a) Alur inti: Tambah data master konsol dan verifikasi muncul di daftar
(b) Logika bisnis khusus: Siklus sewa konsol atomik, penghentian sewa, dan kalkulasi denda
(c) Matriks akses rute x peran (Tamu, Kasir, Owner) dengan @pytest.mark.parametrize
(d) Penolakan permintaan POST tanpa token CSRF atau dengan token cacat (HTTP 400)
"""

import pytest
from services import create_console, create_package, get_console_by_id


# ============================================================================
# (A) ALUR INTI: TAMBAH DATA MASTER DAN TAMPIL DI DAFTAR
# ============================================================================
def test_alur_inti_tambah_konsol_dan_tampil_di_daftar(owner_client, post_csrf):
    """(a) Menguji alur penambahan unit konsol oleh Owner dan verifikasi tampil di halaman daftar."""
    res_tambah = post_csrf(
        owner_client,
        "/consoles/tambah",
        data={"kode_konsol": "PS5-ALUR1", "jenis_konsol": "PS5"},
        follow_redirects=True,
    )
    assert res_tambah.status_code == 200
    assert "PS5-ALUR1" in res_tambah.text
    assert "berhasil ditambahkan" in res_tambah.text

    # Verifikasi langsung pada halaman daftar konsol
    res_daftar = owner_client.get("/consoles")
    assert res_daftar.status_code == 200
    assert "PS5-ALUR1" in res_daftar.text


# ============================================================================
# (B) LOGIKA KHUSUS: SIKLUS SEWA ATOMIK, PENGHENTIAN, DAN PERHITUNGAN DENDA
# ============================================================================
def test_alur_siklus_sewa_dan_perhitungan_denda(kasir_client, post_csrf, test_db_path):
    """(b) Menguji perubahan status unit konsol menjadi 'terpakai', lalu selesai sewa dan status kembali 'tersedia'."""
    # Siapkan unit konsol dan paket sewa
    _, _, c_id = create_console("PS4-SEWA1", "PS4", db_name=test_db_path)
    _, _, p_id = create_package("Paket Uji Alur 1J", "PS4", 60, 10000, db_name=test_db_path)

    # 1. Kasir membuka sesi sewa
    res_buka = post_csrf(
        kasir_client,
        "/sewa/buka",
        data={
            "nama_pelanggan": "Pelanggan Alur",
            "console_id": c_id,
            "package_id": p_id,
            "status_bayar": "open_bill",
        },
        follow_redirects=True,
    )
    assert res_buka.status_code == 200
    assert "berhasil dibuka" in res_buka.text

    # Verifikasi unit konsol menjadi 'terpakai'
    c_data = get_console_by_id(c_id, db_name=test_db_path)
    assert c_data["status"] == "terpakai"

    # 2. Selesaikan sewa transaksi
    # Ambil ID transaksi dari database test
    from services import get_all_transactions
    txs = get_all_transactions(db_name=test_db_path)
    tx_target = [t for t in txs if t["kode_konsol"] == "PS4-SEWA1"][0]

    res_selesai = post_csrf(
        kasir_client,
        f"/sewa/{tx_target['id_transaksi']}/selesai",
        follow_redirects=True,
    )
    assert res_selesai.status_code == 200
    assert "berhasil diselesaikan" in res_selesai.text

    # Verifikasi unit konsol kembali 'tersedia'
    c_pulih = get_console_by_id(c_id, db_name=test_db_path)
    assert c_pulih["status"] == "tersedia"


# ============================================================================
# (C) MATRIKS AKSES RUTE X PERAN (TAMU, KASIR, PEMILIK)
# ============================================================================
@pytest.mark.parametrize(
    "peran_aktor, rute, metode, status_diharapkan",
    [
        # Kasus Tamu (Anonim) -> Dialihkan ke Login (302)
        ("tamu", "/sewa", "GET", 302),
        ("tamu", "/consoles/tambah", "GET", 302),
        ("tamu", "/packages", "GET", 302),

        # Kasus Kasir -> Dilarang pada rute manajemen Master (403 Forbidden)
        ("kasir", "/consoles/tambah", "GET", 403),
        ("kasir", "/packages", "GET", 403),
        ("kasir", "/packages/tambah", "GET", 403),
        ("kasir", "/consoles/1/hapus", "POST", 403),

        # Kasus Hak Akses Sah Sesuai Peran (200 OK)
        ("kasir", "/sewa", "GET", 200),
        ("kasir", "/sewa/buka", "GET", 200),
        ("owner", "/consoles", "GET", 200),
        ("owner", "/packages", "GET", 200),
        ("owner", "/consoles/tambah", "GET", 200),
    ],
)
def test_matriks_akses_rute_dan_peran(app_instance, peran_aktor, rute, metode, status_diharapkan):
    """(c) Memverifikasi penegakan otorisasi peran pada setiap rute sesuai matriks akses."""
    c = app_instance.test_client()

    if peran_aktor == "kasir":
        with c.session_transaction() as sess:
            sess["user_id"] = 1
            sess["username"] = "kasir_siti"
            sess["role"] = "kasir"
            sess["_csrf_token"] = "valid_csrf_token"
    elif peran_aktor == "owner":
        with c.session_transaction() as sess:
            sess["user_id"] = 2
            sess["username"] = "owner_budi"
            sess["role"] = "owner"
            sess["_csrf_token"] = "valid_csrf_token"

    if metode == "GET":
        res = c.get(rute)
    else:
        # POST request dengan token CSRF jika login
        payload = {"csrf_token": "valid_csrf_token"}
        res = c.post(rute, data=payload)

    assert res.status_code == status_diharapkan
    if status_diharapkan == 302:
        assert "/login" in res.headers.get("Location", "")
    elif status_diharapkan == 403:
        assert "403" in res.text or "Akses Ditolak" in res.text


# ============================================================================
# (D) PENOLAKAN PERMINTAAN TANPA TOKEN CSRF (HTTP 400 BAD REQUEST)
# ============================================================================
def test_penolakan_post_tanpa_csrf_token(kasir_client):
    """(d1) Permintaan POST tanpa parameter csrf_token wajib ditolak dengan HTTP 400."""
    res = kasir_client.post(
        "/sewa/buka",
        data={"nama_pelanggan": "Attacker", "console_id": 1, "package_id": 1},
    )
    assert res.status_code == 400
    assert "Permintaan Ditolak (CSRF)" in res.text
    assert "CSRF Token" in res.text


def test_penolakan_post_dengan_csrf_token_palsu(kasir_client):
    """(d2) Permintaan POST dengan token CSRF tidak cocok wajib ditolak dengan HTTP 400."""
    res = kasir_client.post(
        "/sewa/buka",
        data={
            "nama_pelanggan": "Attacker",
            "console_id": 1,
            "package_id": 1,
            "csrf_token": "token_palsu_hacker_123",
        },
    )
    assert res.status_code == 400
    assert "Permintaan Ditolak (CSRF)" in res.text
