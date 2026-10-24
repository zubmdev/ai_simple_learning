import posixpath
import re

MAX_CHARS = 32768
MAX_BLOCKS = 500
MAX_MEDIA = 50
MAX_TABLE_COLS = 20

IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".mp4",
    ".mp3",
    ".ogg",
    ".zip",
    ".svg",
}

SUPPORTED_HTML = {
    "a",
    "aside",
    "audio",
    "b",
    "blockquote",
    "br",
    "caption",
    "cite",
    "code",
    "del",
    "details",
    "em",
    "figcaption",
    "figure",
    "footer",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
    "i",
    "img",
    "input",
    "ins",
    "li",
    "mark",
    "ol",
    "p",
    "pre",
    "s",
    "strike",
    "strong",
    "sub",
    "summary",
    "sup",
    "table",
    "td",
    "th",
    "tr",
    "u",
    "ul",
    "video",
    "tg-button",
    "tg-button-row",
    "tg-collage",
    "tg-document",
    "tg-emoji",
    "tg-map",
    "tg-math",
    "tg-math-block",
    "tg-reference",
    "tg-slideshow",
    "tg-spoiler",
    "tg-time",
}

_LINK_RE = re.compile(r'(!?)\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
_HTML_RE = re.compile(r"<(/?)([a-zA-Z][a-zA-Z0-9-]*)")
_LIST_RE = re.compile(r"^(\-|\*|\+|\d+\.) ")
_CODE_SPAN_RE = re.compile(r"`[^`]*`")
_HR_MASK = "\x00hr\x00"
_PART_MARKER_RESERVE = 24


def _resolve(md_path, url):
    if re.match(r"^(https?://|mailto:|tel:|tg://)", url) or url.startswith("#"):
        return None
    base, _, frag = url.partition("#")
    fragment = f"#{frag}" if frag else ""
    repo_path = posixpath.normpath(posixpath.join(posixpath.dirname(md_path), base))
    return repo_path, fragment


def _rewrite_link(match, md_path, raw_base, blob_base):
    bang, label, url = match.group(1), match.group(2), match.group(3)
    resolved = _resolve(md_path, url)
    if resolved is None:
        return match.group(0)
    repo_path, fragment = resolved
    suffix = posixpath.splitext(repo_path)[1].lower()
    if bang or suffix in IMAGE_EXTENSIONS:
        return f"{bang}[{label}]({raw_base}/{repo_path})"
    return f"[{label}]({blob_base}/{repo_path}{fragment})"


def _mask_code_spans(line):
    spans = []

    def stash(match):
        spans.append(match.group(0))
        return f"\x00{len(spans) - 1}\x00"

    return _CODE_SPAN_RE.sub(stash, line), spans


def _rewrite_links(text, md_path, raw_base, blob_base):
    out = []
    in_fence = False
    for line in text.split("\n"):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        masked, spans = _mask_code_spans(line)
        rewritten = _LINK_RE.sub(
            lambda m: _rewrite_link(m, md_path, raw_base, blob_base), masked
        )
        for i, span in enumerate(spans):
            rewritten = rewritten.replace(f"\x00{i}\x00", span)
        out.append(rewritten)
    return "\n".join(out)


def _lift_inline_media(text):
    lines = text.split("\n")
    out = []
    in_fence = False
    for line in lines:
        if line.strip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence or _CODE_SPAN_RE.search(line):
            out.append(line)
            continue
        images = _IMAGE_RE.findall(line)
        if not images:
            out.append(line)
            continue
        remainder = _IMAGE_RE.sub("", line).strip()
        if not remainder:
            out.append(line)
            continue
        out.append(remainder)
        out.append("")
        out.extend(f"![]({url})" for _, url in images)
    return "\n".join(out)


def _day_label(md_path):
    name = posixpath.basename(md_path)
    week = re.search(r"Week_(\d+)", md_path)
    day = re.match(r"Day_(\d+)\.md$", name)
    day_num = day.group(1) if day else None
    if week and day_num:
        return f"Неделя {week.group(1)} · День {day_num}"
    return f"День {day_num}" if day_num else name


def convert(text, md_path, raw_base, blob_base):
    text = _rewrite_links(text, md_path, raw_base, blob_base)
    text = _lift_inline_media(text)
    label = _day_label(md_path)
    index_url = f"{blob_base}/README.md"
    self_url = f"{blob_base}/{md_path}"
    header = f"> 📚 [Vibe Coding]({index_url}) · **{label}**"
    footer = f"\n\n---\n\n📖 [Читать урок на GitHub]({self_url}) · 📚 [Все уроки]({index_url})\n"
    return f"{header}\n\n{text.rstrip()}{footer}"


def _hard_split(part, budget):
    out = []
    while len(part) > budget:
        cut = 0
        in_fence = False
        pos = 0
        for line in part.split("\n"):
            if pos >= budget:
                break
            stripped = line.strip()
            if not in_fence and not stripped and pos > 0:
                cut = pos - 1
            if stripped.startswith("```"):
                in_fence = not in_fence
            pos += len(line) + 1
        if cut <= 0:
            cut = budget
        out.append(part[:cut])
        part = part[cut:].lstrip("\n")
    out.append(part)
    return out


def _mask_fence_hrs(text):
    out = []
    in_fence = False
    for line in text.split("\n"):
        if line.strip().startswith("```"):
            in_fence = not in_fence
        elif in_fence and line == "---":
            out.append(_HR_MASK)
            continue
        out.append(line)
    return "\n".join(out)


def split_message(text, max_chars=MAX_CHARS):
    if len(text) <= max_chars:
        return [text]
    budget = max_chars - _PART_MARKER_RESERVE
    segments = re.split(r"\n---\n", _mask_fence_hrs(text))
    parts = []
    buf = ""
    for seg in segments:
        seg = seg.replace(_HR_MASK, "---")
        candidate = seg if not buf else f"{buf}\n---\n{seg}"
        if len(candidate) <= budget or not buf:
            buf = candidate
        else:
            parts.append(buf)
            buf = seg
    if buf:
        parts.append(buf)
    final = []
    for part in parts:
        final.extend(_hard_split(part, budget))
    if len(final) == 1:
        return final
    total = len(final)
    return [f"{part}\n\n*(часть {i}/{total})*" for i, part in enumerate(final, 1)]


def stats(text):
    blocks = 0
    in_fence = False
    prev_blank = True
    table_cols = 0
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("```"):
            if not in_fence:
                blocks += 1
            in_fence = not in_fence
            prev_blank = True
            continue
        if in_fence:
            continue
        if not stripped:
            prev_blank = True
            continue
        if stripped.startswith("|"):
            table_cols = max(table_cols, stripped.count("|") - 1)
            blocks += 1
        elif re.match(r"^#{1,6} ", stripped) or stripped == "---":
            blocks += 1
        elif _LIST_RE.match(stripped):
            blocks += 1
        elif stripped.startswith(">"):
            blocks += 1
        elif _IMAGE_RE.fullmatch(stripped):
            blocks += 1
        elif prev_blank:
            blocks += 1
            prev_blank = False
            continue
        else:
            continue
        prev_blank = True
    return {
        "chars": len(text),
        "blocks": blocks,
        "media": len(_IMAGE_RE.findall(text)),
        "table_cols": table_cols,
    }


def warnings(text, max_chars=MAX_CHARS):
    issues = []
    if len(text) > max_chars:
        issues.append(
            f"текст {len(text)} символов — превышает лимит {MAX_CHARS}, нужен сплит"
        )
    in_fence = False
    link_warned = False
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        masked, _ = _mask_code_spans(line)
        if not link_warned:
            for match in re.finditer(r"\]\((\.{1,2}/[^)]*)\)", masked):
                issues.append(f"осталась относительная ссылка: {match.group(1)}")
                link_warned = True
                break
        for match in _HTML_RE.finditer(masked):
            name = match.group(2).lower()
            if name not in SUPPORTED_HTML:
                issues.append(f"неподдерживаемый HTML-тег <{name}>")
                break
    return issues
