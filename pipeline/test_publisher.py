import json
import os
import tempfile
import unittest
import urllib.error
from unittest import mock
from pathlib import Path

from pipeline import publisher
from pipeline.publisher import check_links, load_env, mark_published, mask, repo_bases

SCHEDULE_HEADER = "date\ttime_utc\tfile\tnote\tstatus\n"


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


class SendButtons(unittest.TestCase):
    MARKUP = {
        "inline_keyboard": [[{"text": "к", "url": "https://x"}]],
    }

    def test_sends_markup_via_send_message(self):
        with mock.patch.object(publisher, "_post", return_value={}) as post_mock:
            publisher.send_buttons("T", "@c", self.MARKUP)
        self.assertEqual(post_mock.call_args.args[1], "sendMessage")
        payload = json.loads(post_mock.call_args.args[2])
        self.assertEqual(payload["reply_markup"], self.MARKUP)
        self.assertEqual(payload["chat_id"], "@c")

    def test_rich_message_omits_markup_key(self):
        with mock.patch.object(publisher, "_post", return_value={}) as post_mock:
            publisher.send_rich_message("T", "@c", "текст")
        payload = json.loads(post_mock.call_args.args[2])
        self.assertNotIn("reply_markup", payload)


class PublishButtons(unittest.TestCase):
    def capture_into(self, payloads):
        def capture(token, method, data, headers):
            try:
                payloads.append((method, json.loads(data)))
            except json.JSONDecodeError:
                payloads.append((method, {}))
            return {"result": {"message_id": 1}}

        return capture

    def publish(self, cfg):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "day.md").write_text("Привет", encoding="utf-8")
            payloads = []
            with mock.patch.object(
                publisher, "_post", side_effect=self.capture_into(payloads)
            ):
                code, published = publisher.cmd_publish(["day.md"], cfg, root)
            self.assertEqual(code, 0)
            self.assertEqual(published, ["day.md"])
            return payloads

    def test_buttons_sent_as_separate_message(self):
        payloads = self.publish(
            {
                "BOT_TOKEN": "T",
                "CHANNEL_ID": "@c",
                "REPO_URL": "https://github.com/a/b",
                "REPO_BRANCH": "main",
                "DISCUSS_URL": "https://t.me/c/1",
            }
        )
        rich = [p for m, p in payloads if m == "sendRichMessage"]
        self.assertEqual(len(rich), 1)
        self.assertNotIn("reply_markup", rich[0])
        button_calls = [p for m, p in payloads if m == "sendMessage"]
        self.assertEqual(len(button_calls), 1)
        rows = button_calls[0]["reply_markup"]["inline_keyboard"]
        self.assertEqual(rows[0][0]["url"], "https://github.com/a/b/blob/main/day.md")
        self.assertEqual(rows[1][0]["url"], "https://t.me/c/1")

    def test_no_discuss_url_single_row(self):
        payloads = self.publish(
            {
                "BOT_TOKEN": "T",
                "CHANNEL_ID": "@c",
                "REPO_URL": "https://github.com/a/b",
            }
        )
        button_calls = [p for m, p in payloads if m == "sendMessage"]
        self.assertEqual(len(button_calls), 1)
        rows = button_calls[0]["reply_markup"]["inline_keyboard"]
        self.assertEqual(len(rows), 1)


class LoadEnvKnownKeys(unittest.TestCase):
    def test_known_key_from_os_environ_without_file(self):
        old = os.environ.get("OWNER_CHAT_ID")
        try:
            os.environ["OWNER_CHAT_ID"] = "42"
            values = load_env("/nonexistent/.env")
            self.assertEqual(values.get("OWNER_CHAT_ID"), "42")
        finally:
            if old is None:
                del os.environ["OWNER_CHAT_ID"]
            else:
                os.environ["OWNER_CHAT_ID"] = old

    def test_unknown_env_key_ignored(self):
        old = os.environ.get("NOT_A_CONFIG_KEY")
        try:
            os.environ["NOT_A_CONFIG_KEY"] = "x"
            values = load_env("/nonexistent/.env")
            self.assertNotIn("NOT_A_CONFIG_KEY", values)
        finally:
            if old is None:
                del os.environ["NOT_A_CONFIG_KEY"]
            else:
                os.environ["NOT_A_CONFIG_KEY"] = old

    def test_file_value_overridden_by_environ_for_known_key(self):
        with tempfile.NamedTemporaryFile("w", suffix=".env", delete=False) as f:
            f.write("OWNER_CHAT_ID=1\n")
            path = f.name
        old = os.environ.get("OWNER_CHAT_ID")
        try:
            os.environ["OWNER_CHAT_ID"] = "2"
            values = load_env(path)
            self.assertEqual(values["OWNER_CHAT_ID"], "2")
        finally:
            if old is None:
                del os.environ["OWNER_CHAT_ID"]
            else:
                os.environ["OWNER_CHAT_ID"] = old
            os.unlink(path)


class MarkPublished(unittest.TestCase):
    HEADER = SCHEDULE_HEADER

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.tsv = Path(self.tmp.name) / "schedule.tsv"

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, body):
        self.tsv.write_text(self.HEADER + body, encoding="utf-8")

    def read(self):
        return self.tsv.read_text(encoding="utf-8")

    def test_marks_only_matching_rows(self):
        self.write(
            "2026-10-27\t06:00\td1.md\ta\ttodo\n2026-10-28\t06:00\td2.md\tb\ttodo\n"
        )
        self.assertEqual(mark_published(["d1.md"], self.tsv), ["d1.md"])
        text = self.read()
        self.assertIn("d1.md\ta\tdone\n", text)
        self.assertIn("d2.md\tb\ttodo\n", text)
        self.assertTrue(text.startswith(self.HEADER))

    def test_pads_missing_status_column(self):
        self.tsv.write_text(
            "date\ttime_utc\tfile\tnote\n2026-10-27\t06:00\td1.md\ta\n",
            encoding="utf-8",
        )
        self.assertEqual(mark_published(["d1.md"], self.tsv), ["d1.md"])
        self.assertIn("2026-10-27\t06:00\td1.md\ta\tdone\n", self.read())

    def test_already_done_not_remarked(self):
        body = "2026-10-27\t06:00\td1.md\ta\tdone\n"
        self.write(body)
        self.assertEqual(mark_published(["d1.md"], self.tsv), [])
        self.assertEqual(self.read(), self.HEADER + body)

    def test_missing_schedule_file_noop(self):
        self.assertEqual(mark_published(["d1.md"], self.tsv), [])
        self.assertFalse(self.tsv.exists())

    def test_unrelated_file_untouched(self):
        self.write("2026-10-27\t06:00\td1.md\ta\ttodo\n")
        self.assertEqual(mark_published(["other.md"], self.tsv), [])
        self.assertIn("d1.md\ta\ttodo\n", self.read())


class MarkPublishedFlag(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old_cwd = os.getcwd()
        os.chdir(self.tmp.name)

    def tearDown(self):
        os.chdir(self.old_cwd)
        self.tmp.cleanup()

    def env_and_schedule(self, files):
        Path(".env").write_text("BOT_TOKEN=T\nCHANNEL_ID=@c\n", encoding="utf-8")
        Path("launch").mkdir()
        Path("launch", "schedule.tsv").write_text(
            SCHEDULE_HEADER + files, encoding="utf-8"
        )

    def test_requires_publish_mode(self):
        with self.assertRaises(SystemExit):
            publisher.main(["--check", "--mark-published", "d.md"])

    def test_publish_marks_rows_and_returns_zero(self):
        self.env_and_schedule("2026-10-27\t06:00\tday.md\tx\ttodo\n")
        Path("day.md").write_text("Привет", encoding="utf-8")
        with mock.patch.object(
            publisher, "_post", return_value={"result": {"message_id": 1}}
        ):
            code = publisher.main(
                [
                    "--publish",
                    "--mark-published",
                    "day.md",
                    "--repo-url",
                    "https://github.com/a/b",
                ]
            )
        self.assertEqual(code, 0)
        text = Path("launch", "schedule.tsv").read_text(encoding="utf-8")
        self.assertIn("day.md\tx\tdone\n", text)

    def test_runtime_error_mid_send_marks_only_completed(self):
        self.env_and_schedule(
            "2026-10-27\t06:00\ta.md\tx\ttodo\n2026-10-27\t07:00\tb.md\ty\ttodo\n"
        )
        Path("a.md").write_text("Ок", encoding="utf-8")
        Path("b.md").write_text("Пока", encoding="utf-8")
        calls = []

        def post(token, method, data, headers):
            calls.append(method)
            if len(calls) == 4:
                raise RuntimeError("sendRichMessage: HTTP 500: oops")
            return {"result": {"message_id": 1}}

        with mock.patch.object(publisher, "_post", side_effect=post):
            code = publisher.main(
                [
                    "--publish",
                    "--mark-published",
                    "a.md",
                    "b.md",
                    "--repo-url",
                    "https://github.com/a/b",
                ]
            )
        self.assertEqual(code, 1)
        self.assertEqual(len(calls), 4)
        text = Path("launch", "schedule.tsv").read_text(encoding="utf-8")
        self.assertIn("a.md\tx\tdone\n", text)
        self.assertIn("b.md\ty\ttodo\n", text)

    def test_partial_failure_marks_only_published(self):
        self.env_and_schedule(
            "2026-10-27\t06:00\ta.md\tx\ttodo\n2026-10-27\t07:00\tb.md\ty\ttodo\n"
        )
        Path("a.md").write_text("Ок", encoding="utf-8")
        Path("b.md").write_text("[х](./nope.md)", encoding="utf-8")
        with mock.patch.object(
            publisher, "_post", return_value={"result": {"message_id": 1}}
        ):
            code = publisher.main(
                [
                    "--publish",
                    "--mark-published",
                    "a.md",
                    "b.md",
                    "--repo-url",
                    "https://github.com/a/b",
                ]
            )
        self.assertEqual(code, 1)
        text = Path("launch", "schedule.tsv").read_text(encoding="utf-8")
        self.assertIn("a.md\tx\tdone\n", text)
        self.assertIn("b.md\ty\ttodo\n", text)


if __name__ == "__main__":
    unittest.main()
