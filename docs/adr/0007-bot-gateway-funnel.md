# Deploy the funnel on a stateless bot gateway

**Status:** accepted

**Date:** 2026-10-25

**Amended:** 2026-10-26 — launch pulled forward: Day 0 published Mon 2026-10-26 (manual soft launch), Days 1–5 run Tue–Sat 2026-10-27…10-31 at 09:00 Minsk via the updated schedule.

Week 1+ is deployed on Telegram as three pieces: the public channel «AI - это просто» (the course feed), a linked discussion group for per-lesson comments, and the bot @vibecoding_start_bot. The bot is a **stateless webhook gateway** (`pipeline/bot.py`, stdlib `http.server`) with no server-side state and no database. Every `/start` is answered with a greeting whose first message carries an inline button with the channel invite; nothing gates content.

Grounding: [2026-10-25 research note](../research/2026-10-25-telegram-threads-week1-funnel.md)

1. **Bot behaviour.** Every `/start` gets the channel invite in the first message. Experience buttons (`callback_data=exp:<source>:<tag>`) are optional, come after the invite, and never block it.
2. **Attribution.** Campaign links point to `t.me/vibecoding_start_bot?start=<source>` (e.g. `threads`). Telegram channels have no `?start=` deep links (verified: core.telegram.org, Bots features → Deep Linking), so the bot gateway is the only exact join-source counter; named channel invite links (`createChatInviteLink name=…`) are the secondary mechanism.
3. **Metrics.** Funnel conversion is measured by bot `/start` counts grouped by source (A3 decision) — not Threads API `clicks`, which stay a weak upper-bound proxy. Because the bot is stateless, each `/start` is mirrored as one line to the owner's Telegram DM; the DM history is the ledger («Telegram DM = database»), tallied manually weekly.
4. **Calendar-gated publishing (A4).** `launch/schedule.tsv` lists date (UTC), time, file, note; a GitHub Actions cron at 06:00 UTC (09:00 Minsk) publishes rows whose date equals today's UTC date. Nothing publishes outside the schedule.
5. **$0 infra.** GitHub Actions crons for publisher + subscriber snapshot; the webhook bot runs on a free PaaS tier; no paid services.
6. **Threads (@ai_kontur_by) is a manual feeder.** RU hook posts are written and posted by hand; no Threads API automation for now. The handle needs in-app verification (A5, pending human check).
7. **Launch.** Day 0 soft-launched Mon 2026-10-26 (published manually); one lesson/day at 09:00 Minsk Tue–Sat 2026-10-27…10-31 (Day 1–Day 5).

## Why

Telegram channels cannot carry a `?start=` parameter, so a bot gateway is the only way to attribute joins to an exact source — and Threads `clicks` only measure card taps, not joins. Keeping the bot stateless removes the database entirely: it can live on a free PaaS tier, and the ledger moves to the owner's Telegram DM, which the owner already reads daily. Calendar-gated publishing via `schedule.tsv` means no long-running scheduler is needed and nothing can publish by accident. Threads is a feeder, not a second destination; manual posting avoids token upkeep during launch week and can be automated later without touching the Telegram side.

## Consequences

- No database means `/start` counts must be tallied manually from the owner's Telegram DM.
- Losing the owner DM history loses attribution; mitigation is a weekly manual tally into a metrics file.
- A PaaS free tier can cold-start or sleep, so webhook latency is best-effort — acceptable because onboarding is not real-time critical.
- `schedule.tsv` edits are the only way to change what publishes; the cron publishes nothing outside the listed rows.
- Threads automation is deliberately deferred and may be added later without changing the Telegram side.
- Because experience buttons never gate onboarding, a broken callback path cannot lock a new subscriber out of the channel.
