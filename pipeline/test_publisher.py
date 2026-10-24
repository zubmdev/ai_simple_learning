import os
import tempfile
import unittest
import urllib.error
from unittest import mock
from pathlib import Path

from pipeline import publisher
from pipeline.publisher import check_links, load_env, mask, repo_bases


class LoadEnv(unittest.TestCase):
    def test_parses_quotes_and_skips_comments(self):
        with tempfile.NamedTemporaryFile("w", suffix=".env", delete=False) as f:
            f.write('BOT_TOKEN="abc"\n# comment\nCHANNEL_ID=@chan\n\n')
            path = f.name
        try:
            values = load_env(path)
            self.assertEqual(values["BOT_TOKEN"], "abc")
            self.assertEqual(values["CHANNEL_ID"], "@chan")
        finally:
            os.unlink(path)

    def test_os_environ_wins(self):
        with tempfile.NamedTemporaryFile("w", suffix=".env", delete=False) as f:
            f.write("REPO_BRANCH=file\n")
            path = f.name
        old = os.environ.get("REPO_BRANCH")
        try:
            os.environ["REPO_BRANCH"] = "cli"
            values = load_env(path)
            self.assertEqual(values["REPO_BRANCH"], "cli")
        finally:
            if old is None:
                del os.environ["REPO_BRANCH"]
            else:
                os.environ["REPO_BRANCH"] = old
            os.unlink(path)

    def test_missing_file_empty(self):
        self.assertEqual(load_env("/nonexistent/.env"), {})


class RepoBases(unittest.TestCase):
    def test_github_derives_raw_host(self):
        raw, blob = repo_bases("https://github.com/acme/course/", "main")
        self.assertEqual(raw, "https://raw.githubusercontent.com/acme/course/main")
        self.assertEqual(blob, "https://github.com/acme/course/blob/main")

    def test_other_host_uses_raw_path(self):
        raw, blob = repo_bases("https://gitlab.com/x/y", "dev")
        self.assertEqual(raw, "https://gitlab.com/x/y/raw/dev")
        self.assertEqual(blob, "https://gitlab.com/x/y/blob/dev")


class CheckLinks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "a.md").write_text(
            "[ок](./b.md) ![к](./img.png) [вверх](#якорь) [вне](https://x.ru)",
            encoding="utf-8",
        )
        (self.root / "b.md").write_text("ок", encoding="utf-8")
        (self.root / "img.png").touch()

    def tearDown(self):
        self.tmp.cleanup()

    def test_all_targets_exist(self):
        self.assertEqual(check_links("a.md", self.root), [])

    def test_missing_target_reported(self):
        (self.root / "a.md").write_text("[х](./nope.md)", encoding="utf-8")
        self.assertEqual(check_links("a.md", self.root), ["nope.md"])

    def test_fenced_and_inline_code_ignored(self):
        (self.root / "a.md").write_text(
            "```\n[ф](./ghost.md)\n```\nтекст `[инлайн](./ghost2.md)`",
            encoding="utf-8",
        )
        self.assertEqual(check_links("a.md", self.root), [])

    def test_fragment_resolved(self):
        (self.root / "a.md").write_text("[х](./b.md#раздел)", encoding="utf-8")
        self.assertEqual(check_links("a.md", self.root), [])


class Mask(unittest.TestCase):
    def test_token_hidden(self):
        out = mask(
            "POST https://api.telegram.org/botSEKRIT/sendMessage failed", "SEKRIT"
        )
        self.assertNotIn("SEKRIT", out)
        self.assertIn("***", out)


class PostMasking(unittest.TestCase):
    TOKEN = "SEKRIT123"

    def test_url_error_masks_token(self):
        with mock.patch(
            "urllib.request.urlopen",
            side_effect=urllib.error.URLError(
                OSError(f"connection to bot{self.TOKEN} refused")
            ),
        ):
            with self.assertRaises(RuntimeError) as ctx:
                publisher._post(self.TOKEN, "sendRichMessage", b"{}", {})
        self.assertNotIn(self.TOKEN, str(ctx.exception))
        self.assertIn("***", str(ctx.exception))

    def test_timeout_raises_runtime_error(self):
        with mock.patch(
            "urllib.request.urlopen", side_effect=TimeoutError("timed out")
        ):
            with self.assertRaises(RuntimeError):
                publisher._post(self.TOKEN, "sendRichMessage", b"{}", {})


if __name__ == "__main__":
    unittest.main()
