import json
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from unittest import mock

from pipeline import bot
from pipeline.bot import build_handler, handle_update, parse_start, start_keyboard

CFG = {
    "BOT_TOKEN": "T",
    "OWNER_CHAT_ID": "100",
    "CHANNEL_INVITE_URL": "https://t.me/+abc",
}


class ParseStart(unittest.TestCase):
    def test_source_payload(self):
        self.assertEqual(parse_start("/start threads"), "threads")

    def test_no_payload_is_direct(self):
        self.assertEqual(parse_start("/start"), "direct")

    def test_botname_suffix(self):
        self.assertEqual(parse_start("/start@vibecoding_start_bot threads"), "threads")

    def test_payload_truncated_to_64(self):
        self.assertEqual(parse_start("/start " + "a" * 70), "a" * 64)

    def test_other_command_none(self):
        self.assertIsNone(parse_start("/help"))
        self.assertIsNone(parse_start("привет"))
        self.assertIsNone(parse_start(""))


class StartKeyboard(unittest.TestCase):
    def test_invite_row_first(self):
        kb = start_keyboard("https://t.me/+abc", "threads")
        self.assertEqual(
            kb["inline_keyboard"][0],
            [{"text": "📚 Открыть канал", "url": "https://t.me/+abc"}],
        )

    def test_experience_callbacks(self):
        kb = start_keyboard("https://t.me/+abc", "threads")
        self.assertEqual(
            kb["inline_keyboard"][1][0]["callback_data"], "exp:threads:novice"
        )
        self.assertEqual(
            kb["inline_keyboard"][1][1]["callback_data"], "exp:threads:coder"
        )


def start_update(chat_id=500, text="/start threads", first_name="Аня"):
    return {
        "message": {
            "message_id": 10,
            "chat": {"id": chat_id},
            "from": {"id": 5001, "first_name": first_name},
            "text": text,
        }
    }


class HandleStart(unittest.TestCase):
    def test_greeting_invite_and_owner_log(self):
        with mock.patch.object(bot, "api") as api_mock:
            handle_update(start_update(), CFG)
        user_call, owner_call = api_mock.call_args_list
        self.assertEqual(user_call.args[1], "sendMessage")
        self.assertEqual(user_call.args[2]["chat_id"], 500)
        self.assertEqual(user_call.args[2]["text"], bot.GREETING)
        self.assertEqual(
            user_call.args[2]["reply_markup"]["inline_keyboard"][0][0]["url"],
            "https://t.me/+abc",
        )
        self.assertEqual(owner_call.args[2]["chat_id"], "100")
        self.assertEqual(
            owner_call.args[2]["text"], "🚀 /start source=threads (id=5001)"
        )

    def test_no_invite_omits_markup(self):
        cfg = {"BOT_TOKEN": "T", "OWNER_CHAT_ID": "100"}
        with mock.patch.object(bot, "api") as api_mock:
            handle_update(start_update(), cfg)
        self.assertNotIn("reply_markup", api_mock.call_args_list[0].args[2])

    def test_no_owner_single_send(self):
        cfg = {"BOT_TOKEN": "T", "CHANNEL_INVITE_URL": "https://t.me/+abc"}
        with mock.patch.object(bot, "api") as api_mock:
            handle_update(start_update(), cfg)
        self.assertEqual(api_mock.call_count, 1)

    def test_direct_source_logged(self):
        with mock.patch.object(bot, "api") as api_mock:
            handle_update(start_update(text="/start"), CFG)
        self.assertIn("source=direct", api_mock.call_args_list[1].args[2]["text"])


class HandleText(unittest.TestCase):
    def test_free_text_forwarded_to_owner(self):
        with mock.patch.object(bot, "api") as api_mock:
            handle_update(start_update(text="как начать?"), CFG)
        (call,) = api_mock.call_args_list
        self.assertEqual(call.args[1], "forwardMessage")
        self.assertEqual(call.args[2]["chat_id"], "100")
        self.assertEqual(call.args[2]["from_chat_id"], 500)
        self.assertEqual(call.args[2]["message_id"], 10)

    def test_owner_chat_not_forwarded(self):
        with mock.patch.object(bot, "api") as api_mock:
            handle_update(start_update(chat_id=100, text="заметка"), CFG)
        api_mock.assert_not_called()


class HandleJoins(unittest.TestCase):
    def join_update(self, first_name="Вика", members=None):
        if members is None:
            members = [{"id": 77, "first_name": first_name}]
        return {
            "message": {
                "message_id": 11,
                "chat": {"id": -100123, "type": "supergroup"},
                "from": {"id": 77, "first_name": first_name},
                "new_chat_members": members,
            }
        }

    def test_join_notifies_owner_and_greets_group(self):
        with mock.patch.object(bot, "api") as api_mock:
            handle_update(self.join_update(), CFG)
        owner_call, group_call = api_mock.call_args_list
        self.assertEqual(owner_call.args[2]["chat_id"], "100")
        self.assertEqual(owner_call.args[2]["text"], "👋 новый участник: id=77")
        self.assertEqual(group_call.args[2]["chat_id"], -100123)
        self.assertEqual(group_call.args[2]["text"], bot.GROUP_GREETING)

    def test_bot_members_skipped(self):
        update = self.join_update(members=[{"id": 78, "is_bot": True}])
        with mock.patch.object(bot, "api") as api_mock:
            handle_update(update, CFG)
        api_mock.assert_not_called()

    def test_large_batch_greets_nothing(self):
        update = self.join_update(
            members=[{"id": i} for i in range(bot.JOIN_GREET_BATCH_LIMIT + 1)]
        )
        with mock.patch.object(bot, "api") as api_mock:
            handle_update(update, CFG)
        (owner_call,) = api_mock.call_args_list
        self.assertEqual(owner_call.args[2]["chat_id"], "100")

    def test_join_without_owner_greets_group(self):
        cfg = {"BOT_TOKEN": "T"}
        with mock.patch.object(bot, "api") as api_mock:
            handle_update(self.join_update(), cfg)
        (group_call,) = api_mock.call_args_list
        self.assertEqual(group_call.args[2]["chat_id"], -100123)

    def test_empty_members_not_forwarded(self):
        update = self.join_update()
        update["message"]["new_chat_members"] = []
        with mock.patch.object(bot, "api") as api_mock:
            handle_update(update, CFG)
        (call,) = api_mock.call_args_list
        self.assertEqual(call.args[1], "forwardMessage")


class HandleCallback(unittest.TestCase):
    def callback(self, data):
        return {
            "callback_query": {
                "id": "cb1",
                "data": data,
                "from": {"id": 6001, "first_name": "Боря"},
            }
        }

    def test_answer_and_owner_log(self):
        with mock.patch.object(bot, "api") as api_mock:
            handle_update(self.callback("exp:threads:novice"), CFG)
        answer, owner = api_mock.call_args_list
        self.assertEqual(answer.args[1], "answerCallbackQuery")
        self.assertEqual(owner.args[1], "sendMessage")
        self.assertEqual(
            owner.args[2]["text"], "🎚 опыт: novice (source=threads) (id=6001)"
        )

    def test_malformed_data_answered_without_log(self):
        with mock.patch.object(bot, "api") as api_mock:
            handle_update(self.callback("exp:"), CFG)
        self.assertEqual(api_mock.call_count, 1)
        self.assertEqual(api_mock.call_args_list[0].args[1], "answerCallbackQuery")

    def test_unknown_data_answered_without_log(self):
        with mock.patch.object(bot, "api") as api_mock:
            handle_update(self.callback("zzz"), CFG)
        self.assertEqual(api_mock.call_count, 1)


class UnknownUpdate(unittest.TestCase):
    def test_ignored(self):
        with mock.patch.object(bot, "api") as api_mock:
            handle_update({"edited_message": {}}, CFG)
        api_mock.assert_not_called()


class HandleReactionCount(unittest.TestCase):
    def count_update(self):
        return {
            "message_reaction_count": {
                "chat": {"id": -100200},
                "message_id": 45,
                "date": 1790000000,
                "reactions": [
                    {"type": {"type": "emoji", "emoji": "👍"}, "total_count": 3},
                    {"type": {"type": "emoji", "emoji": "❤"}, "total_count": 2},
                ],
            }
        }

    def test_owner_gets_aggregate_line(self):
        with mock.patch.object(bot, "api") as api_mock:
            handle_update(self.count_update(), CFG)
        (call,) = api_mock.call_args_list
        self.assertEqual(call.args[2]["chat_id"], "100")
        self.assertEqual(call.args[2]["text"], "📊 Пост 45: 5 реакций")

    def test_without_owner_ignored(self):
        cfg = {"BOT_TOKEN": "T"}
        with mock.patch.object(bot, "api") as api_mock:
            handle_update(self.count_update(), cfg)
        api_mock.assert_not_called()


class WebhookServer(unittest.TestCase):
    def setUp(self):
        self.server = ThreadingHTTPServer(
            ("127.0.0.1", 0), build_handler(CFG, "SEKRIT")
        )
        self.port = self.server.server_address[1]
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()

    def post(self, path, body, secret=None):
        headers = {"Content-Type": "application/json"}
        if secret is not None:
            headers["X-Telegram-Bot-Api-Secret-Token"] = secret
        request = urllib.request.Request(
            f"http://127.0.0.1:{self.port}{path}",
            data=body,
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=5) as response:
                return response.status, json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            return error.code, None

    def test_health_get(self):
        with urllib.request.urlopen(
            f"http://127.0.0.1:{self.port}/", timeout=5
        ) as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(response.read(), b"ok")

    def test_wrong_path_404(self):
        status, _ = self.post("/other", b"{}", secret="SEKRIT")
        self.assertEqual(status, 404)

    def test_wrong_secret_401(self):
        status, _ = self.post("/webhook", b"{}", secret="NOPE")
        self.assertEqual(status, 401)

    def test_missing_secret_401(self):
        status, _ = self.post("/webhook", b"{}")
        self.assertEqual(status, 401)

    def test_bad_json_400(self):
        status, _ = self.post("/webhook", b"not json", secret="SEKRIT")
        self.assertEqual(status, 400)

    def test_valid_update_200_and_dispatched(self):
        with mock.patch.object(bot, "api"):
            status, body = self.post(
                "/webhook", json.dumps(start_update()).encode("utf-8"), secret="SEKRIT"
            )
        self.assertEqual(status, 200)
        self.assertEqual(body, {"ok": True})

    def test_api_failure_still_200(self):
        with mock.patch.object(bot, "api", side_effect=RuntimeError("сбой")):
            status, _ = self.post(
                "/webhook", json.dumps(start_update()).encode("utf-8"), secret="SEKRIT"
            )
        self.assertEqual(status, 200)

    def test_unexpected_handler_error_still_200(self):
        with mock.patch.object(bot, "handle_update", side_effect=ValueError("сбой")):
            status, _ = self.post(
                "/webhook", json.dumps(start_update()).encode("utf-8"), secret="SEKRIT"
            )
        self.assertEqual(status, 200)


class CmdServe(unittest.TestCase):
    def test_missing_webhook_secret_exit_2(self):
        cfg = {"BOT_TOKEN": "T", "CHANNEL_INVITE_URL": "https://t.me/+abc"}
        self.assertEqual(bot.cmd_serve(cfg, "127.0.0.1", 0), 2)


if __name__ == "__main__":
    unittest.main()
