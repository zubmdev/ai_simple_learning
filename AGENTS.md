# AGENTS.md

## Repo at a glance

- Static Markdown course (RU/EN), 8 weeks. Content is pure Markdown; the only code is `pipeline/` (Telegram publish: `convert.py` md→rich-md, `publisher.py` Bot API client; stdlib-only, `python3 -m unittest discover -s pipeline`), which the "no build/tests" rule below doesn't apply to.
- RU is the only complete track: `ru/beginner` and `ru/programmer`, each with `Week_N.md` (index), `Week_N/Day_M.md` (lessons), and optional `Week_N/images/`.
- EN is an unfinished mirror: only `en/beginner/Day_0.md` and `en/beginner/Glossary.md` exist. There are no EN week lessons.
- `ru/beginner/Day_0.md` is the free intro; programmer tracks have no Day 0.

## Sources of truth

- `CONTEXT.md` is the product glossary. It is **not auto-loaded** (opencode.json injects only this file), so read it before naming product concepts.
- `docs/pedagogy.md` is the authoritative teaching/tone spec. Read it before writing or editing lessons.
- `docs/adr/` records hard-to-reverse decisions. Read the ADRs that touch the area you are changing.
- `docs/2026-refresh-plan.md` is the current refresh plan, offer, stack, metrics, and 90-day sequencing.
- `README.md` is the public catalog. It was rewritten 2026-10-24 to the open-content offer (free course + paid consultations); do not reintroduce Boosty or per-week prices.
- RU is the complete source; existing EN files are translations of RU counterparts. Don't mass-translate EN unless asked.

## Content rules (from docs/pedagogy.md)

- Every practical setup needs three access tiers: CPU + free API (Groq/Gemini/OpenRouter), 4GB GPU (Ollama), 16GB GPU (Ollama). Exact models and APIs live in `docs/adr/0003-cline-first-stack.md`; date-stamp them.
- FOSS-first: VS Code, Cline for beginners, OpenCode as the programmer upgrade, Ollama, Node/Python examples. Continue.dev is retired; do not add new Continue instructions or `.continue/config.json`.
- Teach delegation, context, and verification; never teach language syntax.
- House style: emoji section markers, fenced prompt/config blocks, a "Daily Mission" practical task.
- Time estimates conflict: README says ~2h/day, and week tables range 10–120 min/day. Treat the week-table times as current truth; don't rewrite them all to 2h.
- "Daily Mission" currently appears only in beginner Weeks 1–7 and programmer Weeks 5–7; the refresh must add it everywhere.

## 2026 refresh

- Plan: `docs/2026-refresh-plan.md`. Decisions: `docs/adr/`.
- Replace the old stack in new or edited lessons: no Continue.dev, `.continue/config.json`, RAG-first Week 4, or 2024-era models.
- New material must teach the agent loop, context engineering, `AGENTS.md`/rules, skills, memory, subagents, MCP security, evals, diff review, and deployment cost.
- Keep the Creator module inside Beginner for now; do not create a third track.

## Layout and lesson shape

- Paths are fixed: `<lang>/<track>/Week_N.md`, `<lang>/<track>/Week_N/Day_M.md`; images live in `Week_N/images/` and are referenced as `./images/foo.png`.
- Week indexes link every day with a time and a learner status column. That status is student progress, not an authoring TODO.
- Day lessons: H1 title, `**Трек:** ... | **Время:** ...` header (all programmer days, most beginner days), goal-of-the-day section, practice, checklist, "what's next", and a prev/next footer. Match the neighboring lesson's structure.
- Beginner days run ~30–60 min (Week 1 is ~2h/day); programmer days ~10–50 min.

## Traps

- `opencode.json` was inherited from an unrelated Rust project (`car_data_intelligence` — cargo agents, `pharos` MCP, `target/**`/`models/ocr/**`/`web/*` watcher ignores) and cleaned up 2026-10-25; don't reintroduce its artifacts or infer this repo's structure from config history.
- `skills-lock.json` and `.agents/skills/` are vendored third-party skills (mattpocock/skills), not course content; don't rewrite them.
- `.env` is gitignored and only defines `GROQ_API_KEY`; never put real keys in lessons.
- Known broken links: `ru/*/Week_8/Day_3.md` is missing in both tracks (footer links skip it).

## Verification

No build or test step. The main regression risk is relative links/images. After edits, run:

```bash
python3 - <<'PY'
import re, pathlib
for md in pathlib.Path('.').glob('[er][nu]/**/*.md'):
    for t in re.findall(r'!?\[[^]]*\]\(([^)#]+)', md.read_text(encoding='utf-8')):
        if not t.startswith(('http','mailto:')) and not (md.parent/t).exists():
            print(f'{md}: {t}')
PY
```

## Agent skills

### Issue tracker

Local markdown under `.scratch/<feature>/`. See `docs/agents/issue-tracker.md`.

### Triage labels

Default five roles (needs-triage, needs-info, ready-for-agent, ready-for-human, wontfix). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: root `CONTEXT.md` + `docs/adr/`. Teaching rules: `docs/pedagogy.md`. Current plan: `docs/2026-refresh-plan.md`. See `docs/agents/domain.md`.
