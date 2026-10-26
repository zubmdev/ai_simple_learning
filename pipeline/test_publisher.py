import json
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


class BuildReplyMarkup(unittest.TestCase):
    def test_empty_is_none(self):
        self.assertIsNone(publisher.build_reply_markup(None, None))

    def test_github_only(self):
        url = "https://github.com/a/b/blob/main/ru/beginner/Week_1/Day_1.md"
        markup = publisher.build_reply_markup(url)
        self.assertEqual(
            markup,
            {
                "inline_keyboard": [
                    [{"text": "📄 Урок на GitHub", "url": url}],
                ]
            },
        )

    def test_discuss_only(self):
        markup = publisher.build_reply_markup(discuss_url="https://t.me/c/1")
        self.assertEqual(
            markup,
            {"inline_keyboard": [[{"text": "💬 Обсудить", "url": "https://t.me/c/1"}]]},
        )

    def test_both_rows(self):
        markup = publisher.build_reply_markup("https://x", "https://y")
        self.assertEqual(len(markup["inline_keyboard"]), 2)


class SendRichMessageMarkup(unittest.TestCase):
    def test_markup_in_payload(self):
        markup = {"inline_keyboard": [[{"text": "к", "url": "https://x"}]]}
        with mock.patch.object(publisher, "_post", return_value={}) as post_mock:
            publisher.send_rich_message("T", "@c", "текст", markup)
        payload = json.loads(post_mock.call_args.args[2])
        self.assertEqual(payload["reply_markup"], markup)

    def test_no_markup_omits_key(self):
        with mock.patch.object(publisher, "_post", return_value={}) as post_mock:
            publisher.send_rich_message("T", "@c", "текст")
        payload = json.loads(post_mock.call_args.args[2])
        self.assertNotIn("reply_markup", payload)


class PublishButtons(unittest.TestCase):
    def test_markup_on_first_part_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "day.md").write_text("Привет", encoding="utf-8")
            cfg = {
                "BOT_TOKEN": "T",
                "CHANNEL_ID": "@c",
                "REPO_URL": "https://github.com/a/b",
                "REPO_BRANCH": "main",
                "DISCUSS_URL": "https://t.me/c/1",
            }
            payloads = []

            def capture(token, method, data, headers):
                try:
                    payloads.append(json.loads(data))
                except json.JSONDecodeError:
                    payloads.append({})
                return {"result": {"message_id": 1}}

            with mock.patch.object(publisher, "_post", side_effect=capture):
                code = publisher.cmd_publish(["day.md"], cfg, root)
            self.assertEqual(code, 0)
            rich = [p for p in payloads if "rich_message" in p]
            self.assertEqual(len(rich), 1)
            self.assertEqual(
                rich[0]["reply_markup"]["inline_keyboard"][0][0]["url"],
                "https://github.com/a/b/blob/main/day.md",
            )
            self.assertEqual(
                rich[0]["reply_markup"]["inline_keyboard"][1][0]["url"],
                "https://t.me/c/1",
            )

    def test_no_discuss_url_single_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "day.md").write_text("Привет", encoding="utf-8")
            cfg = {
                "BOT_TOKEN": "T",
                "CHANNEL_ID": "@c",
                "REPO_URL": "https://github.com/a/b",
            }
            payloads = []

            def capture(token, method, data, headers):
                try:
                    payloads.append(json.loads(data))
                except json.JSONDecodeError:
                    payloads.append({})
                return {"result": {"message_id": 1}}

            with mock.patch.object(publisher, "_post", side_effect=capture):
                code = publisher.cmd_publish(["day.md"], cfg, root)
            self.assertEqual(code, 0)
            rich = [p for p in payloads if "rich_message" in p]
            self.assertEqual(len(rich[0]["reply_markup"]["inline_keyboard"]), 1)


if __name__ == "__main__":
    unittest.main()
