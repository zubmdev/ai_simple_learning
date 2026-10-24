# Pedagogy

Teaching rules for the 2026 refresh. Product vocabulary is in `../CONTEXT.md`; hard-to-reverse choices are in `./adr/`; delivery sequencing is in `./2026-refresh-plan.md`.

## Purpose

Teach learners to direct AI agents through the full loop: define the outcome, supply context, delegate, inspect the result, verify it, and recover when it fails. The course is not a language tutorial and not a tour of AI features.

## Audience

- **Beginner track:** people who have never programmed. Start with outcomes, not syntax. Every command and screen must be explained.
- **Programmer track:** people who already ship code. Skip language basics and focus on agent orchestration, review, testing, and cost.
- **Creator module:** beginners who want an AI-assisted content pipeline for reels, video, and images. It is an applied module, not a third track until demand is validated.

## Tone

Be encouraging, concrete, and concise. Use short explanations, real examples, and visible checkpoints. Avoid academic framing, hype, and tool worship. When a topic is contested, say what is stable and what is likely to change.

## Non-negotiables

1. **Teach delegation, context, and verification, not syntax.** The learner should be able to explain what the agent did, why it did it, and how the result was checked.
2. **Every lesson has a verifiable outcome.** Each lesson ends with an artifact, a command, a test, or a review checklist that proves the learner made progress.
3. **Three access tiers.** Every practical setup must offer CPU + free API, 4GB GPU via Ollama, and 16GB GPU via Ollama. Exact models and APIs live in [ADR-0003](./adr/0003-cline-first-stack.md); date-stamp them and review quarterly.
4. **FOSS-first.** Default to free and open-source tools. If a proprietary tool is materially better for a creator workflow, label it optional and provide a FOSS alternative.
5. **Russian is the source language.** English is a translation/lead-magnet layer, not a parallel authoring burden. Do not mass-translate EN until the paid offer is validated.
6. **Time comes from the week table.** Do not impose a blanket two-hour lesson. Week 1 may be longer; later lessons should fit the time shown in the index.
7. **Security is part of the lesson.** Never put real keys in prompts, screenshots, or lessons. Use `.env`, redact secrets, require approvals for tool calls, and teach least privilege.
8. **Review before trust.** Agents produce diffs, not truth. Teach diff review, tests, rollback, and a second verification path.
9. **Creator ethics are explicit.** Cover consent, copyright, disclosure, and no impersonation in the Creator module.
10. **No legacy stack.** Continue.dev, `.continue/config.json`, RAG-first Week 4, and 2024-era model names are retired. Do not reintroduce them in new lessons.

## Lesson shape

Match the neighboring lesson, with these required parts:

1. H1 title.
2. `**Трек:** ... | **Время:** ...` header where the track uses it.
3. Goal of the day: what the learner will be able to do.
4. Short concept section with one concrete analogy.
5. Guided practice with copyable prompts and commands.
6. Verification: how the learner knows it worked.
7. Checklist of completed steps.
8. "What's next" and a prev/next footer.
9. **Daily Mission**: a small, verifiable task that uses the day's skill.

Use emoji section markers consistently. Put every prompt and config example in a fenced block. Prefer one strong example over five shallow ones.

## Markdown and assets

- Use `🚨`, `💡`, `🛠️`, `🧠`, and `🎯` as section markers where they help scanning.
- Put prompts, commands, and config in fenced blocks with a language tag.
- Store images in the week's `images/` directory and reference them as `./images/foo.png`.
- Add alt text to every image.
- Do not use screenshots as the only explanation; include text steps that survive a UI change.

## Verification standard

A lesson is ready when:

- a beginner can follow it without asking for missing steps;
- every command has an expected result;
- every prompt has a success criterion;
- the learner can undo or recover from the agent's mistake;
- the lesson has a Daily Mission and a checklist;
- no secret, stale model name, or retired tool appears;
- all relative links and images resolve.

## Deprecated patterns

- Continue.dev as the primary assistant; it is read-only/final after the Cursor acquisition.
- `.continue/config.json` and `.continuerules` as the rules mechanism.
- RAG-first Week 4; replace it with context engineering, repo maps, `AGENTS.md`, skills, and memory.
- Qwen 1.5B/3B, Llama 3.1 8B, and DeepSeek Coder as the default local models.
- "Vibe coding" as the paid category; it remains the free entry term.
- A blanket two-hour lesson rule.
- Tool tours without a verifiable outcome.

## Review cadence

Review model names, API limits, screenshots, and setup steps every quarter. Add a "last verified" date to setup lessons. When a tool changes materially, update the lesson and the stack ADR rather than adding a second parallel path.
