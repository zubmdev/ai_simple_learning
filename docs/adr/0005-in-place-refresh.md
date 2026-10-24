# Refresh in place on a 2026-refresh branch

**Status:** accepted
**Date:** 2026-10-24
**Amended:** 2026-10-24 — baseline-commit manifest recorded; the README was rewritten before any public publish.

Create an initial git commit of the current repository as the baseline, then do the rewrite on a `2026-refresh` branch and merge back when the refresh is ready. Rewrite lessons in place; do not create a parallel `v2/` course tree.

## Why

The repo has no commits, so the current state is not recoverable. A baseline commit plus a branch gives a safe rollback without duplicating 78 lesson files. In-place edits preserve the existing paths, internal links, and the week index structure.

## Consequences

- The first commit must include the current content, even though parts of it are outdated.
- The old state remains available in git history; no `legacy/` copy is needed.
- Do not rewrite `main` directly until the refresh branch is reviewed.
- After merge, tag the release so the pre-refresh state remains easy to find.

## Baseline commit manifest

- `main` baseline: `ru/`, `en/`, `README.md`, `.gitignore` only.
- The `2026-refresh` branch additionally commits: `docs/`, `AGENTS.md`, `CONTEXT.md`, `opencode.json`, `.agents/`, `skills-lock.json`.
- The README was rewritten on 2026-10-24 before any public publish; the old `$5`/Boosty text survives only in git history, and nothing was ever sold under it.
