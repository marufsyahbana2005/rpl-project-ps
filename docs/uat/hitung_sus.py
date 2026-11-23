"""
hitung_sus.py — Skrip Perhitungan Skor System Usability Scale (SUS) (Lampiran F.3)
Menghitung skor baku SUS dari 10 pertanyaan skala Likert 1-5.
Aturan:
- Pertanyaan bernomor ganjil (1, 3, 5, 7, 9): kontribusi skor = nilai - 1
- Pertanyaan bernomor genap (2, 4, 6, 8, 10): kontribusi skor = 5 - nilai
- Skor SUS total = jumlah kontribusi skor * 2.5 (rentang 0 - 100)
"""

def hitung_skor_sus(jawaban_list):
    """
    Menghitung skor SUS dari daftar 10 jawaban [q1, q2, ..., q10].
    """
    if len(jawaban_list) != 10:
        raise ValueError("Kuesioner SUS harus memuat tepat 10 jawaban pertanyaan.")

    kontribusi = []
    for i, skor in enumerate(jawaban_list):
        if not (1 <= skor <= 5):
            raise ValueError(f"Nilai jawaban pertanyaan {i+1} harus dalam rentang 1-5.")
        if (i + 1) % 2 != 0:
            # Ganjil: skor - 1
            kontribusi.append(skor - 1)
        else:
            # Genap: 5 - skor
            kontribusi.append(5 - skor)

    skor_total = sum(kontribusi) * 2.5
    return skor_total


def tentukan_grade_sus(skor):
    """Menentukan predikat kelayakan sistem berdasarkan skor SUS."""
    if skor >= 85.0:
        return "Grade A+ (Sangat Unggul / Best Imaginable)"
    elif skor >= 80.3:
        return "Grade A (Unggul / Excellent)"
    elif skor >= 68.0:
        return "Grade B / C (Dapat Diterima / Good - Above Average)"
    elif skor >= 51.0:
        return "Grade D (Cukup / Marginal)"
    else:
        return "Grade F (Tidak Dapat Diterima / Unacceptable)"


if __name__ == "__main__":
    # Data pengisian aktual UAT Exito Playbox
    # Responden 1: Bpk. Hendra Gunawan (Pemilik Rental)
    jawaban_owner = [5, 1, 4, 2, 5, 1, 5, 1, 4, 2]
    # Responden 2: Rian Pratama (Kasir Rental)
    jawaban_kasir = [4, 1, 5, 2, 4, 1, 5, 2, 4, 2]

    skor_owner = hitung_skor_sus(jawaban_owner)
    skor_kasir = hitung_skor_sus(jawaban_kasir)
    rata_rata = (skor_owner + skor_kasir) / 2

    print(f"Skor SUS Pemilik (Bpk. Hendra): {skor_owner:.1f} -> {tentukan_grade_sus(skor_owner)}")
    print(f"Skor SUS Kasir (Rian Pratama): {skor_kasir:.1f} -> {tentukan_grade_sus(skor_kasir)}")
    print(f"Rata-rata Skor SUS Sistem: {rata_rata:.1f} -> {tentukan_grade_sus(rata_rata)}")
