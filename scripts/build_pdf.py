import os
import re
import base64
import subprocess
import markdown
import pypdf

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD_FILE = os.path.join(BASE_DIR, "El Libro de Oro - Saint Germain.md")
COVER_IMG = os.path.join(BASE_DIR, "img", "Cover.png")
PORTRAIT_IMG = os.path.join(BASE_DIR, "img", "Ascended-Master-Saint-Germain-Portrait.jpg")
HTML_FILE = os.path.join(BASE_DIR, "El Libro de Oro - Saint Germain.html")
PDF_FILE = os.path.join(BASE_DIR, "El Libro de Oro - Saint Germain.pdf")

def image_to_base64_data_uri(filepath, mime_type="image/png"):
    if not os.path.exists(filepath):
        return ""
    with open(filepath, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"

def build_pdf():
    print("1. Reading markdown file...")
    with open(MD_FILE, "r", encoding="utf-8") as f:
        md_content = f.read()

    cover_b64 = image_to_base64_data_uri(COVER_IMG, "image/png")
    portrait_b64 = image_to_base64_data_uri(PORTRAIT_IMG, "image/jpeg")

    # Remove the markdown title and raw image markers from md_content
    # because they are rendered cleanly in our Cover and Title Page
    cleaned_md = re.sub(r'^#\s+El Libro de Oro de Saint Germain\s*', '', md_content)
    cleaned_md = re.sub(r'!\[Portada del libro\]\(/img/Cover\.png\)\s*', '', cleaned_md)
    cleaned_md = re.sub(r'##\s+El Maestro Ascendido Saint Germain\s*', '', cleaned_md)
    cleaned_md = re.sub(r'!\[Maestro Ascendido Saint Germain\]\(/img/Ascended-Master-Saint-Germain-Portrait\.jpg\)\s*', '', cleaned_md)

    # In the TOC, normalize anchors so links match generated heading ids
    cleaned_md = re.sub(r'\(#capítulo-', '(#capitulo-', cleaned_md)
    cleaned_md = cleaned_md.replace('(#autorización-para-divulgación)', '(#autorizacion-para-divulgacion)')
    cleaned_md = cleaned_md.replace('(#índice-de-contenidos)', '(#indice-de-contenidos)')

    print("2. Converting Markdown to HTML...")
    html_body = markdown.markdown(
        cleaned_md,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.footnotes',
            'markdown.extensions.toc',
            'markdown.extensions.sane_lists'
        ]
    )

    # Insert clean page breaks before major sections and each chapter
    html_body = re.sub(r'(<h2 id="indice-de-contenidos">)', r'<div class="page-break"></div>\1', html_body)
    html_body = re.sub(r'(<h2 id="autorizacion-para-divulgacion">)', r'<div class="page-break"></div>\1', html_body)
    html_body = re.sub(r'(<h2 id="el-libro-de-oro-de-la-hermandad-saint-germain">)', r'<div class="page-break"></div>\1', html_body)
    html_body = re.sub(r'(<h2 id="capitulo-[^"]*">)', r'<div class="page-break"></div>\1', html_body)

    html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>El Libro de Oro - Saint Germain</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&display=swap');

    @page {{
      size: A4 portrait;
      margin: 22mm 22mm 22mm 22mm;
      @top-center {{
        content: "EL LIBRO DE ORO   •   SAINT GERMAIN";
        font-family: 'Cinzel', serif;
        font-size: 7.5pt;
        letter-spacing: 2px;
        color: #9c8a68;
      }}
      @bottom-center {{
        content: counter(page);
        font-family: 'EB Garamond', Georgia, serif;
        font-size: 10pt;
        color: #555555;
      }}
    }}

    @page :first {{
      margin: 0;
      @top-center {{ content: normal; }}
      @bottom-center {{ content: normal; }}
    }}

    @page title-page-style {{
      margin: 18mm 22mm 18mm 22mm;
      @top-center {{ content: normal; }}
      @bottom-center {{ content: normal; }}
    }}

    * {{
      box-sizing: border-box;
    }}

    html, body {{
      margin: 0;
      padding: 0;
      background: #ffffff;
      color: #1e1e1e;
      font-family: 'EB Garamond', Garamond, 'Palatino Linotype', Georgia, serif;
      font-size: 11pt;
      line-height: 1.62;
      text-rendering: optimizeLegibility;
      -webkit-font-smoothing: antialiased;
    }}

    /* COVER PAGE */
    .cover-page {{
      page-break-after: always;
      break-after: page;
      width: 210mm;
      height: 297mm;
      margin: 0;
      padding: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #06050b;
      overflow: hidden;
    }}

    .cover-page img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}

    /* TITLE PAGE (PORTADILLA) */
    .title-page {{
      page: title-page-style;
      page-break-after: always;
      break-after: page;
      height: 255mm;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      text-align: center;
      padding: 10mm 5mm;
    }}

    .title-page-top {{
      margin-top: 10mm;
    }}

    .title-main {{
      font-family: 'Cinzel', serif;
      font-size: 30pt;
      font-weight: 900;
      letter-spacing: 5px;
      color: #946e22;
      text-transform: uppercase;
      margin: 0 0 6px 0;
      text-shadow: 0 1px 2px rgba(148, 110, 34, 0.15);
    }}

    .title-sub {{
      font-family: 'EB Garamond', serif;
      font-size: 15pt;
      font-style: italic;
      color: #555555;
      letter-spacing: 1.5px;
      margin-bottom: 5mm;
    }}

    .gold-divider {{
      width: 120px;
      height: 2px;
      background: linear-gradient(90deg, transparent, #b8860b, transparent);
      margin: 12px auto;
    }}

    .portrait-box {{
      width: 190px;
      height: 190px;
      border-radius: 50%;
      overflow: hidden;
      margin: 15px auto;
      border: 3.5px solid #c59b27;
      box-shadow: 0 4px 16px rgba(197, 155, 39, 0.35);
    }}

    .portrait-box img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}

    .title-author {{
      font-family: 'Cinzel', serif;
      font-size: 19pt;
      font-weight: 700;
      letter-spacing: 4px;
      color: #222222;
      margin-top: 15px;
      text-transform: uppercase;
    }}

    .title-page-bottom {{
      margin-bottom: 8mm;
    }}

    .title-cycle {{
      font-size: 11pt;
      font-style: italic;
      color: #666666;
      line-height: 1.4;
    }}

    /* PAGE BREAK HELPER */
    .page-break {{
      page-break-before: always;
      break-before: page;
      height: 0;
      margin: 0;
      padding: 0;
    }}

    /* HEADINGS */
    h1, h2, h3, h4 {{
      font-family: 'Cinzel', Georgia, serif;
      color: #241c13;
      page-break-after: avoid;
      break-after: avoid;
    }}

    h2 {{
      font-size: 18pt;
      font-weight: 700;
      text-align: center;
      margin-top: 25px;
      margin-bottom: 12px;
      padding-bottom: 8px;
      letter-spacing: 2.5px;
      color: #8c6418;
      border-bottom: 1px solid #e8dbb8;
    }}

    h3 {{
      font-size: 12.5pt;
      font-weight: 600;
      text-align: center;
      margin-top: 14px;
      margin-bottom: 14px;
      font-style: italic;
      color: #5c4314;
      letter-spacing: 1px;
    }}

    /* BODY PARAGRAPHS */
    p {{
      margin-top: 0;
      margin-bottom: 0.85em;
      text-align: justify;
      hyphens: auto;
      -webkit-hyphens: auto;
      text-indent: 1.8em;
    }}

    /* Headings shouldn't indent first paragraph */
    h1 + p, h2 + p, h3 + p, hr + p, .page-break + h2 + p, .title-page p {{
      text-indent: 0;
    }}

    /* DECREES AND AFFIRMATIONS */
    blockquote {{
      margin: 1.2em 2em;
      padding: 0.7em 1.2em;
      background: #faf7ef;
      border-left: 3px solid #b8860b;
      font-style: italic;
      color: #2b2b2b;
      page-break-inside: avoid;
      break-inside: avoid;
      border-radius: 2px;
    }}

    blockquote p {{
      text-indent: 0;
      margin-bottom: 0;
    }}

    /* HORIZONTAL RULES */
    hr {{
      border: none;
      height: 1px;
      background: linear-gradient(90deg, transparent, #c59b27, transparent);
      margin: 25px auto;
      width: 70%;
    }}

    /* TABLE OF CONTENTS */
    #indice-de-contenidos {{
      margin-bottom: 20px;
    }}

    #indice-de-contenidos + ul {{
      list-style: none;
      padding: 0 10px;
      margin: 20px auto 30px auto;
      columns: 2;
      column-gap: 35px;
    }}

    #indice-de-contenidos + ul li {{
      font-size: 10pt;
      margin-bottom: 8px;
      break-inside: avoid;
      border-bottom: 1px dotted #ddcca6;
      padding-bottom: 3px;
    }}

    #indice-de-contenidos + ul li a {{
      text-decoration: none;
      color: #2a2015;
      font-weight: 500;
      display: block;
      transition: color 0.15s;
    }}

    #indice-de-contenidos + ul li a:hover {{
      color: #946e22;
    }}

    /* FOOTNOTES */
    .footnote {{
      font-size: 8.5pt;
      line-height: 1.45;
      color: #555555;
      margin-top: 25px;
      padding-top: 10px;
      border-top: 1px solid #d5c8a8;
      page-break-inside: avoid;
    }}

    .footnote hr {{
      display: none;
    }}

    .footnote ol {{
      margin: 0;
      padding-left: 20px;
    }}

    .footnote li {{
      margin-bottom: 4px;
    }}

    .footnote-ref, .footnote-backref {{
      font-size: 8pt;
      color: #946e22;
      text-decoration: none;
      font-weight: bold;
    }}

    /* PRINT OPTIMIZATIONS */
    @media print {{
      body {{
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
      }}
      a {{
        color: inherit;
        text-decoration: none;
      }}
    }}
  </style>
</head>
<body>

  <!-- 1. COVER PAGE -->
  <div class="cover-page">
    <img src="{cover_b64}" alt="Portada El Libro de Oro">
  </div>

  <!-- 2. TITLE PAGE (PORTADILLA) -->
  <div class="title-page">
    <div class="title-page-top">
      <h1 class="title-main">El Libro de Oro</h1>
      <div class="title-sub">de la Hermandad Saint Germain</div>
      <div class="gold-divider"></div>
    </div>

    <div class="title-page-middle">
      <div class="portrait-box">
        <img src="{portrait_b64}" alt="Maestro Ascendido Saint Germain">
      </div>
      <div class="title-author">Saint Germain</div>
    </div>

    <div class="title-page-bottom">
      <div class="gold-divider"></div>
      <div class="title-cycle">
        Tercer Ciclo de Enseñanza de la Hermandad Saint Germain<br>
        Sagrada Instrucción del Maestro Ascendido para la Nueva Era
      </div>
    </div>
  </div>

  <!-- 3. BOOK BODY (TOC + PREAMBLE + CHAPTERS) -->
  <div class="book-body">
    {html_body}
  </div>

</body>
</html>"""

    print("3. Writing formatted HTML...")
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html_template)

    print("4. Generating PDF using Chromium...")
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    browser = chrome_path if os.path.exists(chrome_path) else edge_path

    cmd = [
        browser,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={PDF_FILE}",
        HTML_FILE
    ]

    subprocess.run(cmd, check=True)

    print("5. Post-processing PDF with PyPDF (metadata and ordered outlines)...")
    reader = pypdf.PdfReader(PDF_FILE)
    total_pages = len(reader.pages)
    print(f"   Initial PDF generated with {total_pages} pages.")

    writer = pypdf.PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    writer.add_metadata({
        '/Title': 'El Libro de Oro',
        '/Author': 'Saint Germain',
        '/Subject': 'Enseñanza del Maestro Ascendido Saint Germain - Actividad Sagrada YO SOY',
        '/Creator': 'El Libro de Oro de Saint Germain',
        '/Producer': 'Chromium & PyPDF Book Engine',
        '/Keywords': 'Saint Germain, Yo Soy, Metafísica, Libro de Oro, Hermandad Saint Germain'
    })

    # Add outline bookmarks IN ORDER
    # 1. Portada (page 0)
    writer.add_outline_item("Portada", 0)

    # 2. Portadilla (page 1)
    writer.add_outline_item("Portadilla", 1)

    # 3. Índice de Contenidos (page 2)
    writer.add_outline_item("Índice de Contenidos", 2)

    # Search for sections on pages >= 3 (0-indexed) so we don't match the TOC on page 2
    front_sections = [
        ("Autorización para divulgación", r"Autorizaci[óo]n para divulgaci[óo]n"),
        ("El Libro de Oro de la Hermandad Saint Germain", r"El Libro de Oro de la Hermandad Saint\s+Germain"),
    ]

    found_front = {}
    for p_idx in range(3, min(8, total_pages)):
        text = reader.pages[p_idx].extract_text()
        for title, pattern in front_sections:
            if title not in found_front and re.search(pattern, text, re.IGNORECASE):
                found_front[title] = p_idx

    for title, _ in front_sections:
        if title in found_front:
            writer.add_outline_item(title, found_front[title])

    # 4. Chapters
    chapter_roman = [
        "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
        "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX",
        "XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI", "XXVII", "XXVIII", "XXIX", "XXX",
        "XXXI", "XXXII"
    ]

    chapter_subtitles = {
        "XI": "El Dios Himalaya",
        "XIV": "Fe - Esperanza - Caridad",
        "XVI": "Día de Acción de Gracias",
        "XIX": "Plática del Maestro Jesús",
        "XXIII": "Preparación de la Pascua",
        "XXV": "Día de Navidad / Cha Ara / Templos de Luz",
        "XXVII": "Víspera de Navidad",
        "XXIX": "Plática en Acción de Gracias",
        "XXX": "Plática en Navidad",
        "XXXI": "Plática en Año Nuevo",
        "XXXII": "El Nuevo Ciclo (Conclave de Tetón Real)"
    }

    found_chapters = {}
    for p_idx in range(4, total_pages):
        text = reader.pages[p_idx].extract_text()
        if not text:
            continue
        for r in chapter_roman:
            if r not in found_chapters:
                # Find "Capítulo {r}" as a standalone line or header
                if re.search(rf"\bCap[íi]tulo\s+{r}\b", text):
                    found_chapters[r] = p_idx

    for r in chapter_roman:
        if r in found_chapters:
            sub = chapter_subtitles.get(r)
            title = f"Capítulo {r} - {sub}" if sub else f"Capítulo {r}"
            writer.add_outline_item(title, found_chapters[r])

    with open(PDF_FILE, "wb") as f_out:
        writer.write(f_out)

    if os.path.exists(HTML_FILE):
        try:
            os.remove(HTML_FILE)
        except OSError:
            pass

    file_size_mb = os.path.getsize(PDF_FILE) / (1024 * 1024)
    print(f"6. Completed! Final PDF saved to: {PDF_FILE}")
    print(f"   Size: {file_size_mb:.2f} MB | Total Pages: {total_pages}")

if __name__ == "__main__":
    build_pdf()
