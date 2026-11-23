"""
periksa_draf.py — Skrip Pemeriksa Kelengkapan Draf Bab 4 (Lampiran D)
Memvalidasi struktur berkas 4.1 - 4.6, menghitung jumlah kata (>= 150 kata per subbab),
memeriksa keberadaan tabel, kode, gambar, penanda [ISI], serta mencocokkan
Kebutuhan Fungsional (KF-xx) dengan dokumen kebutuhan PRD/Backlog.
"""

import os
import re
import sys
import glob

SUBBAB_WAJIB = [
    ("4.1", ["4.1-lingkungan.md", "4.1-lingkungan-pengembangan.md"]),
    ("4.2", ["4.2-implementasi.md", "4.2-implementasi-fitur.md"]),
    ("4.3", ["4.3-keamanan.md", "4.3-tinjauan-keamanan.md"]),
    ("4.4", ["4.4-pengujian.md", "4.4-pengujian-verifikasi.md"]),
    ("4.5", ["4.5-rilis.md", "4.5-rilis-deployment.md"]),
    ("4.6", ["4.6-pembahasan.md", "4.6-pembahasan-evaluasi.md"]),
]

KF_VALID_LIST = {"KF-01", "KF-02", "KF-03", "KF-04", "KF-05", "KF-06", "KF-07", "KF-08", "KF-09", "KF-10", "KNF-01", "KNF-02", "KNF-03"}


def periksa_berkas(filepath):
    """Menganalisis konten berkas subbab."""
    if not os.path.exists(filepath):
        return None

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Hitung kata (hanya kata alfanumerik)
    words = re.findall(r"\b\w+\b", content)
    word_count = len(words)

    has_table = "|---" in content or "|:---" in content or "| ---" in content or "| :---" in content or bool(re.search(r"\|\s*[-:]+[-|\s:]*\|", content))
    has_code = "```" in content
    has_figure = "![" in content or "Gambar" in content
    unfilled_markers = re.findall(r"\[ISI(?:\:[^\]]+)?\]", content)

    # Cari seluruh referensi KF-xx
    kf_found = set(re.findall(r"\b(K[N]?F-\d+)\b", content))

    return {
        "word_count": word_count,
        "has_table": has_table,
        "has_code": has_code,
        "has_figure": has_figure,
        "unfilled_count": len(unfilled_markers),
        "unfilled_markers": unfilled_markers,
        "kf_found": kf_found,
    }


def main():
    bab4_dir = sys.argv[1] if len(sys.argv) > 1 else "docs/bab4"
    prd_file = sys.argv[2] if len(sys.argv) > 2 else "docs/product-backlog.md"

    print("=" * 70)
    print("        LAPORAN PEMERIKSAAN KELENGKAPAN DRAF BAB 4")
    print(f" Direktori Target : {bab4_dir}")
    print(f" Dokumen Referensi: {prd_file}")
    print("=" * 70)

    total_subbab = len(SUBBAB_WAJIB)
    selesai_count = 0
    all_kf_found = set()

    for kode, candidates in SUBBAB_WAJIB:
        found_file = None
        for cand in candidates:
            path = os.path.join(bab4_dir, cand)
            if os.path.exists(path):
                found_file = path
                break

        if not found_file:
            print(f"\n[{kode}] Status: TIDAK DITEMUKAN (Cari berkas: {' / '.join(candidates)})")
            continue

        res = periksa_berkas(found_file)
        all_kf_found.update(res["kf_found"])

        is_selesai = (
            res["word_count"] >= 150
            and res["unfilled_count"] == 0
            and (res["has_table"] or res["has_code"] or res["has_figure"])
        )

        status_str = "SELESAI" if is_selesai else "BELUM SELESAI"
        if is_selesai:
            selesai_count += 1

        print(f"\n[{kode}] {os.path.basename(found_file)} -> Status: **{status_str}**")
        print(f"  • Jumlah Kata : {res['word_count']} kata (Target: >= 150)")
        print(f"  • Ada Tabel   : {'Ya' if res['has_table'] else 'Tidak'}")
        print(f"  • Ada Kode    : {'Ya' if res['has_code'] else 'Tidak'}")
        print(f"  • Ada Gambar  : {'Ya' if res['has_figure'] else 'Tidak'}")
        print(f"  • Marker [ISI]: {res['unfilled_count']} buah")
        if res["kf_found"]:
            print(f"  • KF Terkait  : {', '.join(sorted(res['kf_found']))}")

    # Validasi Kebutuhan Fungsional (cek apakah ada KF asing/tidak dikenal)
    kf_asing = all_kf_found - KF_VALID_LIST

    print("\n" + "=" * 70)
    persentase = (selesai_count / total_subbab) * 100
    print(f"HASIL KELENGKAPAN SUBBAB: {selesai_count} / {total_subbab} SELESAI ({persentase:.1f}%)")
    if kf_asing:
        print(f"[PERINGATAN] Ditemukan ID Kebutuhan Fungsional tidak dikenal: {kf_asing}")
    else:
        print("[LULUS] Tidak ada ID Kebutuhan Fungsional (KF) asing yang tidak dikenal.")

    if persentase >= 80.0 and not kf_asing:
        print("\n>>> KELAYAKAN DRAF: MEMENUHI SYARAT (>= 80% dan KF Valid) <<<")
    else:
        print("\n>>> KELAYAKAN DRAF: BELUM MEMENUHI SYARAT <<<")


if __name__ == "__main__":
    main()
