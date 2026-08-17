/* ═══════════════════════════════════════════════════════════════
   Agent Harness Engineering — GSAP Timeline
   10 clips · 382s total · single paused timeline
   Pacing: badge 0.7s, subtitle 1.8s, Two-Card Rule (9s gap),
           bullets 1.5s stagger, callout last 12s
   ═══════════════════════════════════════════════════════════════ */

window.__timelines = window.__timelines || {};

const tl = gsap.timeline({
  paused: true,
  defaults: { ease: "power3.out", overwrite: "auto" },
});

const COMP_ID = "agent-harness-engineering";

/* ── Pacing constants (from HOT_TIPS) ── */
const BADGE_DELAY = 0.7;        // badge after clip start
const SUBTITLE_DELAY = 1.8;    // subtitle after badge/title
const LEFT_CARD_DELAY = 3.0;   // left card after subtitle
const CARD_GAP = 9.0;          // Two-Card Rule: 9s between cards
const BULLET_STAGGER = 1.5;    // per-bullet stagger
const BULLET_DURATION = 0.6;   // each bullet tween
const CARD_DURATION = 1.0;     // card entrance
const CALLOUT_OFFSET = 26.0;   // callout: last ~12s of clip
const PROGRESS_DURATION = 38.0; // progress bar fill duration

/* ─────────────────────────────────────
   Helper: animate a standard clip scene
   ─────────────────────────────────────
   clipSelector: "#clip-N"
   clipStart:    absolute start time (s)
   clipDuration: clip duration (s)
   opts:
     leftBullets:  number of bullets in left card
     rightBullets: number of bullets in right card
     hasFlow:      boolean — left card has flow nodes
     flowNodes:    number of flow nodes
     calloutOffset: override for callout start (default 26)
   ───────────────────────────────────── */
function setupClip(clipSelector, clipStart, clipDuration, opts) {
  opts = opts || {};
  const t = clipStart;
  const leftBullets = opts.leftBullets || 4;
  const rightBullets = opts.rightBullets || 4;
  const hasFlow = !!opts.hasFlow;
  const flowNodes = opts.flowNodes || 0;
  const calloutOffset = opts.calloutOffset || CALLOUT_OFFSET;

  /* Badge + Title — badge at +0.7s */
  tl.from(clipSelector + " [data-el='badge']",
    { opacity: 0, y: -24, duration: 0.5 }, t + BADGE_DELAY);
  tl.from(clipSelector + " .title",
    { opacity: 0, y: 40, duration: 0.8 }, t + BADGE_DELAY + 0.15);

  /* Subtitle — +1.8s after badge (≈ +2.5s local) */
  tl.from(clipSelector + " .subtitle",
    { opacity: 0, y: 24, duration: 0.7 }, t + BADGE_DELAY + SUBTITLE_DELAY);

  /* Left card — +3.0s after subtitle (≈ +5.5s local) */
  const leftCardStart = t + BADGE_DELAY + SUBTITLE_DELAY + LEFT_CARD_DELAY;
  tl.from(clipSelector + " [data-el='left-card']",
    { opacity: 0, x: -60, duration: CARD_DURATION }, leftCardStart);

  if (hasFlow && flowNodes > 0) {
    /* Flow nodes: 5s stagger (storyboard) but capped for readability */
    const nodeStagger = flowNodes > 5 ? 3.5 : 5.0;
    tl.from(clipSelector + " [data-el='node']",
      { opacity: 0, scale: 0.85, duration: 0.6, stagger: nodeStagger },
      leftCardStart + 0.3);
  } else {
    /* Bullets: 1.5s stagger */
    tl.from(clipSelector + " [data-el='left-card'] [data-el='bullet']",
      { opacity: 0, x: -30, duration: BULLET_DURATION, stagger: BULLET_STAGGER },
      leftCardStart + 0.4);
  }

  /* Right card — Two-Card Rule: 9s after left card */
  const rightCardStart = leftCardStart + CARD_GAP;
  tl.from(clipSelector + " [data-el='right-card']",
    { opacity: 0, x: 60, duration: CARD_DURATION }, rightCardStart);

  /* Right bullets: 1.5s stagger */
  tl.from(clipSelector + " [data-el='right-card'] [data-el='bullet']",
    { opacity: 0, x: 30, duration: BULLET_DURATION, stagger: BULLET_STAGGER },
    rightCardStart + 0.4);

  /* Callout — last 10-12s of clip */
  tl.from(clipSelector + " [data-el='callout']",
    { opacity: 0, y: 30, duration: 0.8 }, t + calloutOffset);

  /* Progress bar — fills across clip duration */
  tl.fromTo(clipSelector + " [data-el='progress']",
    { scaleX: 0 },
    { scaleX: 1, duration: clipDuration, ease: "none" },
    t);
}

/* ─────────────────────────────────────
   CLIP 1 — Introduction (0–38s, 38s)
   ───────────────────────────────────── */
setupClip("#clip-1", 0, 38, {
  leftBullets: 4,
  rightBullets: 5,
});

/* ─────────────────────────────────────
   CLIP 2 — Framework vs Harness (38–76s, 38s)
   ───────────────────────────────────── */
setupClip("#clip-2", 38, 38, {
  leftBullets: 4,
  rightBullets: 4,
});

/* ─────────────────────────────────────
   CLIP 3 — The Execution Loop (76–116s, 40s)
   ───────────────────────────────────── */
setupClip("#clip-3", 76, 40, {
  leftBullets: 4,
  rightBullets: 4,
  hasFlow: true,
  flowNodes: 5,
  calloutOffset: 28,
});

/* ─────────────────────────────────────
   CLIP 4 — Context Management & Compaction (116–154s, 38s)
   ───────────────────────────────────── */
setupClip("#clip-4", 116, 38, {
  leftBullets: 4,
  rightBullets: 4,
  hasFlow: true,
  flowNodes: 5,
});

/* ─────────────────────────────────────
   CLIP 5 — Tools, Skills & Permission Gating (154–192s, 38s)
   ───────────────────────────────────── */
setupClip("#clip-5", 154, 38, {
  leftBullets: 4,
  rightBullets: 4,
});

/* ─────────────────────────────────────
   CLIP 6 — Sub-Agent Delegation (192–230s, 38s)
   ───────────────────────────────────── */
setupClip("#clip-6", 192, 38, {
  leftBullets: 4,
  rightBullets: 4,
});

/* ─────────────────────────────────────
   CLIP 7 — Session Persistence & Prompt Assembly (230–268s, 38s)
   ───────────────────────────────────── */
setupClip("#clip-7", 230, 38, {
  leftBullets: 4,
  rightBullets: 4,
});

/* ─────────────────────────────────────
   CLIP 8 — Hooks, Permissions & Safety (268–306s, 38s)
   ───────────────────────────────────── */
setupClip("#clip-8", 268, 38, {
  leftBullets: 4,
  rightBullets: 4,
});

/* ─────────────────────────────────────
   CLIP 9 — Research Insights (306–344s, 38s)
   ───────────────────────────────────── */
setupClip("#clip-9", 306, 38, {
  leftBullets: 4,
  rightBullets: 4,
});

/* ─────────────────────────────────────
   CLIP 10 — Minimal Python Harness Synthesis (344–382s, 38s)
   ───────────────────────────────────── */
setupClip("#clip-10", 344, 38, {
  leftBullets: 4,
  rightBullets: 4,
  hasFlow: true,
  flowNodes: 9,
});

/* ── Register the timeline ── */
window.__timelines[COMP_ID] = tl;

/* ── Blank-screen fallback (from HOT_TIPS) ── */
/* Auto-play only when NOT in HyperFrames render/seek mode */
if (!window.location.search.includes("hyperframes") && !window.__HYPERFRAMES__) {
  tl.play();
}