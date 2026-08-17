# STORYBOARD — Agent Harness Engineering Course

**Composition:** `agent-harness-engineering` · **Total Duration:** 382s (6:22) · **Clips:** 10 · **Resolution:** 1920×1080

**Design System:** Dark tech theme `#090d16` slate gradient · Inter (headers/body) + JetBrains Mono (badges/code/metrics) · Glassmorphism cards `rgba(22,27,38,0.85)` + `backdrop-filter: blur(12px)` · Electric accents: Cyan `#38bdf8`, Emerald `#3fb950`, Amber `#d29922`, Ruby `#f85149`, Purple `#a371f7` · Brick-snapping diagram nodes · Glowing SVG connectors · Kinetic text reveals · Timeline progress bar.

**Pacing Standards (from HYPERFRAMES_HOT_TIPS.md):**

| Element | Timing Rule |
|---|---|
| Badge / Title | `clip_start + 0.7s` |
| Subtitle | `title_start + 1.8s` |
| First card (left) | `subtitle_start + 3.0s` |
| Second card (right) | `left_card_start + 9–10s` (Two-Card Rule) |
| Bullets (stagger) | `1.5s` per bullet |
| Diagram nodes (stagger) | `5s` per node |
| Code lines (stagger) | `0.8s` per line |
| Callout / summary | Last 10–12s of clip |

---

## Clip Timing Summary

| Clip | Section | data-start | data-duration | End |
|---|---|---|---|---|
| 1 | Introduction to Agent Harness Engineering | 0 | 38 | 38 |
| 2 | Framework vs Harness | 38 | 38 | 76 |
| 3 | The Execution Loop | 76 | 40 | 116 |
| 4 | Context Management & Compaction | 116 | 38 | 154 |
| 5 | Tools, Skills & Permission Gating | 154 | 38 | 192 |
| 6 | Sub-Agent Delegation | 192 | 38 | 230 |
| 7 | Session Persistence & Prompt Assembly | 230 | 38 | 268 |
| 8 | Hooks, Permissions & Safety | 268 | 38 | 306 |
| 9 | Research Insights | 306 | 38 | 344 |
| 10 | Minimal Python Harness Synthesis | 344 | 38 | 382 |

---

## Clip 1 — Introduction to Agent Harness Engineering

| Attribute | Value |
|---|---|
| **Section** | 1 — Introduction to Agent Harness Engineering |
| **data-start** | `0` |
| **data-duration** | `38` |
| **data-track-index** | `1` |

### Content Layout

| Element | Local Offset | Absolute Time | Details |
|---|---|---|---|
| Badge | +0.7s | 0.7s | `SECTION 01` — JetBrains Mono, Cyan `#38bdf8`, glassmorphism pill |
| Title | +0.7s | 0.7s | "Agent Harness Engineering" — Inter Bold 64px, white, fade-up |
| Subtitle | +2.5s | 2.5s | "What wraps an LLM to make it an agent?" — Inter 28px, slate-300 |
| Left Card | +5.5s | 5.5s | **"Agent = Model + Harness"** — glassmorphism card, Cyan border accent |
| Left Bullets | +7.0s → +11.5s | 7.0/8.5/10.0/11.5s | • Model = the brain (LLM) · • Harness = everything around it · • Analogy: OS wraps a CPU · • Same model, 6× performance difference |
| Right Card | +14.5s | 14.5s | **"The OS Analogy"** — glassmorphism card, Purple `#a371f7` border |
| Right Bullets | +16.0s → +22.0s | 16.0/17.5/19.0/20.5/22.0s | • LLM = CPU · • Context = RAM · • Database = Disk · • Tools = Drivers · • Harness = Operating System |
| Callout | +26.0s | 26.0s | "The harness is the operating system for your AI agent." — Amber `#d29922` accent box, last 12s |

### Visual Elements (from Qwen analysis — sec1-AI Agent System Architecture)

- Six horizontal brick-snapping nodes in a single row: LLM Engine, Loop & Execution Controller, Context Window, External DB / State Files, Tool Registry, Permissions & Hooks
- Context Window rendered as a left-flat blue cylinder; External DB as a green 3D database cylinder
- Cyan borders on rounded rectangles, blue label text
- No explicit arrows — conceptual peer layout; glowing SVG connectors added for motion
- Nodes animate in at 5s stagger starting at +5.5s (first node), continuing through the row
- Ambient glow circles behind the row, subtle grid overlay

---

## Clip 2 — Framework vs Harness

| Attribute | Value |
|---|---|
| **Section** | 2 — Framework vs Harness |
| **data-start** | `38` |
| **data-duration** | `38` |
| **data-track-index** | `1` |

### Content Layout

| Element | Local Offset | Absolute Time | Details |
|---|---|---|---|
| Badge | +0.7s | 38.7s | `SECTION 02` — Cyan pill |
| Title | +0.7s | 38.7s | "Framework vs Harness" — Inter Bold 64px |
| Subtitle | +2.5s | 40.5s | "Two paradigms for building AI agents" — Inter 28px |
| Left Card | +5.5s | 43.5s | **"Frameworks"** — Amber `#d29922` border, "Build from parts" |
| Left Bullets | +7.0s → +11.5s | 43.5/45.0/46.5/48.0s | • LangChain, AutoGen · • Manual wiring of chains & retrievers · • You assemble the pipeline · • Building blocks, not a working agent |
| Right Card | +14.5s | 52.5s | **"Harnesses"** — Emerald `#3fb950` border, "Pre-wired & ready" |
| Right Bullets | +16.0s → +22.0s | 54.0/55.5/57.0/58.5s | • Claude Code, Cursor · • Pre-wired execution loop · • Targets user goals directly · • Industry is converging here |
| Callout | +26.0s | 64.0s | "Frameworks give you parts. Harnesses give you a working agent." — Emerald accent, last 12s |

### Visual Elements (from Qwen analysis — sec2-Framework vs Harness Paradigms)

- Two parallel columns of rounded rectangles: Amber-bordered on left (Framework), Ruby-bordered on right (Harness)
- Three horizontal glowing SVG arrows pointing left-to-right pairing each column:
  - Manual Wiring → Pre-Wired Engine
  - Custom App Pipeline → User Goal Execution
  - Building Blocks → Integrated Loop
- Cards animate in column-by-column; left column first (stagger 5s), arrows draw at +12s, right column at +14.5s
- Small caption text beneath each box explaining its meaning

---

## Clip 3 — The Execution Loop

| Attribute | Value |
|---|---|
| **Section** | 3 — The Execution Loop |
| **data-start** | `76` |
| **data-duration** | `40` |
| **data-track-index** | `1` |

### Content Layout

| Element | Local Offset | Absolute Time | Details |
|---|---|---|---|
| Badge | +0.7s | 76.7s | `SECTION 03` — Cyan pill |
| Title | +0.7s | 76.7s | "The Execution Loop" — Inter Bold 64px |
| Subtitle | +2.5s | 78.5s | "The heartbeat of every agent harness" — Inter 28px |
| Left Card (Diagram) | +5.5s | 81.5s | **"The While Loop"** — flowchart diagram card, Cyan border |
| Diagram Nodes | +5.5s → +25.5s | 81.5/86.5/91.5/96.5/101.5s | 5s stagger: Initialize → Read Context → Call LLM → Evaluate Output → (branch) |
| Branch Labels | +26.5s | 102.5s | "No Tool Calls → Final Answer" / "Tool Calls → Execute → Observe → loop back" |
| Right Card | +16.5s | 92.5s | **"Two Exit Conditions"** — glassmorphism card, Purple border |
| Right Bullets | +18.0s → +24.0s | 94.0/95.5/97.0/98.5s | • Clean exit: model returns final answer (no tool calls) · • Hard stop: max iterations exceeded · • Each turn appends tool observations · • Bounded by a max iteration counter |
| Callout | +28.0s | 104.0s | "Read → Call → Inspect → Act → Repeat. Two ways out." — Cyan accent, last 12s |

### Visual Elements (from Qwen analysis — sec-3 Harness Execution Loop)

- Blue rounded process boxes with small icons and two-line labels
- Two Orange hexagonal decision nodes (Evaluate Output, Check Iteration Limit) — rendered with Amber `#d29922` accent
- Branch labels in Cyan text on arrows: "No Tool Calls" / "Tool Calls" / "Max Reached" / "Not Max"
- Long feedback loop-back line from Check Iteration Limit returning to before Read Context
- Two terminal exit paths converging on a single "Task Complete" node
- Nodes animate at 5s stagger; decision hexagons pulse on appear; loop-back arrow draws with GSAP

---

## Clip 4 — Context Management & Compaction

| Attribute | Value |
|---|---|
| **Section** | 4 — Context Management & Compaction |
| **data-start** | `116` |
| **data-duration** | `38` |
| **data-track-index** | `1` |

### Content Layout

| Element | Local Offset | Absolute Time | Details |
|---|---|---|---|
| Badge | +0.7s | 116.7s | `SECTION 04` — Cyan pill |
| Title | +0.7s | 116.7s | "Context Management & Compaction" — Inter Bold 56px (longer title) |
| Subtitle | +2.5s | 118.5s | "Keeping the agent's memory manageable" — Inter 28px |
| Left Card (Diagram) | +5.5s | 121.5s | **"Compaction Flow"** — horizontal flowchart, Cyan border |
| Diagram Nodes | +5.5s → +25.5s | 121.5/126.5/131.5/136.5/141.5s | 5s stagger: Count Tokens → Threshold? → (Yes) Trigger Compaction → Fan-out (Prefix/Recent/Summarize Middle) → Reassemble |
| Right Card | +14.5s | 130.5s | **"What Gets Preserved"** — glassmorphism card, Emerald border |
| Right Bullets | +16.0s → +22.0s | 132.0/133.5/135.0/136.5s | • Prefix (system prompt + goal): kept verbatim · • Recent turns: kept as working memory · • Middle history: compressed into summary · • Reassembled into a smaller message list |
| Callout | +26.0s | 142.0s | "Compaction = save the ends, summarize the middle." — Amber accent, last 12s |

### Visual Elements (from Qwen analysis — sec-4 Agent Harness Context Compaction)

- Orange hexagon threshold decision node contrasting with blue process nodes
- Light-blue rounded rectangles with small line icons and two-line captions
- "Yes" and "No" labeled edges from hexagon — "No" bypasses to Return Messages (fast path)
- Parallel fan-out then fan-in pattern: Trigger Compaction → (Extract Prefix + Extract Recent + Summarize Middle) → Reassemble
- Left-to-right horizontal flow with vertical branch for the three extraction steps
- Hexagon pulses Amber on appear; fan-out arrows draw with stagger; fan-in converges with glow

---

## Clip 5 — Tools, Skills & Permission Gating

| Attribute | Value |
|---|---|
| **Section** | 5 — Tools, Skills & Permission Gating |
| **data-start** | `154` |
| **data-duration** | `38` |
| **data-track-index** | `1` |

### Content Layout

| Element | Local Offset | Absolute Time | Details |
|---|---|---|---|
| Badge | +0.7s | 154.7s | `SECTION 05` — Cyan pill |
| Title | +0.7s | 154.7s | "Tools, Skills & Permission Gating" — Inter Bold 56px |
| Subtitle | +2.5s | 156.5s | "How the harness controls what tools may run" — Inter 28px |
| Left Card | +5.5s | 159.5s | **"Tool Registry"** — glassmorphism card, Cyan border |
| Left Bullets | +7.0s → +11.5s | 161.0/162.5/164.0/165.5s | • Tools registered by name + metadata · • LLM addresses tools by name only · • Registry decouples definition from execution · • Examples: view_file, write_file, run_bash |
| Right Card | +14.5s | 168.5s | **"Permission Tiers"** — glassmorphism card, Ruby `#f85149` border |
| Right Bullets | +16.0s → +22.0s | 170.0/171.5/173.0/174.5s | • Read-only: view files, search · • Workspace: write within project dir · • Full: any command, any path · • Intercept before execute — never run blindly |
| Callout | +26.0s | 180.0s | "The harness intercepts every tool call before it runs." — Ruby accent, last 12s |

### Visual Elements (from Qwen analysis — sec-5 LLM Tool Execution Flow)

- Central Amber hexagon representing the permission gate / decision point
- Light-blue rounded rectangles for linear process steps: LLM Output → Lookup Tool → Check Permissions → Built-in Shell / Permission Denied
- Small icons inside each box: robot, database, shield, terminal, warning
- Branching arrows labeled "Allowed" (Emerald) and "Denied" (Ruby)
- Hexagon gate pulses on appear; "Denied" path flashes Ruby; "Allowed" path glows Emerald
- Linear pipeline animates left-to-right with 5s node stagger

---

## Clip 6 — Sub-Agent Delegation

| Attribute | Value |
|---|---|
| **Section** | 6 — Sub-Agent Delegation |
| **data-start** | `192` |
| **data-duration** | `38` |
| **data-track-index** | `1` |

### Content Layout

| Element | Local Offset | Absolute Time | Details |
|---|---|---|---|
| Badge | +0.7s | 192.7s | `SECTION 06` — Cyan pill |
| Title | +0.7s | 192.7s | "Sub-Agent Delegation" — Inter Bold 64px |
| Subtitle | +2.5s | 194.5s | "Spawning specialist agents for exploration and verification" — Inter 26px |
| Left Card | +5.5s | 197.5s | **"Explorer Sub-Agent"** — glassmorphism card, Cyan border |
| Left Bullets | +7.0s → +11.5s | 199.0/200.5/202.0/203.5s | • Spawned with isolated session · • Restricted tools (search, read) · • Runs search turns · • Returns findings summary, not raw logs |
| Right Card | +14.5s | 206.5s | **"Verifier Sub-Agent"** — glassmorphism card, Emerald border |
| Right Bullets | +16.0s → +22.0s | 208.0/209.5/211.0/212.5s | • Separate isolated session · • Restricted to pytest only · • Runs the test suite · • Returns pass/fail result to parent |
| Callout | +26.0s | 218.0s | "Sub-agents return summaries, not raw logs — protecting the parent's context." — Purple accent, last 12s |

### Visual Elements (from Qwen analysis — sec-6 Sub-Agent Workflow)

- Central horizontal timeline arrow with small circular node markers at each step
- Two staggered rows of rounded rectangular cards: top row (parent-side actions), bottom row (sub-agent-side actions)
- Color-coded cards: blue, green, yellow, red on top; cyan, green, orange, pink on bottom
- Simple line icons inside each card: agent nodes, search, folder, speech bubble, person, checkmark
- Top row: Spawn Explorer → Create Explorer Session → Run Search Turns → Return Findings Summary
- Bottom row: Spawn Verifier → Create Verifier Session → Run Test Suite → Return Verification Result
- Timeline arrow draws left-to-right; cards pop in at 5s stagger per row; parent-child connection lines glow

---

## Clip 7 — Session Persistence & Prompt Assembly

| Attribute | Value |
|---|---|
| **Section** | 7 — Session Persistence & Prompt Assembly |
| **data-start** | `230` |
| **data-duration** | `38` |
| **data-track-index** | `1` |

### Content Layout

| Element | Local Offset | Absolute Time | Details |
|---|---|---|---|
| Badge | +0.7s | 230.7s | `SECTION 07` — Cyan pill |
| Title | +0.7s | 230.7s | "Session Persistence & Prompt Assembly" — Inter Bold 52px (long title) |
| Subtitle | +2.5s | 232.5s | "How agents remember and rebuild context" — Inter 28px |
| Left Card | +5.5s | 235.5s | **"Event Log (JSONL)"** — glassmorphism card, Cyan border |
| Left Bullets | +7.0s → +11.5s | 237.0/238.5/240.0/241.5s | • Every turn recorded as a discrete event · • USER_INPUT → MODEL_CALL → TOOL_RESULT · • Append-only JSONL stream · • Compaction events flushed to disk |
| Right Card | +14.5s | 244.5s | **"Three-Layer Prompt Rebuild"** — glassmorphism card, Purple border |
| Right Bullets | +16.0s → +22.0s | 246.0/247.5/249.0/250.5s | • Layer 1: Static base harness instructions · • Layer 2: Injected AGENTS.md config · • Layer 3: Replayed compacted history · • Assembled fresh every turn |
| Callout | +26.0s | 256.0s | "Log everything. Rebuild the prompt from three layers each turn." — Cyan accent, last 12s |

### Visual Elements (from Qwen analysis — sec-7 Session Persistence & Prompt Pipeline)

- Two parallel horizontal lanes of light-blue rounded rectangles connected by right-pointing arrows
- **Top lane (Event Log):** USER_INPUT → MODEL_CALL → TOOL_RESULT → COMPACTION_EVENT → session_transcript.json
- Green database cylinder capping the right end of the top lane (disk storage)
- **Bottom lane (Prompt Assembly):** Base Harness Instructions → Injected AGENTS.md → Replayed History
- Small monochrome icons embedded in each box: terminal, gears, clock, layers
- Cyan step labels with grey description text inside each box
- Top lane animates left-to-right first (5s stagger), bottom lane follows 2s offset; database cylinder glows Emerald on appear

---

## Clip 8 — Hooks, Permissions & Safety

| Attribute | Value |
|---|---|
| **Section** | 8 — Hooks, Permissions & Safety |
| **data-start** | `268` |
| **data-duration** | `38` |
| **data-track-index** | `1` |

### Content Layout

| Element | Local Offset | Absolute Time | Details |
|---|---|---|---|
| Badge | +0.7s | 268.7s | `SECTION 08` — Cyan pill |
| Title | +0.7s | 268.7s | "Hooks, Permissions & Safety" — Inter Bold 60px |
| Subtitle | +2.5s | 270.5s | "The multi-stage safety pipeline" — Inter 28px |
| Left Card | +5.5s | 273.5s | **"Pre-Tool Hooks"** — glassmorphism card, Amber border |
| Left Bullets | +7.0s → +11.5s | 275.0/276.5/278.0/279.5s | • Intercept before execution · • Allow → run the tool · • Deny → block with error · • Modify → rewrite the command |
| Right Card | +14.5s | 282.5s | **"Post-Tool & Interactive Approval"** — glassmorphism card, Ruby border |
| Right Bullets | +16.0s → +22.0s | 284.0/285.5/287.0/288.5s | • Post-tool hooks: audit every result · • Destructive commands escalate to user · • Interactive approval prompt: approve or deny · • Audit log injected back into context |
| Callout | +26.0s | 294.0s | "Never execute directly — traverse the safety pipeline first." — Ruby accent, last 12s |

### Visual Elements (from Qwen analysis — sec-8 Tool Execution Workflow)

- Five color-coded rounded cards laid out horizontally: blue, green, red, pink, blue
  - Tool Call Proposed → Dynamic Command Parser → Active Permission Tier → Interactive User Approval → Execution and Audit
- Distinct line-art icons centered above each card: terminal, code+search, shield, person+speech bubble, checkmark
- Circular bullet markers with internal down-arrows listing each stage's sub-steps
- Looping connector lines with arrowheads arcing from bottom of one card to top of next
- Cards animate at 5s stagger left-to-right; connector arcs draw with glow; "Interactive Approval" card pulses Ruby

---

## Clip 9 — Research Insights

| Attribute | Value |
|---|---|
| **Section** | 9 — Research Insights |
| **data-start** | `306` |
| **data-duration** | `38` |
| **data-track-index** | `1` |

### Content Layout

| Element | Local Offset | Absolute Time | Details |
|---|---|---|---|
| Badge | +0.7s | 306.7s | `SECTION 09` — Cyan pill |
| Title | +0.7s | 306.7s | "Research Insights" — Inter Bold 64px |
| Subtitle | +2.5s | 308.5s | "What Tsinghua's NLAH study tells us about harness design" — Inter 26px |
| Left Card | +5.5s | 311.5s | **"Module Ablation Results"** — glassmorphism card, Cyan border, data table style |
| Left Bullets | +7.0s → +11.5s | 313.0/314.5/316.0/317.5s | • Self-Evolution Attempt Loop: +4.8 SWE-bench ✓ · • Evaluation Verifiers: −0.8 SWE-bench ✗ · • Multi-Candidate Search: −2.4 SWE-bench ✗ · • Only Self-Evolution consistently helps |
| Right Card | +14.5s | 320.5s | **"Harness Design Principle"** — glassmorphism card, Purple `#a371f7` border |
| Right Bullets | +16.0s → +22.0s | 322.0/323.5/325.0/326.5s | • Narrowing attempt loop > broadening search · • Verifiers and search hurt performance · • Fold Self-Evolution into core rule · • Drop what doesn't help |
| Callout | +26.0s | 332.0s | "Narrowing the attempt loop beats broadening the search space." — Purple accent, last 12s |

### Visual Elements (from Qwen analysis — sec-9 Tsinghua NLAH Ablation)

- Three color-coded rounded cards: light blue (Ablation Results), lavender (Design Principle), light blue (Integration Mapping)
- Line-art header icons: bar/signal chart, stacked hexagons, connected node graph
- Hollow-circle bullet markers next to each ablation row
- Green check ✓ flags marking "CONSISTENTLY HELPS"; red cross ✗ flags marking "HURTS PERFORMANCE"
- Curved connector lines with arrowheads linking left card to the two right cards
- Left card animates first (rows stagger 1.5s); connectors draw at +12s; right cards appear at +14.5s; ✓/✗ flags pop with scale animation

---

## Clip 10 — Minimal Python Harness Synthesis

| Attribute | Value |
|---|---|
| **Section** | 10 — Minimal Python Harness Synthesis |
| **data-start** | `344` |
| **data-duration** | `38` |
| **data-track-index** | `1` |

### Content Layout

| Element | Local Offset | Absolute Time | Details |
|---|---|---|---|
| Badge | +0.7s | 344.7s | `SECTION 10` — Cyan pill |
| Title | +0.7s | 344.7s | "Minimal Python Harness" — Inter Bold 64px |
| Subtitle | +2.5s | 346.5s | "Nine components, zero dependencies, one file" — Inter 28px |
| Left Card (Diagram) | +5.5s | 349.5s | **"The 9-Component Architecture"** — tree/flow diagram card, Cyan-to-Purple gradient border |
| Diagram Nodes | +5.5s → +30.5s | 349.5/354.5/359.5/364.5/369.5s | 5s stagger (9 nodes, every other gets emphasis): System Prompt Assembly → Execution Loop → Context Management → Pre-Tool Hooks → Permissions & Safety → Tool Registry → Built-in Primitives → Sub-Agent Management → Session Persistence |
| Right Card | +16.5s | 360.5s | **"The Complete Checklist"** — glassmorphism card, Emerald border |
| Right Bullets | +18.0s → +24.0s | 362.0/363.5/365.0/366.5s | • Zero external dependencies · • Pure Python standard library · • One file: minimal_harness.py · • A complete, working agent harness |
| Callout | +26.0s | 370.0s | "Nine components. Zero dependencies. One file. That's a harness." — Emerald accent, last 12s |

### Visual Elements (from Qwen analysis — sec-10 Minimal Python Agent)

- Outer container rectangle with blue-to-magenta gradient border enclosing all nine nodes
- Nine white rounded boxes, each outlined with the same gradient, soft drop shadow
- Bold directional arrows showing top-down tree/flow structure
- Two visible branching points: 3-way at the Execution Loop, 2-way at Tool Registry Dispatch
  - Loop → Context Management, Pre-Tool Hooks, Session Persistence
  - Tool Registry → Built-in Primitives + Sub-Agent Management
- Numbered labels 1–9 inside each box (JetBrains Mono)
- Nodes animate top-down at 5s stagger; branching arrows draw with glowing SVG connectors; gradient border pulses on clip entry

---

## Global Composition Attributes

```html
<div id="root"
     data-composition-id="agent-harness-engineering"
     data-width="1920"
     data-height="1080"
     data-start="0"
     data-duration="382">
  <!-- 10 clips, data-start/duration per table above -->
</div>
```

### Timeline Registration (anim.js)

```js
window.__timelines = window.__timelines || {};
window.__timelines["agent-harness-engineering"] = gsap.timeline({ paused: true });
```

### Color Assignment by Clip

| Clip | Primary Accent | Secondary Accent |
|---|---|---|
| 1 | Cyan `#38bdf8` | Purple `#a371f7` |
| 2 | Amber `#d29922` (Framework) | Emerald `#3fb950` (Harness) |
| 3 | Cyan `#38bdf8` | Amber `#d29922` (decision nodes) |
| 4 | Cyan `#38bdf8` | Emerald `#3fb950` (preserved) |
| 5 | Cyan `#38bdf8` | Ruby `#f85149` (permissions) |
| 6 | Cyan `#38bdf8` (Explorer) | Emerald `#3fb950` (Verifier) |
| 7 | Cyan `#38bdf8` (log) | Purple `#a371f7` (prompt) |
| 8 | Amber `#d29922` (pre-hook) | Ruby `#f85149` (post-hook) |
| 9 | Cyan `#38bdf8` (data) | Purple `#a371f7` (principle) |
| 10 | Cyan→Purple gradient | Emerald `#3fb950` (checklist) |