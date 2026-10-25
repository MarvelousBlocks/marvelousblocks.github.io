"""Integrationstests mit ExifTool; keine zusätzlichen Python-Pakete nötig."""

import base64
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".github/scripts/strip-image-metadata.sh"
BASH = shutil.which("bash") or "bash"


class ImageMetadataTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name) / "_site"
        self.site.mkdir()

    def exiftool(self, *args):
        return subprocess.run(
            [BASH, "-c", 'exiftool "$@"', "exiftool", *map(str, args)],
            check=True, capture_output=True, text=True
        ).stdout

    def clean(self, directory=None):
        return subprocess.run(
            [BASH, SCRIPT.as_posix(), (directory or self.site).as_posix()],
            capture_output=True, text=True,
        )

    def metadata(self, image, *tags):
        return json.loads(self.exiftool("-j", "-n", *tags, image))[0]

    def jpeg_scan(self, image):
        # JPEG-Metadatensegmente überspringen und komprimierte Bilddaten vergleichen.
        data = image.read_bytes()
        offset = 2  # SOI
        while data[offset:offset + 2] != b"\xff\xda":  # SOS
            size = int.from_bytes(data[offset + 2:offset + 4], "big")
            offset += 2 + size
        # Trailer (z. B. Samsung-Vorschaubilder) gehören zu den entfernten Metadaten.
        return data[offset:data.index(b"\xff\xd9", offset) + 2]

    def test_jpeg_removes_private_tags_and_preserves_orientation_and_image_data(self):
        source = ROOT / "assets/images/mocs/MarvelCity/MarvelCity_1.jpg"
        original = source.read_bytes()
        image = self.site / "nested directory" / "PHOTO.JPEG"
        image.parent.mkdir()
        shutil.copyfile(source, image)
        self.exiftool(
            "-overwrite_original", "-GPSLatitude=48.2", "-GPSLongitude=16.3",
            "-Artist=Private Person", "-Make=Private Camera",
            "-DateTimeOriginal=2026:01:02 03:04:05", "-Orientation#=6",
            "-XMP-dc:Creator=Private Person", "-IPTC:By-line=Private Person",
            "-Comment=Private comment", image,
        )
        before = self.jpeg_scan(image)
        self.assertIn("GPSLatitude", self.metadata(image, "-GPSLatitude"))

        result = self.clean()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        tags = self.metadata(image, "-EXIF:all", "-XMP:all", "-IPTC:all", "-Comment")
        tags.pop("SourceFile")
        self.assertEqual(tags.pop("Orientation"), 6)
        # ExifTool kann beim Erhalten von Orientation technische Pflichtfelder anlegen.
        self.assertLessEqual(set(tags), {
            "YCbCrPositioning", "XResolution", "YResolution", "ResolutionUnit",
        })
        self.assertEqual(self.jpeg_scan(image), before)
        self.assertEqual(source.read_bytes(), original)
        self.assertFalse(list(self.site.rglob("*_original")))

    def test_png_removes_text_and_exif_metadata(self):
        image = self.site / "logo.png"
        shutil.copyfile(ROOT / "assets/images/logo-small.png", image)
        self.exiftool(
            "-overwrite_original", "-PNG:Author=Private Person",
            "-PNG:Comment=Private comment", "-XMP-dc:Creator=Private Person",
            "-EXIF:GPSLatitude=48.2", image,
        )
        self.assertIn("Author", self.metadata(image, "-PNG:Author"))
        result = self.clean()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        tags = self.metadata(image, "-EXIF:all", "-XMP:all", "-PNG:Author", "-Comment")
        self.assertEqual(set(tags), {"SourceFile"})
        self.assertFalse(list(self.site.rglob("*_original")))

    def test_webp_and_gif_remove_xmp_metadata(self):
        fixtures = {
            "gif": "R0lGODdhAgACAIEAAP8AAAAAAAAAAAAAACwAAAAAAgACAAAIBgABCAQQEAA7",
            "webp": "UklGRjwAAABXRUJQVlA4IDAAAADQAQCdASoCAAIAAUAmJaACdLoB+AADsAD+8ut//NgVzXPv9//S4P0uD9Lg/9KQAAA=",
        }
        for extension, encoded in fixtures.items():
            with self.subTest(format=extension):
                image = self.site / f"test.{extension}"
                image.write_bytes(base64.b64decode(encoded))
                self.exiftool(
                    "-overwrite_original", "-XMP-dc:Creator=Private Person", image,
                )
                self.assertIn("Creator", self.metadata(image, "-XMP:all"))
                result = self.clean()
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                tags = self.metadata(image, "-XMP:all", "-EXIF:all", "-Comment")
                self.assertEqual(set(tags), {"SourceFile"})

    def test_non_images_are_unchanged_and_empty_image_set_succeeds(self):
        page = self.site / "index.html"
        page.write_text("<h1>Unverändert</h1>", encoding="utf-8")
        original = page.read_bytes()
        result = self.clean()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(page.read_bytes(), original)

    def test_missing_build_directory_fails(self):
        self.assertNotEqual(self.clean(self.site / "missing").returncode, 0)

    def test_corrupt_image_fails_instead_of_allowing_upload(self):
        (self.site / "broken.jpg").write_bytes(b"not an image")
        self.assertNotEqual(self.clean().returncode, 0)

    def test_repeated_cleanup_succeeds(self):
        shutil.copyfile(ROOT / "assets/images/logo-small.png", self.site / "logo.png")
        for _ in range(2):
            result = self.clean()
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
