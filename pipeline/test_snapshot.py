import tempfile
import unittest
from datetime import datetime, timezone
from unittest import mock
from pathlib import Path

from pipeline import snapshot
from pipeline.snapshot import append_count, read_last_count, read_last_date


class ReadLastCount(unittest.TestCase):
    def test_missing_file_none(self):
        self.assertIsNone(read_last_count("/nonexistent/sub.log"))

    def test_last_line_wins(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp, "sub.log")
            path.write_text(
                "2026-11-01T06:30:00Z\t10\n2026-11-02T06:30:00Z\t12\n",
                encoding="utf-8",
            )
            self.assertEqual(read_last_count(path), 12)

    def test_garbage_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp, "sub.log")
            path.write_text("мусор\n", encoding="utf-8")
            self.assertIsNone(read_last_count(path))


class AppendCount(unittest.TestCase):
    def test_appends_and_creates_dirs(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp, "metrics", "sub.log")
            now = datetime(2026, 11, 1, 6, 30, tzinfo=timezone.utc)
            append_count(path, 42, now)
            self.assertEqual(
                path.read_text(encoding="utf-8"), "2026-11-01T06:30:00Z\t42\n"
            )


class ReadLastDate(unittest.TestCase):
    def test_missing_file_none(self):
        self.assertIsNone(read_last_date("/nonexistent/sub.log"))

    def test_last_line_date(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp, "sub.log")
            path.write_text(
                "2026-11-01T06:30:00Z\t10\n2026-11-02T18:00:00Z\t12\n",
                encoding="utf-8",
            )
            self.assertEqual(read_last_date(path), "2026-11-02")


class Main(unittest.TestCase):
    def run_main(self, log):
        cfg = {"BOT_TOKEN": "T", "CHANNEL_ID": "@chan", "OWNER_CHAT_ID": "100"}
        sent = []

        def fake_api(token, method, payload):
            if method == "getChatMemberCount":
                return {"ok": True, "result": 1240}
            sent.append(payload)
            return {"ok": True}

        with mock.patch.object(snapshot, "api", side_effect=fake_api):
            with mock.patch.object(snapshot, "load_env", return_value=cfg):
                code = snapshot.main(["--log", str(log)])
        return code, sent

    def test_delta_dmed_and_logged(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp, "metrics", "sub.log")
            log.parent.mkdir()
            log.write_text("2026-10-31T06:30:00Z\t1234\n", encoding="utf-8")
            code, sent = self.run_main(log)
            self.assertEqual(code, 0)
            last = log.read_text(encoding="utf-8").splitlines()[-1]
            self.assertEqual(last.split("\t")[1], "1240")
            self.assertEqual(len(sent), 1)
            self.assertEqual(sent[0]["chat_id"], "100")
            self.assertEqual(sent[0]["text"], "📈 Подписчиков: 1240 (+6)")

    def test_first_run_no_delta(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp, "sub.log")
            code, sent = self.run_main(log)
            self.assertEqual(code, 0)
            self.assertEqual(sent[0]["text"], "📈 Подписчиков: 1240")

    def test_same_day_rerun_skips(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp, "sub.log")
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            log.write_text(f"{today}T06:30:00Z\t1240\n", encoding="utf-8")
            code, sent = self.run_main(log)
            self.assertEqual(code, 0)
            self.assertEqual(sent, [])
            self.assertEqual(len(log.read_text(encoding="utf-8").splitlines()), 1)

    def test_missing_config(self):
        with mock.patch.object(snapshot, "load_env", return_value={}):
            self.assertEqual(snapshot.main(["--log", "x"]), 2)


if __name__ == "__main__":
    unittest.main()
