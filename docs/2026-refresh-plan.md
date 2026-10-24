# 2026 Refresh Plan: Vibe Coding -> Agentic Engineering

**Status:** Approved v2, confirmed 2026-10-24 (open-content: free course, paid consultations)

**Scope:** RU-first 8-week course, Beginner and Programmer tracks, Creator module, 90-day open-content launch.

**Decisions:** [ADR-0001](./adr/0001-dual-brand.md), [ADR-0002](./adr/0002-open-content-offer.md), [ADR-0003](./adr/0003-cline-first-stack.md), [ADR-0004](./adr/0004-legal-and-payments.md), [ADR-0005](./adr/0005-in-place-refresh.md), [ADR-0006](./adr/0006-creator-module.md).

## 1. Outcome

By **2027-01-22**:

- 100+ free Telegram subscribers; the entire 8-week RU course stays free and public (repo + channel feed).
- At least 15 paid 1:1 consultation sessions delivered under НПД.
- Three case studies with real artifacts.
- The RU course is current for 2026: no Continue.dev, no `.continue/config.json`, no RAG-first Week 4, no 2024-era models.
- A consultation loop is live: 2-3 slots/week, a чек per session, advisory framing respected.
- EN remains a free lead magnet only; a full EN translation waits for a validated revenue stream.

## 2. Product

### Brand hierarchy

- **Umbrella:** Vibe Coding Course (existing recognition and search demand).
- **Free entry:** Vibe Coding Day 0; then the entire course free on Telegram + repo.
- **Paid product:** Agentic Engineering consultations (RU subtitle: AI-инженерия).
- **Migration:** revisit a full umbrella rename after 100 paying clients.

### Offer

- **Free:** the entire 8-week course. Lessons stay public in the repo; Telegram subscribers get a guided feed (a post per lesson).
- **Paid consultations:** single ad-hoc 60-minute 1:1 sessions under НПД; strict advisory framing per the ADR-0004 boundary. 2-3 slots/week. No gated content, ever. No paid cohort, no certificate, no library SKU.

### Pricing

| Offer | Price | Notes |
|---|---|---|
| 1:1 consultation, 60 min | 60 BYN | Intro price, first 10 sessions; then 90 BYN. НПД, чек |

Do not sell individual weeks, packages, or subscriptions. Revisit pricing after 15 sessions.

### Funnel

Free lesson -> Telegram subscription -> paid consultation (single session) -> repeat sessions for new problems / future products.

### 90-day targets

- 100 free subscribers.
- 15 consultations delivered.
- 3 case studies.
- Consultation revenue ≥ 900 BYN.

## 3. Curriculum

### Tracks

- **Beginner:** no programming background; setup, first agent loop, context, harness, MCP safety, project, debugging, capstone.
- **Programmer:** already ships code; skip syntax, focus on orchestration, review, tests, cost, and advanced tooling.
- **Creator module:** optional applied module inside Beginner; one content pipeline, not a third track.

### Week-by-week refresh

| Week | Current | 2026 outcome | Rewrite order |
|---|---|---|---|
| 1 | Setup + Vibe Coding mindset | Agentic mindset, Cline/Ollama/free API setup, first verified agent loop | First |
| 2 | Prompt engineering | Prompts as specs, acceptance criteria, structured outputs, iteration | First |
| 3 | Context engineering | Context budget, file selection, `AGENTS.md`, terminal/log context | First |
| 4 | RAG and Rules | Agent harness: rules, skills, memory, subagents, permissions | First |
| 5 | MCP introduction | MCP tools, approvals, least privilege, secrets, local vs remote | Second |
| 6 | Real project | Agentic build; Creator module as alternate project | Second |
| 7 | Debugging and refactoring | Debug loop, tests, evals, diff review, rollback | Second |
| 8 | Final project and OSS | Capstone, deployment, cost, portfolio, OSS contribution | Second |

### Creator module

One applied pipeline inside Week 6:

1. Idea -> script -> storyboard.
2. Image/video generation with a FOSS-first stack (ComfyUI, Stable Diffusion/Flux, FFmpeg).
3. Voice, edit, publish (Whisper, Piper, Kdenlive), plus consent, copyright, disclosure, and no-impersonation rules.

The module must include a CPU/free-API path and a 16GB GPU path. A 4GB GPU may require cloud/free APIs for image/video generation; state this explicitly.

### Content rules

- Add a Daily Mission to every lesson.
- Keep the week-table time estimates; do not force two-hour lessons.
- Add a "last verified" date to every setup lesson.
- Replace tool tours with verifiable outcomes.
- Add a migration note for learners who used the old Continue-based course.

## 4. Stack

Full decision: [ADR-0003](./adr/0003-cline-first-stack.md).

- **Beginner:** VS Code + Cline + Ollama or a free API.
- **Programmer upgrade:** OpenCode in P1.
- **Retired:** Continue.dev, `.continue/config.json`, `.continuerules`, RAG-first Week 4.
- **Tier 1:** CPU + Groq, Gemini AI Studio, or OpenRouter.
- **Tier 2:** 4GB GPU + Qwen3 8B or Qwen2.5-Coder 7B (quantized).
- **Tier 3:** 16GB GPU + gpt-oss:20b, Qwen3.6-35B-A3B, or Gemma 4 12B (quantized; verify fit).
- **Rules and context:** `AGENTS.md`, project instructions, skills, memory, explicit file context.
- Pin model tags and API versions. Review quarterly.

## 5. Legal and payments

Full decision: [ADR-0004](./adr/0004-legal-and-payments.md).

- НПД cannot cover the course. The МНС letter of 20.01.2023 № 3-1-13/00223 explicitly treats programming courses, including online courses, as educational activity and limits them to organizations and ИП.
- The course is free forever (marketing, no sale). Paid revenue is single-session 1:1 consultations under НПД only. Do not take course payments as an individual.
- НПД mechanics: «Профессиональный доход» app, a чек per session, 60,000 BYN annual income limit.
- ИП is not required while revenue is consultations only. Reassess when the НПД limit approaches or when any course/cohort/certificate/library product returns; then register ИП (ОКЭД 85.59) before accepting a single course payment.
- No paid course platforms are in scope (Boosty excluded; PaidSub.by/Lava.top/GetCourse dropped with the cohort). Consultation payment: transfer to a personal account before the session; чек after.
- Refund policy: full refund on cancellation ≥24 hours before the session; no refunds after the session.
- Boundary rules: ADR-0004 — advisory framing, no packages, no tethering to course weeks.
- Optional: written accountant or tax confirmation. This is not legal advice.

## 6. Delivery plan

### Phase 0: Setup (Oct 24-31)

- [x] Finalize the approved plan, glossary, pedagogy, and ADRs.
- [x] Publish the rewritten README (open-content offer; no Boosty or $5 table).
- [x] Create the baseline commit and `2026-refresh` branch.
- [ ] Launch the Telegram channel: pinned course-index post, bot form (nick, experience, current task).
- [ ] Start the manual Threads feed (≤500 characters, dedicated attributed t.me invite first, ≤20% of marketing time; kill after 4 weeks with zero inbound).
- [ ] Open 2-3 consultation slots (60 BYN) and run the first sessions.
- [ ] Optional: confirm НПД чек mechanics with the accountant or the 189 hotline.

### P0: Fix the course (Nov 1-14)

- Fix all broken relative links and images.
- Resolve the missing `Week_8/Day_3.md` by collapsing Day 2-3 in the indexes; do not invent a lesson.
- Fix the Week 1 `Day_0.md` link and the Week 8 `README.md` links.
- Remove or replace the 7 link placeholders in `ru/programmer/Week_8/Day_5.md`.
- Add the missing screenshot in `ru/beginner/Week_6/Day_5.md` or replace it with text.
- Replace Continue.dev in Week 1 with Cline; rebuild setup screenshots.
- Verify every model name/API tag exists before writing it into a lesson.
- Test Tier 2 end-to-end on a 4GB GPU; if the Week 1 agent loop fails, ship Tier 2 as a 4GB + free-API hybrid and record the change in ADR-0003.
- Refresh models/APIs and add free-tier privacy warnings.
- Sweep for `Continue`, `config.json`, `qwen2.5`, `llama 3.1`, `deepseek-coder`, `HuggingFace` free tier, and RAG-first Week 4.
- Add "last verified" dates.

### P1: Content refresh (Nov 15-Dec 26)

- Rewrite Weeks 1-5 around the agent loop, specs, context engineering, harness, and MCP safety.
- Update Weeks 6-8 for agentic build, evals, diff review, deployment, cost, and capstone.
- Add the Creator module and free lead magnet.
- Add new lessons: `AGENTS.md`/rules, skills, memory, subagents, permissions, MCP security, evals, cost, sandboxing.
- Update both glossaries with the new vocabulary.
- Test Weeks 1-4 with 3-5 beginners; record time, blockers, and first-artifact time.
- Grow to 100 subscribers; keep the 2-3 consultations/week cadence (≥10 sessions).
- Log every consultation (problem type, repeat request) to prepare the pricing step.

### P2: Scale and consolidate (Dec 27-Jan 22)

- Deliver session 15; decide the pricing step after session 10.
- Publish 3 case studies from consultations and course artifacts.
- Threads keep/kill decision after the 4-week test window.
- First quarterly model/tag re-verification.

### Week 13: Review

- Compare subscriber, session, revenue, and case-study targets.
- Decide: more slots + pricing step; ИП reassessment if the НПД limit nears; EN translation only if a revenue stream is stable.
- Update ADRs if a decision changed.

## 7. Workstreams

| Workstream | Output | Cadence |
|---|---|---|
| Content | 8-week RU refresh, Creator module, glossaries, channel posts | Weekly lesson batch |
| Product | Offer, funnel, pricing step | Weekly |
| Legal/finance | НПД checks and taxes; ИП reassessment trigger | Monthly |
| Marketing | Telegram/YouTube, Threads feeder, case studies | 3 posts/week |
| Ops | Consultation scheduling, чеки, feedback | Weekly |

Use one weekly review: what shipped, what blocked, what metric moved. Keep a decision log in `docs/adr/`.

## 8. Metrics

| Metric | Target | Source |
|---|---|---|
| Free subscribers | 100 | Telegram channel |
| Consultations | 15 | НПД app |
| Consultation revenue | ≥900 BYN | НПД app |
| Repeat rate | ≥30% | App/notes |
| Case studies | 3 | Published |
| Broken links | 0 | Link checker |
| Legacy mentions | 0 | Repo search |
| Daily Mission coverage | 100% | Lesson audit |
| Three access tiers | 100% of setup lessons | Lesson audit |
| CAC | <20 BYN | Manual |
| Time to first artifact | <60 min | User tests |

## 9. Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Consultation drifts into teaching | Legal | Single-session rule; standing slots refused; framing check |
| НПД 60,000 BYN limit | Revenue ceiling | ИП reassessment when approaching |
| 78-lesson workload | Burnout/quality | Prioritize Weeks 1-4; templates; weekly batches |
| Slow subscriber growth | Pipeline | Daily channel cadence; Threads/YouTube feeders; CTA in every lesson |
| Model/API churn | Stale lessons | Pin versions; date-stamp; quarterly review |
| FOSS-only vs creator tools | Contradiction | FOSS-first; label proprietary tools optional |
| Threads/Russia limits | Weak reach | Telegram primary; Threads is a feeder only |
| Consultation quality | Reputation | 2-3 slots/week; session notes per client |
| Secret leakage | Security | `.env`, redaction, approvals, no screenshots with keys |
| Solo capacity | Delay | Timebox; cut P2 extras; ask for help on editing |

## 10. Definition of done

- 100 subscribers, 15 consultations, ≥900 BYN revenue, 3 case studies.
- Weeks 1-4 rewritten and tested with beginners; Weeks 5-8 updated for the 2026 stack.
- Creator module shipped; Telegram cadence stable.
- Every lesson has a Daily Mission, verification, and checklist.
- 0 broken links, 0 legacy mentions, 100% setup lessons with three access tiers.
- Consultation boundary respected (0 program-like sessions).
- ADRs and glossaries match the shipped product.

**Not in scope for 90 days:** paid cohort/beta, certificates, library SKU, gated content, full EN translation, a third full track, a mobile app, a custom community platform, paid ads, and any certification/accreditation. Any of these can return only through an ADR-0004 revisit (with ИП).

## 11. Immediate next 7 days

- [x] Approve the plan and the ADRs; write plan/ADRs/pedagogy/glossary.
- [x] Rewrite the README (open-content offer; no Boosty or $5 table).
- [x] Create the baseline commit and `2026-refresh` branch.
- [ ] Launch the Telegram channel: pinned post + bot form.
- [ ] Start the Threads feed; open 2-3 consultation slots (60 BYN) and run the first sessions.
- [x] Fix the P0 links and the missing Day 3.
- [ ] Rewrite Week 1 setup with Cline; test with 3 beginners.

## 12. Open implementation choices

These do not block the plan:

- Exact FOSS image/video stack for the Creator module.
- Whether a paid cohort/library SKU ever returns (requires an ADR-0004 revisit + ИП).
- Whether to keep `programmer/Week_8/Day_2.md` as "Day 2-3" or split it.
