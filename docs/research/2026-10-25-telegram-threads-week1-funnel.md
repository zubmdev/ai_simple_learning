# Research: Week 1 → Telegram deployment, beginner UX, Threads→Telegram subscriber funnel

**Date:** 2026-10-25. Primary sources: core.telegram.org (Bot API method pages, bots/features, channels FAQ), Meta Threads API docs via the official docs mirror (developers.facebook.com/documentation/threads — direct fetch blocked 2026-10-25, content verified through the llms.txt mirror), plus the prior verified note [2026-10-24-models-and-telegram-publishing.md](./2026-10-24-models-and-telegram-publishing.md). Third-party/secondary claims are labelled. Unverifiable items are marked **[HUMAN CHECK]**.

**Interpretation note:** «Describe and take free course» is read here as a lead magnet: a Threads post describes a real beginner problem, readers reply describing *their* task, and each reply gets a personal pointer plus the free Telegram course. DM-based variants are analysed but not recommended (see §4.2).

---

## Part 1 — Deploying Week 1 in Telegram

### 1.1 Architecture: channel + discussion group + bot (three pieces)

| Piece | Role | Grounding |
|---|---|---|
| **Public channel** | The course feed. Unlimited subscribers; new subscribers see the entire history on join (so the whole course stays readable in-app); posts searchable by username; per-post view counter ([Channels FAQ](https://telegram.org/faq_channels), verified 2026-10-25) | Public, not private: search + `t.me/s/<name>` web preview make lessons discoverable without joining |
| **Linked discussion group** | Comments button under every lesson post ([Channels FAQ → feedback options](https://telegram.org/faq_channels)) | Beginners ask questions per-lesson; admin answers stay attached to the lesson |
| **Bot (admin)** | Posts via `sendRichMessage`; pins; handles onboarding form; optional gateway for attribution | `sendRichMessage` to a channel requires the bot to be an admin with post/media rights ([sendRichMessage](https://core.telegram.org/bots/api/methods/sendrichmessage), verified 2026-10-25) |

Why not other shapes: a bot alone has no broadcast surface (no message to users who never pressed Start); a plain group has no one-way feed discipline. The plan's "bot form (nick, experience, current task)" ([plan §6 Phase 0](../2026-refresh-plan.md)) stays: the bot DMs, not the channel — bots cannot enumerate channel subscribers or DM anyone who hasn't started them ([Bots FAQ](https://core.telegram.org/bots/faq)).

New-2026 bonus: **Channel Direct Messages** — a forum-like DM directory where subscribers privately message channel staff; a bot with `can_manage_direct_messages` can answer those topics, and *suggested posts* let users propose content ([Bots features → Channel Direct Messages](https://core.telegram.org/bots/features), verified 2026-10-25). Use it as the consultations intake instead of exposing a personal phone number.

### 1.2 Beginner UX: what a lesson looks like in-app

Confirmed rendering surfaces (all from [2026-10-24 research](./2026-10-24-models-and-telegram-publishing.md), verified 2026-10-24 against core.telegram.org):

- One lesson = one rich post: GFM headings, tables, lists, code blocks, inline images, copy-text buttons; **32,768 chars / 500 blocks / 50 media** per post (`sendRichMessage` + [rich-messages](https://core.telegram.org/bots/api/rich-messages)).
- `sendRichMessage` also accepts **`reply_markup` inline keyboards** ([method table](https://core.telegram.org/bots/api/methods/sendrichmessage), verified 2026-10-25) — so a lesson post can carry URL buttons: «Урок на GitHub», «Задать вопрос», «Следующий день». **Not yet used by `pipeline/`** — the cheapest big UX win.
- Attached `Day_M.md` opens in the **Telegram Browser rendered as Markdown** (June 2026 blog); `pipeline/publisher.py` already attaches the source file after each post.
- GitHub links open rendered pages; on iOS the GitHub app may intercept → long-press → Open (§2.4 of the 10-24 note).

Mobile pitfalls to design around: Week-1 lessons run 9–26 KB (one post each, no split needed — `--check` reports parts=1); tables must stay ≤3–4 columns to survive a phone screen; `convert.py` already lifts inline images out of paragraphs and splits at `---` fences when needed.

Reading flow for a beginner (target): pinned index → today's lesson post → do the mission → comments button for questions → footer buttons to GitHub/tomorrow. New joiners read the full history from Day 0 ([FAQ](https://telegram.org/faq_channels)).

### 1.3 Onboarding + attribution mechanics (verified 2026-10-25)

- **Deep links are bot-only:** `t.me/<bot>?start=<64-char param>` fires `/start <param>` in the bot chat; `?startgroup` exists for groups. There is **no** `?start=` for channels ([Bots features → Deep Linking](https://core.telegram.org/bots/features)).
- **Named channel invite links:** `createChatInviteLink` accepts `name` (0–32 chars), `member_limit`, `creates_join_request` ([method page](https://core.telegram.org/bots/api/methods/createchatinvitelink)). Works on public channels too → create `threads`, `youtube`, `postbot` links and count joins per source (visible in admin invite-link list; [HUMAN CHECK: exact per-link stats UI on your client]).
- **Pinning:** in channels a bot pins with the `can_edit_messages` right ([pinChatMessage](https://core.telegram.org/bots/api/methods/pinchatmessage)).
- **No UTM survives into Telegram.** Measure inbound source by (a) named invite links, (b) bot `?start=<source>` gateway (exact count, but adds one tap), (c) off-platform click metrics (Threads `clicks`, §3.3).

### 1.4 Ops

- No native Bot API scheduling → cron/systemd fires `pipeline.publisher`; one post/day at a fixed hour.
- Rate limits: keep to a handful of posts/day per chat (well under the ~1 msg/s per chat guidance, [Bots FAQ](https://core.telegram.org/bots/faq)); handle 429 with `retry_after`.
- Wiring checklist: BotFather bot → add as channel admin (post messages, edit messages, invite users via links) → link the discussion group → set `BOT_TOKEN`, `CHANNEL_ID`, `REPO_URL` in `.env` (`publisher.py --check` validates everything offline first).
- Secrets: token stays in `.env` (gitignored); publisher already masks tokens in errors.

### 1.5 Week 1 post plan (5 lessons + scaffolding)

1. **Pinned: «Как читать этот курс»** — the beginner mini-guide from §2.4 of the 10-24 note + course index + rules (nothing to install to read; everything free).
2. **Pinned/second: course index post** — 8-week table, tracks, «начни с Day 0».
3. **Day 0 intro post** (free lead magnet), then **Day 1…Day 5** — one per day: rich post + inline buttons + attached `.md` + «завтра: …» teaser.
4. Week close: results teaser + Week 2 date. Comments open on every post.

**Pipeline gap vs this plan:** converter/publisher/splitter/validator are done; missing are (a) inline button injection, (b) pinned-posts content + pin call, (c) named invite links per source, (d) a cron entry, (e) the onboarding bot flow (plan Phase 0 item).

---

## Part 2 — Threads as the subscriber engine («опиши задачу — забирай курс»)

### 2.1 What the Threads API allows (official docs, verified 2026-10-25 via mirror)

| Capability | Fact | Source note |
|---|---|---|
| Publish | `TEXT`, `IMAGE`, `VIDEO`, `CAROUSEL`; text posts support `auto_publish_text` (one call, no two-step container→publish) | [publishing reference](https://developers.facebook.com/documentation/threads/reference/publishing) |
| Rate | **250 API posts / 24h** rolling; carousels count once; `threads_publishing_limit` endpoint reports usage | [overview/rate limiting](https://developers.facebook.com/documentation/threads/overview) |
| Text length | 500 chars (emoji count as UTF-8 bytes) | verified 2026-10-22 in prior research; docs note byte-counting |
| Links | `link_attachment` param, or first URL in a text-only post becomes the preview card; **≤5 links per post** (Dec 22, 2025: >5 fails with `THREADS_API__LINK_LIMIT_EXCEEDED`) | [posts](https://developers.facebook.com/documentation/threads/posts) |
| Topic tags | one `topic_tag` per post, 1–50 chars, no `.` or `&`; or inline `#tag` in text | [posts → topic tags] |
| Replies | `reply_control`: everyone / accounts_you_follow / mentioned_only / parent_post_author_only / followers_only; API can hide/unhide replies | [reply management] |
| Polls, quotes, geo | `poll_attachment`, `quote_post_id`, `allowlisted_country_codes` (restrict visibility by ISO country), `crossreshare_to_ig` (post → Instagram Story) | [publishing reference] |
| Webhooks | real-time notifications for **replies** and **mentions** (topics `moderate`/`interaction`) | [webhooks] |
| Insights | user metrics: `views, likes, replies, reposts, quotes,` **`clicks` (URL clicks you shared)**, `followers_count`, `follower_demographics` (≥100 followers); per-post: `views, likes, replies, reposts, quotes, shares` | [insights] |
| Auth | `threads_basic` + `threads_content_publish` (+ `threads_manage_insights` for insights); **own account as app tester needs no App Review**; long-lived tokens 60 days, refreshable after 24h; since Sep 23, 2025 no linked Instagram required (except follower metrics) | [get-started / long-lived tokens / changelog] |

No DM endpoints exist in the API — the funnel must run through **public replies**, which is actually better for reach (replies feed distribution).

### 2.2 The mechanic, concretely

Post format (≤500 chars, one topic tag, CTA to replies):

> Неделя AI-курса, день 1: человек хочет «писать код с ИИ», открывает редактор — и залипает: какой модели доверить первый шаг?
> Напиши в ответах, что хочешь собрать (или что застряло), — отвечу персонально, а бесплатный 8-недельный курс целиком лежит в Telegram → карточка ниже.
> #айдишник #обучение

Loop: publish → webhook catches replies → human answers each reply (personal pointer) → questioner taps the `link_attachment` card → Telegram channel (named invite link `threads`). Every lesson yields 1 hook post + a week-summary post; plan already budgets 3 marketing posts/week and a 4-week kill criterion ([plan §6](../2026-refresh-plan.md)).

Variants ranked:

1. **Replies + link card (recommended):** allowed, no review needed, replies boost reach, each reply is a warm lead.
2. **Bot gateway:** same, but the card links to `t.me/<bot>?start=threads`; the bot DMs the channel invite. Exact join attribution, one extra tap.
3. **DM-first:** not implementable via API (no DM endpoints); in-app DM behaviour for Threads **[HUMAN CHECK]** — and cold DMs violate Telegram-side spam etiquette anyway.
4. **Auto-reply via API:** technically possible (publish with `reply_to_id`) but robotic; keep the reply human.

### 2.3 Attribution math

- Threads `clicks` metric counts URL clicks you shared → daily proxies for card taps.
- Telegram side: joins counted via the `threads` named invite link (and `threads` bot `?start=` if the gateway variant is used).
- Conversion funnel per week: post views → replies → clicks → joins → Day-1 post views (channel eye counter). Any zero for 4 straight weeks → kill per plan §6.

---

## Part 3 — Telegram × Threads combination: difficulties and fixes

| # | Difficulty | Fix |
|---|---|---|
| 1 | **No join-source data on Telegram for plain `t.me/channel` links** | Named invite links per source (`createChatInviteLink name=…`); bot `?start=` gateway for exact counting; never post the bare public link in campaigns |
| 2 | **Geo: Threads is blocked in Russia; works in Belarus (~533K users, secondary source: DataReportal 2026 via prior research 2026-10-22); RU-store availability [HUMAN CHECK]** | Telegram-first audience (TG is universal in BY/RU); Threads is only a feeder; content stays RU; don't gate anything by geo; `allowlisted_country_codes` exists but leave off |
| 3 | **Meta app review fear** | Not needed: own profile as app tester covers posting + insights (advanced access is only for posting on behalf of strangers) |
| 4 | **Token upkeep (60-day expiry)** | Refresh job next to the publish cron; refresh allowed after 24h, valid another 60 days |
| 5 | **500-char constraint vs 9–26 KB lessons** | Don't repost lessons — repost *problems*. One hook per lesson: claim → micro-insight → reply-CTA → card. Draft pipeline: lesson `## Цели недели` + Day-1 mission → hook template |
| 6 | **Link-reach folklore («links kill reach»)** | No official Meta statement — treat as unverified. Mitigate anyway: hook post without links, link card in the **first reply** of the same thread (A/B against card-on-post) |
| 7 | **Reply load / spam risk** | Manual replies to every respondent; never mass-DM (Telegram bans for unsolicited links — [Channels FAQ warning](https://telegram.org/faq_channels)); reply_control=everyone on hook posts |
| 8 | **Two-platform abandonment** | Single destination (channel), single CTA, single named link; Threads metrics reviewed weekly with the kill criterion — no vanity posting |
| 9 | **Threads API lacks comment-read endpoints for arbitrary threads** | Webhooks cover replies/mentions to *your* posts (the only ones you need); polling fallback: `GET /{id}/replies` exists for own posts |
| 10 | **Legal (НПД boundary)** | Threads posts advertise the free course only; consultations are sold inside Telegram DMs per ADR-0004 — never on Meta platforms |

---

## Part 4 — 14-day launch sequence

1. Channel + discussion group + BotFather bot as admin (post/edit/invite rights).
2. `.env`: `BOT_TOKEN`, `CHANNEL_ID`, `REPO_URL`, `REPO_BRANCH`; `python3 -m pipeline.publisher --check ru/beginner/Week_1/Day_*.md`.
3. Write + publish + pin the two scaffold posts (how-to-read, course index).
4. Publish Day 0 + Day 1 with buttons + attached `.md`; set the daily cron.
5. Create invite links `threads`, `github-readme`, `youtube` (if any); record baselines.
6. Threads: app + developer app + tester token; publish hook #1 (Day 0 angle) with link card; subscribe to reply webhooks or plan a 2×/day manual reply check.
7. Weekly: Threads `clicks`/`replies` vs invite-link joins vs channel views in one table; 4-week zero-inbound → kill.

---

## Sources

- core.telegram.org: /bots/features · /bots/api/methods/sendrichmessage · /bots/api/methods/createchatinvitelink · /bots/api/methods/pinchatmessage · /bots/faq · /bots/api/rich-messages (via 10-24 note) · telegram.org/faq_channels
- telegram.org/blog/watch-apps-and-more (rich messages, .md browser rendering — via 10-24 note)
- developers.facebook.com/documentation/threads: overview (rate limiting) · posts (link_attachment, topic tags) · reference/publishing · insights · reply-management · webhooks · get-started/long-lived-tokens · changelog (2025-09-23, 2025-12-22 notes) — accessed via official-docs mirror 2026-10-25; direct site returned HTTP 400 to automated fetch
- Secondary: DataReportal Digital 2026 (Belarus Threads audience) via prior session research 2026-10-22

## Unverified / human check

- [ ] Threads DM existence/behavior in-app (not in API docs) — only matters if the DM variant is reconsidered.
- [ ] Per-invite-link join statistics UI on your Telegram client (feature exists per API; UI varies by app).
- [ ] Whether Threads is installable from Russian app stores in Oct 2026.
- [ ] Link-in-first-reply vs link-card-on-post reach A/B (folklore mitigation, no official data).
