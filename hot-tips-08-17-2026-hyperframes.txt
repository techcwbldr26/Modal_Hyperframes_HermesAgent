# AI Agent Guide for HyperFrames Video Generation

This guide provides instructions, architectural rules, workflow patterns, and battle-tested gotcha solutions for AI coding agents (LLMs) generating agent-native motion graphics videos using **HyperFrames** (`heygen-com/hyperframes`), HTML, CSS, and GSAP.

---

## 🎯 Executive Overview

HyperFrames is a framework for **Video as Code**. It allows an AI agent to build deterministic, programmatic MP4 video compositions using web technologies (HTML, CSS, JavaScript, GSAP). 

When given a request to generate a video based on a **YouTube URL**, **documents (.pdf, .docx, .md)**, or **topic notes**, follow the systematic agent workflow detailed below.

---

## 🛠️ Step-by-Step AI Agent Workflow

### Phase 1: Knowledge Extraction & Script Generation
1. **Source Content Analysis**:
   - Extract raw text from documents (`.pdf`, `.docx`, `.md`) using standard tools (e.g. `textutil`, `pypdf`, `python-docx`, `pandoc`).
   - Summarize YouTube videos by extracting title, transcript, description, or key technical takeaways.
2. **Pedagogical Structuring**:
   - Divide content into **distinct, well-timed scene clips** (e.g., Intro/Title, Paradigm 1, Paradigm 2, ..., Applied Hybrid System Architecture, Outro).
   - Ensure the pacing is **natural and instructional** (slower pacing, clear titles, readable bullet points, syntax-highlighted code snippets).
   - Do NOT clutter a single screen with too much text—split content across sequential, readable clips.

### Phase 2: Visual Style & Design System Engineering
1. **Reference Video Aesthetics (e.g., DeepSeek Harness Explainer)**:
   - **Backdrop**: Dark tech theme (`#090d16` slate gradient) with subtle ambient glow circles and subtle grid line overlays.
   - **Typography**: Dual font hierarchy (`Inter` for headers/body, `JetBrains Mono` for badges, code, and metrics).
   - **Containers**: Translucent glassmorphism cards (`background: rgba(22, 27, 38, 0.85); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.1);`).
   - **Color System**: High-contrast electric accents (Cyan `#38bdf8`, Emerald `#3fb950`, Amber `#d29922`, Ruby `#f85149`, Purple `#a371f7`).
   - **Motion Graphics**: Modular "brick-snapping" diagram nodes, glowing SVG connectors, kinetic text reveals, syntax-highlighted code blocks, and timeline progress bars.

### Phase 3: Composition Structure ("Rule of Three")
HyperFrames requires strict adherence to 3 core structural rules:

```html
<!-- 1. ROOT ELEMENT: Defines global composition metadata -->
<div id="root" 
     data-composition-id="when-to-use-ai" 
     data-width="1920" 
     data-height="1080" 
     data-start="0" 
     data-duration="225">

  <!-- 2. TIMED CLIP ELEMENTS: Timed scenes with class="clip" -->
  <div id="clip-1" class="clip" data-start="0" data-duration="25" data-track-index="1">
    <!-- Scene Content -->
  </div>

  <div id="clip-2" class="clip" data-start="25" data-duration="40" data-track-index="1">
    <!-- Scene Content -->
  </div>
</div>
```

```js
// 3. GSAP TIMELINE REGISTRATION: Must be initialized with { paused: true }
window.__timelines = window.__timelines || {};

const tl = gsap.timeline({ paused: true });

// Build sequenced scene animations...

// Register globally under the exact same composition ID as data-composition-id
window.__timelines["when-to-use-ai"] = tl;
```

---

## ⚠️ Critical Gotchas, Pitfalls & Solutions

| Issue / Gotcha | Root Cause | Solution for AI Agent |
|---|---|---|
| **Render Error: `Not a directory: index.html`** | Passing `index.html` directly to `npx hyperframes render index.html` | **ALWAYS** pass the project directory path (`.`), e.g.: `npx hyperframes render . -o output.mp4` |
| **`FFmpeg / FFprobe not found`** | System PATH lacks `ffmpeg` or `ffprobe` binaries | Download static pre-compiled binaries to project root (`evermeet.cx` on macOS or `@ffmpeg-installer/ffmpeg`) and prepend to PATH: `export PATH="$(pwd):$PATH"` |
| **Blank / Dark Screen on `localhost:8080`** | GSAP timeline is `{ paused: true }` for HyperFrames frame-seeking engine | Add standalone browser auto-play fallback to `anim.js`: `if (!window.location.search.includes('hyperframes') && !window.__HYPERFRAMES__) { tl.play(); }` |
| **Export Error (503) in HyperFrames Studio** | Studio export button invoked with file target instead of folder | Use the CLI render command directly: `npx hyperframes render . -o output.mp4` |
| **Audio Lint Warning / Failures** | Untimed `<audio>` element or missing audio file path | Ensure audio files exist in `assets/`, or add `data-start="0"` attributes. Remove unused `<audio>` tags before rendering. |

---

---

## 🐌 Pacing & Human Comprehension Standards

This is the most commonly violated rule by AI-generated videos. **LLMs animate far too fast for humans to read.**

### Minimum Timing Standards (Non-Negotiable)

| Element | Minimum Delay / Stagger | Why |
|---|---|---|
| **Badge / Title** | 0.7s after clip fade-in | Viewer needs to orient to new scene |
| **Subtitle** | 1.8s after title | Title must register before subtitle |
| **First card (left)** | 3.0s after subtitle | Let subtitle be read first |
| **Second card (right)** | `left_card_start + 9–10s` | Viewer needs to finish reading left card |
| **Bullet points (stagger)** | `1.5s` minimum per bullet | Each bullet = one spoken sentence |
| **Callout / summary box** | `startTime + 28s` (last 10–12s of clip) | Should feel like a conclusion, not an interruption |
| **Diagram nodes (stagger)** | `5s` between nodes | Viewer must read node description before next appears |
| **Code lines (stagger)** | `0.8s` per line | Mimics live typing, keeps attention |

### The Two-Card Rule
When a scene has a LEFT card and a RIGHT card:
```
Left card appears  →  [8–10 seconds pass]  →  Right card appears
```
Never stack both cards in the same stagger call. Use separate `tl.from()` calls with explicit time offsets:
```js
// CORRECT — deliberate 10s gap for reading
tl.from("#clip-2 .card:nth-child(1)", { opacity: 0, x: -60, duration: 1.4 }, t + 3.0);
tl.from("#clip-2 .card:nth-child(2)", { opacity: 0, x:  60, duration: 1.4 }, t + 13.0);

// WRONG — both cards animate simultaneously
tl.from("#clip-2 .card", { opacity: 0, duration: 1.4, stagger: 0.5 });
```

### Clip Duration Budget
For a 40-second clip covering two cards:
```
0:00 – 0:02  Badge / Title
0:02 – 0:05  Subtitle
0:05 – 0:14  Left card + bullets appear (stagger 1.5s × 4 bullets)
0:14 – 0:23  Right card + bullets appear (stagger 1.5s × 3 bullets)
0:23 – 0:28  Both cards on screen — reading silence
0:28 – 0:40  Callout / summary emphasis
```

### Audio Sync Workflow (Post-Recording)
1. Record voiceover using `VOICEOVER_SCRIPT.txt` as script.
2. Note actual timestamps where each topic begins in your recording.
3. Update `data-start` and `data-duration` on each `<div class="clip">` in `index.html`.
4. Update the matching `setupClip("#clip-N", startTime, duration, ...)` calls in `anim.js`.
5. Update `data-duration` on `#root` to match total recording duration.
6. Add `<audio id="bg-audio" src="assets/voiceover.mp3" data-start="0" data-duration="225" preload="auto">` inside `#root`.
7. Re-render: `export PATH="$(pwd):$PATH" && npx hyperframes render . -o output_v2.mp4`

---

## 📋 Agent Quality Check Protocol

Before declaring a video composition ready for rendering:
1. Verify `data-composition-id` in `index.html` **EXACTLY matches** `window.__timelines["<id>"]` in `anim.js`.
2. Confirm GSAP timeline is initialized with `{ paused: true }`.
3. Check that total `data-duration` on `#root` matches the sum of clip timelines.
4. Ensure `styles/main.css` has `width: 1920px; height: 1080px; overflow: hidden;` on body and `#root`.
5. Run verification test: `python3 -c "import os; ..."` to validate HTML/CSS/JS syntax.
