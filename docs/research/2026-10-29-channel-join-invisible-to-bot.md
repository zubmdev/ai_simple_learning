# Research: channel joins are invisible to the bot — re-subscribing produces nothing, by design

**Date:** 2026-10-29. Sources: Telegram Bot API reference ([Update](https://core.telegram.org/bots/api#update), [setWebhook](https://core.telegram.org/bots/api#setwebhook), [Message](https://core.telegram.org/bots/api#message), [getChatMemberCount](https://core.telegram.org/bots/api#getchatmembercount)), [Bots features → Privacy mode](https://core.telegram.org/bots/features#privacy-mode), [Telegram Core → Discussion groups](https://core.telegram.org/api/discussion) (all fetched 2026-10-29); live Bot API checks (`getWebhookInfo`, `getChat`, `getChatMember`, `getChatMemberCount`) run 2026-10-29; [ADR-0007](../adr/0007-bot-gateway-funnel.md), [ADR-0008](../adr/0008-count-only-interactivity.md), [runbook](../launch/telegram-threads-runbook.md).

## Symptom

The owner's wife unsubscribed from the channel «AI - это просто» and subscribed again from her phone. Expected per the owner: a «👋 новый участник» line in the owner's DM (and the group greeting). Observed: nothing at all.

## Live state at test time (verified 2026-10-29)

Everything on our side was healthy, so the silence is not a delivery failure:

- Webhook set: `https://ai-simple-learning.onrender.com/webhook`, `allowed_updates = ["message", "callback_query", "message_reaction_count"]`, `pending_update_count: 0`. Probe `POST /webhook` with the correct secret → `200 {"ok":true}`, wrong secret → `401` (secret match verified end-to-end).
- Bot `@vibecoding_start_bot` is administrator in the channel (`@simpleaiengeneer`, id `-1003846086394`) and in the linked private supergroup «AI - это просто(обсуждение)» (id `-1004403760424`).
- Channel member count: **11** live, matching [subscribers.log](../metrics/subscribers.log) (9 → 11 on Oct 28). Leave + rejoin nets to the same count.
- Timeline caveat: the webhook was **absent** earlier on 2026-10-29 (`getWebhookInfo` returned `url: None`) and was re-set that day. Any test before that point hit a bot that received zero updates of any kind. But even after the fix, a channel-only join stays silent — see root cause.

## Root cause (documented in Bot API)

A channel join generates **no update the bot receives**. Chain of facts, each from the official docs:

1. **`new_chat_members` is a group-only service message.** *"New members that were added to the group or supergroup"* — there is no channel variant in the [Message](https://core.telegram.org/bots/api#message) schema. Channels only emit `channel_post` / `edited_channel_post`.
2. **The only channel-join signal is `chat_member` — and it is opt-in.** *"A chat member's status was updated in a chat. The bot must be an administrator in the chat and must explicitly specify `chat_member` in the list of allowed_updates"* ([Update](https://core.telegram.org/bots/api#update)). Our `ALLOWED_UPDATES` ([pipeline/bot.py](../../pipeline/bot.py)) deliberately does not include it — ADR-0008 §7 defers join flows.
3. **`chat_join_request` doesn't apply.** It requires approval-gated invites (*"The bot must have the can_invite_users administrator right"* and a join-request link); a public channel's plain «Join» button never sends it.
4. **Joining the channel does not join the linked discussion group**, and guest commenting does not add the user to the group either: *"a user can comment in channel posts without joining the actual discussion supergroup"* ([api/discussion](https://core.telegram.org/api/discussion)). So the comment button never produces a group `new_chat_members` event.
5. The design wires the greeting and the «👋 новый участник: id=…» DM **only to group joins**: ADR-0008 §3 ("When the gateway bot sees `new_chat_members`…") and the runbook («вступления в группу встречает одной общей фразой»). For privacy-shape reasons (ADR-0008 §1, §7) no channel-membership stream was subscribed.

Therefore: channel leave + rejoin → Telegram sends the bot nothing → owner DM stays empty. **Working as designed; the expectation, not the pipeline, was wrong.**

The only growth metric that does react to channel joins is the snapshot delta ([runbook §кроны](../launch/telegram-threads-runbook.md), 06:30/08:41 UTC → `docs/metrics/subscribers.log`), and a same-day leave+rejoin correctly nets zero.

## Consequences

- **The real-time join signal only covers the private discussion group.** A subscriber who never explicitly joins «(обсуждение)» via an invite link — i.e. the default path, since guest commenting works without membership — never triggers the greeting or the owner notification. The batch-greeting mechanic (ADR-0008 §3) is near-unreachable in the current funnel.
- Real-time channel-join visibility is buildable without any rights change: the bot is already channel admin; adding `chat_member` to `ALLOWED_UPDATES` plus a `ChatMemberUpdated` handler (owner-DM id-only on `left → member` transitions, per ADR-0008 §1 constraints) is the minimal change. That amends ADR-0008 §7 — owner decision, tracked separately, not made here.
- The «(id=…)» deploy fingerprint (new `OWNER_TEXT_START` format) is orthogonal: both old and new bot code behave identically for channel joins.

## Verification commands

Re-checkable at any time (reads `.env` for `BOT_TOKEN`/`CHANNEL_ID`):

```bash
python3 - <<'PY'
import json
from pipeline.publisher import load_env
from pipeline.telegram import post_json
cfg = load_env('.env')
print(json.dumps(post_json(cfg['BOT_TOKEN'], 'getWebhookInfo', {}), indent=1))
print(post_json(cfg['BOT_TOKEN'], 'getChat', {'chat_id': cfg['CHANNEL_ID']}))
me = post_json(cfg['BOT_TOKEN'], 'getMe', {})['result']
print(post_json(cfg['BOT_TOKEN'], 'getChatMember', {'chat_id': cfg['CHANNEL_ID'], 'user_id': me['id']}))
print(post_json(cfg['BOT_TOKEN'], 'getChatMemberCount', {'chat_id': cfg['CHANNEL_ID']}))
PY
```
