"""
analisis_jurnal.py — Skrip Rekapitulasi & Analisis Jurnal Vibe Coding (Lampiran C)
Membaca satu atau lebih berkas jurnal markdown, mem-parsing entri tabel,
menghitung proporsi keputusan (Terima/Ubah/Tolak), mengidentifikasi tag galat AI,
dan menyusun ringkasan dampak waktu.
"""

import os
import re
import sys
import glob


def parse_jurnal_file(filepath):
    """Mem-parsing berkas jurnal markdown dan mengembalikan daftar entri."""
    entries = []
    if not os.path.exists(filepath):
        print(f"[PERINGATAN] Berkas tidak ditemukan: {filepath}")
        return entries

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    in_table = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            parts = [p.strip() for p in stripped.split("|")[1:-1]]
            if len(parts) >= 7:
                # Cek apakah header atau separator
                if parts[0].lower() in ("no", ":--:", "---", "-"):
                    continue
                if re.match(r"^\**\d+\**$", parts[0]):
                    no_clean = parts[0].replace("*", "").strip()
                    waktu = parts[1]
                    siklus = parts[2]
                    prompt = parts[3]
                    hasil = parts[4]
                    keputusan_raw = parts[5].replace("*", "").strip()
                    refleksi = parts[6]

                    # Standardisasi Keputusan
                    keputusan = "Lainnya"
                    if "terima" in keputusan_raw.lower():
                        keputusan = "Terima"
                    elif "ubah" in keputusan_raw.lower():
                        keputusan = "Ubah"
                    elif "tolak" in keputusan_raw.lower():
                        keputusan = "Tolak"

                    # Ekstraksi Tag Galat AI: [Galat: <kategori>]
                    galat_match = re.findall(r"\[Galat:\s*([^\]]+)\]", refleksi, re.IGNORECASE)
                    tag_galat = [g.strip().lower() for g in galat_match]

                    entries.append({
                        "file": os.path.basename(filepath),
                        "no": int(no_clean),
                        "waktu": waktu,
                        "siklus": siklus,
                        "prompt": prompt,
                        "hasil": hasil,
                        "keputusan": keputusan,
                        "keputusan_raw": keputusan_raw,
                        "refleksi": refleksi,
                        "tag_galat": tag_galat,
                    })
    return entries


def analisis_rekap(entries):
    """Menghitung agregasi statistik keputusan dan jenis galat."""
    total = len(entries)
    if total == 0:
        return None

    counts = {"Terima": 0, "Ubah": 0, "Tolak": 0, "Lainnya": 0}
    galat_counts = {}

    for e in entries:
        counts[e["keputusan"]] = counts.get(e["keputusan"], 0) + 1
        for g in e["tag_galat"]:
            galat_counts[g] = galat_counts.get(g, 0) + 1

    return {
        "total": total,
        "counts": counts,
        "persen": {k: (v / total * 100) for k, v in counts.items()},
        "galat_counts": galat_counts,
    }


def main():
    args = sys.argv[1:]
    if not args:
        # Default: cari di jurnal/*.md dan jurnal-vibe-coding.md
        files = glob.glob("jurnal/*.md")
        if not files and os.path.exists("jurnal-vibe-coding.md"):
            files = ["jurnal-vibe-coding.md"]
    else:
        files = []
        for a in args:
            files.extend(glob.glob(a))

    if not files:
        print("[GALAT] Tidak ada berkas jurnal yang cocok ditemukan.")
        sys.exit(1)

    print("=" * 70)
    print("      HASIL ANALISIS REKAPITULASI JURNAL VIBE CODING")
    print("=" * 70)

    semua_entri = []
    for f in sorted(files):
        e = parse_jurnal_file(f)
        semua_entri.extend(e)
        stat = analisis_rekap(e)
        if stat:
            print(f"\n[Berkas: {os.path.basename(f)}]")
            print(f"Total Entri: {stat['total']}")
            print(f"• Terima : {stat['counts']['Terima']} ({stat['persen']['Terima']:.1f}%)")
            print(f"• Ubah   : {stat['counts']['Ubah']} ({stat['persen']['Ubah']:.1f}%)")
            print(f"• Tolak  : {stat['counts']['Tolak']} ({stat['persen']['Tolak']:.1f}%)")
            if stat["galat_counts"]:
                print("Distribusi Tag Galat AI:")
                for k, v in sorted(stat["galat_counts"].items()):
                    print(f"  - [Galat: {k}]: {v} kali")

    if len(files) > 1:
        total_stat = analisis_rekap(semua_entri)
        print("\n" + "=" * 70)
        print("          REKAPITULASI GABUNGAN SELURUH BERKAS JURNAL")
        print("=" * 70)
        print(f"Total Seluruh Entri: {total_stat['total']}")
        print(f"• Terima : {total_stat['counts']['Terima']} ({total_stat['persen']['Terima']:.1f}%)")
        print(f"• Ubah   : {total_stat['counts']['Ubah']} ({total_stat['persen']['Ubah']:.1f}%)")
        print(f"• Tolak  : {total_stat['counts']['Tolak']} ({total_stat['persen']['Tolak']:.1f}%)")
        if total_stat["galat_counts"]:
            print("Distribusi Tag Galat AI Gabungan:")
            for k, v in sorted(total_stat["galat_counts"].items()):
                print(f"  - [Galat: {k}]: {v} kali")

    print("\n[OK] Pemindaian selesai tanpa galat parsing format.")


if __name__ == "__main__":
    main()
