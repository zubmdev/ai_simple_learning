import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
import uuid
from pathlib import Path

from pipeline.convert import (
    MAX_BLOCKS,
    MAX_CHARS,
    MAX_MEDIA,
    MAX_TABLE_COLS,
    _CODE_SPAN_RE,
    _resolve,
    convert,
    split_message,
    stats,
    warnings,
)

API_BASE = "https://api.telegram.org"
PLACEHOLDER_RAW = "https://raw.githubusercontent.com/PLACEHOLDER/course/main"
PLACEHOLDER_BLOB = "https://github.com/PLACEHOLDER/course/blob/main"

_MD_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)[^)]*\)")

CONFIG_KEYS = frozenset(
    {
        "BOT_TOKEN",
        "CHANNEL_ID",
        "REPO_URL",
        "REPO_BRANCH",
        "OWNER_CHAT_ID",
        "DISCUSS_URL",
        "CHANNEL_INVITE_URL",
        "WEBHOOK_SECRET",
    }
)


def load_env(path):
    values = {}
    env_path = Path(path)
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            values[key.strip()] = value.strip().strip('"').strip("'")
    for key in sorted(set(values) | CONFIG_KEYS):
        if key in os.environ:
            values[key] = os.environ[key]
    return values


def repo_bases(repo_url, branch):
    repo_url = repo_url.rstrip("/")
    blob_base = f"{repo_url}/blob/{branch}"
    prefix = "https://github.com/"
    if repo_url.startswith(prefix):
        raw_base = (
            f"https://raw.githubusercontent.com/{repo_url[len(prefix) :]}/{branch}"
        )
    else:
        raw_base = f"{repo_url}/raw/{branch}"
    return raw_base, blob_base


def _outside_code(text):
    out = []
    in_fence = False
    for line in text.split("\n"):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else _CODE_SPAN_RE.sub("", line))
    return "\n".join(out)


def check_links(md_rel, repo_root):
    path = Path(repo_root, *md_rel.split("/"))
    text = _outside_code(path.read_text(encoding="utf-8"))
    missing = []
    for match in _MD_LINK_RE.finditer(text):
        resolved = _resolve(md_rel, match.group(1))
        if resolved is None:
            continue
        repo_path, _ = resolved
        if not Path(repo_root, *repo_path.split("/")).exists():
            missing.append(repo_path)
    return missing


def validate(text):
    issues = list(warnings(text, max_chars=10**9))
    s = stats(text)
    if s["blocks"] > MAX_BLOCKS:
        issues.append(f"блоков {s['blocks']} — превышает лимит {MAX_BLOCKS}")
    if s["media"] > MAX_MEDIA:
        issues.append(f"медиа {s['media']} — превышает лимит {MAX_MEDIA}")
    if s["table_cols"] > MAX_TABLE_COLS:
        issues.append(
            f"колонок таблицы {s['table_cols']} — превышает лимит {MAX_TABLE_COLS}"
        )
    return issues


def mask(text, token):
    if token:
        text = text.replace(token, "***")
    return text


def _post(token, method, data, headers):
    url = f"{API_BASE}/bot{token}/{method}"
    request = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", "replace")
        raise RuntimeError(f"{method}: HTTP {error.code}: {mask(body, token)}")
    except OSError as error:
        raise RuntimeError(f"{method}: {mask(str(error), token)}")
    except json.JSONDecodeError:
        raise RuntimeError(f"{method}: некорректный JSON-ответ")


def build_reply_markup(blob_url=None, discuss_url=None):
    rows = []
    if blob_url:
        rows.append([{"text": "📄 Урок на GitHub", "url": blob_url}])
    if discuss_url:
        rows.append([{"text": "💬 Обсудить", "url": discuss_url}])
    if not rows:
        return None
    return {"inline_keyboard": rows}


def send_rich_message(token, chat_id, markdown_text):
    payload = {
        "chat_id": chat_id,
        "rich_message": {"markdown": markdown_text},
    }
    return _post(
        token,
        "sendRichMessage",
        json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        {"Content-Type": "application/json"},
    )


def send_buttons(token, chat_id, markup):
    payload = {
        "chat_id": chat_id,
        "text": "🔗 Ссылки урока:",
        "reply_markup": markup,
    }
    return _post(
        token,
        "sendMessage",
        json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        {"Content-Type": "application/json"},
    )


def _multipart(fields, file_field, filename, content):
    boundary = uuid.uuid4().hex
    chunks = []
    for name, value in fields:
        chunks.append(
            (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'
                f"{value}\r\n"
            ).encode("utf-8")
        )
    chunks.append(
        (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="{file_field}"; '
            f'filename="{filename}"\r\n'
            f"Content-Type: text/markdown\r\n\r\n"
        ).encode("utf-8")
    )
    chunks.append(content)
    chunks.append(f"\r\n--{boundary}--\r\n".encode("utf-8"))
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def send_document(token, chat_id, filename, content, caption=None):
    fields = [("chat_id", chat_id)]
    if caption:
        fields.append(("caption", caption))
    body, content_type = _multipart(fields, "document", filename, content)
    return _post(token, "sendDocument", body, {"Content-Type": content_type})


def _message_label(response):
    if not isinstance(response, dict):
        return "?"
    result = response.get("result")
    if not isinstance(result, dict):
        return "?"
    if "message_id" in result:
        return str(result["message_id"])
    nested = result.get("rich_message")
    if isinstance(nested, dict) and "message_id" in nested:
        return str(nested["message_id"])
    return "?"


def _resolve_bases(cfg):
    if cfg.get("REPO_URL"):
        branch = cfg.get("REPO_BRANCH") or "main"
        return repo_bases(cfg["REPO_URL"], branch), False
    return (PLACEHOLDER_RAW, PLACEHOLDER_BLOB), True


def _prepare(md_rel, repo_root, raw_base, blob_base):
    path = Path(repo_root, *md_rel.split("/"))
    src = path.read_text(encoding="utf-8")
    problems = []
    for target in check_links(md_rel, repo_root):
        problems.append(f"битая ссылка: {target} (файл не найден)")
    converted = convert(src, md_rel, raw_base, blob_base)
    problems.extend(validate(converted))
    parts = split_message(converted)
    for part in parts:
        if len(part) > MAX_CHARS:
            problems.append(f"часть {len(part)} символов — превышает лимит {MAX_CHARS}")
            break
    return src, converted, parts, problems


def _report(md_rel, parts, problems, converted):
    s = stats(converted)
    status = "ОШИБКА" if problems else "OK"
    print(
        f"{status} {md_rel}: частей {len(parts)}, "
        f"символов {s['chars']}, блоков {s['blocks']}, медиа {s['media']}"
    )
    for problem in problems:
        print(f"  ⚠ {problem}")


def cmd_check(files, cfg, repo_root):
    (raw_base, blob_base), placeholder = _resolve_bases(cfg)
    failed = 0
    for md_rel in files:
        md_rel = os.path.normpath(md_rel).replace(os.sep, "/")
        if not Path(repo_root, *md_rel.split("/")).exists():
            print(f"ОШИБКА {md_rel}: файл не найден")
            failed += 1
            continue
        _, converted, parts, problems = _prepare(md_rel, repo_root, raw_base, blob_base)
        _report(md_rel, parts, problems, converted)
        if problems:
            failed += 1
    if placeholder:
        print(
            "REPO_URL/REPO_BRANCH не заданы — ссылки в статистике условные, "
            "для --publish задай их в .env"
        )
    return 1 if failed else 0


def cmd_dry_run(files, cfg, repo_root):
    (raw_base, blob_base), _ = _resolve_bases(cfg)
    failed = 0
    for md_rel in files:
        md_rel = os.path.normpath(md_rel).replace(os.sep, "/")
        if not Path(repo_root, *md_rel.split("/")).exists():
            print(f"ОШИБКА {md_rel}: файл не найден")
            failed += 1
            continue
        _, converted, parts, problems = _prepare(md_rel, repo_root, raw_base, blob_base)
        _report(md_rel, parts, problems, converted)
        markup = build_reply_markup(
            f"{blob_base}/{md_rel}", cfg.get("DISCUSS_URL") or None
        )
        if markup:
            labels = [b["text"] for row in markup["inline_keyboard"] for b in row]
            print(f"  кнопки (отдельным сообщением): {', '.join(labels)}")
        if problems:
            failed += 1
            continue
        for i, part in enumerate(parts, 1):
            print(f"\n{'=' * 20} часть {i}/{len(parts)} {'=' * 20}\n")
            print(part)
    return 1 if failed else 0


def cmd_publish(files, cfg, repo_root):
    missing = [
        name for name in ("BOT_TOKEN", "CHANNEL_ID", "REPO_URL") if not cfg.get(name)
    ]
    if missing:
        print(f"не заданы обязательные переменные: {', '.join(missing)}")
        return 2
    token = cfg["BOT_TOKEN"]
    chat_id = cfg["CHANNEL_ID"]
    (raw_base, blob_base), _ = _resolve_bases(cfg)
    failed = 0
    for md_rel in files:
        md_rel = os.path.normpath(md_rel).replace(os.sep, "/")
        path = Path(repo_root, *md_rel.split("/"))
        if not path.exists():
            print(f"ОШИБКА {md_rel}: файл не найден")
            failed += 1
            continue
        src, converted, parts, problems = _prepare(
            md_rel, repo_root, raw_base, blob_base
        )
        _report(md_rel, parts, problems, converted)
        if problems:
            failed += 1
            continue
        markup = build_reply_markup(
            f"{blob_base}/{md_rel}", cfg.get("DISCUSS_URL") or None
        )
        for i, part in enumerate(parts, 1):
            response = send_rich_message(token, chat_id, part)
            print(
                f"  отправлена часть {i}/{len(parts)} (message_id {_message_label(response)})"
            )
        if markup:
            response = send_buttons(token, chat_id, markup)
            print(f"  отправлены кнопки (message_id {_message_label(response)})")
        caption = f"📄 Исходник урока: {blob_base}/{md_rel}"
        response = send_document(
            token, chat_id, path.name, src.encode("utf-8"), caption
        )
        print(f"  приложен исходник (message_id {_message_label(response)})")
    return 1 if failed else 0


def build_parser():
    parser = argparse.ArgumentParser(
        prog="publisher",
        description="Публикация уроков курса в Telegram-канал через Bot API",
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="офлайн-проверка файлов")
    mode.add_argument(
        "--dry-run", action="store_true", help="показать посты без отправки"
    )
    mode.add_argument("--publish", action="store_true", help="отправить в канал")
    parser.add_argument("files", nargs="+", help="пути к Day_*.md от корня репозитория")
    parser.add_argument(
        "--repo-url", help="URL репозитория, напр. https://github.com/user/repo"
    )
    parser.add_argument("--repo-branch", help="ветка репозитория (по умолчанию main)")
    parser.add_argument(
        "--discuss-url",
        help="URL кнопки «Обсудить» (переопределяет DISCUSS_URL из .env)",
    )
    parser.add_argument("--env", default=".env", help="путь к .env-файлу")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    cfg = load_env(args.env)
    if args.repo_url:
        cfg["REPO_URL"] = args.repo_url
    if args.repo_branch:
        cfg["REPO_BRANCH"] = args.repo_branch
    if args.discuss_url:
        cfg["DISCUSS_URL"] = args.discuss_url
    repo_root = Path.cwd()
    try:
        if args.check:
            return cmd_check(args.files, cfg, repo_root)
        if args.dry_run:
            return cmd_dry_run(args.files, cfg, repo_root)
        return cmd_publish(args.files, cfg, repo_root)
    except RuntimeError as error:
        print(f"ОШИБКА: {mask(str(error), cfg.get('BOT_TOKEN', ''))}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
