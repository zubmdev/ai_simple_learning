# Research: 2026 model refresh + Telegram publishing of Week 1

**Date:** 2026-10-24. Two parallel investigations against primary sources (ollama.com, console.groq.com, openrouter.ai, core.telegram.org, telegram.org blog, instantview.telegram.org, docs.github.com). Every claim cites its source; unverifiable items are marked **[UNVERIFIED]** or **[HUMAN CHECK]**.

**Standing caveat:** model catalogs and rate limits change weekly. Re-verify quarterly (per ADR-0003) and date-stamp every setup lesson.

---

## Part 1 — Model refresh (replace the legacy stack)

### 1.1 Summary of what must change

1. **Groq free tier no longer serves Llama.** `llama-3.1-8b-instant` and `llama-3.3-70b-versatile` are still listed but **Enterprise-only** (price/limits = "ContactSales"); `llama-3.1-70b-versatile` is **gone from the catalog** ([Groq models](https://console.groq.com/docs/models)). The free-tier workhorses are now `openai/gpt-oss-20b` and `openai/gpt-oss-120b`.
2. **ADR-0003 pins are half right.** `gpt-oss:20b` ✅, `gemma4:12b` ✅ ("Gemma 4 12B" is real), `qwen3.6:35b` ✅ exists — **but at 23–24 GB it does not fit the 16 GB tier** and must move to a "more than 16GB / CPU-offload" note ([ollama.com/library/qwen3.6](https://ollama.com/library/qwen3.6)). "Qwen2.5-Coder 7B/14B" still exist but are ~1 year stale; `qwen3:8b` exists but its 40K default context is weak for agent work ([ollama.com/library/qwen3/tags](https://ollama.com/library/qwen3/tags)).
3. **Tier 2 changes family:** `qwen3.5:2b` replaces `llama3.2:3b` / `qwen2.5-coder:1.5b/3b` ([ollama.com/library/qwen3.5](https://ollama.com/library/qwen3.5)).
4. **Gemini is [HUMAN CHECK]:** `ai.google.dev` did not load during research (transport errors ×3). Whether `gemini-3.1-flash-lite-preview` (used in `ru/beginner/Week_1/Day_3.md:247`) exists **could not be confirmed or refuted** — verify manually against [ai.google.dev/gemini-api/docs/models](https://ai.google.dev/gemini-api/docs/models) before editing the lesson. Do not guess a replacement ID.

### 1.2 Tier 1 — free cloud APIs

**Groq** (verified 2026-10-24, [models](https://console.groq.com/docs/models), [rate limits](https://console.groq.com/docs/rate-limits)):

| Model ID | Status | Free-tier limits |
|---|---|---|
| `openai/gpt-oss-20b` | Production — **primary pick for the course** | 30 RPM / 1,000 RPD / 8K TPM / 200K TPD |
| `openai/gpt-oss-120b` | Production — stronger reasoning | same shape |
| `qwen/qwen3.8-27b` | Preview ("may be discontinued at short notice") | same shape |
| `llama-3.1-8b-instant`, `llama-3.3-70b-versatile` | Enterprise-only | unusable for learners |
| `llama-3.1-70b-versatile` | not in catalog | treat as retired |

- Privacy: Groq does **not retain customer data by default**; Zero Data Retention toggle available; no training on customer data described ([Groq data policy](https://console.groq.com/docs/your-data)). Good default for the course.
- Bonus: Groq ships first-party guides for both course agents — `console.groq.com/docs/coding-with-groq/cline` and `.../opencode`.
- Caveat: per-plan limits sit behind an accordion on the docs page; re-check the Free-plan table at publish time.

**Gemini** — [HUMAN CHECK] (see 1.1.4).

**OpenRouter** (verified 2026-10-24, [limits](https://openrouter.ai/docs/api-reference/limits), [free variant](https://openrouter.ai/docs/guides/routing/model-variants/free.md)):

- Free caps: **20 req/min**; **50 req/day** if <10 credits ever purchased, **1,000 req/day** once ≥10 credits purchased.
- Notable `:free` coding-agent models seen: `recursive/flint-v1.0:free` (40B MoE, 262K ctx, "built for coding agents"), `xingchen-agi/xing4.0-29b-a4b:free` ([openrouter.ai/models](https://openrouter.ai/models)).
- Privacy: **some free-variant providers may train on prompts**; separate allow-training toggles for free and paid models in [privacy settings](https://openrouter.ai/settings/privacy). The MCP/security lesson must teach: opt out of training on free models immediately after signup.

### 1.3 Tier 2 — 4GB GPU (Ollama)

| Pull | Download | Why |
|---|---|---|
| `qwen3.5:2b` | 2.7–3.1 GB | **Primary.** Newest small Qwen, 256K ctx, tools/thinking ([library](https://ollama.com/library/qwen3.5)) |
| `qwen3:4b` | 2.5 GB | Runner-up, dense ([tags](https://ollama.com/library/qwen3/tags)) |
| `qwen3.5:0.8b` | ~1.2 GB | Fallback for old laptops |

Remove from lessons: `llama3.2:1b/3b` (~2 yrs stale), `qwen2.5-coder:1.5b/3b`, `phi3.5`.

### 1.4 Tier 3 — 16GB GPU (Ollama)

| Pull | Download | Why |
|---|---|---|
| `gpt-oss:20b` | 14 GB | **Flagship.** MXFP4, "runs on as little as 16GB memory", native tool calling ([library](https://ollama.com/library/gpt-oss)) |
| `gemma4:12b` | 7.7–8.0 GB | Long-context option, 256K ctx ([library](https://ollama.com/library/gemma4)) |
| `qwen3:14b` | 9.3 GB | Dense middle; 40K ctx is its weak spot |
| `qwen3-coder:30b` | 19 GB | Coder-specific; **needs CPU offload** ([library](https://ollama.com/library/qwen3-coder)) |
| `qwen3.6:35b` | 23–24 GB | **Beyond the tier** — mention only as "if you have more" ([library](https://ollama.com/library/qwen3.6)) |

### 1.5 Legacy → replacement map

| Legacy (where it sits in the repo) | Status 2026-10-24 | Replace with |
|---|---|---|
| `llama-3.3-70b-versatile`, `llama-3.1-8b-instant` (`ru/beginner/Week_1/Day_3.md:185-204`, `ru/beginner/Week_4/Day_5.md:70`) | Enterprise-only | `openai/gpt-oss-20b` / `gpt-oss-120b` |
| `llama-3.1-70b-versatile` (`ru/beginner/Week_4/Day_5.md:70`) | not in catalog | `openai/gpt-oss-120b` |
| `qwen2.5-coder:1.5b/3b`, `phi-3.5`, `llama3.2:1b/3b` (`ru/beginner/Week_1/Day_3.md:280-541`) | 1–2 yrs stale | `qwen3.5:0.8b` / `qwen3.5:2b` |
| `Llama 3.1` as 16GB path (`ru/beginner/Week_1/Day_2.md:434`, `Week_1/Day_3.md:75`) | stale | `gpt-oss:20b` |
| `qwen2.5-coder:7b/14b` (ADR-0003:15) | stale | `gemma4:12b` / `qwen3:14b`; coder: `qwen3-coder:30b` (offload) |
| `qwen3.6-35b` as a 16GB tier model (ADR-0003:15, plan §4) | wrong tier | move to ">16GB / offload" note |
| `gemini-3.1-flash-lite-preview` (`Week_1/Day_3.md:247`) | [HUMAN CHECK] | verify at ai.google.dev first |
| typo "grok" (`Week_1/Day_3.md:206`) | — | "Groq" |

### 1.6 Suggested ADR-0003 edits

1. Tier 1: Groq default → `openai/gpt-oss-20b` with the free-limit table; drop all `llama-*` Groq IDs; add OpenRouter free-cap + privacy-toggle rules; leave Gemini as "verify at publish".
2. Tier 2: pin `qwen3.5:2b`, fallback `qwen3:4b`; remove `llama3.2`, `qwen2.5-coder` small tags, `phi3.5`.
3. Tier 3: pin `gpt-oss:20b` + `gemma4:12b`; `qwen3-coder:30b` as offload note; **move `qwen3.6:35b` out of the tier**.
4. Add: "Model IDs verified 2026-10-24 against ollama.com / console.groq.com / openrouter.ai; re-verify quarterly."

---

## Part 2 — Publishing Week 1 in Telegram

### 2.1 TL;DR

The old constraints died in June 2026: Telegram bots can now send **rich messages** — GitHub-Flavored-Markdown-compatible posts (headings, tables, lists, code blocks, inline images) up to **32,768 characters** ([Bot API rich messages](https://core.telegram.org/bots/api/rich-messages), [June 11 2026 blog](https://telegram.org/blog/watch-apps-and-more)). Lessons are 10–40 KB, so **one lesson ≈ one natively-rendered post, images included**. Also: **Telegram's in-app browser now renders `.md` files natively** ([same blog post](https://telegram.org/blog/watch-apps-and-more#support-for-md-files)), so attaching the lesson file works for beginners too.

### 2.2 What formatting survives

| Surface | Headings/tables/lists | Inline images | Length cap |
|---|---|---|---|
| Classic `sendMessage` (MarkdownV2/HTML) | ✘ ([formatting options](https://core.telegram.org/bots/api/formatting)) | ✘ (media only via `sendPhoto`) | 4096 chars ([sendMessage](https://core.telegram.org/bots/api/methods/sendmessage)) |
| **Rich message (`sendRichMessage`)** | ✔ GFM-compatible, plus `<details>`, spoilers, copy-text buttons | ✔ via HTTP(S) URLs | **32,768 chars**, 500 blocks, 50 media ([rich-messages](https://core.telegram.org/bots/api/rich-messages)) |
| Manual post by admin | Only with **Premium** Rich Text Editor (headings/tables/code/inline media, [July 2026 blog](https://telegram.org/blog/communities-editor-invisible-messages)) | ✔ with Premium | 32,768 |
| Attached `.md` file | rendered in Telegram Browser after tap | if links are absolute | 50 MB upload ([Bot API](https://core.telegram.org/bots/api)) |

Raw lesson Markdown will NOT survive classic `parse_mode` (MarkdownV2 requires escaping 18 chars; no headings/tables) — automation via `sendRichMessage` is the reliable route.

### 2.3 Recommended pipeline (post per lesson)

1. Create a bot via [@BotFather](https://t.me/botfather); add it as **channel admin** with post + media rights ([sendRichMessage requirement](https://core.telegram.org/bots/api/methods/sendrichmessage)).
2. One-time converter script: lesson `.md` → rich markdown. Fixes needed: rewrite `./images/foo.png` → absolute `https://raw.githubusercontent.com/<user>/<repo>/main/...` (media must be HTTP/HTTPS URLs); strip/downgrade HTML outside the [supported tag list](https://core.telegram.org/bots/api/rich-messages); check ≤32,768 chars, else split at an `---` boundary.
3. Publish each lesson as one `sendRichMessage` to `chat_id=@channel`; end with the GitHub blob link + one-line "tomorrow" teaser.
4. Attach the actual `Day_M.md` via `sendDocument` (multipart — sending by URL works only for PDF/ZIP): subscribers tap the file card and the **Telegram Browser renders the Markdown natively**.
5. Make key prompt blocks copy-friendly with `<tg-button type="copy_text">` ([rich-messages](https://core.telegram.org/bots/api/rich-messages)).
6. Pin a "How to read this course" post (§2.4) + the course-index post; one lesson per day.
7. Fallback while the script is unbuilt: with Premium, hand-format in the Rich Text Editor; without, post a formatted teaser + GitHub link + attached `.md`.

Not needed: Telegra.ph (API still functional but unmaintained tooling; docs page unreachable 2026-10-24 — treat as a dead end) and Instant View (github.com already has [approved templates](https://instantview.telegram.org/templates/github.com/); coverage of `/blob/**.md` pages [UNVERIFIED] — free bonus at most).

### 2.4 Beginner mini-guide (for the pinned post)

1. Nothing to install: the lesson post renders fully in Telegram (headings, tables, code, images).
2. The GitHub link opens a **rendered** page, not raw code ([GitHub docs: viewing a file](https://docs.github.com/en/repositories/working-with-files/using-files/viewing-a-file)). On iOS the GitHub app may intercept the link; long-press → "Open" to stay in the browser ([GitHub Mobile docs](https://docs.github.com/en/get-started/using-github/github-mobile)).
3. The attached `.md` file **is** the lesson: tap → Telegram Browser renders it; save it to open later in VS Code.
4. To copy prompt text: use the post's "Copy" buttons, or GitHub → **Raw** → **Copy raw content** ([GitHub docs](https://docs.github.com/en/repositories/working-with-files/using-files/viewing-a-file)).
5. Links open in the Telegram Browser by default; choose another browser via long-press ([June 2026 blog](https://telegram.org/blog/watch-apps-and-more#quick-browser-selection)).

### 2.5 Sources

- https://core.telegram.org/bots/api/rich-messages · /methods/sendrichmessage · /formatting · /methods/sendmessage · /methods/sendphoto · /bots/faq
- https://telegram.org/blog/watch-apps-and-more (2026-06-11: rich text for bots, .md rendering, browser) · https://telegram.org/blog/communities-editor-invisible-messages (2026-07-14: Premium editor)
- https://instantview.telegram.org/ · /docs · /templates/github.com/
- https://docs.github.com/en/repositories/working-with-files/using-files/viewing-a-file · /en/get-started/writing-on-github/... · /en/get-started/using-github/github-mobile
- https://telegra.ph/api ([UNVERIFIED page]; API verified live via `api.telegra.ph/createAccount`/`createPage`)

---

### Open items for humans

- [ ] Verify current Gemini free-tier model IDs at ai.google.dev (site down during research); fix `Week_1/Day_3.md:247` accordingly.
- [ ] Confirm Groq Free-plan limit table at publish time (accordion-hidden in docs).
- [ ] Decide channel handle; create bot + admin wiring; write the md→rich-md converter.
- [ ] Apply Part 1 replacements to ADR-0003, then sweep lessons (files listed in §1.5).
