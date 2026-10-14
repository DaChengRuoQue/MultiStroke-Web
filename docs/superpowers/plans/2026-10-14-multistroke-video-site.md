# MultiStroke Video Site Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local static webpage whose only visible content is the existing MultiStroke video.

**Architecture:** A single buildless `index.html` contains the native video element and embedded responsive CSS. A small standard-library test parses the document and pins the required player behavior.

**Tech Stack:** HTML5, CSS, Python standard-library `unittest`

**Spec:** `docs/superpowers/specs/2026-10-14-multistroke-video-site-design.md`

## Global Constraints

- Keep `MultiStroke.mp4` unchanged.
- Do not add dependencies, a build step, visible copy, autoplay, or looping.
- Keep the site local; do not publish it.

## Review Focus

- The body must not acquire visible content besides the video.
- Browsers must expose native playback controls.
- Playback must not begin or repeat automatically.
- The relative source must resolve to `MultiStroke.mp4`.
- Portrait and landscape viewports must contain the full uncropped video.

---

### Task 1: Static video page

**Files:**
- Create: `index.html`
- Create: `tests/test_page.py`

**Interfaces:**
- Consumes: the existing `MultiStroke.mp4` asset.
- Produces: a directly openable static webpage with one responsive native video player.

- [ ] **Step 1: Write the failing page-contract tests**

Create `tests/test_page.py` with assertions for one video as the body's sole element, `controls` and `playsinline`, absence of `autoplay` and `loop`, the exact `MultiStroke.mp4` source, no external dependencies, and viewport-contained styling.

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -m unittest tests.test_page -v`

Expected: FAIL because `index.html` does not exist.

- [ ] **Step 3: Implement the static page**

Create `index.html` with embedded CSS, a marginless dark viewport, and one centered video using native controls, metadata preloading, inline playback, and uncropped responsive sizing.

- [ ] **Step 4: Verify the page contract and asset integrity**

Run: `python -m unittest tests.test_page -v`

Expected: all tests pass. Confirm `MultiStroke.mp4` retains its pre-implementation checksum.

- [ ] **Step 5: Commit the implementation**

Run: `git add index.html tests/test_page.py && git commit -m "feat: add MultiStroke video page"`
