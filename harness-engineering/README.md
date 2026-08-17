# Harness Engineering: AI Agent Scaffolding & Technical Course

This repository contains a comprehensive technical course, reference implementation, and interactive visual slides based on **Harness Engineering** research and the video tutorial *"What is an Agent Harness? and How to Build One"* (Prime-Agent) by Muhammad Farooq.

An **Agent Harness** is the operating system layer wrapped around an LLM—managing execution loops, context compaction, tool registries, sub-agent delegation, session persistence, prompt assembly, hooks, and safety. Research demonstrates that harness engineering accounts for up to **6x performance variance** on complex engineering benchmarks, making the harness layer the primary site of architectural differentiation in modern AI systems.

---

## 📁 Repository Contents

harness-engineering/

├── README.md                                         \# Project documentation & instructions

├── agent\_harness\_technical\_course.md                 \# Complete 10-Section Written Tutorial & Course

├── implementation\_plan.md                            \# Execution plan & capability audit

├── minimal\_harness.py                                \# Zero-dependency 9-component Python reference implementation

├── v3\_Youtube\_Technical\_Course\_System\_Prompt.md      \# Master system prompt defining generation rules

├── Harness engineering\_...· Muhammad Farooq.pdf      \# Reference Paper 1: NLAH & Meta-Harness research

├── What is an agent harness\_...· Muhammad Farooq.pdf  \# Reference Paper 2: 9 Harness Components essay

└── slides/                                           \# 10 High-Fidelity Animated HTML Slides

    ├── section\_1\_os\_analogy.html                     \# Section 1: OS Analogy (CPU/RAM/Disk/Drivers)

    ├── section\_2\_framework\_vs\_harness.html           \# Section 2: Framework vs Harness Architecture

    ├── section\_3\_execution\_loop.html                 \# Section 3: Component 1 — The Execution Loop

    ├── section\_4\_context\_compaction.html             \# Section 4: Component 2 — Context Compaction

    ├── section\_5\_tools\_and\_skills.html               \# Section 5: Component 3 & 5 — Tools vs Skills

    ├── section\_6\_subagent\_delegation.html            \# Section 6: Component 4 — Sub-Agent Delegation

    ├── section\_7\_persistence\_and\_prompts.html        \# Section 7: Component 6 & 7 — Session Persistence & Prompts

    ├── section\_8\_hooks\_and\_permissions.html          \# Section 8: Component 8 & 9 — Hooks & Safety

    ├── section\_9\_ablation\_research.html              \# Section 9: Tsinghua NLAH & Meta-Harness Ablations

    └── section\_10\_minimal\_harness\_synthesis.html     \# Section 10: 9-Component Architecture Synthesis

---

## 🖥️ How to View the Animated HTML Slides

All slides in the `slides/` directory are single-file, standalone HTML documents with embedded CSS keyframe animations and dot-chrome browser frames.

### Option 1: Direct File Opening

- **macOS / Linux:** Double-click any `.html` file in `slides/` or run:  
    
  open slides/section\_1\_os\_analogy.html  
    
- **Windows:** Double-click the file in File Explorer or open via Chrome / Edge / Firefox.

### Option 2: Local Web Server (using Astral `uv`)

To preview all slides seamlessly in your browser with standard web URLs:

uv run python \-m http.server 8000

Then navigate to:

- `http://localhost:8000/slides/section_1_os_analogy.html`  
- `http://localhost:8000/slides/section_2_framework_vs_harness.html`  
- (or any slide `section_1` through `section_10`)

---

## ✏️ How to Edit & Fine-Tune HTML Slide Callouts

Each slide includes editable CSS properties for **callout positioning** (`top`, `left`, `width`, `height`) and **animation timing** (`animation-delay`). If a red callout highlight box or speech bubble bubble needs adjustment to fit your display resolution or target screen element, edit the corresponding `.html` file directly.

### 1\. Adjusting Callout Box Position & Proportions

Open the `.html` file in your code editor and locate the callout ID CSS blocks near the bottom of the `<style>` element:

/\* \--- EDITABLE CALLOUT POSITIONING \--- \*/

\#callout-highlight-box {

  top: 245px;     /\* Adjust vertical offset from top of container \*/

  left: 360px;    /\* Adjust horizontal offset from left of container \*/

  width: 580px;   /\* Adjust width of red highlight box \*/

  height: 250px;  /\* Adjust height of red highlight box \*/

}

- **To move right/left:** Increase or decrease `left` (e.g., `left: 380px`).  
- **To move up/down:** Increase or decrease `top` (e.g., `top: 220px`).  
- **To resize the red box:** Modify `width` and `height` to enclose your desired UI element cleanly.

---

### 2\. Adjusting Speech Bubble Arrows & Positioning

Speech bubble text callouts rely on a parent container `#id` and pseudo-element `::after` arrow:

\#callout-text-bubble {

  top: 190px;

  left: 620px;

}

/\* Adjust speech bubble arrow direction/position \*/

\#callout-text-bubble::after {

  content: '';

  position: absolute;

  bottom: \-8px;   /\* \-8px places arrow pointing DOWN at top of box \*/

  left: 24px;     /\* Horizontal offset of arrow along bubble \*/

  border-width: 8px 8px 0;

  border-style: solid;

  border-color: \#ef4444 transparent;

}

---

### 3\. Adjusting Animation Delay (Timing Sync)

To change when a callout appears during video narration or slide playback, locate the `animation-delay` property:

.callout-border-box {

  opacity: 0;

  /\* Change '2.5s' to delay or speed up when the red box draws \*/

  animation: fadeIn 0.5s ease-out 2.5s forwards;

}

.callout-bubble {

  opacity: 0;

  /\* Change '2.7s' to synchronize bubble pop-in after border draw \*/

  animation: fadeIn 0.4s ease-out 2.7s forwards;

}

---

## ⚡ How to Install, Run & Use `minimal_harness.py` (Using Astral `uv`)

This project strictly adheres to [Astral `uv`](https://github.com/astral-sh/uv) for fast, robust, zero-config Python execution. **No conda, virtualenv, or pydotenv setup is required.**

### 1\. Install `uv` (if not already installed)

- **macOS / Linux:**  
    
  curl \-LsSf https://astral.sh/uv/install.sh | sh  
    
- **Homebrew:**  
    
  brew install uv

---

### 2\. Running `minimal_harness.py` with `uv`

Because `minimal_harness.py` is written using **Python Standard Library primitives only** (`os`, `sys`, `json`, `time`, `subprocess`, `pathlib`), you can run it instantly with zero dependency installation:

uv run python minimal\_harness.py

#### Expected Output:

🚀 Initializing Minimal Harness with goal: 'Fix issue \#402 in repo.'

🔄 Turn 1/25 \- Context Message Count: 2

✅ Harness Loop Initialized & Verified.

---

### 3\. Inspecting the Harness Session Logs

`minimal_harness.py` features an append-only JSONL session logger (**Component 6**). When executed, it creates/appends events to `session_log.jsonl`:

cat session\_log.jsonl

#### Example Log Record:

{"timestamp": 1770956800.12, "type": "SESSION\_START", "data": {"goal": "Fix issue \#402 in repo."}}

---

### 4\. Customizing Tasks & Workspace Rules

To test dynamic **System Prompt Assembly** (**Component 7**):

1. Create an `AGENTS.md` or `CLAUDE.md` file in the root workspace directory.  
2. Run the harness via `uv`:  
     
   uv run python minimal\_harness.py  
     
3. The harness automatically discovers `AGENTS.md`, injects it into the prompt pipeline behind static system rules, and maintains KV-cache prefix hits\!

---

## 📚 Key Research References

- **Tsinghua NLAH Paper (2026):** Natural-Language Agent Harnesses — proved that rewriting control logic into NLAH increased benchmark resolve rates from **30.4% to 47.2% (+16.8 pts)** and collapsed LLM call counts from 1,200 to 34 calls.  
- **Stanford Meta-Harness Paper (2026):** Meta-Harness — automatically optimizes harness pipelines using raw execution traces (\~10M tokens/iter), taking Claude Haiku to **\#1 on Terminal-Bench 2 (76.4%)** over larger hand-engineered models.  
- **The Lesson of Subtraction:** Harness engineering is a craft of subtraction: self-evolution attempt loops help (+4.8 pts), whereas added verifiers (-0.8 to \-8.4 pts) and multi-candidate search (-2.4 to \-5.6 pts) degrade performance.

