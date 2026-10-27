import os
import re
import markdown

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MD_FILE = os.path.join(BASE_DIR, "El Libro de Oro - Saint Germain.md")
HTML_FILE = os.path.join(BASE_DIR, "index.html")

def build_web():
    print("1. Reading markdown file...")
    with open(MD_FILE, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Extract clean markdown body
    # Remove original header and raw image tags because we will render a rich hero / cover
    cleaned_md = re.sub(r'^#\s+El Libro de Oro de Saint Germain\s*', '', md_content)
    cleaned_md = re.sub(r'!\[Portada del libro\]\(/img/Cover\.png\)\s*', '', cleaned_md)
    cleaned_md = re.sub(r'##\s+El Maestro Ascendido Saint Germain\s*', '', cleaned_md)
    cleaned_md = re.sub(r'!\[Maestro Ascendido Saint Germain\]\(/img/Ascended-Master-Saint-Germain-Portrait\.jpg\)\s*', '', cleaned_md)

    # Normalize anchors in the markdown
    cleaned_md = re.sub(r'\(#capítulo-', '(#capitulo-', cleaned_md)
    cleaned_md = cleaned_md.replace('(#autorización-para-divulgación)', '(#autorizacion-para-divulgacion)')
    cleaned_md = cleaned_md.replace('(#índice-de-contenidos)', '(#indice-de-contenidos)')

    # Remove the embedded markdown table of contents from the body because we'll have an interactive sidebar TOC
    toc_pattern = r'## Índice de Contenidos[\s\S]*?---\s*'
    cleaned_md = re.sub(toc_pattern, '', cleaned_md)

    print("2. Converting markdown to HTML...")
    html_content = markdown.markdown(
        cleaned_md,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.footnotes',
            'markdown.extensions.toc',
            'markdown.extensions.sane_lists'
        ]
    )

    # Wrap chapters in semantic <section class="book-chapter">
    # Add id attributes where missing and wrap each chapter
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

    # Generate the sidebar navigation items HTML
    toc_items = []
    toc_items.append("""<li class="toc-item"><a href="#portada" class="toc-link active"><span class="toc-title">Portada del Libro</span></a></li>""")
    toc_items.append("""<li class="toc-item"><a href="#portadilla" class="toc-link"><span class="toc-title">Portadilla &amp; Maestro</span></a></li>""")
    toc_items.append("""<li class="toc-item"><a href="#autorizacion-para-divulgacion" class="toc-link"><span class="toc-title">Autorización de Divulgación</span></a></li>""")
    toc_items.append("""<li class="toc-item"><a href="#el-libro-de-oro-de-la-hermandad-saint-germain" class="toc-link"><span class="toc-title">La Hermandad Saint Germain</span></a></li>""")

    for r in chapter_roman:
        cid = f"capitulo-{r.lower()}"
        sub = chapter_subtitles.get(r, "")
        sub_html = f'<span class="toc-sub">{sub}</span>' if sub else ""
        toc_items.append(f"""<li class="toc-item"><a href="#{cid}" class="toc-link"><span class="toc-title">Capítulo {r}</span>{sub_html}</a></li>""")

    toc_nav_html = "\n".join(toc_items)

    web_template = f"""<!DOCTYPE html>
<html lang="es" data-theme="sepia">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>El Libro de Oro — Saint Germain | Lector Web Oficial</title>
  <meta name="description" content="Edición web digital e interactiva de El Libro de Oro del Maestro Ascendido Saint Germain. Incluye los 32 capítulos, temas claro/sepia/oscuro y descarga en PDF.">
  <meta name="color-scheme" content="light dark">

  <!-- Open Graph / Meta -->
  <meta property="og:type" content="book">
  <meta property="og:title" content="El Libro de Oro — Saint Germain">
  <meta property="og:description" content="Sagrada Enseñanza del Maestro Ascendido Saint Germain para la Nueva Era.">
  <meta property="og:image" content="img/Cover.png">

  <!-- FOUC Prevention Script -->
  <script>
    (function() {{
      try {{
        const savedTheme = localStorage.getItem('book-theme') || 'sepia';
        document.documentElement.setAttribute('data-theme', savedTheme);
        const metaColor = document.querySelector('meta[name="color-scheme"]');
        if (metaColor) {{
          metaColor.content = savedTheme === 'dark' ? 'dark' : (savedTheme === 'light' ? 'light' : 'light dark');
        }}
        const savedSize = localStorage.getItem('book-font-size');
        if (savedSize) {{
          document.documentElement.style.setProperty('--font-scale', savedSize);
        }}
      }} catch (e) {{}}
    }})();
  </script>

  <!-- Typography -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&display=swap" rel="stylesheet">

  <style>
    /* CSS Variables & Themes */
    :root {{
      --font-serif: 'EB Garamond', Garamond, 'Palatino Linotype', Georgia, serif;
      --font-display: 'Cinzel', serif;
      --font-scale: 1;
      
      --header-height: 60px;
      --sidebar-width: 320px;
      --reading-width: 68ch;
      --transition-speed: 0.25s;
    }}

    /* Light Theme */
    [data-theme="light"] {{
      color-scheme: light;
      --bg-base: #fcfbf9;
      --bg-surface: #ffffff;
      --bg-sidebar: #f8f6f0;
      --border-color: #e5ded0;
      --text-main: #1f1b18;
      --text-muted: #6e675f;
      --gold-accent: #9d7426;
      --gold-glow: rgba(157, 116, 38, 0.15);
      --blockquote-bg: #f9f5eb;
      --link-hover: #b8860b;
      --shadow-soft: 0 4px 20px rgba(0, 0, 0, 0.05);
    }}

    /* Sepia / Warm Paper Theme (Default) */
    [data-theme="sepia"] {{
      color-scheme: light;
      --bg-base: #f4ecd8;
      --bg-surface: #fbf7ee;
      --bg-sidebar: #efe5cb;
      --border-color: #dfd2b5;
      --text-main: #2c2419;
      --text-muted: #736551;
      --gold-accent: #8f651c;
      --gold-glow: rgba(143, 101, 28, 0.18);
      --blockquote-bg: #ebe0c5;
      --link-hover: #a37521;
      --shadow-soft: 0 4px 20px rgba(78, 59, 29, 0.08);
    }}

    /* Dark / Midnight Theme */
    [data-theme="dark"] {{
      color-scheme: dark;
      --bg-base: #0f1013;
      --bg-surface: #17191e;
      --bg-sidebar: #131418;
      --border-color: #2b2e37;
      --text-main: #e6e2da;
      --text-muted: #9ea3b0;
      --gold-accent: #d4af37;
      --gold-glow: rgba(212, 175, 55, 0.25);
      --blockquote-bg: #1f2229;
      --link-hover: #f1c40f;
      --shadow-soft: 0 4px 24px rgba(0, 0, 0, 0.4);
    }}

    /* Base Reset */
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    html {{
      scroll-behavior: smooth;
      scroll-padding-top: calc(var(--header-height) + 24px);
    }}

    body {{
      background: var(--bg-base);
      color: var(--text-main);
      font-family: var(--font-serif);
      font-size: calc(18px * var(--font-scale));
      line-height: 1.75;
      transition: background-color var(--transition-speed) ease, color var(--transition-speed) ease;
      min-height: 100vh;
      overflow-x: hidden;
      text-rendering: optimizeLegibility;
      -webkit-font-smoothing: antialiased;
    }}

    /* Progress Bar (Scroll-driven animation with modern web guidance compliance) */
    #scroll-progress {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 3.5px;
      background: linear-gradient(90deg, var(--gold-accent), #f39c12);
      z-index: 1001;
      transform-origin: 0 50%;
      transform: scaleX(0);
    }}

    @media (prefers-reduced-motion: no-preference) {{
      @supports (animation-timeline: scroll()) {{
        #scroll-progress {{
          animation: grow-progress auto linear;
          animation-timeline: scroll();
        }}
        @keyframes grow-progress {{
          from {{ transform: scaleX(0); }}
          to {{ transform: scaleX(1); }}
        }}
      }}
    }}

    /* Top Sticky Header */
    .site-header {{
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      height: var(--header-height);
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
      z-index: 1000;
      backdrop-filter: blur(8px);
      box-shadow: var(--shadow-soft);
    }}

    .header-left, .header-right {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .btn-icon {{
      background: transparent;
      border: 1px solid var(--border-color);
      color: var(--text-main);
      cursor: pointer;
      border-radius: 6px;
      padding: 6px 12px;
      font-size: 14px;
      font-family: inherit;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
    }}

    .btn-icon:hover {{
      border-color: var(--gold-accent);
      color: var(--gold-accent);
      background: var(--gold-glow);
    }}

    .book-title-header {{
      font-family: var(--font-display);
      font-size: 15px;
      font-weight: 700;
      letter-spacing: 1.5px;
      color: var(--gold-accent);
      text-transform: uppercase;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      margin: 0 8px;
    }}

    @media (max-width: 600px) {{
      .book-title-header {{
        display: none;
      }}
    }}

    /* Theme Switcher */
    .theme-group {{
      display: flex;
      background: var(--bg-base);
      border: 1px solid var(--border-color);
      border-radius: 6px;
      padding: 2px;
    }}

    .theme-btn {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 600;
      transition: all 0.15s ease;
    }}

    .theme-btn.active {{
      background: var(--bg-surface);
      color: var(--gold-accent);
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }}

    /* Font Size Controls */
    .font-group {{
      display: flex;
      align-items: center;
      gap: 2px;
    }}

    .font-btn {{
      background: transparent;
      border: 1px solid var(--border-color);
      color: var(--text-main);
      cursor: pointer;
      border-radius: 4px;
      padding: 3px 8px;
      font-size: 13px;
      font-weight: 600;
    }}
    .font-btn:hover {{
      border-color: var(--gold-accent);
      color: var(--gold-accent);
    }}

    /* Download PDF Button */
    .btn-pdf {{
      background: var(--gold-accent);
      color: #ffffff !important;
      border: none;
      font-weight: 600;
      font-size: 13px;
      padding: 6px 12px;
      border-radius: 6px;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: opacity 0.2s;
    }}
    .btn-pdf:hover {{
      opacity: 0.9;
    }}

    /* Main Container with Sidebar */
    .layout-container {{
      display: flex;
      margin-top: var(--header-height);
      min-height: calc(100vh - var(--header-height));
    }}

    /* Sidebar Drawer */
    .sidebar {{
      width: var(--sidebar-width);
      background: var(--bg-sidebar);
      border-right: 1px solid var(--border-color);
      position: fixed;
      top: var(--header-height);
      bottom: 0;
      left: 0;
      overflow-y: auto;
      z-index: 900;
      transition: transform var(--transition-speed) ease;
      display: flex;
      flex-direction: column;
    }}

    .sidebar.closed {{
      transform: translateX(-100%);
    }}

    .sidebar-header {{
      padding: 16px;
      border-bottom: 1px solid var(--border-color);
      position: sticky;
      top: 0;
      background: var(--bg-sidebar);
      z-index: 2;
    }}

    .sidebar-search {{
      width: 100%;
      padding: 8px 12px;
      border-radius: 6px;
      border: 1px solid var(--border-color);
      background: var(--bg-surface);
      color: var(--text-main);
      font-family: inherit;
      font-size: 14px;
      outline: none;
    }}

    .sidebar-search:focus {{
      border-color: var(--gold-accent);
      box-shadow: 0 0 0 2px var(--gold-glow);
    }}

    .sidebar-nav {{
      list-style: none;
      padding: 12px 8px 30px 8px;
      flex: 1;
    }}

    .toc-item {{
      margin-bottom: 2px;
    }}

    .toc-link {{
      display: flex;
      flex-direction: column;
      padding: 8px 12px;
      border-radius: 6px;
      color: var(--text-main);
      text-decoration: none;
      font-size: 14px;
      line-height: 1.35;
      transition: all 0.15s ease;
    }}

    .toc-link:hover {{
      background: var(--gold-glow);
      color: var(--gold-accent);
      padding-left: 16px;
    }}

    .toc-link.active {{
      background: var(--gold-accent);
      color: #ffffff;
      font-weight: 600;
    }}

    .toc-title {{
      font-size: 14.5px;
      font-weight: 500;
    }}

    .toc-sub {{
      font-size: 12px;
      opacity: 0.85;
      font-style: italic;
      margin-top: 2px;
    }}

    /* Main Reading Area */
    .main-content {{
      flex: 1;
      margin-left: var(--sidebar-width);
      padding: 40px 24px 100px 24px;
      transition: margin-left var(--transition-speed) ease;
      display: flex;
      justify-content: center;
    }}

    .sidebar.closed + .main-content {{
      margin-left: 0;
    }}

    .reader-article {{
      max-width: var(--reading-width);
      width: 100%;
    }}

    /* Hero / Cover Page */
    .hero-cover {{
      text-align: center;
      padding: 20px 0 60px 0;
      border-bottom: 1px solid var(--border-color);
      margin-bottom: 50px;
    }}

    .cover-art {{
      max-width: 320px;
      width: 100%;
      height: auto;
      border-radius: 8px;
      box-shadow: 0 12px 35px rgba(0,0,0,0.25);
      margin-bottom: 24px;
    }}

    .hero-title {{
      font-family: var(--font-display);
      font-size: 2.2rem;
      font-weight: 900;
      letter-spacing: 3px;
      color: var(--gold-accent);
      text-transform: uppercase;
      margin-bottom: 6px;
    }}

    .hero-sub {{
      font-size: 1.25rem;
      font-style: italic;
      color: var(--text-muted);
      margin-bottom: 24px;
    }}

    /* Portrait Section */
    .portrait-card {{
      text-align: center;
      padding: 40px 0;
      border-bottom: 1px solid var(--border-color);
      margin-bottom: 50px;
    }}

    .portrait-frame {{
      width: 160px;
      height: 160px;
      border-radius: 50%;
      border: 3.5px solid var(--gold-accent);
      overflow: hidden;
      margin: 0 auto 16px auto;
      box-shadow: 0 4px 18px var(--gold-glow);
    }}

    .portrait-frame img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
    }}

    .master-name {{
      font-family: var(--font-display);
      font-size: 1.3rem;
      letter-spacing: 2px;
      color: var(--gold-accent);
      margin-bottom: 4px;
    }}

    .master-title {{
      font-size: 0.95rem;
      font-style: italic;
      color: var(--text-muted);
    }}

    /* Prose Typography */
    h1, h2, h3, h4 {{
      font-family: var(--font-display);
      color: var(--text-main);
      line-height: 1.3;
    }}

    h2 {{
      font-size: 1.8rem;
      text-align: center;
      margin-top: 60px;
      margin-bottom: 20px;
      padding-top: 30px;
      border-top: 1px solid var(--border-color);
      color: var(--gold-accent);
      letter-spacing: 2px;
    }}

    h3 {{
      font-size: 1.2rem;
      text-align: center;
      font-style: italic;
      color: var(--text-muted);
      margin-top: -8px;
      margin-bottom: 24px;
    }}

    p {{
      margin-bottom: 1.25em;
      text-align: justify;
      hyphens: auto;
      text-indent: 1.8em;
    }}

    h2 + p, h3 + p, hr + p, blockquote + p {{
      text-indent: 0;
    }}

    /* Initial drop cap on chapter opening */
    h2 + p::first-letter {{
      font-family: var(--font-display);
      font-size: 2.8em;
      float: left;
      line-height: 0.8;
      margin-right: 0.12em;
      margin-top: 0.05em;
      color: var(--gold-accent);
      font-weight: 700;
    }}

    /* Decrees & Affirmations */
    blockquote {{
      background: var(--blockquote-bg);
      border-left: 4px solid var(--gold-accent);
      margin: 1.8em 0;
      padding: 16px 22px;
      border-radius: 4px;
      font-style: italic;
    }}

    blockquote p {{
      text-indent: 0;
      margin-bottom: 0;
    }}

    hr {{
      border: none;
      height: 1px;
      background: linear-gradient(90deg, transparent, var(--gold-accent), transparent);
      margin: 40px auto;
      width: 70%;
    }}

    /* Footnotes */
    .footnote {{
      font-size: 0.88em;
      color: var(--text-muted);
      border-top: 1px solid var(--border-color);
      margin-top: 40px;
      padding-top: 16px;
    }}

    .footnote hr {{
      display: none;
    }}

    .footnote ol {{
      padding-left: 20px;
    }}

    .footnote li {{
      margin-bottom: 6px;
    }}

    .footnote-ref, .footnote-backref {{
      color: var(--gold-accent);
      text-decoration: none;
      font-weight: bold;
    }}

    /* Floating Navigation (Back to top / Previous - Next) */
    .floating-nav {{
      position: fixed;
      bottom: 20px;
      right: 20px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      z-index: 800;
    }}

    .btn-float {{
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      transition: all 0.2s ease;
      text-decoration: none;
      font-size: 16px;
    }}

    .btn-float:hover {{
      background: var(--gold-accent);
      color: #ffffff;
      transform: translateY(-2px);
    }}

    /* Responsive Adjustments */
    @media (max-width: 900px) {{
      .sidebar {{
        transform: translateX(-100%);
      }}
      .sidebar.open {{
        transform: translateX(0);
      }}
      .main-content {{
        margin-left: 0 !important;
        padding: 24px 16px 80px 16px;
      }}
      .sidebar-backdrop {{
        display: none;
        position: fixed;
        inset: 0;
        background: rgba(0, 0, 0, 0.45);
        z-index: 850;
      }}
      .sidebar-backdrop.active {{
        display: block;
      }}
    }}
  </style>
</head>
<body>

  <!-- Decorative Scroll Progress -->
  <div id="scroll-progress" aria-hidden="true"></div>

  <!-- Header -->
  <header class="site-header">
    <div class="header-left">
      <button id="toggle-sidebar" class="btn-icon" aria-label="Abrir o cerrar índice">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
        <span>Índice</span>
      </button>
      <span class="book-title-header">El Libro de Oro &bull; Saint Germain</span>
    </div>

    <div class="header-right">
      <!-- Font size controls -->
      <div class="font-group" title="Tamaño de letra">
        <button id="font-dec" class="font-btn" aria-label="Disminuir tamaño">A-</button>
        <button id="font-reset" class="font-btn" aria-label="Restablecer tamaño">A</button>
        <button id="font-inc" class="font-btn" aria-label="Aumentar tamaño">A+</button>
      </div>

      <!-- Theme Switcher -->
      <div class="theme-group">
        <button class="theme-btn" data-set-theme="light" title="Modo Claro">Claro</button>
        <button class="theme-btn active" data-set-theme="sepia" title="Modo Sepia">Sepia</button>
        <button class="theme-btn" data-set-theme="dark" title="Modo Oscuro">Oscuro</button>
      </div>

      <!-- PDF Download Button -->
      <a href="El%20Libro%20de%20Oro%20-%20Saint%20Germain.pdf" download class="btn-pdf" title="Descargar libro en PDF completo">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
        <span>PDF</span>
      </a>
    </div>
  </header>

  <div class="layout-container">
    <!-- Backdrop for mobile sidebar -->
    <div id="sidebar-backdrop" class="sidebar-backdrop"></div>

    <!-- Sidebar Navigation -->
    <aside id="sidebar" class="sidebar">
      <div class="sidebar-header">
        <input type="text" id="search-input" class="sidebar-search" placeholder="🔍 Buscar capítulo..." aria-label="Filtrar capítulos">
      </div>
      <ul id="toc-list" class="sidebar-nav">
        {toc_nav_html}
      </ul>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
      <article class="reader-article">

        <!-- Portada -->
        <section id="portada" class="hero-cover">
          <img src="img/Cover.png" alt="Portada El Libro de Oro" class="cover-art">
          <h1 class="hero-title">El Libro de Oro</h1>
          <div class="hero-sub">de la Hermandad Saint Germain</div>
          <p style="text-align: center; text-indent: 0; color: var(--text-muted); font-size: 0.95rem;">
            Tercer Ciclo de Enseñanza &bull; Sagrada Enseñanza para la Nueva Era
          </p>
        </section>

        <!-- Portadilla y Retrato -->
        <section id="portadilla" class="portrait-card">
          <div class="portrait-frame">
            <img src="img/Ascended-Master-Saint-Germain-Portrait.jpg" alt="Maestro Ascendido Saint Germain">
          </div>
          <div class="master-name">Saint Germain</div>
          <div class="master-title">Maestro Ascendido</div>
        </section>

        <!-- Cuerpo del libro (Preámbulos y 32 Capítulos) -->
        <div class="book-body">
          {html_content}
        </div>

      </article>
    </main>
  </div>

  <!-- Floating Nav Controls -->
  <div class="floating-nav">
    <a href="#portada" class="btn-float" title="Subir al inicio" aria-label="Volver arriba">
      ▲
    </a>
  </div>

  <!-- Interactive Reader Logic -->
  <script>
    document.addEventListener('DOMContentLoaded', () => {{
      // 1. Sidebar Toggle
      const toggleBtn = document.getElementById('toggle-sidebar');
      const sidebar = document.getElementById('sidebar');
      const backdrop = document.getElementById('sidebar-backdrop');

      function toggleSidebar() {{
        if (window.innerWidth <= 900) {{
          sidebar.classList.toggle('open');
          backdrop.classList.toggle('active');
        }} else {{
          sidebar.classList.toggle('closed');
        }}
      }}

      toggleBtn.addEventListener('click', toggleSidebar);
      backdrop.addEventListener('click', () => {{
        sidebar.classList.remove('open');
        backdrop.classList.remove('active');
      }});

      // Auto-close sidebar on mobile when a link is clicked
      document.querySelectorAll('.toc-link').forEach(link => {{
        link.addEventListener('click', () => {{
          if (window.innerWidth <= 900) {{
            sidebar.classList.remove('open');
            backdrop.classList.remove('active');
          }}
        }});
      }});

      // 2. Search / Filter in TOC
      const searchInput = document.getElementById('search-input');
      const tocItems = document.querySelectorAll('.toc-item');
      searchInput.addEventListener('input', (e) => {{
        const term = e.target.value.toLowerCase().trim();
        tocItems.forEach(item => {{
          const text = item.textContent.toLowerCase();
          item.style.display = text.includes(term) ? '' : 'none';
        }});
      }});

      // 3. Theme Switching
      const themeBtns = document.querySelectorAll('.theme-btn');
      function setTheme(theme) {{
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('book-theme', theme);
        const metaColor = document.querySelector('meta[name="color-scheme"]');
        if (metaColor) {{
          metaColor.content = theme === 'dark' ? 'dark' : (theme === 'light' ? 'light' : 'light dark');
        }}
        themeBtns.forEach(btn => {{
          btn.classList.toggle('active', btn.dataset.setTheme === theme);
        }});
      }}

      themeBtns.forEach(btn => {{
        btn.addEventListener('click', () => setTheme(btn.dataset.setTheme));
      }});

      // Sync active state with stored theme
      const currentTheme = localStorage.getItem('book-theme') || 'sepia';
      themeBtns.forEach(btn => {{
        btn.classList.toggle('active', btn.dataset.setTheme === currentTheme);
      }});

      // 4. Font Size Controls
      let currentScale = parseFloat(localStorage.getItem('book-font-size')) || 1;
      function applyScale(scale) {{
        currentScale = Math.min(1.4, Math.max(0.85, scale));
        document.documentElement.style.setProperty('--font-scale', currentScale);
        localStorage.setItem('book-font-size', currentScale);
      }}

      document.getElementById('font-inc').addEventListener('click', () => applyScale(currentScale + 0.08));
      document.getElementById('font-dec').addEventListener('click', () => applyScale(currentScale - 0.08));
      document.getElementById('font-reset').addEventListener('click', () => applyScale(1.0));

      // 5. Scroll Progress Fallback for browsers not supporting CSS scroll()
      if (!CSS.supports('animation-timeline', 'scroll()')) {{
        const progressBar = document.getElementById('scroll-progress');
        window.addEventListener('scroll', () => {{
          const scrollable = document.documentElement.scrollHeight - window.innerHeight;
          const scrolled = window.scrollY;
          const pct = scrollable > 0 ? (scrolled / scrollable) : 0;
          progressBar.style.transform = `scaleX(${{pct}})`;
        }}, {{ passive: true }});
      }}

      // 6. Active TOC Item Tracking with IntersectionObserver
      const headings = document.querySelectorAll('section[id], h2[id]');
      const navLinks = document.querySelectorAll('.toc-link');

      const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
          if (entry.isIntersecting) {{
            const id = entry.target.getAttribute('id');
            navLinks.forEach(link => {{
              const href = link.getAttribute('href');
              if (href === `#${{id}}`) {{
                link.classList.add('active');
                // Scroll link into view in sidebar smoothly
                link.scrollIntoView({{ block: 'nearest', behavior: 'smooth' }});
              }} else {{
                link.classList.remove('active');
              }}
            }});
          }}
        }});
      }}, {{
        rootMargin: '-80px 0px -60% 0px',
        threshold: 0
      }});

      headings.forEach(h => observer.observe(h));
    }});
  </script>

</body>
</html>"""

    print("3. Writing index.html...")
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(web_template)

    size_kb = os.path.getsize(HTML_FILE) / 1024
    print(f"4. Success! index.html generated ({size_kb:.1f} KB).")

if __name__ == "__main__":
    build_web()
