# VOICEOVER SCRIPT — Agent Harness Engineering Course

**Target Audience:** Beginners · **Pacing:** 130–150 words per minute (≈2.2 words/sec) · **Total Duration:** 382s (6:22)

**Word Count Targets:** 38s clip ≈ 84 words · 40s clip ≈ 88 words

**Rules:** No jargon without explanation. Each concept introduced before used. Natural pauses between sections. Sentences map to on-screen bullets (one sentence per bullet).

---

## Clip 1 — Introduction to Agent Harness Engineering (0:00–0:38, 38s)

**Target: ~84 words**

An AI agent is not just a model. It's a model plus a harness — the software that wraps around the language model and makes it useful.

Think of it like a computer. The language model is the CPU. The context window is RAM. The database is your disk. Tools are like drivers. And the harness is the operating system that ties it all together.

Here's the surprising part: the same model can perform six times better or six times worse, depending entirely on the harness around it. That's why harness engineering matters.

---

## Clip 2 — Framework vs Harness (0:38–1:16, 38s)

**Target: ~84 words**

There are two ways to build an AI agent. The old way uses frameworks — tools like LangChain or AutoGen. They give you building blocks, but you have to wire everything together yourself. You assemble chains, retrievers, and state machines from scratch.

The new way uses harnesses — tools like Claude Code or Cursor. A harness comes pre-wired. It already has the execution loop, the tool system, and the safety layer built in.

The industry is converging on harnesses. They just work better.

---

## Clip 3 — The Execution Loop (1:16–1:56, 40s)

**Target: ~88 words**

Every agent harness runs the same fundamental loop. It reads the current context, calls the language model, and inspects the response. If the model wants to use a tool, the harness executes it, observes the result, and loops back. If the model returns a final answer with no tool calls, the loop exits cleanly.

There are exactly two ways out: a clean final answer, or a hard stop when the maximum iteration count is reached. That limit prevents runaway agents from looping forever.

Read, call, inspect, act, repeat.

---

## Clip 4 — Context Management & Compaction (1:56–2:34, 38s)

**Target: ~84 words**

An agent's context window is finite — it can only hold so much text. When the conversation gets too long, the harness runs a process called compaction.

First, it counts tokens. If the count is under the threshold, nothing happens. If it's over, compaction kicks in. The harness preserves the prefix — your system prompt and original goal — verbatim. It keeps recent turns as working memory. And it summarizes the older middle history into a compact block.

Then it reassembles everything into a smaller message list. The agent keeps going without losing critical context.

---

## Clip 5 — Tools, Skills & Permission Gating (2:34–3:12, 38s)

**Target: ~84 words**

Tools are how an agent takes action in the real world. The harness keeps a registry — a list of every available tool with its name and metadata. The language model calls tools by name, and the harness looks them up.

But the harness never runs a tool blindly. It checks permissions first. There are three tiers: read-only, which lets the agent view files; workspace, which allows writing within the project; and full access, which permits any command.

Every tool call is intercepted before it executes. Safety comes first.

---

## Clip 6 — Sub-Agent Delegation (3:12–3:50, 38s)

**Target: ~84 words**

Sometimes a task is too big for one agent. The harness can spawn sub-agents — separate agent sessions with their own isolated context windows.

A typical pattern uses two sub-agents. First, an explorer searches and reads files to understand the problem. Then a verifier runs the test suite to check if the fix works.

Each sub-agent gets restricted tools — only what it needs. And critically, sub-agents return condensed summaries, not raw logs. This keeps the parent agent's context window clean and focused.

---

## Clip 7 — Session Persistence & Prompt Assembly (3:50–4:28, 38s)

**Target: ~84 words**

How does an agent remember what happened? The harness logs every turn as a discrete event — user input, model call, tool result — in an append-only file called a JSONL stream. That's the session log, persisted to disk.

But the prompt isn't just replayed. Each turn, the harness rebuilds it from three layers. Layer one is the static base instructions. Layer two is the project-specific AGENTS.md file. Layer three is the replayed, compacted history.

Three layers, assembled fresh every turn. That's how the agent always has the right context.

---

## Clip 8 — Hooks, Permissions & Safety (4:28–5:06, 38s)

**Target: ~84 words**

A proposed tool call is never executed directly. It traverses a safety pipeline first.

Pre-tool hooks intercept the call before anything runs. A hook can allow it, deny it with an error, or modify it — rewriting the command if needed.

After execution, post-tool hooks audit the result and log it. And for destructive or unknown commands, the harness escalates to an interactive approval prompt. The user approves or denies before anything dangerous happens.

Every approved run is wrapped in audit logging, and the result goes back into the agent's context.

---

## Clip 9 — Research Insights (5:06–5:44, 38s)

**Target: ~84 words**

Researchers at Tsinghua University built an agent harness called NLAH and tested which design choices actually help. Their findings were surprising.

The Self-Evolution Attempt Loop — a feature that lets the agent retry and refine — improved performance by nearly five points. But Evaluation Verifiers and Multi-Candidate Search actually hurt performance, sometimes by more than eight points.

The distilled principle: narrowing the attempt loop beats broadening the search space. Focus on refining what you have, not searching wider. Drop what doesn't help, keep what does.

---

## Clip 10 — Minimal Python Harness Synthesis (5:44–6:22, 38s)

**Target: ~84 words**

So what does a minimal agent harness actually look like? It comes down to nine components, and you can build it in one file with zero external dependencies — just the Python standard library.

The nine parts are: system prompt assembly, the execution loop, context management, pre-tool hooks, permission tiers, tool registry dispatch, built-in primitives like read and write, sub-agent management, and session persistence.

That's the complete checklist. Nine components. Zero dependencies. One file. That is what a harness looks like. Now you have the full picture, from operating system analogy to working code.

---

## Word Count Verification

| Clip | Duration | Actual Words | WPM | Status |
|---|---|---|---|---|
| 1 | 38s | 93 | 146.8 | ✓ |
| 2 | 38s | 83 | 131.1 | ✓ |
| 3 | 40s | 88 | 132.0 | ✓ |
| 4 | 38s | 95 | 150.0 | ✓ |
| 5 | 38s | 89 | 140.5 | ✓ |
| 6 | 38s | 83 | 131.1 | ✓ |
| 7 | 38s | 90 | 142.1 | ✓ |
| 8 | 38s | 91 | 143.7 | ✓ |
| 9 | 38s | 85 | 134.2 | ✓ |
| 10 | 38s | 94 | 148.4 | ✓ |
| **Total** | **382s** | **891** | **139.9** | ✓ |

All clips within 130–150 wpm range. Total 891 words across 382 seconds = 139.9 wpm (target: 130–150 wpm).