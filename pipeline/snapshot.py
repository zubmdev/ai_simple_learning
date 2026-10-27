import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from pipeline.bot import api
from pipeline.publisher import load_env, mask, missing_config

DEFAULT_LOG = "docs/metrics/subscribers.log"


def read_last_count(path):
    log_path = Path(path)
    if not log_path.exists():
        return None
    lines = [
        line
        for line in log_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not lines:
        return None
    try:
        return int(lines[-1].split("\t")[1])
    except (IndexError, ValueError):
        return None


def append_count(path, count, now=None):
    moment = now or datetime.now(timezone.utc)
    log_path = Path(path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as log_file:
        log_file.write(f"{moment.strftime('%Y-%m-%dT%H:%M:%SZ')}\t{count}\n")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="snapshot",
        description="Дневной снимок числа подписчиков канала в docs/metrics/subscribers.log",
    )
    parser.add_argument("--env", default=".env", help="путь к .env-файлу")
    parser.add_argument("--log", default=DEFAULT_LOG, help="файл журнала")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    cfg = load_env(args.env)
    missing = missing_config(cfg, ("BOT_TOKEN", "CHANNEL_ID"))
    if missing:
        print(f"не заданы обязательные переменные: {', '.join(missing)}")
        return 2
    token = cfg["BOT_TOKEN"]
    try:
        response = api(token, "getChatMemberCount", {"chat_id": cfg["CHANNEL_ID"]})
        count = response["result"]
        previous = read_last_count(args.log)
        append_count(args.log, count)
        if cfg.get("OWNER_CHAT_ID"):
            delta = ""
            if previous is not None:
                sign = "+" if count >= previous else ""
                delta = f" ({sign}{count - previous})"
            api(
                token,
                "sendMessage",
                {
                    "chat_id": cfg["OWNER_CHAT_ID"],
                    "text": f"📈 Подписчиков: {count}{delta}",
                },
            )
    except RuntimeError as error:
        print(f"ОШИБКА: {mask(str(error), token)}")
        return 2
    except (KeyError, TypeError, ValueError):
        print("ОШИБКА: некорректный ответ getChatMemberCount")
        return 2
    suffix = "" if previous is None else f" (было {previous})"
    print(f"подписчиков: {count}{suffix} → {args.log}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
