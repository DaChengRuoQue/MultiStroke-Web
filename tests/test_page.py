from html.parser import HTMLParser
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "index.html"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_body = False
        self.body_tags = []
        self.body_text = []
        self.video_attributes = None
        self.external_dependency_tags = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "body":
            self.in_body = True
        elif self.in_body:
            self.body_tags.append(tag)
            if tag == "video":
                self.video_attributes = attributes

        if tag in {"link", "script"}:
            self.external_dependency_tags.append((tag, attributes))

    def handle_endtag(self, tag):
        if tag == "body":
            self.in_body = False

    def handle_data(self, data):
        if self.in_body and data.strip():
            self.body_text.append(data.strip())


class VideoPageTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(PAGE.exists(), "index.html must exist")
        self.html = PAGE.read_text(encoding="utf-8")
        self.parser = PageParser()
        self.parser.feed(self.html)

    def test_video_is_the_only_visible_body_content(self):
        self.assertEqual(self.parser.body_tags, ["video"])
        self.assertEqual(self.parser.body_text, [])

    def test_video_uses_native_manual_playback_controls(self):
        attributes = self.parser.video_attributes
        self.assertIsNotNone(attributes)
        self.assertIn("controls", attributes)
        self.assertIn("playsinline", attributes)
        self.assertNotIn("autoplay", attributes)
        self.assertNotIn("loop", attributes)
        self.assertEqual(attributes.get("preload"), "metadata")

    def test_video_uses_the_existing_local_asset(self):
        self.assertEqual(
            self.parser.video_attributes.get("src"),
            "MultiStroke.mp4",
        )
        self.assertTrue((ROOT / "MultiStroke.mp4").is_file())

    def test_page_has_no_external_dependencies(self):
        self.assertEqual(self.parser.external_dependency_tags, [])

    def test_video_is_contained_within_the_viewport(self):
        self.assertRegex(
            self.html,
            re.compile(
                r"video\s*\{[^}]*max-width:\s*100vw;"
                r"[^}]*max-height:\s*100vh;"
                r"[^}]*object-fit:\s*contain;",
                re.DOTALL,
            ),
        )

    def test_video_uses_dynamic_viewport_height(self):
        self.assertRegex(
            self.html,
            re.compile(
                r"body\s*\{[^}]*height:\s*100vh;"
                r"[^}]*height:\s*100dvh;",
                re.DOTALL,
            ),
        )
        self.assertRegex(
            self.html,
            re.compile(
                r"video\s*\{[^}]*max-height:\s*100vh;"
                r"[^}]*max-height:\s*100dvh;",
                re.DOTALL,
            ),
        )


if __name__ == "__main__":
    unittest.main()
