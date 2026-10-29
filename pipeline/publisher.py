import argparse
import json
import os
import re
import sys
import uuid
from pathlib import Path
from typing import NamedTuple

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
from pipeline.telegram import mask, post_raw as _post

PLACEHOLDER_RAW = "https://raw.githubusercontent.com/PLACEHOLDER/course/main"
PLACEHOLDER_BLOB = "https://github.com/PLACEHOLDER/course/blob/main"

SCHEDULE_FILE_COL = 2
SCHEDULE_STATUS_COL = 4

SUBSCRIBERS_LOG = Path("docs/metrics/subscribers.log")

WELCOME_LINE = (
    "👋 За сутки канал пополнили ещё {n} человек. "
    "Застряли на миссии урока — напишите боту, разберём."
)

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


def norm_rel(path):
    return os.path.normpath(path).replace(os.sep, "/")


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


def missing_config(cfg, names):
    return [name for name in names if not cfg.get(name)]


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
        "text": "💬 Обсуждение урока — ссылки тут:",
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


class RepoBases(NamedTuple):
    raw_base: str
    blob_base: str
    placeholder: bool


def _resolve_bases(cfg):
    if cfg.get("REPO_URL"):
        branch = cfg.get("REPO_BRANCH") or "main"
        raw_base, blob_base = repo_bases(cfg["REPO_URL"], branch)
        return RepoBases(raw_base, blob_base, False)
    return RepoBases(PLACEHOLDER_RAW, PLACEHOLDER_BLOB, True)


def growth_footer(log_path):
    path = Path(log_path)
    if not path.exists():
        return None
    lines = [
        line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
    ]
    if len(lines) < 2:
        return None
    try:
        previous = int(lines[-2].split("\t")[1])
        last = int(lines[-1].split("\t")[1])
    except (IndexError, ValueError):
        return None
    delta = last - previous
    if delta <= 0:
        return None
    return WELCOME_LINE.format(n=delta)


def _prepare(md_rel, repo_root, raw_base, blob_base, footer=None):
    path = Path(repo_root, *md_rel.split("/"))
    src = path.read_text(encoding="utf-8")
    problems = []
    for target in check_links(md_rel, repo_root):
        problems.append(f"битая ссылка: {target} (файл не найден)")
    converted = convert(src, md_rel, raw_base, blob_base)
    if footer:
        converted = converted.rstrip() + "\n\n" + footer
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


def _process(files, repo_root, bases, on_report=None, on_ready=None, footer=None):
    failed = 0
    for md_rel in files:
        md_rel = norm_rel(md_rel)
        path = Path(repo_root, *md_rel.split("/"))
        if not path.exists():
            print(f"ОШИБКА {md_rel}: файл не найден")
            failed += 1
            continue
        src, converted, parts, problems = _prepare(
            md_rel, repo_root, bases.raw_base, bases.blob_base, footer
        )
        _report(md_rel, parts, problems, converted)
        if on_report:
            on_report(md_rel, path, src, parts, bases)
        if problems:
            failed += 1
            continue
        if on_ready and not on_ready(md_rel, path, src, parts, bases):
            failed += 1
    return failed


def cmd_check(files, cfg, repo_root):
    bases = _resolve_bases(cfg)
    failed = _process(files, repo_root, bases)
    if bases.placeholder:
        print(
            "REPO_URL/REPO_BRANCH не заданы — ссылки в статистике условные, "
            "для --publish задай их в .env"
        )
    return 1 if failed else 0


def cmd_dry_run(files, cfg, repo_root):
    bases = _resolve_bases(cfg)

    def on_report(md_rel, path, src, parts, bases):
        markup = build_reply_markup(
            f"{bases.blob_base}/{md_rel}", cfg.get("DISCUSS_URL") or None
        )
        if markup:
            labels = [b["text"] for row in markup["inline_keyboard"] for b in row]
            print(f"  кнопки (отдельным сообщением): {', '.join(labels)}")

    def on_ready(md_rel, path, src, parts, bases):
        for i, part in enumerate(parts, 1):
            print(f"\n{'=' * 20} часть {i}/{len(parts)} {'=' * 20}\n")
            print(part)
        return True

    return 1 if _process(files, repo_root, bases, on_report, on_ready) else 0


def mark_published(files, schedule_path):
    pending = {f.replace(os.sep, "/") for f in files}
    path = Path(schedule_path)
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    out = []
    marked = []
    for i, line in enumerate(lines):
        cols = line.split("\t")
        if (
            i > 0
            and len(cols) > SCHEDULE_FILE_COL
            and cols[SCHEDULE_FILE_COL] in pending
            and (
                len(cols) <= SCHEDULE_STATUS_COL or cols[SCHEDULE_STATUS_COL] != "done"
            )
        ):
            while len(cols) <= SCHEDULE_STATUS_COL:
                cols.append("")
            cols[SCHEDULE_STATUS_COL] = "done"
            line = "\t".join(cols)
            marked.append(cols[SCHEDULE_FILE_COL])
        out.append(line)
    if marked:
        path.write_text("\n".join(out) + "\n", encoding="utf-8")
    return marked


def cmd_publish(files, cfg, repo_root):
    missing = missing_config(cfg, ("BOT_TOKEN", "CHANNEL_ID", "REPO_URL"))
    if missing:
        print(f"не заданы обязательные переменные: {', '.join(missing)}")
        return 2, []
    token = cfg["BOT_TOKEN"]
    chat_id = cfg["CHANNEL_ID"]
    bases = _resolve_bases(cfg)
    footer = growth_footer(Path(repo_root, SUBSCRIBERS_LOG))
    if footer:
        print(f"  приветственная строка: {footer}")
    published = []

    def on_ready(md_rel, path, src, parts, bases):
        markup = build_reply_markup(
            f"{bases.blob_base}/{md_rel}", cfg.get("DISCUSS_URL") or None
        )
        try:
            for i, part in enumerate(parts, 1):
                response = send_rich_message(token, chat_id, part)
                print(
                    f"  отправлена часть {i}/{len(parts)} (message_id {_message_label(response)})"
                )
            if markup:
                response = send_buttons(token, chat_id, markup)
                print(f"  отправлены кнопки (message_id {_message_label(response)})")
            caption = f"📄 Исходник урока: {bases.blob_base}/{md_rel}"
            response = send_document(
                token, chat_id, path.name, src.encode("utf-8"), caption
            )
            print(f"  приложен исходник (message_id {_message_label(response)})")
        except RuntimeError as error:
            print(f"ОШИБКА {md_rel}: {mask(str(error), token)}")
            return False
        published.append(md_rel)
        return True

    failed = _process(files, repo_root, bases, on_ready=on_ready, footer=footer)
    return (1 if failed else 0), published


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
    parser.add_argument(
        "--mark-published",
        action="store_true",
        help="после успешной отправки пометить строки в launch/schedule.tsv как done",
    )
    parser.add_argument("--env", default=".env", help="путь к .env-файлу")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.mark_published and not args.publish:
        parser.error("--mark-published работает только вместе с --publish")
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
        code, published = cmd_publish(args.files, cfg, repo_root)
        if args.mark_published and published:
            schedule = Path(repo_root, "launch", "schedule.tsv")
            for md_rel in mark_published(published, schedule):
                print(f"  launch/schedule.tsv: помечено done ({md_rel})")
        return code
    except RuntimeError as error:
        print(f"ОШИБКА: {mask(str(error), cfg.get('BOT_TOKEN', ''))}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
