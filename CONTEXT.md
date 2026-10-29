# Vibe Coding Course

A Russian-first, bilingual course that teaches beginners and programmers to direct AI coding agents. This file is a product glossary only; teaching rules live in `docs/pedagogy.md`, decisions in `docs/adr/`, and the current refresh plan in `docs/2026-refresh-plan.md`.

## Language

**Course**:
The umbrella product: the entire free 8-week content set and the Telegram subscription feed. Paid consultations are a separate service, not part of the course.
_Avoid_: program, training, school.

**Vibe Coding**:
The free entry term and public umbrella used for search and beginner recognition; it names the entry point, not the paid category.
_Avoid_: using it as the name of the paid category (consultations).

**Agentic Engineering**:
The paid category: designing, delegating, and verifying multi-step work performed by AI coding agents.
_Avoid_: vibe coding, prompt engineering (as the whole category).

**Track**:
A learner path through the course. Current tracks are Beginner and Programmer.
_Avoid_: stream, direction, course.

**Creator module**:
An optional applied module inside the Beginner track that teaches an AI-assisted content pipeline for reels, video, and images.
_Avoid_: Creator track, content course (until validated as a separate track).

**Lesson**:
One day-sized unit stored as `Day_M.md`, with a goal, practice, verification, and Daily Mission.
_Avoid_: chapter, module, class.

**Daily Mission**:
The end-of-lesson practical task that produces a verifiable artifact.
_Avoid_: homework, exercise, assignment.

**Self-paced library**:
The async 8-week lesson set that learners can use without live support.
_Avoid_: archive, content, course.

**Open-content**:
The commercial model: the entire course content is free; the only paid offering is 1:1 consultations.
_Avoid_: open-core (implies gated content), freemium.

**Subscriber**:
A person subscribed (free) to the course Telegram channel, where every lesson is posted.
_Avoid_: waitlist, follower, pre-sale.

**Consultation**:
A paid, single, ad-hoc 1:1 session that analyzes the learner's own problem or project. Sold as a single session under НПД and must stay advisory (no program, schedule, homework, or certificate).
_Avoid_: lesson, tutoring, mentoring.

**Learner**:
A person taking the course, whether in the free entry, the self-paced library, or as a consultation client.
_Avoid_: student, user.

**Gateway bot**:
The stateless Telegram bot (@vibecoding_start_bot) that answers /start with a channel invite, records the source in the owner's DM, and forwards free-text messages to the owner. It keeps no server-side state and no database.
_Avoid_: onboarding form, registration bot, chatbot.

**Hook post**:
A short (≤500 character) Threads post that describes a real beginner problem and invites replies; the channel link goes in the card or first reply. Written and posted manually, one per lesson.
_Avoid_: repost, cross-post, announcement (it is a conversation starter, not a lesson copy).

**Named invite link**:
A channel invite link created with a source name (e.g. threads) so joins can be counted per campaign; the secondary attribution mechanism after the gateway bot's ?start= parameter.
_Avoid_: UTM link, tracking link.

**Join snapshot**:
The daily subscriber-count record appended to docs/metrics/subscribers.log by pipeline/snapshot.py (getChatMemberCount), with the delta DM'd to the owner.
_Avoid_: analytics, dashboard, stats export.

**Welcome line**:
The count-only growth line («За сутки канал пополнили ещё N человек…») that the publisher appends to the lesson post when the last two Join snapshot rows show a positive delta. No names, no per-person data.
_Avoid_: welcome message (the bot's greeting), growth post, announcement.

**Join batch greeting**:
The single generic greeting the gateway bot sends to the chat when 1–3 humans join in one update; bot joins and batches over 3 get nothing, and the owner receives an id-only line for the batch.
_Avoid_: personal welcome, member announcement.
