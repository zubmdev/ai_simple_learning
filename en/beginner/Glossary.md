# Glossary

📚 **[← Back to Day 0](./Day_0.md)**

---

## Basic Terms

| Term | Simple Explanation | Example |
|------|--------------------|---------|
| **LLM** (Large Language Model) | "Brain" of AI — program that understands text and generates answers | GPT-OSS, Qwen, Gemma |
| **Prompt** | Your message/request to AI | "Write a Python game" |
| **Code** | Instructions for computer in language it understands | `print("Hello")` |
| **Program** | Set of instructions (code) that computer executes | Game, website, app |
| **Script** | Small program, usually automating something | Script for sorting files |

---

## AI & Models

| Term | Simple Explanation | Example |
|------|--------------------|---------|
| **Model** | Specific version of AI with certain capabilities | qwen3.5:2b, gpt-oss:20b |
| **API** (Application Programming Interface) | Way programs communicate with each other | Groq API, OpenAI API |
| **API Key** | Password for API access | `gsk_abc123...` |
| **Token** | Unit of text for AI (≈ 1 word or part) | "Hello" = ~1-2 tokens |
| **Inference** | Process of AI generating response | AI "thinks" and answers |
| **Context window** | How much text AI can "remember" at once | 4K, 128K, 1M tokens |

---

## Hardware & Local AI

| Term | Simple Explanation | Example |
|------|--------------------|---------|
| **GPU** (Graphics Processing Unit) | Graphics card — needed for fast local AI | NVIDIA RTX 3060 |
| **VRAM** (Video RAM) | GPU memory — more = stronger model | 8GB, 16GB VRAM |
| **CPU** (Central Processing Unit) | Processor — main "brain" of computer | Intel i7, AMD Ryzen 5 |
| **RAM** | Temporary computer memory | 16GB, 32GB RAM |
| **Ollama** | Program for running AI on your computer | `ollama run qwen3.5:2b` |
| **CUDA** | NVIDIA technology for AI acceleration | — |

---

## Programming

| Term | Simple Explanation | Example |
|------|--------------------|---------|
| **Python** | Programming language (most popular for beginners) | — |
| **Library** | Ready-to-use code | `art`, `random` |
| **Dependency** | Library needed for program to work | — |
| **pip** | Python package manager (installs libraries) | `pip install art` |
| **Terminal** | Text interface for commands | cmd, PowerShell, bash |
| **IDE / Code Editor** | Program for writing code | VS Code, PyCharm |
| **Git** | Version control system (saves change history) | — |
| **Repository** | Project folder tracked by Git | GitHub repository |

---

## AI Agents & Tools

| Term | Simple Explanation | Example |
|------|--------------------|---------|
| **Extension** | Plugin for VS Code, adds functionality | Cline, Python |
| **Workspace** | Project folder open in VS Code | — |
| **Terminal (in VS Code)** | Built-in terminal in VS Code | `Ctrl + `` ` |
| **Cline** | AI agent for VS Code: reads files, edits code, and runs commands for your task | Describe the task in the Cline panel |
| **OpenCode** | Terminal (CLI) AI agent — the next step for programmers | `opencode` in the project folder |
| **`AGENTS.md`** | Project rules file for AI agents: what's allowed, what's forbidden, how to verify the result | `AGENTS.md` at the project root |

---

## Agent Loop & Harness

| Term | Simple Explanation | Example |
|------|--------------------|---------|
| **Agent loop** | How an AI agent works: result → context → delegation → verification → recovery | You describe a task → agent edits code → you verify the diff |
| **Context engineering** | Choosing what to show the agent: the right files, logs, rules — within the context budget | Give 2 relevant files instead of the whole project |
| **Agent harness** | Everything that turns a model into an agent: rules, skills, memory, subagents, permissions | Cline + `AGENTS.md` + skills |
| **Skill** | Ready-made playbook for a typical task, reusable | A "check code before commit" skill |
| **Agent memory** | Agent notes: session-scoped (live in the chat) and persistent (saved between sessions) | File with project agreements |
| **Subagent** | Mini-agent the main agent launches for a subtask to spare the main context | Subagent searches the whole project |
| **MCP** (Model Context Protocol) | Protocol connecting tools, resources, and prompts to the agent; servers are local (stdio) or remote | MCP server with GitHub access |
| **Approvals** | You confirm each agent action — least privilege principle | Click Approve before a file edit |
| **Diff review** | Reviewing changes before approval: you see exactly what the agent will change | Red and green lines in the diff |
| **Evals** | Checklist of "input → expected output" to verify the agent works | 5 tasks — all solved correctly |
| **Three access tiers** | Three ways to run AI in the course: CPU + free API; 4GB GPU; 16GB GPU | CPU + Groq `openai/gpt-oss-20b`; 4GB GPU — Ollama `qwen3.5:2b`; 16GB GPU — Ollama `gpt-oss:20b`. Verified: 2026-10-24 |

---

## Vibe Coding

| Term | Simple Explanation | Example |
|------|--------------------|---------|
| **Vibe Coding** | Programming by describing task to AI | "Write a game" → AI writes code |
| **Context** | Information you give AI to understand task | Project files, requirements |
| **Chat** | Q&A mode in AI | — |
| **Edit** | Code editing mode by AI | — |
| **Autocomplete** | AI code completion | — |
| **Creator module** | Applied module inside the Beginner track: AI-assisted content creation (reels, video, images) — a module, not a separate track | — |

---

📚 **[← Back to Day 0](./Day_0.md)**
