# Onam Men's Dance 2026 — Project Memory & Technical Overview

## 1. Project Overview
**Onam Men's Dance 2026** is the audio production and interactive rehearsal platform for the 2026 Onam Men's stage performance routine. It includes a custom-engineered 9-track master audio mix and a mobile-optimized web rehearsal studio with instant section seeking, A-B looping, tempo control, multi-version routine tabs, and an interactive choreography pause cue beat system.

- **GitHub Repository:** `https://github.com/vinchess1989/onam-mens-dance-2026`
- **Hosted Rehearsal Studio (GitHub Pages):** `https://vinchess1989.github.io/onam-mens-dance-2026/`
- **Master Audio (Baked Cues):** [`onam_mens_final_26_0909.mp3`](file:///c:/Users/vinee/Video%20Editing/onam_mens_final_26_0909.mp3) (4m 10s / 249.66s)
- **Previous Clean Mix:** [`onam_mens_final_26_0906.mp3`](file:///c:/Users/vinee/Video%20Editing/onam_mens_final_26_0906.mp3) (4m 10s / 249.66s)

---

## 2. Tech Stack & Architecture

### Audio Engineering & Pipeline
- **Engine:** FFmpeg (`libmp3lame`, `-q:a 0` high-fidelity VBR) and `ffprobe` for precise millisecond measurement.
- **Normalization Standard:** EBU R128 (`-10.8 LUFS`, peak `~ -4.2 dBTP`) across all 9 routine tracks to prevent abrupt volume drops or clipping between spoken dialogues and high-energy music.
- **Configuration Source of Truth:** [`track_config.json`](file:///c:/Users/vinee/Video%20Editing/track_config.json) declaring the sequence, file references, pause gaps, and overlap rules.
- **Automation Skill:** [`update_final`](file:///c:/Users/vinee/.gemini/config/skills/update_final/SKILL.md) located at `C:\Users\vinee\.gemini\config\skills\update_final\scripts\update_final.py`. Automatically creates timestamped backups before regenerating the master MP3 and updating player timestamps.

### Frontend Web Player
- **Core Files:**
  - [`dance_practice_player.html`](file:///c:/Users/vinee/Video%20Editing/dance_practice_player.html) — Main development rehearsal player.
  - [`index.html`](file:///c:/Users/vinee/Video%20Editing/index.html) — Mirror file served directly by GitHub Pages.
  - [`generate_3tab_player.py`](file:///c:/Users/vinee/Video%20Editing/generate_3tab_player.py) — Python script to regenerate both HTML files synchronously.
- **Styling & UI:** Vanilla HTML5, CSS3 Glassmorphism (dark theme, responsive mobile grid), Web Audio / HTML5 Audio API.
- **Key Features:**
  - 4-tab multi-version switcher: **Final Mix 260909** (Baked Cues, 04:10), **Sep 8 Master** (Clean Audio, 04:10), **Previous Mix Backup** (7 Tracks, 04:07), and **Sep 7 Legacy Mix** (6 Tracks, 04:40).
  - Tap-to-skip 3-second ready countdown (default OFF per dancer feedback).
  - A-B section repeat loops & variable playback speeds (0.75x, 0.85x, 1.0x, 1.15x).
  - Keyboard shortcuts: Space (Play/Pause), Left/Right (Seek ±5s), `[` / `]` (Prev/Next Song), `L` (Loop Song), `C` (Countdown).

---

## 3. Current Master Routine Timeline (9 Tracks • 04:10)

| # | Track Title | Badge | Start | End | Duration | Notes |
|---|---|---|---|---|---|---|
| 1 | Kalyanaraman (Intro) | Intro Hook | `00:00.0` | `00:09.5` | 9.5s | Dialogue intro; cue overlap active on last 3s (`00:06.5 → 00:09.5`) |
| 2 | Chettikulangara | Song 1 | `00:09.5` | `00:50.5` | 41.0s | First full group dance |
| 3 | Sablazki Dialogue (+3s Reverb) | Dialogue | `00:50.5` | `01:12.91` | 22.41s | Smooth 3s reverb decay tail; cue overlap active on last 3s (`01:09.9 → 01:12.9`) |
| 4 | Shanthamee Rathri | Song 2 | `01:12.91` | `01:41.91` | 29.0s | Melodic transition piece |
| 5 | Pondicherry Dialogue | Dialogue 2 | `01:41.91` | `01:52.16` | 10.25s | Cut at exactly 10.25s to preserve punchline clean ending |
| — | *Choreography Pause* | *3s Gap* | `01:52.16` | `01:55.16` | 3.0s | Dedicated stage silence / countdown window into drop |
| 6 | Ivalkoruvan Song | Song 3 | `01:55.16` | `01:44.66` | 29.5s | High-energy beat drop starting on count 1 |
| 7 | Njanondaliyanum | Song 4 | `01:44.66` | `03:18.66` | 54.0s | Group formation dance segment |
| 8 | Velmuruka Harohara | Fast Beats | `03:18.66` | `04:01.66` | 43.0s | 2s fade-out beginning at `03:59.66` as applause starts |
| 9 | Crowd Applause & Cheering | Applause | `03:59.66` | `04:09.66` | 10.0s | 2s crossfade overlap into end of Velmuruka |

---

## 4. Choreography Cue Beat System

Designed to guide dancers with clear countdown cues before music drops without permanently altering the stage audio until approved.

### Sound Options (each 3.0s in length):
1. **Option 1: Stick Clicks** ([`cue_option1_sticks.mp3`](file:///c:/Users/vinee/Video%20Editing/cue_option1_sticks.mp3)) — 3 crisp clave/woodblock clicks (`0.75s`, `1.50s`, `2.25s` ➔ Drop at `3.00s`).
2. **Option 2: Heartbeat Thump** ([`cue_option2_thump.mp3`](file:///c:/Users/vinee/Video%20Editing/cue_option2_thump.mp3)) — 3 deep sub-bass kicks (`45–110 Hz`).
3. **Option 3: Energy Riser** ([`cue_option3_riser.mp3`](file:///c:/Users/vinee/Video%20Editing/cue_option3_riser.mp3)) — Rising pitch/noise swoosh swell landing on count 1.

### Active Dialogue Cue Assignments:
- **Before Chettikulangara (Part 1 - Kalyanaraman tail):** **Option 3: Energy Riser** (`cue_option3_riser.mp3`) overlapping `00:06.50 ➔ 00:09.50`. Quick jump: `00:05.0`.
- **Before Sablazki Dialogue (Part 2 - Chettikulangara tail):** **Option 1: Stick Clicks (Metronome)** (`cue_option1_sticks.mp3`) overlapping `00:47.50 ➔ 00:50.50`. Overlays 3 metronome ticks (1, 2, 3 ➔ Drop) across the end of Chettikulangara with continuous, uninterrupted playback into Sablazki. Quick jump: `00:45.0`.
- **Before Shanthamee (Part 3 - Sablazki tail):** **Option 2: Heartbeat Thump** (`cue_option2_thump.mp3`) overlapping `01:09.91 ➔ 01:12.91`. Quick jump: `01:08.0`.
- **Before Ivalkoruvan (Part 5 - Pondicherry 3s pause):** **Option 1: Stick Clicks** (`cue_option1_sticks.mp3`) playing `01:52.16 ➔ 01:55.16`. Quick jump: `01:50.0`.

### Player Synchronization Engine:
- Uses a 60fps `requestAnimationFrame` sync loop paired with `timeupdate` to synchronize the secondary cue audio object against `mainAudio.currentTime` with sub-16ms jitter.
- Automatically inherits playback speed changes (`cue.playbackRate = audio.playbackRate`).
- Resets and stops cues on pause, seek, routine tab switch, or routine end.

---

## 5. Key Workflows & Commands

### Updating Routine Mix
To rebuild the master mix and sync HTML after adjusting `track_config.json`:
```powershell
powershell -ExecutionPolicy Bypass -Command "& 'C:\Users\vinee\screen translator\venv\Scripts\python.exe' 'C:\Users\vinee\.gemini\config\skills\update_final\scripts\update_final.py'"
```

### Regenerating Player HTML
```powershell
powershell -ExecutionPolicy Bypass -Command "& 'C:\Users\vinee\screen translator\venv\Scripts\python.exe' 'generate_3tab_player.py'"
```

### Deploying to GitHub Pages
```bash
git add .
git commit -m "Update rehearsal studio player"
git push origin main
```
The live player at `https://vinchess1989.github.io/onam-mens-dance-2026/` updates automatically within 1–2 minutes.
