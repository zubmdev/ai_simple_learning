import email.message
import io
import json
import unittest
import urllib.error
from unittest import mock

from pipeline import telegram


def urlopen_response(body):
    response = mock.MagicMock()
    response.__enter__.return_value = response
    response.read.return_value = body
    return response


class Mask(unittest.TestCase):
    def test_token_hidden(self):
        self.assertEqual(telegram.mask("botT/x", "T"), "bot***/x")

    def test_empty_token_noop(self):
        self.assertEqual(telegram.mask("botT/x", ""), "botT/x")


class PostRaw(unittest.TestCase):
    def test_success_parses_json_and_builds_url(self):
        with mock.patch(
            "urllib.request.urlopen",
            return_value=urlopen_response(b'{"ok": true}'),
        ) as urlopen:
            out = telegram.post_raw("T", "getMe", b"{}", {})
        self.assertEqual(out, {"ok": True})
        request = urlopen.call_args.args[0]
        self.assertEqual(request.full_url, "https://api.telegram.org/botT/getMe")
        self.assertEqual(request.data, b"{}")

    def test_http_error_masks_token(self):
        error = urllib.error.HTTPError(
            "url", 500, "oops", email.message.Message(), io.BytesIO(b"botSEKRIT broke")
        )
        with mock.patch("urllib.request.urlopen", side_effect=error):
            with self.assertRaises(RuntimeError) as ctx:
                telegram.post_raw("SEKRIT", "send", b"{}", {})
        self.assertNotIn("SEKRIT", str(ctx.exception))
        self.assertIn("HTTP 500", str(ctx.exception))

    def test_os_error_masks_token(self):
        with mock.patch(
            "urllib.request.urlopen",
            side_effect=urllib.error.URLError(OSError("botSEKRIT refused")),
        ):
            with self.assertRaises(RuntimeError) as ctx:
                telegram.post_raw("SEKRIT", "send", b"{}", {})
        self.assertNotIn("SEKRIT", str(ctx.exception))

    def test_bad_json_raises(self):
        with mock.patch(
            "urllib.request.urlopen", return_value=urlopen_response(b"<html>")
        ):
            with self.assertRaises(RuntimeError):
                telegram.post_raw("T", "send", b"{}", {})

    def test_timeout_passes_default(self):
        with mock.patch(
            "urllib.request.urlopen",
            return_value=urlopen_response(b"{}"),
        ) as urlopen:
            telegram.post_raw("T", "send", b"{}", {})
        self.assertEqual(urlopen.call_args.kwargs["timeout"], 120)


class PostJson(unittest.TestCase):
    def test_encodes_payload_with_json_headers(self):
        with mock.patch(
            "urllib.request.urlopen",
            return_value=urlopen_response(b'{"ok": true}'),
        ) as urlopen:
            out = telegram.post_json("T", "sendMessage", {"chat_id": 1})
        self.assertEqual(out, {"ok": True})
        request = urlopen.call_args.args[0]
        self.assertEqual(request.headers["Content-type"], "application/json")
        self.assertEqual(json.loads(request.data), {"chat_id": 1})
        self.assertEqual(urlopen.call_args.kwargs["timeout"], 30)


if __name__ == "__main__":
    unittest.main()
