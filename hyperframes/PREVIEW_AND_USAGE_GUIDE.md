# HyperFrames — Preview UI & Local Usage Guide

Complete instructions for running the HyperFrames **preview studio** locally and for using/running the **`index.html` composition** directly. Applies to this project (`hyperframes/`, CLI pinned at `hyperframes@0.7.109`).

---

## 0. Prerequisites (one-time)

| Requirement | Check |
|---|---|
| Node.js 22+ | `node -v` → v24.16.0 on this machine |
| FFmpeg on PATH | `ffmpeg -version` → 8.1.1 on this machine |
| Network | GSAP is loaded from `cdn.jsdelivr.net` (see §3.3) |
| CLI | `npx --yes hyperframes@0.7.109 doctor` → ok |

No global install needed — `npx` fetches the pinned CLI on demand.

---

## 1. Run the Preview Studio (interactive UI)

The studio is a local web app with a **scrubber timeline**, per-clip navigation, element inspection, and an **Export** button. It pre-renders every frame of the composition into a cache so scrubbing is smooth.

### 1.1 Start it

```bash
cd /Users/gregorykennedy-salemi/Desktop/modal-hyperframes-hermes/hyperframes
npm run dev
# equivalent: npx --yes hyperframes@0.7.109 preview
```

- Opens your browser automatically at **http://localhost:3002** (default port).
- **The command blocks** — it is a long-running server. Keep its terminal window open; close it (Ctrl-C) to stop the studio.
- First load is slow: the studio captures all 11,460 frames (6:22 × 30 fps) in software mode (~2 s/frame on this iMac) into `renders/work-*/captured-frames/`. Scrubbing is choppy until the cache fills; the page is usable immediately.

### 1.2 Useful flags

```bash
# Different port
npx --yes hyperframes@0.7.109 preview --port=4000

# Don't auto-open the browser (e.g. when an agent starts it)
npx --yes hyperframes@0.7.109 preview --no-open

# Start as a detached background server (keeps running after the command exits)
npx --yes hyperframes@0.7.109 preview --background

# Manage background previews
npx --yes hyperframes@0.7.109 preview --status   # is it running?
npx --yes hyperframes@0.7.109 preview --list     # all active servers
npx --yes hyperframes@0.7.109 preview --stop      # stop this project's server
npx --yes hyperframes@0.7.109 preview --kill-all  # stop everything

# Force a fresh server if one is already running for this project
npx --yes hyperframes@0.7.109 preview --force-new
```

### 1.3 What you can do in the studio

- **Scrub** the timeline (0–382 s) to preview any moment of the 10-clip composition.
- **Jump between clips** — each clip is a timed `<section class="clip">` (see §3.2 for the timing table).
- **Inspect elements** — select an element to see its `data-*` attributes and timeline position.
- **Export** — the studio's Export button renders the composition to a video file. It reuses the same capture pipeline as `hyperframes render`; a 6:22 export on this iMac takes roughly 1.5–2 hours (software rendering). Watch `~/Downloads/` and `hyperframes/renders/` for the finished file.

### 1.4 Troubleshooting the studio

| Symptom | Fix |
|---|---|
| Port 3002 already in use | `--force-new`, or pick another port with `--port=4000` |
| Scrubbing is choppy | Normal while the frame cache builds; wait for `renders/work-*/captured-frames/` to fill |
| Studio won't start | `npx --yes hyperframes@0.7.109 doctor` — missing Node/FFmpeg |
| Black/blank preview | The composition needs the HyperFrames runtime; always open via the studio URL, not `file://` |
| Export seems stuck | Software rendering is slow (~2 s/frame); a 6:22 export legitimately takes 1.5–2 h. Check CPU usage in Activity Monitor |

---

## 2. Render to MP4 (the real video file)

The studio's Export and the CLI render are the **only** ways to produce an actual video file. The `.html` alone is not a video.

```bash
cd /Users/gregorykennedy-salemi/Desktop/modal-hyperframes-hermes/hyperframes

# Draft (fastest, for review)
npx --yes hyperframes@0.7.109 render --quality draft --output ../out_harness_draft.mp4

# Standard (default)
npx --yes hyperframes@0.7.109 render --output ../out_harness.mp4

# High quality
npx --yes hyperframes@0.7.109 render --quality high --output ../out_harness.mp4

# Verify the result
ffprobe -v error -show_format ../out_harness.mp4   # duration should be ~382 s (6:22)
```

Key flags: `--quality draft|standard|high`, `--output <path>`, `--fps <n>`, `--format mp4|webm|mov|gif|png-sequence`, `--workers <n>` (parallel Chrome processes), `--resolution 1080p|4k`.

**Time estimates on this iMac (software rendering, ~2 s/frame):**

| Quality | Approx. time for 6:22 @ 30 fps |
|---|---|
| draft | ~1.5–2 h |
| standard | ~2–3 h |
| high | ~3–6 h |

**Faster alternatives:**
- **HeyGen cloud render** (official offload, no local Chrome/FFmpeg): `npx --yes hyperframes@0.7.109 cloud render --quality standard --output ../out_harness.mp4` (billed by HeyGen; `--no-wait` for fire-and-forget, `cloud list`/`cloud get` to track).
- A machine with a GPU or more cores (the render is CPU-bound; the H200 Modal GPU does not help — see the chat notes).
- `--docker` for deterministic renders in a container.

---

## 3. Using the `index.html` file directly

### 3.1 What it is

`hyperframes/index.html` is the **source composition** — the editable "project file" (like a Premiere `.prproj`), not a video. It contains:

- The **root element** declaring the canvas and total duration:
  ```html
  <div id="root" data-composition-id="agent-harness-engineering"
       data-width="1920" data-height="1080" data-start="0" data-duration="382">
  ```
- **10 clip sections** (`<section class="clip" data-start="..." data-duration="..." data-track-index="1">`) — one per course section, timed sequentially.
- **`anim.js`** — the GSAP timeline that animates every element (badges, cards, bullets, diagram nodes, callouts) at the hot-tips pacing.
- The **timeline registration** at the bottom:
  ```js
  window.__timelines["agent-harness-engineering"] = gsap.timeline({ paused: true });
  ```

### 3.2 Clip timing table (from `STORYBOARD.md`)

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

### 3.3 Three ways to run it

**Option A — double-click the file (simplest).**
Open `hyperframes/index.html` in any browser. `anim.js` contains a blank-screen fallback that auto-plays the timeline when the page is NOT inside the HyperFrames runtime:

```js
if (!window.location.search.includes("hyperframes") && !window.__HYPERFRAMES__) {
  tl.play();
}
```

So the full 6:22 animation plays immediately. Two caveats:
- **Needs internet** — GSAP loads from `https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js`. Without network the page is blank.
- The canvas is 1920×1080; in a browser window it scales down (letterboxed). That's expected — it's a video canvas, not a responsive page.

**Option B — serve it locally (recommended for repeated use).**
```bash
cd /Users/gregorykennedy-salemi/Desktop/modal-hyperframes-hermes/hyperframes
python3 -m http.server 8080
# then open http://localhost:8080/index.html
```
Same auto-play behavior, but served over HTTP like a real page.

**Option C — the preview studio (interactive).**
See §1 — this is the proper way to scrub, inspect, and export.

### 3.4 Editing workflow (if you change anything)

1. Edit `index.html` (structure/copy) or `anim.js` (animation/timing).
2. Run the gate: `npx --yes hyperframes@0.7.109 check` — must pass 0 errors / 0 warnings / 61/61 WCAG AA.
3. Preview: `npm run dev` → review in the studio.
4. Render: `npx --yes hyperframes@0.7.109 render --quality draft --output ../out_harness_draft.mp4`.

**Rules that must never be broken** (from `HYPERFRAMES_HOT_TIPS.md`):
- Every timed element needs `class="clip"` + `data-start` + `data-duration` + `data-track-index`.
- Clips must be direct children of `#root`; same-track clips must not overlap.
- The timeline must stay `{ paused: true }` and registered under the exact composition id.
- Root `data-duration` must equal the sum of clip durations (382 s).
- No `Math.random()`, no `Date.now()`, no network fetches inside the composition.
- `harness-engineering/` is read-only input — never modify it.

---

## 4. Quick reference

```bash
npm run dev        # preview studio (long-running server)
npm run check      # lint + runtime + layout + motion + contrast gate
npm run render     # render to MP4
npx --yes hyperframes@0.7.109 preview --status | --stop | --list | --kill-all
npx --yes hyperframes@0.7.109 cloud render --quality standard -o ../out_harness.mp4
npx --yes hyperframes@0.7.109 docs <topic>   # data-attributes, gsap, rendering, troubleshooting
```
