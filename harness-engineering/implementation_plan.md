# Technical Course Implementation Plan: "What is an Agent Harness? and How to Build One"

Implementation plan following the system prompt in `v3_Youtube_Technical_Course_System_Prompt.md` for YouTube Video: [https://youtu.be/8vUCjYsWeSU](https://youtu.be/8vUCjYsWeSU) ("What is an Agent Harness? and How to Build One" / Prime-Agent by Muhammad Farooq).

---

## 1. Step 0: Capability Self-Check

| Capability | Detected Status | Active Workflow & Adaptation |
|---|---|---|
| **Reference documents provided** | **YES** | 2 PDF reference documents found in workspace and ingested (`Harness engineering: why agent performance now lives outside the model` and `What is an agent harness? The nine components of a great one`). Following the **Reference Document Integration Protocol**. |
| **Video frame extraction** | **NO (Web URL)** | Remote YouTube URL without local `.mp4` file. Visuals will be reconstructed from transcript + UI schemas + reference doc figures. Slides will carry explicit positioning comments. |
| **Browser tool** | **YES (Node/Playwright via sandbox command)** | Using Node/Puppeteer/Playwright or static coordinate calculation for slide verification. |
| **Firecrawl MCP tools** | **NO** | Falling back to headless browser verification / static verification loop. |
| **Extended output** | **YES** | Emitting full, non-truncated section outputs per response turn. |

---

## 2. Reference Document Inventory

1. **`What is an agent harness_ The nine components of a great one · Muhammad Farooq.pdf`** — *Type: PDF Essay (9 min read / 21 min video companion)* — Detailed breakdown of the 9 core components of an agent harness (Loop, Context Management, Tools & Skills, Sub-agents, Built-in Skills, Session Persistence, System Prompt Assembly, Lifecycle Hooks, Permissions & Safety), framework vs. harness comparison, and Python reference architecture.
2. **`Harness engineering_ why agent performance now lives outside the model · Muhammad Farooq.pdf`** — *Type: PDF Research Essay (10 min read)* — Deep dive into 2026 harness engineering research (Tsinghua's Natural-Language Agent Harness NLAH, Stanford's Meta-Harness, DeepMind's AutoHarness, AgentSpec), module ablations (self-evolution vs. verifiers/search), and operating system analogy.

---

## 3. Course Curriculum & Granular Section Breakdown

To provide exhaustive, second-by-second coverage without skipping or summarizing, the course will be delivered in **10 Granular Sections**, each featuring step-by-step written instructions, code blocks, Mermaid logic diagrams, and a **High-Fidelity Animated HTML Slide** matching the Golden Standard architecture.

### Planned Sections:

- **SECTION 1: Introduction to Agent Harness Engineering [00:00–02:00]**
  - **Topic:** The fundamental formula: `Agent = Model (Weights) + Harness (Operating System)`.
  - **Reference Doc:** `[ref: Harness engineering: why agent performance now lives outside the model]`
  - **Visual:** Mermaid architecture diagram + Animated HTML Slide replicating the LLM-as-CPU / Harness-as-OS model breakdown.

- **SECTION 2: Framework vs. Harness — Resolving the Confusion [02:00–04:30]**
  - **Topic:** Frameworks (LangChain, AutoGen, CrewAI) vs. Harnesses (Claude Code, Codex, Cursor, Windsurf).
  - **Reference Doc:** `[ref: What is an agent harness? The nine components of a great one]`
  - **Visual:** Comparison matrix + Animated HTML Slide of pre-wired harness architecture vs component library.

- **SECTION 3: Component 1 — The Execution Loop [04:30–06:45]**
  - **Topic:** `while` loop mechanics: Read → Act → Observe → Repeat cycle, termination criteria, and iteration caps.
  - **Reference Doc:** `[ref: What is an agent harness? The nine components of a great one]`
  - **Visual:** Loop execution state diagram + Animated HTML Slide showing live turn-by-turn state transitions.

- **SECTION 4: Component 2 — Context Management & Compaction [06:45–09:00]**
  - **Topic:** Context degradation, token thresholds, compaction strategies (recent raw vs old summarized), and silent failure traps.
  - **Reference Doc:** `[ref: What is an agent harness? The nine components of a great one]`
  - **Visual:** Memory window compaction diagram + Animated HTML Slide with highlighted memory buffers.

- **SECTION 5: Component 3 & 5 — Tools, Skills, and Built-in Primitives [09:00–11:30]**
  - **Topic:** Universal tools vs team skills, standard library constraints, registry binding, and built-in coding primitives.
  - **Reference Doc:** `[ref: What is an agent harness? The nine components of a great one]`
  - **Visual:** Tool registry architecture diagram + Animated HTML Slide showing tool execution and output capture.

- **SECTION 6: Component 4 — Sub-Agent Management & Delegation [11:30–13:45]**
  - **Topic:** The "Spawn, Restrict, Collect" pattern, isolated sessions, scope reduction, and token conservation.
  - **Reference Doc:** `[ref: What is an agent harness? The nine components of a great one]`
  - **Visual:** Parent-child agent orchestration diagram + Animated HTML Slide displaying parallel worker execution.

- **SECTION 7: Component 6 & 7 — Session Persistence & Prompt Assembly [13:45–16:00]**
  - **Topic:** Crash-safe append-only JSONL logging, `AGENTS.md` / `CLAUDE.md` discovery pipeline, and prefix caching ordering rules.
  - **Reference Doc:** `[ref: What is an agent harness? The nine components of a great one]`
  - **Visual:** File system persistence pipeline + Animated HTML Slide with JSONL stream and cached system prompt layers.

- **SECTION 8: Component 8 & 9 — Lifecycle Hooks, Permissions, and Safety [16:00–18:15]**
  - **Topic:** Pre-tool allow/deny/modify filters, post-tool auditing, permission modes (read-only / workspace / full), and dynamic command parsing.
  - **Reference Doc:** `[ref: What is an agent harness? The nine components of a great one]`
  - **Visual:** Pre-tool interceptor flow + Animated HTML Slide showcasing real-time permission evaluation and red callout alerts.

- **SECTION 9: Modern Research & Harness Ablation Insights [18:15–20:00]**
  - **Topic:** Tsinghua NLAH (Natural-Language Agent Harness), Stanford Meta-Harness, ablations (Self-Evolution +4.8 vs Verifiers -0.8 / Search -2.4), and loop narrowing over search expansion.
  - **Reference Doc:** `[ref: Harness engineering: why agent performance now lives outside the model]`
  - **Visual:** Ablation bar chart diagram + Animated HTML Slide of self-evolution attempt loop.

- **SECTION 10: Building a Minimal Python Harness & Synthesis [20:00–21:00]**
  - **Topic:** End-to-end Python implementation, zero-dependency philosophy, and final course QA synthesis.
  - **Reference Doc:** `[ref: What is an agent harness? The nine components of a great one]`
  - **Visual:** Full harness class diagram + Animated HTML Slide of running minimal Python agent harness.

---

## 4. Execution Rules & Workflow

1. **Step-by-Step Approval Protocol:** Emitting **SECTION 1** in full detail, then stopping to ask for user approval before moving to **SECTION 2**, per the prompt instructions.
2. **Traceability:** Every fact, code block, or concept drawn from the reference documents will carry `[ref: filename]`, video timestamps `[MM:SS]`, or `[general knowledge]`.
3. **Visual Standard:** Each section includes:
   - Exhaustive direct-voice tutorial steps.
   - Code snippets and key concepts.
   - Mermaid logic diagram.
   - Golden Standard Animated HTML Slide with CSS keyframes, dot-chrome header, editable callout positions, and distinct timing delays.
   - Reference Cross-Check summary.

---

## 5. Verification Plan

### Automated / Browser Verification
- HTML slide code validation (ensuring valid single-file HTML/CSS/JS without external CDN dependencies).
- CSS animation delay sequencing review to guarantee non-overlapping speech bubbles and callout highlights.

### User Review Process
- After generating **SECTION 1**, the assistant will pause for user approval before generating subsequent sections.
