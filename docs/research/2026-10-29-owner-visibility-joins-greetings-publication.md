# Research: owner visibility — subscribe/unsubscribe, greetings, and the missing Oct 29 publication

**Date:** 2026-10-29. Sources: GitHub Actions runs API (`api.github.com/repos/zubmdev/ai_simple_learning/actions/runs`, queried unauthenticated 2026-10-29 ~11:12 UTC), [launch/schedule.tsv](../../launch/schedule.tsv), live Bot API checks, Telegram Bot API docs ([Update](https://core.telegram.org/bots/api#update), [ChatMemberUpdated](https://core.telegram.org/bots/api#chatmemberupdated), [ChatMember](https://core.telegram.org/bots/api#chatmember), [setWebhook](https://core.telegram.org/bots/api#setwebhook), [Bots: how different](https://core.telegram.org/bots#how-are-bots-different-from-users)) fetched 2026-10-29; [ADR-0008](../adr/0008-count-only-interactivity.md), [runbook](../launch/telegram-threads-runbook.md), and the two prior notes [2026-10-28](2026-10-28-github-actions-schedule-delay.md), [2026-10-29](2026-10-29-channel-join-invisible-to-bot.md).

## 1. Today's publication was missing — GitHub cron never fired; published manually per runbook

Facts (11:12 UTC):

- `launch/schedule.tsv` had today's row `2026-10-29 … Day_3.md … todo`; `origin/main` == local `main` (no drift).
- The Actions API showed **zero runs on Oct 29** — neither the 06:00 UTC `publish`, nor the 06:30 UTC `snapshot`, nor the 08:41 UTC retries had been *created* by GitHub. This is the same platform-side `schedule` delay documented in the [Oct 28 note](2026-10-28-github-actions-schedule-delay.md) (there: runs created 5–6 h late; GitHub's docs: *"in extreme cases, scheduled workflow runs can be dropped"*). Nothing repo-side blocked it.
- Consequence also visible: `docs/metrics/subscribers.log` had no Oct 29 row, so the daily snapshot was equally late.

Action taken (runbook → «Аварийные процедуры», same stopgap as Day_2 on Oct 28):

1. `python3 -m pipeline.snapshot` → Oct 29 row `11 (+0)` appended (truthful zero delta, so no «👋 За сутки…» line was added to the post — correct count-only semantics).
2. `python3 -m pipeline.publisher --publish ru/beginner/Week_1/Day_3.md --mark-published` → post sent (message_id 46, buttons 47, source attached 48), schedule row marked `done`.
3. Committed `4723a86` and pushed **before** the late retry-cron could fire — origin's `todo` row is now `done`, so whenever GitHub finally creates today's runs, publish and snapshot both no-op (same-day idempotency, ADR-0008 §6).

Residual risk: GitHub may still not create today's runs at all (documented drop case). The 08:41 retry did not exist as a run at query time. Mitigation is unchanged: check `getChatMemberCount`/`subscribers.log` each morning and re-run the same two local commands when a day goes unpublished past ~09:00 Minsk. The durable fix options (external dispatcher → `workflow_dispatch`) remain as listed in the Oct 28 note — owner decision, needs ADR.

## 2. Seeing subscribes/unsubscribes in real time — feasible via `chat_member` opt-in (needs owner decision)

Per the [morning note](2026-10-29-channel-join-invisible-to-bot.md): channel joins produce no update today. The full mechanism, primary-source verified:

- **Opt-in works**: *"The bot must be an administrator in the chat and must explicitly specify `chat_member` in the list of allowed_updates"* ([Update](https://core.telegram.org/bots/api#update)). The bot **is** channel admin (verified live) — no rights change needed. The list is **exclusive** and persists until the next `setWebhook`, so the code change is exactly `ALLOWED_UPDATES = ["message", "callback_query", "message_reaction_count", "chat_member"]` in [pipeline/bot.py](../../pipeline/bot.py) plus one `--set-webhook` re-run; omitting any current type would silently stop it.
- **Payload**: `ChatMemberUpdated` = `chat`, `from`, `date`, `old_chat_member`, `new_chat_member` (+ optional `invite_link`, `via_join_request`, `via_chat_folder_invite_link`). Handler logic: `old.status → new.status` transitions; `member → left` = unsubscribe, `* → member` = join; also `member → kicked` (ban) and `kicked → left` (unban) are status changes; `chat.id` splits channel vs linked discussion group.
- **Source attribution is partial**: `invite_link` is *"for joining by invite link events only"* — joins via the public `t.me/simpleaiengeneer` username carry no source. Named invite links (already in ADR-0007 as the secondary mechanism) would restore attribution for those who join through them.
- **Id-only privacy shape is preserved**: the payload is ids/ statuses; nothing forces names (ADR-0008 §1). Volume is one update per membership action; no documented throttling (only `message_reaction_count` documents delay). The same opt-in also delivers join/leave of the linked discussion group (bot is admin there) — filter by `chat.id`.
- **Ground truth stays `getChatMemberCount`**: there is no method to list members (`getChatMember` works per-id for admins only); treat the event feed as advisory, the daily snapshot as the ledger.

This amends ADR-0008 §7 (deferred join flows) — decision and ADR amendment belong to the owner; implementation is small (handler + tests + one webhook re-run).

## 3. Seeing greetings — what exists, what's impossible

- **What the owner already sees**: `🚀 /start source=… (id=…)` for every bot DM greeting (funnel entry), `🎚 опыт: …` for experience buttons, `👋 новый участник: id=…` per group-join batch greeting, `📊 Пост N: X реакций` aggregates, `📈 Подписчиков: N (±delta)` from the snapshot (that Oct 29 line was sent by today's manual snapshot run).
- **What nobody can see today**: group-join greetings — nobody reaches them, because guest commenting doesn't join the linked group and channel joins aren't visible (see [morning note](2026-10-29-channel-join-invisible-to-bot.md)). The `chat_member` opt-in from §2 fixes the visibility gap: joins/leaves land in the owner DM as id-only lines, but…
- **Hard limit — no bot-initiated greetings to channel subscribers**: *"Bots can't start conversations with users. A user must either add them to a group or send them a message first"* ([bots](https://core.telegram.org/bots#how-are-bots-different-from-users)). A subscriber who joins the channel and never messages the bot is unreachable — the channel-join «greeting» can only ever be a line in the owner's DM, never a message to the subscriber. The generic welcome remains the publisher's lesson post + the `/start` DM greeting.

## Suggested next step (decision, not made here)

If the owner wants §2 visibility: write an ADR-0008 amendment (id-only join/leave feed incl. `kicked` cases; named invite links optional for attribution), implement the handler in `pipeline/bot.py` with tests, re-run `--set-webhook`, then watch the feed for a few days before deciding whether the «👋 новый участник» group greeting still earns its place.
