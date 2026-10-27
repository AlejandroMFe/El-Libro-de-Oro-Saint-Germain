import os
import unittest
import pypdf

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROMAN_CHAPTERS = [
    "i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x",
    "xi", "xii", "xiii", "xiv", "xv", "xvi", "xvii", "xviii", "xix", "xx",
    "xxi", "xxii", "xxiii", "xxiv", "xxv", "xxvi", "xxvii", "xxviii", "xxix", "xxx",
    "xxxi", "xxxii"
]

class TestBookIntegrity(unittest.TestCase):

    def test_markdown_and_assets(self):
        """Verifica que el libro markdown consolidado, los 32 capítulos y las imágenes existan."""
        md_file = os.path.join(BASE_DIR, "El Libro de Oro - Saint Germain.md")
        self.assertTrue(os.path.exists(md_file), "Falta el archivo principal Markdown.")

        cover_img = os.path.join(BASE_DIR, "img", "Cover.png")
        portrait_img = os.path.join(BASE_DIR, "img", "Ascended-Master-Saint-Germain-Portrait.jpg")
        self.assertTrue(os.path.exists(cover_img), "Falta la imagen de portada img/Cover.png.")
        self.assertTrue(os.path.exists(portrait_img), "Falta el retrato del Maestro.")

        # Verificar los 32 archivos de capítulos individuales
        for i in range(1, 33):
            ch_filename = f"{i:02d}_capitulo_{i}.md"
            ch_path = os.path.join(BASE_DIR, "Capitulos", ch_filename)
            self.assertTrue(os.path.exists(ch_path), f"Falta el archivo de capítulo {ch_filename}")

    def test_web_reader(self):
        """Verifica que index.html contenga todos los capítulos, temas y navegación."""
        html_file = os.path.join(BASE_DIR, "index.html")
        self.assertTrue(os.path.exists(html_file), "Falta el archivo index.html generado.")

        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Verificar todos los capítulos en el HTML
        for r in ROMAN_CHAPTERS:
            self.assertIn(f'id="capitulo-{r}"', content.lower(), f"Falta el capítulo {r} en index.html")

        # Verificar secciones preliminares
        self.assertIn('id="portada"', content)
        self.assertIn('id="portadilla"', content)
        self.assertIn('id="autorizacion-para-divulgacion"', content)
        self.assertIn('id="el-libro-de-oro-de-la-hermandad-saint-germain"', content)

        # Verificar temas y controles
        self.assertIn('data-set-theme="light"', content)
        self.assertIn('data-set-theme="sepia"', content)
        self.assertIn('data-set-theme="dark"', content)
        self.assertIn('id="scroll-progress"', content)
        self.assertIn('El%20Libro%20de%20Oro%20-%20Saint%20Germain.pdf', content)

    def test_pdf_document(self):
        """Verifica que el PDF esté generado con sus metadatos y marcadores completos."""
        pdf_file = os.path.join(BASE_DIR, "El Libro de Oro - Saint Germain.pdf")
        self.assertTrue(os.path.exists(pdf_file), "Falta el archivo PDF compilado.")

        reader = pypdf.PdfReader(pdf_file)
        self.assertGreaterEqual(len(reader.pages), 100, "El PDF debería tener al menos 100 páginas.")

        # Verificar metadatos
        metadata = reader.metadata
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata.title, "El Libro de Oro")
        self.assertEqual(metadata.author, "Saint Germain")

        # Verificar marcadores (outlines)
        self.assertGreaterEqual(len(reader.outline), 30, "El PDF debería tener más de 30 marcadores de navegación.")

if __name__ == "__main__":
    unittest.main()
