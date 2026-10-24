# Cline-first stack; OpenCode later; retire Continue.dev

**Status:** accepted

**Date:** 2026-10-24

The beginner course uses **VS Code + Cline + Ollama or a free API**. The programmer track adds **OpenCode** as an advanced upgrade in P1, not at launch. **Continue.dev is retired**; it is read-only/final after the Cursor acquisition and must not appear in new lessons.

## Stack baseline

- **Editor:** VS Code.
- **Beginner agent:** Cline.
- **Programmer agent:** OpenCode (P1).
- **Local runtime:** Ollama.
- **Local models:** Qwen3 8B, Qwen2.5-Coder 7B/14B, gpt-oss:20b, Qwen3.6-35B-A3B, Gemma 4 12B. Pin tags; do not use `latest`.
- **Free APIs:** Groq, Gemini AI Studio, OpenRouter. HuggingFace free inference is no longer viable for this course.
- **Rules and context:** `AGENTS.md`, project instructions, skills, memory, and explicit file context; not `.continue/config.json`.

## Why

One stack at launch reduces screenshots, configuration drift, and support load. Cline is the lowest-friction GUI path for beginners; OpenCode is the stronger CLI path for programmers. Continue.dev is no longer a viable forward-looking dependency.

## Consequences

- Week 1 and all setup screenshots must be rebuilt around Cline.
- Free-tier limits, model names, and privacy terms must be date-stamped and reviewed quarterly.
- The programmer track can diverge only after the beginner course rewrite is stable.
- Add a migration note for learners who used the old Continue-based course.
- Tier 2 (4GB GPU) must pass the Week 1 agent loop on real hardware; if it does not, redefine Tier 2 as a 4GB GPU + free-API hybrid in this ADR and in the lessons.
