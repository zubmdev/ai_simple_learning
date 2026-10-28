# Research: GitHub Actions scheduled runs fire hours late — publish SLA at risk

**Date:** 2026-10-28. Sources: the repo's own Actions run history (`api.github.com/repos/zubmdev/ai_simple_learning/actions/runs`, queried unauthenticated 2026-10-28), `git log origin/main -- .github/workflows/publish.yml`, GitHub Actions docs on the [`schedule` event](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#schedule) (verified 2026-10-28). Repo-internal facts are verifiable via the linked commands.

## Symptom

The product promise ([runbook](../launch/telegram-threads-runbook.md)): one lesson post at 09:00 Minsk (06:00 UTC) daily.

Observed:

| Cron | Actually ran | Delay |
|---|---|---|
| publish 06:00 UTC, Oct 27 | 11:23:53Z | **+5h23m** |
| publish 08:41 UTC (retry), Oct 27 | 14:53:47Z | **+6h12m** |
| snapshot 06:30 UTC, Oct 27 | 12:30:44Z | **+6h00m** |
| publish 06:00 UTC, Oct 28 | no run by 06:20Z | pending |

For every run, `created_at == run_started_at` hours after the cron time — GitHub created the run late, before any repo code executes. The delay is platform-side.

## Ruled out (repo-side)

- Cron workflow on the default branch since Oct 26/27: `git log origin/main -- .github/workflows/publish.yml`.
- Gate data correct: `launch/schedule.tsv` on origin has the day's row with status `todo`; the target `Day_*.md` exists on origin.
- Secrets work: Oct 26–27 runs succeeded end-to-end (posted, marked done).
- Not the 60-day-inactivity auto-disable: the repo had runs the day before.

## Root cause (documented)

GitHub's `schedule` event is best-effort: *"During periods of high load of GitHub Actions workflow runs, the time when the workflow runs may be delayed… high load times are at the start of each hour… in extreme cases, scheduled workflow runs can be dropped."* There is no timing guarantee, and a repo cannot opt out or prioritize. On this repo the observed delay is ~5–6 hours, not minutes.

## Consequences

- The 08:41 retry was designed assuming the morning run fires near-time. When the platform is late, both crons slip by the same amount — there is no same-morning recovery.
- The runbook's «утренний cron не сработал → жди 08:41 retry» advice currently means «жди ~15:00 Minsk», not 09:00.
- Stopgap used 2026-10-28 for `Day_2.md`: local publish per [runbook §Аварийные процедуры](../launch/telegram-threads-runbook.md), origin marked `done` in `5c868ca` so the late cron no-ops instead of double-posting.
- Caveat: a locally published post links «📄 Урок на GitHub» to `origin/main`, which still holds the pre-refresh `Day_2.md` (the 2026-refresh commits sit unpushed on local main pending owner approval; delta currently 36+/4− lines). Resolves when the refresh is pushed.

## Options for a durable fix

1. **External dispatcher → `workflow_dispatch`** (exact 09:00 Minsk): a free external cron (e.g. cron-job.org) calls `POST /repos/…/actions/workflows/publish.yml/dispatches` with a fine-grained PAT (Actions: write, one repo). Costs: a PAT stored at a third party — a new secret surface (scope-minimize, rotate on leak, same lifecycle as the «Токен утёк» runbook entry). Needs an owner decision; if adopted, record an ADR.
2. **Harden with more cron slots** (free, no secrets): add slots every ~20 min across 06:00–09:00Z. The `done`-row gate makes duplicates harmless no-ops. Does not beat a uniform +6h delay, but caps typical slippage and self-heals once platform delays normalize.
3. **Self-hosted runner** on an always-on owner box: exact timing, no third-party PAT, new ops burden and uptime dependency.
4. **Accept slippage**: restate the promise as «выходит утром, может доехать к ~15:00 Minsk».

**Prediction made 2026-10-28 06:20Z:** today's delayed run should appear ~11:00–13:00Z, see `done`, and no-op. If it never appears, that also confirms the "runs can be dropped" clause.

**Recommendation:** apply 2 immediately (zero risk), decide 1 vs 3 vs 4 after observing the delay distribution for a week.
