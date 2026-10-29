# Keep interactivity count-only and id-only

**Status:** accepted

**Date:** 2026-10-29

Amends [ADR-0007](0007-bot-gateway-funnel.md).

The launch funnel works, but the channel had no visible growth signal and no path from a free lesson to a paid consultation. Interactivity v2 adds a minimal set of mechanics with privacy as the hard constraint: nothing about an identifiable subscriber is ever published where other people can read it.

1. **Privacy: ids only, nowhere public.** The owner-DM ledger records Telegram user ids, never names (`(id=…)` suffix, `👋 новый участник: id=…`). The `/start` greeting carries a one-line data notice explaining that the join source and experience mark are stored in the owner's correspondence and used only to count subscribers. Rationale: the channel's `t.me/s/` archive is public, and under Belarus law 99-З publishing personal data requires consent — silence is not consent. Names were also unbuildable statelessly: the webhook bot cannot pass data to the snapshot cron.
2. **Welcome line.** The publisher reads the last two rows of `docs/metrics/subscribers.log`; a positive delta appends one count-only line («👋 За сутки канал пополнили ещё N человек. Застряли на миссии урока — напишите боту, разберём.») to the lesson post before validation and splitting, so Telegram length limits still hold. Zero or negative delta, or a missing/garbage log, means no line.
3. **Join batch greeting.** When the gateway bot sees `new_chat_members`, it greets the chat once with a generic line («Добро пожаловать! 👋 Вопросы по урокам — в комментариях под постами канала.»). Bots are skipped, the greeting fires only for batches of up to 3 humans (larger batches are treated as mass-join/spam and greeted with nothing), and the owner receives one id-only line per batch instead of per-person names.
4. **Reactions are an aggregate-only vanity metric.** `ALLOWED_UPDATES` becomes a superset that includes `message_reaction_count`; per-user `message_reaction` is intentionally ignored. Each reaction-count update produces one aggregate owner-DM line («📊 Пост N: X реакций»). Kill criterion: if within 3 weeks reactions, DMs, and consultation touches attributable to these mechanics all stay at zero, the mechanics are removed.
5. **Webhook hardening.** `WEBHOOK_SECRET` is mandatory for serving. `do_POST` answers 200 to every update whose JSON parses, even when handling raises: Telegram retries non-2xx deliveries, so a single poison-pill update would loop forever and re-trigger non-idempotent greetings. The secret check itself still runs first.
6. **Snapshot freshness.** The snapshot skips the run if today's row already exists (same-day idempotency makes the retry safe), a second cron at 08:41 UTC re-runs it as a safety net, and the workflow rebases with `--rebase --autostash` before pushing to survive push races with the publish workflow.
7. **Join-request flow is deferred.** `chat_join_request` handling is not implemented; the current join path (invite links + group) works without it.

## Why

A three-way adversary review (tech/legal/product) killed the original plan of greeting each joiner by name: names are unlawful without consent in a public archive, unbuildable in a stateless design, and bad UX at 0–2 joins/day. The count-only welcome line survived as the cheapest visible growth signal and the only nudge toward consultations. Separately, the prerequisite audit found real defects: a hardcoded `ALLOWED_UPDATES` list that would silently drop reaction updates on any webhook re-set, an optional `WEBHOOK_SECRET` that allowed forged updates, a `RuntimeError`-only catch that let unexpected handler exceptions turn updates into poison pills, and a stale `subscribers.log` (last row 2026-10-27) that broke the measurement the whole design depends on.

## Consequences

- Old ledger entries in the owner's DM still contain names; new entries are id-only. Purging history is manual and optional.
- The welcome line depends on the snapshot cron: if snapshots stop, the line silently disappears rather than showing a stale delta.
- Reaction counts are cosmetic; per-user reaction data never leaves Telegram.
- Deploying this bot requires one `--set-webhook` re-run: Telegram keeps the previous `allowed_updates` until the webhook is set again.
- Mass joins (>3 humans in one update) get no greeting by design; the owner still sees the batch as ids.
