# Cline-first stack; OpenCode later; retire Continue.dev

**Status:** accepted

**Date:** 2026-10-24

The beginner course uses **VS Code + Cline + Ollama or a free API**. The programmer track adds **OpenCode** as an advanced upgrade in P1, not at launch. **Continue.dev is retired**; it is read-only/final after the Cursor acquisition and must not appear in new lessons.

## Stack baseline

- **Editor:** VS Code.
- **Beginner agent:** Cline.
- **Programmer agent:** OpenCode (P1).
- **Local runtime:** Ollama.
- **Tier 2 local models (4GB GPU):** `qwen3.5:2b` (primary), `qwen3:4b` (fallback).
- **Tier 3 local models (16GB GPU):** `gpt-oss:20b` (flagship), `gemma4:12b` (long context), `qwen3:14b` (dense middle); `qwen3-coder:30b` only with CPU offload. `qwen3.6:35b` (23-24 GB) does not fit this tier; mention only as "more than 16GB".
- **Free APIs:** Groq (default `openai/gpt-oss-20b`; free tier ~30 RPM / 1,000 RPD / 8K TPM / 200K TPD), Gemini AI Studio, OpenRouter (free models: 20 req/min, 50 req/day below 10 credits, 1,000 req/day above; disable training on free models in privacy settings). All `llama-*` Groq IDs are Enterprise-only or retired and must not be taught.
- Model IDs verified 2026-10-24 against ollama.com, console.groq.com, and openrouter.ai (research: `docs/research/2026-10-24-models-and-telegram-publishing.md`); Gemini ID still needs a human check at ai.google.dev. Pin tags; do not use `latest`. Re-verify quarterly.
- **Rules and context:** `AGENTS.md`, project instructions, skills, memory, and explicit file context; not `.continue/config.json`.

## Why

One stack at launch reduces screenshots, configuration drift, and support load. Cline is the lowest-friction GUI path for beginners; OpenCode is the stronger CLI path for programmers. Continue.dev is no longer a viable forward-looking dependency.

## Consequences

- Week 1 and all setup screenshots must be rebuilt around Cline.
- Free-tier limits, model names, and privacy terms must be date-stamped and reviewed quarterly.
- The programmer track can diverge only after the beginner course rewrite is stable.
- Add a migration note for learners who used the old Continue-based course.
- Tier 2 (4GB GPU) must pass the Week 1 agent loop on real hardware; if it does not, redefine Tier 2 as a 4GB GPU + free-API hybrid in this ADR and in the lessons.
