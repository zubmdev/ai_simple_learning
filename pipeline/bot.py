import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from pipeline.publisher import load_env, mask

API_BASE = "https://api.telegram.org"
EXP_PREFIX = "exp:"
ALLOWED_UPDATES = ["message", "callback_query"]

GREETING = (
    "Привет! 👋 Это бот бесплатного курса «AI - это просто».\n\n"
    "Каждый день в 09:00 в канале выходит один урок: короткая теория, "
    "практика и ежедневная миссия. Нажимай кнопку ниже — все уроки уже там."
)

OWNER_TEXT_START = "🚀 /start source={source}{name}"
OWNER_TEXT_EXP = "🎚 опыт: {tag} (source={source}){name}"


def api(token, method, payload):
    request = urllib.request.Request(
        f"{API_BASE}/bot{token}/{method}",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", "replace")
        raise RuntimeError(f"{method}: HTTP {error.code}: {mask(body, token)}")
    except OSError as error:
        raise RuntimeError(f"{method}: {mask(str(error), token)}")
    except json.JSONDecodeError:
        raise RuntimeError(f"{method}: некорректный JSON-ответ")


def parse_start(text):
    parts = (text or "").split()
    if not parts:
        return None
    command = parts[0]
    if command != "/start" and not command.startswith("/start@"):
        return None
    if len(parts) > 1:
        return parts[1][:64]
    return "direct"


def display_name(user):
    if not isinstance(user, dict):
        return ""
    return user.get("first_name") or user.get("username") or ""


def name_suffix(user):
    name = display_name(user)
    return f" — {name}" if name else ""


def start_keyboard(invite_url, source):
    rows = [[{"text": "📚 Открыть канал", "url": invite_url}]]
    rows.append(
        [
            {"text": "Я новичок", "callback_data": f"{EXP_PREFIX}{source}:novice"},
            {"text": "Я программист", "callback_data": f"{EXP_PREFIX}{source}:coder"},
        ]
    )
    return {"inline_keyboard": rows}


def handle_update(update, cfg):
    token = cfg.get("BOT_TOKEN", "")
    owner = cfg.get("OWNER_CHAT_ID", "")
    message = update.get("message")
    if isinstance(message, dict):
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text") or ""
        source = parse_start(text)
        if source:
            payload = {"chat_id": chat_id, "text": GREETING}
            invite = cfg.get("CHANNEL_INVITE_URL", "")
            if invite:
                payload["reply_markup"] = start_keyboard(invite, source)
            api(token, "sendMessage", payload)
            if owner:
                api(
                    token,
                    "sendMessage",
                    {
                        "chat_id": owner,
                        "text": OWNER_TEXT_START.format(
                            source=source, name=name_suffix(message.get("from"))
                        ),
                    },
                )
            return
        if owner and chat_id is not None and str(chat_id) != str(owner):
            api(
                token,
                "forwardMessage",
                {
                    "chat_id": owner,
                    "from_chat_id": chat_id,
                    "message_id": message.get("message_id"),
                },
            )
        return
    callback = update.get("callback_query")
    if isinstance(callback, dict):
        api(token, "answerCallbackQuery", {"callback_query_id": callback.get("id")})
        data = callback.get("data") or ""
        if owner and data.startswith(EXP_PREFIX):
            parts = data.split(":", 2)
            while len(parts) < 3:
                parts.append("")
            _, source, tag = parts
            if source and tag:
                api(
                    token,
                    "sendMessage",
                    {
                        "chat_id": owner,
                        "text": OWNER_TEXT_EXP.format(
                            source=source,
                            tag=tag,
                            name=name_suffix(callback.get("from")),
                        ),
                    },
                )


def build_handler(cfg, secret):
    class WebhookHandler(BaseHTTPRequestHandler):
        server_version = "course-bot/1.0"

        def _respond(self, code, body=b'{"ok":true}', content_type="application/json"):
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            self._respond(200, b"ok", "text/plain")

        def do_POST(self):
            if self.path != "/webhook":
                self._respond(404, b'{"ok":false}')
                return
            if secret and self.headers.get("X-Telegram-Bot-Api-Secret-Token") != secret:
                self._respond(401, b'{"ok":false}')
                return
            length = int(self.headers.get("Content-Length") or 0)
            try:
                update = json.loads(self.rfile.read(length).decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                self._respond(400, b'{"ok":false}')
                return
            try:
                handle_update(update, cfg)
            except RuntimeError as error:
                sys.stderr.write(f"webhook: {error}\n")
            self._respond(200)

        def log_message(self, format, *args):
            sys.stderr.write("%s - %s\n" % (self.address_string(), format % args))

    return WebhookHandler


def cmd_serve(cfg, host, port):
    missing = [
        name for name in ("BOT_TOKEN", "CHANNEL_INVITE_URL") if not cfg.get(name)
    ]
    if missing:
        print(f"не заданы обязательные переменные: {', '.join(missing)}")
        return 2
    if not cfg.get("OWNER_CHAT_ID"):
        print("OWNER_CHAT_ID не задан — события /start не будут записываться")
    server = ThreadingHTTPServer(
        (host, port), build_handler(cfg, cfg.get("WEBHOOK_SECRET", ""))
    )
    print(f"webhook слушает http://{host}:{port}/webhook")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


def cmd_set_webhook(cfg, url):
    payload = {"url": url, "allowed_updates": ALLOWED_UPDATES}
    secret = cfg.get("WEBHOOK_SECRET", "")
    if secret:
        payload["secret_token"] = secret
    api(cfg["BOT_TOKEN"], "setWebhook", payload)
    print(f"webhook установлен: {url}")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(
        prog="bot",
        description="Stateless webhook-шлюз бота курса: /start, кнопки, пересылка сообщений владельцу",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--serve", action="store_true", help="запустить HTTP-сервер (по умолчанию)"
    )
    mode.add_argument(
        "--set-webhook", metavar="URL", help="зарегистрировать webhook у Telegram"
    )
    parser.add_argument(
        "--host", default="0.0.0.0", help="интерфейс сервера (по умолчанию 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("PORT", "8000")),
        help="порт сервера (по умолчанию $PORT или 8000)",
    )
    parser.add_argument("--env", default=".env", help="путь к .env-файлу")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    cfg = load_env(args.env)
    try:
        if args.set_webhook:
            return cmd_set_webhook(cfg, args.set_webhook)
        return cmd_serve(cfg, args.host, args.port)
    except RuntimeError as error:
        print(f"ОШИБКА: {mask(str(error), cfg.get('BOT_TOKEN', ''))}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
