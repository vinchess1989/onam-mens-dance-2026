# Onam Men's Dance 2026 — Project Memory & Technical Overview

## 1. Project Overview
**Onam Men's Dance 2026** is the audio production and interactive rehearsal platform for the 2026 Onam Men's stage performance routine. It includes a custom-engineered 9-track master audio mix and a mobile-optimized web rehearsal studio with instant section seeking, A-B looping, tempo control, multi-version routine tabs, and an interactive choreography pause cue beat system.

- **GitHub Repository:** `https://github.com/vinchess1989/onam-mens-dance-2026`
- **Hosted Rehearsal Studio (GitHub Pages):** `https://vinchess1989.github.io/onam-mens-dance-2026/`
- **Master Audio (Baked Cues):** [`onam_mens_final_26_0909.mp3`](file:///c:/Users/vinee/Video%20Editing/onam_mens_final_26_0909.mp3) (4m 12.7s / 252.70s)
- **Previous Clean Mix:** [`onam_mens_final_26_0906.mp3`](file:///c:/Users/vinee/Video%20Editing/onam_mens_final_26_0906.mp3) (4m 09.7s / 249.70s)

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
  - **2-Column Studio Layout:** Persistent sticky master controller on the left column (timeline, 0.01s precision jog shuttle, playback, loop, countdown, speed) paired with routine segments and component studio in the right column.
  - 4-tab multi-version switcher: **Final Mix 260909** (Baked Cues & 3s Chettikulangara Metronome Pause, 04:12), **Sep 8 Master** (Clean Audio, 04:09), **Previous Mix Backup** (7 Tracks, 04:07), and **Sep 7 Legacy Mix** (6 Tracks, 04:40).
  - **0.01s Precision Seeking & Jog Shuttle:** Frame-accurate timecode display (`MM:SS.ss`), direct numeric jump input (`[ 50.50 ]`), 0.01s step scrubber slider, and micro-nudge buttons (`±0.01s`, `±0.10s`, `±1.00s`).
  - **Individual Component Studio (11 Tracks):** Isolated solo decks for all individual dialogue and music component tracks with local 0.01s scrubbers, independent playback, single-click MP3 downloads, and `⚡ Sync to Mix` synchronization into the master timeline.
  - One-click master MP3 download button (`⬇ Download Final Mix [7.0 MB]`).
  - Tap-to-skip 3-second ready countdown (default OFF per dancer feedback).
  - **Audio Waveform & Beat Transient Graph:** Interactive canvas showing audio peaks and beat drops/clave spikes. Kept **OFF by default** to maximize player compactness; toggleable on/off anytime via the `📊 Waveform: OFF/ON` control button, status tag, panel header `✕ Hide`, or `W` keyboard shortcut.
  - **Real-Time Tempo Speed Slider (0.1x to 4.0x):** Dynamic smooth range slider allowing playback speed adjustments from ultra-slow motion (0.10x) up to 4.0x while playing any audio (master routine mix, individual component solo tracks, and countdown cues), with quick presets (0.25x, 0.5x, 0.75x, 1.0x, 1.25x, 1.5x, 2.0x) and single-click 1x reset.
  - **Reference Video Rehearsal Studio (`Fusion Malayalam dance.mp4`):** Dedicated video player tab accessible via header tabs (`Video • Fusion Dance • 5 Cues`) and view switcher (`Reference Video`), hosting the 05:14 reference video with **5 named song seek points**:
    - **`shanthamee`** at **0:28** (`00:28.00` • 8.90% marker tick)
    - **`ivalkkoruvan`** at **1:01** (`01:01.00` • 19.38% marker tick)
    - **`chettikulangara`** at **2:06** (`02:06.00` • 40.04% marker tick)
    - **`njanondaliyan`** at **2:50** (`02:50.00` • 54.02% marker tick)
    - **`vel muruka`** at **3:25** (`03:25.00` • 65.14% marker tick)
    Includes individual jump cue cards, interactive timeline tick markers, quick jump presets, individual section A-B repeat loops (`shanthamee 0:28-1:01`, `ivalkkoruvan 1:01-2:06`, `chettikulangara 2:06-2:50`, `njanondaliyan 2:50-3:25`, `vel muruka 3:25-4:25`), 0.01s scrub slider, micro-nudges (`±0.01s` to `±5s`), **smooth real-time video playback speed slider (0.1x to 3.0x)** with live readout badge, quick presets (0.25x-2.0x), reset 1x, and theater view.
  - A-B section repeat loops.
  - Keyboard shortcuts: Space (Play/Pause), Left/Right (Seek ±5s), `[` / `]` (Prev/Next Song), `L` (Loop Song), `C` (Countdown), `W` (Toggle Waveform), `V` (Toggle Reference Video).

---

## 3. Final Master Routine Timeline (9 Tracks + 2 Stage Pauses • 04:12.70 / 252.70s)

| # | Track Title | Badge | Start | End | Duration | Notes |
|---|---|---|---|---|---|---|
| 1 | Kalyanaraman (Intro) | Intro Hook | `00:00.0` | `00:09.5` | 9.5s | Dialogue intro; 🚀 Energy Riser baked into last 3s (`00:06.5 → 00:09.5`) |
| 2 | Chettikulangara | Song 1 | `00:09.5` | `00:50.5` | 41.0s | First full group dance; ends cleanly without overlap |
| — | *Choreography Pause 1* | *3s Metronome Gap* | `00:50.5` | `00:53.5` | 3.0s | Dedicated stage silence with 3 metronome clicks at 0.25x volume (`cue_option1_sticks.mp3`) |
| 3 | Sablazki Dialogue (+3s Reverb) | Dialogue | `00:53.5` | `01:15.01` | 21.51s | 8.90-9.80 removed (-0.90s); smooth 3s reverb decay tail (clean dialogue, 3s drum beat cue removed) |
| 4 | Shanthamee Rathri | Song 2 | `01:15.01` | `01:46.01` | 31.0s | Melodic transition piece |
| 5 | Pondicherry Dialogue | Dialogue 2 | `01:46.01` | `01:55.70` | 9.69s | Dialogue punchline ending |
| — | *Choreography Pause 2* | *3s Sticks Gap* | `01:55.70` | `01:58.70` | 3.0s | Dedicated stage silence with 3 stick clicks at 0.25x volume into beat drop |
| 6 | Ivalkoruvan Song | Song 3 | `01:58.70` | `02:27.70` | 29.0s | High-energy beat drop; 2s Fade In & 2s Fade Out (`ivalkoruvan_new.mp3`) |
| 7 | Njanondaliyanum | Song 4 | `02:27.70` | `03:21.70` | 54.0s | Group formation dance segment |
| 8 | Velmuruka Harohara | Fast Beats | `03:21.70` | `04:04.70` | 43.0s | 2s fade-out beginning at `04:02.70` as applause starts |
| 9 | Crowd Applause & Cheering | Applause | `04:02.70` | `04:12.70` | 10.0s | 2s crossfade overlap into end of Velmuruka |

---

## 4. Choreography Cue Beat System

Designed to guide dancers with clear countdown cues before music drops without permanently altering the stage audio until approved.

### Sound Options (each 3.0s in length):
1. **Option 1: Stick Clicks** ([`cue_option1_sticks.mp3`](file:///c:/Users/vinee/Video%20Editing/cue_option1_sticks.mp3)) — 3 crisp clave/woodblock clicks (`0.75s`, `1.50s`, `2.25s` ➔ Drop at `3.00s`), volume reduced to **0.25x** for subtle background stage counting.
2. **Option 2: Heartbeat Thump** ([`cue_option2_thump.mp3`](file:///c:/Users/vinee/Video%20Editing/cue_option2_thump.mp3)) — 3 deep sub-bass kicks (`45–110 Hz`).
3. **Option 3: Energy Riser** ([`cue_option3_riser.mp3`](file:///c:/Users/vinee/Video%20Editing/cue_option3_riser.mp3)) — Rising pitch/noise swoosh swell landing on count 1.

### Active Dialogue Cue Assignments (Baked into Final Mix 260909):
- **Before Chettikulangara (Part 1 - Kalyanaraman tail):** **Option 3: Energy Riser** (`cue_option3_riser.mp3`) overlapping `00:06.50 ➔ 00:09.50`. Quick jump: `00:05.0`.
- **Between Chettikulangara & Sablazki (3s Stage Pause):** **Option 1: Metronome Stick Clicks at 0.25x volume** (`cue_option1_sticks.mp3`) playing in dedicated 3-second stage pause `00:50.50 ➔ 00:53.50` (no music overlap). Gives dancers 3 seconds to reset formation before Sablazki dialogue drops at 00:53.50. Quick jump: `00:48.0`.
- **Before Shanthamee (Part 3 - Sablazki tail):** **Removed per request** (clean dialogue audio with natural vocal reverb decay tail into Shanthamee).
- **Before Ivalkoruvan (Part 5 - Pondicherry 3s pause):** **Option 1: Stick Clicks at 0.25x volume** (`cue_option1_sticks.mp3`) playing in dedicated 3-second stage pause `01:55.70 ➔ 01:58.70`. Quick jump: `01:53.0`.

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
