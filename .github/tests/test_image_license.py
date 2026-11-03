"""Regressionsprüfungen für die sichtbare, bildbezogene CC-Lizenzierung."""
from html.parser import HTMLParser
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
LICENSE_URL = "https://creativecommons.org/licenses/by-nc-sa/4.0/"


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.append(dict(attrs))


class ImageLicenseTests(unittest.TestCase):
    def test_shared_footer_contains_license_and_attribution_links(self):
        footer = (ROOT / "_includes/footer.html").read_text(encoding="utf-8")
        parser = LinkParser()
        parser.feed(footer)
        license_links = [link for link in parser.links if link.get("rel") == "license"]
        self.assertEqual(len(license_links), 1)
        self.assertEqual(license_links[0]["href"], LICENSE_URL)
        self.assertIn("Attribution-NonCommercial-ShareAlike 4.0", license_links[0]["title"])
        self.assertIn("{{ site.author | escape }}", footer)
        self.assertIn("'/image-license/' | relative_url", footer)
        layout = (ROOT / "_layouts/default.html").read_text(encoding="utf-8")
        self.assertIn("{% include footer.html %}", layout)

    def test_license_page_covers_all_images_and_excludes_text_and_code(self):
        page = (ROOT / "image-license.md").read_text(encoding="utf-8")
        self.assertIn("permalink: /image-license/", page)
        self.assertIn("including photographs and logos", page)
        self.assertIn(LICENSE_URL, page)
        self.assertIn("Andreas Willich / Marvelous Blocks", page)
        self.assertIn("indicate any changes", page)
        self.assertIn("does not cover the website's text or code", page)

    def test_repository_image_license_matches_public_license(self):
        license_file = (ROOT / "assets/images/LICENSE.md").read_text(encoding="utf-8")
        self.assertIn(LICENSE_URL, license_file)
        self.assertIn("Andreas Willich / Marvelous Blocks", license_file)
        self.assertIn("Unterordnern", license_file)
        self.assertIn("nicht für Texte oder Code", license_file)


if __name__ == "__main__":
    unittest.main()
