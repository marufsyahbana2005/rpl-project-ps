"""
generate_doc_pdf.py — Skrip Kompilasi Dokumen Lengkap (SRS, PRD, Bab 3, Bab 4) ke HTML & PDF
Mengonversi seluruh dokumentasi ke dokumen HTML berstandar cetak A4, lalu mencetaknya ke PDF
menggunakan engine headless Chromium (Microsoft Edge / Google Chrome).
"""

import os
import re
import sys
import subprocess
import html


def parse_markdown_to_html(md_text):
    """Konversi subset Markdown terstruktur ke HTML semantik yang rapi."""
    lines = md_text.split("\n")
    html_lines = []
    in_code = False
    in_table = False
    in_list = False
    table_header_done = False

    for line in lines:
        stripped = line.strip()

        # 1. Code Block
        if stripped.startswith("```"):
            if not in_code:
                in_code = True
                lang = stripped[3:].strip()
                html_lines.append(f'<pre class="code-block {lang}"><code>')
            else:
                in_code = False
                html_lines.append("</code></pre>")
            continue

        if in_code:
            html_lines.append(html.escape(line))
            continue

        # 2. Table
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            if not in_table:
                in_table = True
                table_header_done = False
                html_lines.append('<div class="table-container"><table class="doc-table">')

            # Cek apakah baris pemisah |:---|---|
            if cells and all(re.match(r"^:?-+:?$", c) for c in cells):
                table_header_done = True
                continue

            if not table_header_done:
                html_lines.append("<thead><tr>")
                for c in cells:
                    formatted_c = format_inline(c)
                    html_lines.append(f"<th>{formatted_c}</th>")
                html_lines.append("</tr></thead><tbody>")
            else:
                html_lines.append("<tr>")
                for c in cells:
                    formatted_c = format_inline(c)
                    html_lines.append(f"<td>{formatted_c}</td>")
                html_lines.append("</tr>")
            continue
        else:
            if in_table:
                in_table = False
                html_lines.append("</tbody></table></div>")

        # 3. Lists
        if stripped.startswith("- ") or stripped.startswith("* "):
            if not in_list:
                in_list = True
                html_lines.append('<ul class="doc-list">')
            item_text = format_inline(stripped[2:])
            html_lines.append(f"<li>{item_text}</li>")
            continue
        elif re.match(r"^\d+\.\s+", stripped):
            if not in_list:
                in_list = True
                html_lines.append('<ol class="doc-list">')
            match = re.match(r"^\d+\.\s+(.*)$", stripped)
            item_text = format_inline(match.group(1))
            html_lines.append(f"<li>{item_text}</li>")
            continue
        else:
            if in_list:
                in_list = False
                html_lines.append("</ul>")

        # 4. Headers
        if stripped.startswith("# "):
            h_text = format_inline(stripped[2:])
            html_lines.append(f'<h1 class="heading-1">{h_text}</h1>')
            continue
        elif stripped.startswith("## "):
            h_text = format_inline(stripped[3:])
            html_lines.append(f'<h2 class="heading-2">{h_text}</h2>')
            continue
        elif stripped.startswith("### "):
            h_text = format_inline(stripped[4:])
            html_lines.append(f'<h3 class="heading-3">{h_text}</h3>')
            continue
        elif stripped.startswith("#### "):
            h_text = format_inline(stripped[5:])
            html_lines.append(f'<h4 class="heading-4">{h_text}</h4>')
            continue

        # 5. Blockquotes & Callouts
        if stripped.startswith("> "):
            bq_text = format_inline(stripped[2:])
            html_lines.append(f'<blockquote class="doc-quote">{bq_text}</blockquote>')
            continue

        # 6. Horizontal Rule
        if stripped in ("---", "***", "___"):
            html_lines.append('<hr class="doc-divider" />')
            continue

        # 7. Empty line
        if not stripped:
            continue

        # 8. Regular Paragraph
        p_text = format_inline(stripped)
        html_lines.append(f'<p class="doc-p">{p_text}</p>')

    if in_table:
        html_lines.append("</tbody></table></div>")
    if in_list:
        html_lines.append("</ul>")

    return "\n".join(html_lines)


def format_inline(text):
    """Format teks inline: bold, italic, code, links."""
    # Bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # Italic
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    # Inline code
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    # Markdown Links
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<span class="doc-link">\1</span>', text)
    return text


def build_full_html():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prd_path = os.path.join(base_dir, "PRD.md")
    srs_path = os.path.join(base_dir, "docs", "srs.md")
    laporan_path = os.path.join(base_dir, "docs", "laporan", "Laporan-Akhir-Exito-Playbox.md")

    prd_content = ""
    srs_content = ""
    laporan_content = ""

    if os.path.exists(prd_path):
        with open(prd_path, "r", encoding="utf-8") as f:
            prd_content = f.read()

    if os.path.exists(srs_path):
        with open(srs_path, "r", encoding="utf-8") as f:
            srs_content = f.read()

    if os.path.exists(laporan_path):
        with open(laporan_path, "r", encoding="utf-8") as f:
            laporan_content = f.read()

    prd_html = parse_markdown_to_html(prd_content)
    srs_html = parse_markdown_to_html(srs_content)
    laporan_html = parse_markdown_to_html(laporan_content)

    full_html = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Dokumentasi Lengkap Sistem Exito Playbox (SRS, PRD, & Laporan Akhir)</title>
    <style>
        @page {{
            size: A4;
            margin: 20mm 15mm 20mm 15mm;
            @bottom-right {{
                content: counter(page);
            }}
        }}

        body {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
            font-size: 10.5pt;
            line-height: 1.6;
            color: #1e293b;
            background: #ffffff;
            margin: 0;
            padding: 0;
        }}

        .cover-page {{
            page-break-after: always;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            min-height: 85vh;
            border: 2px solid #0f172a;
            padding: 40px 30px;
            box-sizing: border-box;
            background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
        }}

        .cover-badge {{
            display: inline-block;
            background: #2563eb;
            color: #ffffff;
            font-weight: 600;
            font-size: 9pt;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            padding: 6px 16px;
            border-radius: 20px;
            margin-bottom: 25px;
        }}

        .cover-title {{
            font-size: 24pt;
            font-weight: 800;
            color: #0f172a;
            margin: 0 0 15px 0;
            line-height: 1.25;
            text-transform: uppercase;
        }}

        .cover-subtitle {{
            font-size: 13pt;
            font-weight: 500;
            color: #475569;
            margin: 0 0 40px 0;
            max-width: 80%;
            line-height: 1.5;
        }}

        .cover-divider {{
            width: 120px;
            height: 4px;
            background: #2563eb;
            border: none;
            margin: 0 auto 40px auto;
        }}

        .cover-meta {{
            width: 85%;
            margin-top: 30px;
            border-top: 1px solid #cbd5e1;
            padding-top: 25px;
            text-align: left;
            font-size: 10pt;
        }}

        .cover-meta table {{
            width: 100%;
            border-collapse: collapse;
        }}

        .cover-meta td {{
            padding: 6px 10px;
            vertical-align: top;
        }}

        .cover-meta td.label {{
            width: 32%;
            font-weight: 600;
            color: #334155;
        }}

        .cover-meta td.val {{
            color: #0f172a;
        }}

        .section-break {{
            page-break-before: always;
            margin-top: 30px;
        }}

        .section-header-box {{
            background: #0f172a;
            color: #ffffff;
            padding: 16px 20px;
            border-radius: 6px;
            margin: 30px 0 25px 0;
        }}

        .section-header-box h1 {{
            margin: 0;
            font-size: 16pt;
            font-weight: 700;
            letter-spacing: 0.5px;
            color: #ffffff;
        }}

        h1.heading-1 {{
            font-size: 16pt;
            font-weight: 700;
            color: #0f172a;
            border-bottom: 2px solid #2563eb;
            padding-bottom: 6px;
            margin-top: 30px;
            margin-bottom: 15px;
        }}

        h2.heading-2 {{
            font-size: 13pt;
            font-weight: 700;
            color: #1e3a8a;
            margin-top: 22px;
            margin-bottom: 10px;
        }}

        h3.heading-3 {{
            font-size: 11.5pt;
            font-weight: 600;
            color: #0f172a;
            margin-top: 18px;
            margin-bottom: 8px;
        }}

        h4.heading-4 {{
            font-size: 10.5pt;
            font-weight: 600;
            color: #334155;
            margin-top: 14px;
            margin-bottom: 6px;
        }}

        p.doc-p {{
            margin: 0 0 10px 0;
            text-align: justify;
        }}

        .doc-list {{
            margin: 0 0 12px 0;
            padding-left: 24px;
        }}

        .doc-list li {{
            margin-bottom: 5px;
            text-align: justify;
        }}

        .table-container {{
            margin: 15px 0 20px 0;
            width: 100%;
            overflow-x: auto;
        }}

        table.doc-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 9pt;
            line-height: 1.45;
        }}

        table.doc-table th {{
            background: #1e293b;
            color: #ffffff;
            font-weight: 600;
            text-align: left;
            padding: 8px 10px;
            border: 1px solid #334155;
        }}

        table.doc-table td {{
            padding: 7px 10px;
            border: 1px solid #cbd5e1;
            vertical-align: top;
        }}

        table.doc-table tr:nth-child(even) {{
            background: #f8fafc;
        }}

        pre.code-block {{
            background: #0f172a;
            color: #f8fafc;
            padding: 12px 16px;
            border-radius: 6px;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 8.5pt;
            line-height: 1.45;
            overflow-x: auto;
            margin: 12px 0 16px 0;
            border: 1px solid #334155;
            white-space: pre-wrap;
            word-break: break-all;
        }}

        code {{
            background: #f1f5f9;
            color: #0f172a;
            padding: 2px 5px;
            border-radius: 4px;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 9pt;
            border: 1px solid #e2e8f0;
        }}

        pre.code-block code {{
            background: transparent;
            color: inherit;
            padding: 0;
            border: none;
            font-size: inherit;
        }}

        blockquote.doc-quote {{
            margin: 12px 0;
            padding: 10px 16px;
            background: #f8fafc;
            border-left: 4px solid #2563eb;
            color: #334155;
            font-style: italic;
        }}

        hr.doc-divider {{
            border: none;
            border-top: 1px solid #e2e8f0;
            margin: 25px 0;
        }}

        .doc-link {{
            color: #2563eb;
            font-weight: 500;
            text-decoration: underline;
        }}
    </style>
</head>
<body>

    <!-- HALAMAN COVER / SAMPUL -->
    <div class="cover-page">
        <div class="cover-badge">Dokumentasi Tugas Besar Rekayasa Perangkat Lunak</div>
        <h1 class="cover-title">SISTEM MANAJEMEN RENTAL PLAYSTATION BERBASIS WEB</h1>
        <div class="cover-subtitle">Kompilasi Dokumen Spesifikasi Kebutuhan (PRD & SRS), Perancangan Sistem, Implementasi, dan Evaluasi Pengujian Operasional</div>
        <hr class="cover-divider" />
        
        <div class="cover-meta">
            <table>
                <tr>
                    <td class="label">Nama Sistem:</td>
                    <td class="val"><strong>Exito Playbox Management System (rpl-project-ps)</strong></td>
                </tr>
                <tr>
                    <td class="label">Pengembang / NIM:</td>
                    <td class="val">Maruf Syahbana (2024xx / Full-Stack & Scrum Master)</td>
                </tr>
                <tr>
                    <td class="label">Mitra Usaha:</td>
                    <td class="val">Exito Playbox Rental PS (Bpk. Hendra — Kota Sampit)</td>
                </tr>
                <tr>
                    <td class="label">Status Rilis Produksi:</td>
                    <td class="val"><strong>Versi 1.0.1 (Production Ready)</strong></td>
                </tr>
                <tr>
                    <td class="label">Framework & Runtime:</td>
                    <td class="val">Python 3.12 / Flask 3.1.3 / SQLite 3 / Waitress WSGI</td>
                </tr>
                <tr>
                    <td class="label">Repositori GitHub:</td>
                    <td class="val">https://github.com/marufsyahbana2005/rpl-project-ps</td>
                </tr>
                <tr>
                    <td class="label">Tanggal Dokumen:</td>
                    <td class="val">November 2026</td>
                </tr>
            </table>
        </div>
    </div>

    <!-- BAGIAN 1: PRODUCT REQUIREMENTS DOCUMENT (PRD) -->
    <div class="section-break">
        <div class="section-header-box">
            <h1>BAGIAN I: PRODUCT REQUIREMENTS DOCUMENT (PRD)</h1>
        </div>
        {prd_html}
    </div>

    <!-- BAGIAN 2: SOFTWARE REQUIREMENTS SPECIFICATION (SRS) -->
    <div class="section-break">
        <div class="section-header-box">
            <h1>BAGIAN II: SOFTWARE REQUIREMENTS SPECIFICATION (SRS)</h1>
        </div>
        {srs_html}
    </div>

    <!-- BAGIAN 3 & 4: PERANCANGAN, IMPLEMENTASI, & EVALUASI -->
    <div class="section-break">
        <div class="section-header-box">
            <h1>BAGIAN III: PERANCANGAN, IMPLEMENTASI, DAN EVALUASI PENGUJIAN</h1>
        </div>
        {laporan_html}
    </div>

</body>
</html>
"""
    output_html_path = os.path.join(base_dir, "docs", "laporan", "Laporan-Lengkap-Exito-Playbox.html")
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"[OK] Berkas HTML kompilasi berhasil dibuat: {output_html_path}")
    return output_html_path


def convert_html_to_pdf(html_path):
    pdf_path = html_path.replace(".html", ".pdf")
    
    # Cek browser engine (Edge / Chrome)
    browser_exe = None
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]
    for c in candidates:
        if os.path.exists(c):
            browser_exe = c
            break

    if not browser_exe:
        print("[PERINGATAN] Tidak menemukan executable browser Chromium (Edge/Chrome).")
        return None

    print(f"[*] Menjalankan browser engine: {browser_exe}")
    cmd = [
        browser_exe,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
        print(f"[SUKSES] Berkas PDF berhasil dicetak: {pdf_path} (Ukuran: {os.path.getsize(pdf_path):,} bytes)")
        return pdf_path
    else:
        print(f"[GALAT] Gagal mencetak PDF. Kode keluar: {res.returncode}")
        print("Stdout:", res.stdout)
        print("Stderr:", res.stderr)
        return None


def main():
    print("=" * 70)
    print(" EXITO PLAYBOX — PEMBUATAN DOKUMEN PDF LENGKAP (SRS, PRD, & LAPORAN)")
    print("=" * 70)
    html_path = build_full_html()
    pdf_path = convert_html_to_pdf(html_path)
    if pdf_path:
        print("\n[SELESAI] Dokumen PDF siap digunakan untuk ujian tugas besar!")
    else:
        print("\n[PERHATIAN] HTML terbentuk. Anda dapat membukanya di browser dan tekan Ctrl + P untuk Save as PDF.")


if __name__ == "__main__":
    main()
