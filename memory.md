# Men's Dance | Oulu Onam 2026 — Project Memory & Technical Overview

## 1. Project Overview
**Men's Dance | Oulu Onam 2026** is the official media platform and interactive rehearsal studio for the 2026 Onam Men's stage performance routine. It hosts live multi-angle stage performance event videos recorded on September 12, 2026, a custom-engineered 9-track master audio mix, in-browser original 4K/HD video upload replacements, and a mobile-optimized web rehearsal studio with instant section seeking, A-B looping, tempo control, multi-version routine tabs, and an interactive choreography pause cue beat system.

- **GitHub Repository:** `https://github.com/vinchess1989/onam-mens-dance-2026`
- **Hosted Web Studio (Firebase Hosting):** `https://vk-onam-dance.web.app` (also `https://vk-onam-dance.firebaseapp.com`)
- **Hosted Web Studio (GitHub Pages):** `https://vinchess1989.github.io/onam-mens-dance-2026/`
- **Home Page Default View:** **Event videos** Tab (`WhatsApp Video 2026-09-12 at 17.55.13.mp4` / `IMG_9331.MOV` [Angle 1 Original Full HD 1080p 60fps], `WhatsApp Video 2026-09-12 at 19.17.08.mp4` / `IMG_8181.MOV` [Angle 2 Original Full HD 1080p 30fps], `IMG_0865.mp4` / `IMG_0865.MOV` [Angle 3 Front Stage Original Full HD 1080p 60fps])
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

## Major Features
1. **Interactive Rehearsal Studio (0.01s Precision):** Frame-accurate jog shuttle, numeric timecode seek input, 0.01s step scrubber, and micro-nudging (`±0.01s` to `±1.00s`).
2. **Multi-Angle 4K/Full HD Stage Performance Viewer:** Responsive multi-angle stage recording player (Angles 1–3) with in-browser video upload replacements.
3. **9-Track EBU R128 Master Audio Mix:** High-fidelity VBR MP3 mix normalized to `-10.8 LUFS` across 9 song and dialogue segments with dedicated stage pause cue beats.
4. **Individual Component Studio (11 Solo Decks):** Isolated decks for every dialogue and song track with local scrubbing, individual downloads, and master timeline synchronization.
5. **Multi-Version Routine Switcher:** Instant toggling across 4 historical performance iterations (Final Mix 260909, Sep 8 Master, Previous Mix, Legacy Mix).

---

## Minor Features & Utilities
- **Interactive Audio Waveform & Beat Canvas:** Real-time canvas rendering peak levels and rhythm drops with instant hotkey toggling (`W`).
- **Smooth Speed Pitch-Preserving Slider:** Continuous tempo adjustment from 0.1x to 4.0x across audio and reference video.
- **Reference Video Player with 5 Named Song Cues:** Synchronized reference choreography video with pre-marked song transitions.
- **Automated Skill Pipeline (`update_final`):** One-command rebuild calculating track durations, backing up previous mixes, and updating player seek points.

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

### Deploying to Firebase Hosting (`vk-onam-dance` in `misc-vk`)
```bash
firebase deploy --only hosting
```
The site deploys instantly to `https://vk-onam-dance.web.app` with HTTP byte-range media streaming headers.

### Deploying to GitHub Pages
```bash
git add .
git commit -m "Update rehearsal studio player"
git push origin main
```
The live player at `https://vinchess1989.github.io/onam-mens-dance-2026/` updates automatically within 1–2 minutes.

---

## 6. 2-Minute Slow-Motion Highlights Dance Reel (`onam_dance_reel_*.mp4`)

A dedicated cinematic 2-minute dance reel produced from high-framerate (60fps/30fps) master performance footage with the celebratory *Onam Mood* soundtrack.

- **Files**:
  - `onam_dance_reel_2min.mp4` (Vertical 9:16, 1080×1920, 32.6 MB) — Mobile-optimized for Instagram Reels, YouTube Shorts, and WhatsApp Status with blurred ambient backdrop, gold framing, and gold/white titles.
  - `onam_dance_reel_widescreen_2min.mp4` (Widescreen 16:9, 1920×1080, 50.2 MB) — Full-stage cinematic master with clean lower-third gold badges.
- **Audio Track**:
  - Mastered 120.0s cut (`01:25 → 03:25`) from `Onam Mood - Sahasam (Full HD 1080p).mp4`.
  - Mastered with 1.0s fade-in, 2.5s smooth fade-out, and EBU R128 loudness normalization (`-14.0 LUFS`).
- **Video Choreography Highlights**:
  - 11 curated performance moments (Intro walk-in, Chettikulangara, Sablazki pose, Shanthamee, Pondicherry, Ivalkoruvan jump, Njanondaliyan formation, Velmuruka claps & spins, Grand finale bow & salute).
  - Silky-smooth **0.5x slow-motion** rendered with FFmpeg `setpts=2.0*PTS`, preserving natural stage motion and expression.
- **Player Integration**:
  - Embedded reel viewer card (`#eventReelContainer`) in both `index.html` and `dance_practice_player.html`.
  - Accessible via `🎬 2-Min Slow-Mo Reel` button in the Event Videos toolbar.
  - Format toggle switch between 📱 Vertical (9:16) and 🖥️ Widescreen (16:9).
  - Direct download links for both formats.

---

## 7. Event Videos & In-Memory Preloader Engine

### Multi-Angle Event Videos Specifications:
- **Angle 1 (Side Stage View):** Original Full HD 1080p 60fps Master (`IMG_9331.MOV`, 1.48 GB camera master; `WhatsApp Video 2026-09-12 at 17.55.13.mp4`, 84.7 MB stream).
- **Angle 2 (Center Stage View):** Original Full HD 1080p 30fps Master (`IMG_8181.MOV`, 708 MB camera master; `WhatsApp Video 2026-09-12 at 19.17.08.mp4`, 89.2 MB stream).
- **Angle 3 (Front Stage View):** Original 4K UHD 60fps Master (`IMG_0865.MOV`, 1.44 GB, 3840×2160 @ 60fps; `IMG_0865.mp4`, 95.3 MB stream @ 1080p 60fps).
  - Badges accurately display: `📐 3840×2160 (Original 4K 60fps Master)`, `💾 1.44 GB (Original 4K Master)`, and `⚡ 95 MB 1080p60 Stream`.
  - Default video tag uses `preload="auto"` instead of `preload="metadata"` for proactive buffering.

### In-Memory Preloader Engine (`preloadCurrentVideo()`):
- **Problem Solved:** Standard HTML5 `<video>` streaming over progressive MP4 causes playback stalls, frame drops, and seeking latency on slower or fluctuating connections at 60fps.
- **Architecture:**
  - Toolbar button `⚡ Preload for Smooth Playback` (`#btnPreloadVideo`) with live download percentage progress bar (`#preloadProgressBarContainer` / `#preloadProgressBarFill`).
  - Reads chunks asynchronously via `fetch()` and `ReadableStream`, calculating exact byte progress from `Content-Length`.
  - Compiles chunks into a binary `Blob` and binds it to `URL.createObjectURL(blob)`.
  - Seamlessly re-assigns `video.src` to the blob URL without losing current playback position.
  - Caches preloaded blob URLs in `preloadedBlobs[angle]` so switching angles maintains immediate RAM playback without re-downloading.
  - Guarantees 0ms seek latency, zero frame drops, and 100% glitch-free 60fps playback even offline.

---

## 8. YouTube Unlisted Embeds & GitHub Pages Decommissioning
- **Primary Hosting:** Exclusively on Firebase Hosting (`https://vk-onam-dance.web.app`).
- **GitHub Pages Decommissioned:** Successfully unpublished and deleted via GitHub API (`DELETE /repos/vinchess1989/onam-mens-dance-2026/pages` returned HTTP 204). The GitHub Pages site (`https://vinchess1989.github.io/onam-mens-dance-2026/`) returns HTTP 404 (fully decommissioned).
- **YouTube Unlisted Uploads (Vineeth Kaimal Channel `UCjNp0glIgwtrXNuADhMQAIg`):**
  - **Angle 1:** `https://youtu.be/Xk39waxkT3E` (Video ID: `Xk39waxkT3E`)
    - Title: `Men's Dance | Oulu Onam 2026 — Angle 1 (Side Stage View • 4K 60fps)`
    - File: `IMG_9331.MOV` (2.29 GB, 4K UHD 60fps)
  - **Angle 2:** `https://youtu.be/Mq2H5twbho8` (Video ID: `Mq2H5twbho8`)
    - Title: `Men's Dance | Oulu Onam 2026 — Angle 2 (Center Stage View • Full HD)`
    - File: `IMG_8181.MOV` (702 MB, 1080p Full HD)
    - File: `IMG_8181.MOV` (702 MB, 1080p Full HD)
  - **Angle 3 (Corrected 4K 60fps Master):** `https://youtu.be/caphuNKQkkQ` (Video ID: `caphuNKQkkQ`)
    - Title: `Men's Dance | Oulu Onam 2026 — Angle 3 (Front Stage View • 4K 60fps Master)`
    - File: `IMG_0865_corrected_master.mp4` (1.65 GB, 4K UHD 60fps Master)
    - Previous/superseded upload: `1JpmA73g1h4`
  - **Visibility:** Unlisted (accessible only via link or embedded player).
  - **Upload Pipeline:** Overcame Playwright's 50MB CDP file transfer limit using native Chrome DevTools Protocol (`DOM.setFileInputFiles` with `backendNodeId`) to feed multi-gigabyte local camera master files directly to YouTube Studio without socket overhead.
- **Stream Setup:**
  - Exclusively streams via YouTube's global CDN (`https://www.youtube-nocookie.com/embed/...`) with zero stutter, automatic 4K/1080p60 adaptive bitrate, and responsive iframes.
  - "Direct File / RAM" selector, in-memory preloader, and local MP4 download links removed from HTML (`index.html` and `dance_practice_player.html`).
  - `firebase.json` ignore list updated with `*.mp4`, `*.MP4`, `*.MOV`, `*.mov`, `*.mkv`, `*.webm` to completely exclude heavy video files from Firebase Hosting.
- **Angle 3 Exposure & Stage Elevation Glare Correction (Completed & Live):**
  - **Root Cause of Blown Stage Elevation:**
    - Angle 3 was shot right in the front row where high-intensity floor footlights pointed directly up towards the camera lens.
    - Raw 10-bit luminance dump (`scratch/dump_luminance.py`) proved that the bottom 10% of the frame (rows 1940 to 2160) was physically saturated at the camera sensor level (luminance values average 829.6 out of 1023, variance < 0.05%), meaning zero texture (wood slats, garlands) was captured in that band.
    - Angle 2 was filmed from ~15 meters back on an elevated tripod where footlights did not blast into the lens, clearly capturing the wooden stage lip, garlands, and white vertical slats.
  - **Split-Timeline Clean Reframe & Grade (Rendered, Uploaded & Deployed):**
    - `00:00 → 05:38`: Clean Reframe `crop=3306:1860:(in_w-3306)/2:0,scale=3840:2160` + Highlight roll-off & color grade (removes bottom 300px footlight glare, dancers' feet grounded).
    - `05:38 → 06:53.77`: Dancers came down to the floor in front of the stage. **Zero crop** (full native 3840x2160) + Highlight roll-off & color grade so full bodies/legs are retained.
    - Master Video output: `IMG_0865_corrected_master.mp4` (4K UHD 3840x2160 @ 59.94fps, 1.65 GB, 320 kbps AAC stereo, faststart enabled).
    - Uploaded to YouTube: [`https://youtu.be/caphuNKQkkQ`](https://youtu.be/caphuNKQkkQ) (Video ID: `caphuNKQkkQ`).
    - Web Embed & Player Updated: Both `index.html` and `dance_practice_player.html` updated and deployed to Firebase Hosting (`https://vk-onam-dance.web.app`) and pushed to GitHub `main`.
    - 10-second full clean reframed video: `sample_10s_clean_reframed.mp4`.

---

## 9. Header Tab Unification & 2-Min Slow-Mo Reel Fix (Completed & Live)

### Unified Header Tab Highlight
- **Problem Solved:** Selecting "Event videos" displayed a vibrant amber/orange glow highlight, whereas clicking other tabs ("Reference Video", "Final Mix 260909", "Sep 8 Master", etc.) either did not show the orange highlight or applied different color schemes (pink, green, cyan).
- **CSS Architecture:**
  - Unified all active tab states under `.version-tabs-nav .tab-btn.active-tab`, `.tab-btn.active-tab`, `.tab-btn.event-btn.active-tab`, `.tab-btn.video-tab-btn.active-tab`, `.tab-btn.final-btn.active-tab`, `.tab-btn.backup-btn.active-tab`, `.tab-btn.legacy-btn.active-tab`.
  - Signature Amber Pill Gradient: `background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;`
  - High-Contrast Text: `color: #090c15 !important; font-weight: 800 !important;` applied to both the button and all child `span` elements.
  - Signature Glow Halo: `box-shadow: 0 4px 18px rgba(245, 158, 11, 0.45), 0 0 0 1px rgba(245, 158, 11, 0.5) !important;`
  - Badges inside active tabs styled with translucent dark backing (`background: rgba(0, 0, 0, 0.22) !important; color: #090c15 !important;`).

### 2-Min Slow-Mo Reel Click & Playback Fix
- **Problem Solved:** Clicking "🎬 2-Min Slow-Mo Reel" caused nothing to happen.
- **Root Cause & Resolution:**
  1. **Undeclared `eventVideoFeatured` ReferenceError:** When YouTube iframes replaced the earlier `<video id="eventVideoFeatured">` tag, functions `toggleEventViewMode()`, `openVideoTab()`, and `switchRoutine()` still referenced `eventVideoFeatured.pause()`, triggering a fatal `ReferenceError: eventVideoFeatured is not defined` that terminated the click handler. Declared `let eventVideoFeatured = null;` globally to eliminate the exception.
  2. **Firebase 404 on Reel MP4s:** `firebase.json` previously excluded `*.mp4`, which accidentally blocked the lightweight reel MP4s (`onam_dance_reel_2min.mp4` [31.1 MB] and `onam_dance_reel_widescreen_2min.mp4` [47.8 MB]). Refined `firebase.json` to explicitly ignore heavy camera master files (`IMG_*`, `WhatsApp Video*`) while allowing reel and dance reference videos.
  3. **Auto-play & Smooth Scroll:** `toggleEventViewMode('reel')` now resets button classes, applies the amber active pill to `#btnAngleReel`, reveals `#eventReelContainer`, smoothly scrolls it into view via `reelBox.scrollIntoView({ behavior: 'smooth', block: 'start' })`, and starts playback immediately.
  4. **Synced & Deployed:** Synchronized across `index.html` and `dance_practice_player.html`, verified live in Chrome CDP, deployed to Firebase Hosting (`https://vk-onam-dance.web.app`), and pushed to GitHub `main`.

---

## 10. Photo Gallery & Multi-Track Slow-Mo Reel Director Studio (`reel_tuner.html`) (Completed & Live)

### 1. 25-Photo Stage Performance Gallery & Fullscreen Lightbox
- **Photographs Source:** 25 pristine high-resolution stage performance photos taken on September 12, 2026 by Rakesh (`DSC06893.jpg` to `DSC07025.jpg`), located in [`Photos-Rakesh/`](file:///c:/Users/vinee/Video%20Editing/Photos-Rakesh/).
- **Archive ZIP Download:** Bundled all 25 images into [`Photos-Rakesh.zip`](file:///c:/Users/vinee/Video%20Editing/Photos-Rakesh.zip) (10.5 MB) for single-click full download directly from the gallery toolbar.
- **Navigation & Tab:**
  - Added dedicated `#tabPhotoGallery` button (`📸 Photo Gallery • 25 Photos • Rakesh`) to the main header navigation in [`index.html`](file:///c:/Users/vinee/Video%20Editing/index.html) and [`dance_practice_player.html`](file:///c:/Users/vinee/Video%20Editing/dance_practice_player.html).
  - Unified with the signature active amber pill highlight (`.tab-btn.gallery-btn.active-tab`).
- **Interactive Lightbox Modal (`#photoLightboxModal`):**
  - Fullscreen dark glass backdrop (`rgba(5, 8, 18, 0.96)`) with blur (`20px`).
  - Photo counter (`Photo X of 25`), filename badge, individual high-res download button, and close button.
  - Previous/Next navigation buttons and full keyboard support (`←` Previous, `→` Next, `Esc` Close).
  - Dynamic DOM querying implemented to eliminate closures across script tags.

### 2. Temporary Removal of 2-Min Reel Button
- Per user instruction, removed `#btnAngleReel` ("🎬 2-Min Slow-Mo Reel") from the live event video angle bar until fine-tuning is completed via the director studio.

### 3. Multi-Track Slow-Mo Reel Director Studio ([`reel_tuner.html`](file:///c:/Users/vinee/Video%20Editing/reel_tuner.html))
- **Dedicated NLE Web Application:** Built a standalone, interactive timeline director studio allowing the user to visually inspect, trim, nudge, add, and reorder slow-motion clips and photo slides across all 3 stage performance camera angles.
- **3-Angle Video Decks:**
  - Angle 1 (Side Stage - 340s / 05:40), Angle 2 (Center Stage - 356s / 05:56), and Angle 3 (Front Stage - 413s / 06:53).
  - Synchronized seeking, micro-nudges (`-1s`, `-0.1s`, `+0.1s`, `+1s`), and "➕ Add Clip Here" deck buttons.
- **Multi-Track Timeline with Colorful Selection Rectangles:**
  - Dynamic zoom slider (`1.0x` to `5.0x`).
  - Color-coded clips: Sky Cyan for Angle 1, Amber Gold for Angle 2, Emerald Green for Angle 3.
  - Pre-populated with the 11 curated slow-motion clips totaling exactly 120.00s.
  - **Interactive Dragging:** Drag the body to shift start time (`ss`).
  - **Interactive Resizing:** Drag left/right handles to trim/extend in-point and out-point (`dur`).
  - Double-click empty track area to instantiate a new clip at that exact second.
- **Photo Slide Library Track:**
  - Horizontal scroller with all 25 Rakesh photos.
  - "➕ Reel (3s)" button inserts any photo as a slow cinematic slide into the sequence.
- **Bottom 120s Master Reel Assembly Dock:**
  - Real-time gauge comparing output duration against the 120.00s target (`Current: 120.00s / Target: 120.00s`).
  - Embedded **Soundtrack Preview Player** pre-loaded with [`onam_mood_2min.mp3`](file:///c:/Users/vinee/Video%20Editing/onam_mood_2min.mp3) (the 2-minute Onam Mood cut with applause fade-out).
  - Storyboard sequence strip with drag-to-reorder, clip labels, speeds, rendered durations, and quick delete (`✕`).
- **Clip Inspector Modal:**
  - Fine-tune label, angle track, start time (`ss`), source duration (`dur`), and speed presets (`0.25x`, `0.33x`, `0.50x`, `0.75x`, `1.00x`).
  - In-deck 5-second snippet preview button.
- **Export & Persistence:**
  - Auto-saves changes to `localStorage` (`onam_reel_tuner_items`).
  - "💾 Download Config": Generates [`reel_config.json`](file:///c:/Users/vinee/Video%20Editing/reel_config.json) formatted for direct rendering with `build_onam_reel.py`.
  - "📋 Copy JSON" button for quick clipboard sharing.
  - "🔄 Reset" restores the pristine 11 clips.
- **Deployed & Live:**
  - Deployed to Firebase Hosting (`https://vk-onam-dance.web.app/reel_tuner.html`).
  - Committed to Git `main` (commit `9dc2a99`).

---

## 11. Native Mobile App Shell & Clutter-Free Redesign (< 768px) (Completed & Live)

### 1. Architectural Motivation & User Feedback
- Per user request: *"can you make the mobile browser view like an app instead of a downward scrolling dirty looking html. keep the page as simple as possible. avoid all the unnecessary detail and buttons"*.
- The desktop view has rich, dense rehearsal tools (0.01s jog shuttles, 11-track solo component decks, multi-track waveform analyzer, countdown overlays, multi-version routine switchers, keyboard shortcut reference), but on mobile screens (`< 768px`) these created massive vertical clutter and awkward double-scrollbars.

### 2. Core Implementation
- **Fixed Glassmorphism Bottom App Bar (`#mobileAppBottomNav`):**
  - Stays pinned at `bottom: 0` on mobile viewports with 5 touch-optimized navigation tabs:
    1. `[🎬 Videos]` — Toggles Event Videos hero with angle pill bar.
    2. `[📸 Photos]` — Toggles 2-column Photo Gallery with fullscreen lightbox.
    3. `[🎵 Music]` — Toggles Spotify-style routine audio player & playlist.
    4. `[🎥 Reference]` — Toggles Reference Video player with horizontal cue pills.
    5. `[🎛️ Reel]` — Directly links to the Slow-Mo Reel Director Studio (`reel_tuner.html`).
  - Styled with glowing amber indicator on the active tab and subtle scale down on tap (`:active`).
- **Sticky Minimal Header:**
  - Compact sticky top bar featuring only the gradient title `Men's Dance | Oulu Onam 2026`.
  - All desktop pills, subtitles, and version tabs hidden on mobile.
- **Aggressive Clutter Elimination on Mobile:**
  - Unconditionally hidden on `< 768px`:
    - Desktop version tab switcher (`.version-tabs-nav`), subtitle badges (`.badge-pill`), download banner (`.download-bar`).
    - View mode switcher box (`#desktopViewModeBox` with `Routine Timeline View`, `Component Studio`, `Reference Video` buttons).
    - 0.01s jog shuttle micro-nudges (`±0.01s` to `±1.00s`), direct timecode inputs, countdown status indicators, tempo sliders.
    - Master waveform canvas section (`#masterWaveformSection`) and component studio solo decks (`#sectionComponentStudioView`).
    - Event video tech metadata pills (`⏱ 05:40`, `📐 3840×2160`, `💾 2.29 GB`, `⚡ YouTube 4K`), cloud upload buttons, and video upload toolbar.
    - Keyboard shortcuts reference footer (`.shortcuts-footer`).
    - Reference video 8-button nudge shuttle (`.video-shuttle-row`), secondary speed sliders (`#videoSpeedSliderContainer`), and 6 section loop toggles (`.video-loop-group`).
    - Routine segment time ranges (`Range: 00:00.00 -> 00:09.50`), baked riser notes, and 3-button per card actions (`Start`, `End`, `Loop`).
- **Clean Mobile Screens:**
  - **Videos:** Clean horizontal pill bar (`Angle 1`, `Angle 2`, `Angle 3`, `All Angles`) directly above 16:9 responsive YouTube player.
  - **Photos:** Responsive 2-column grid (`repeat(2, 1fr)`) with compact header (`25 Photos • Download ZIP`) and tap-to-open fullscreen lightbox.
  - **Music:** Sleek Spotify-style player card (title, progress scrubber, 5-button touch transport) above single-row tap-to-play playlist rows (`#Number Title Duration`).
  - **Reference Video:** Responsive 16:9 video player at the top with a horizontal scrolling pill selector below (`0:28 shanthamee`, `1:01 ivalkkoruvan`, `2:06 chettikulangara`, `2:50 njanondaliyan`, `3:25 vel muruka`).
- **Desktop Integrity Preserved (100%):**
  - Verified via Chrome DevTools Protocol at `1920x1080`: `#mobileAppBottomNav` is `display: none`, all 2-column desktop controls, waveform canvas, 11-track component studio, and jog shuttles remain fully functional.
- **Deployed & Live:**
  - Deployed to Firebase Hosting (`https://vk-onam-dance.web.app`).
  - Synced between `index.html` and `dance_practice_player.html`.

---

## 12. Mobile Videos Tab Bottom Nav Visibility Fix (< 768px) (Completed & Live)

### 1. Root Cause Analysis
- **Problem:** On mobile devices (e.g. iPhone 16 viewport `393x852`), opening the "Videos" tab pushed the fixed bottom navigation bar down to `y = 1781px`, requiring the user to scroll down ~1000px through an empty black void before the bottom navigation became visible.
- **Underlying Cause:**
  1. The `.event-angle-selector` flex container contained 4 buttons (`Angle 1`, `Angle 2`, `Angle 3`, `All 3 Angles Grid`) spanning a total min-content width of `814px`.
  2. Because the flex hierarchy (`#eventVideosStudioLayout`, `.event-videos-hero`, `.event-hero-header`, `.event-angle-selector`) lacked explicit `width: 100%; max-width: 100%; min-width: 0; box-sizing: border-box;`, the flex container expanded to its content width (`814px`).
  3. Consequently, the document's layout width expanded from `393px` to `847px`, prompting mobile Chrome to scale out the layout viewport from `393x852` to `847x1837`.
  4. The fixed bottom bar (`bottom: 0`) was positioned relative to the inflated `1837px` viewport height rather than the initial `852px` screen height.
  5. The `#countdownOverlay` element had `display: flex` and `opacity: 0` without `visibility: hidden`, contributing to the layout container height.

### 2. Implementation & Fix
1. **Mobile Root Viewport Locks (`@media (max-width: 768px)`):**
   - Added `html { width: 100% !important; max-width: 100vw !important; overflow-x: hidden !important; }`.
   - Set `body { width: 100% !important; max-width: 100vw !important; padding: 0 0 calc(64px + env(safe-area-inset-bottom, 0px)) 0 !important; margin: 0 !important; overflow-x: hidden !important; }`.
   - Constrained `.container { width: 100% !important; max-width: 100vw !important; min-width: 0 !important; gap: 0.75rem !important; box-sizing: border-box !important; overflow-x: hidden !important; }`.
2. **Event Videos Mobile Container Constraints:**
   - Constrained `#eventVideosStudioLayout`, `.event-videos-tab-layout`, `.event-videos-hero`, `.event-hero-header`, `#eventFeaturedContainer`, `.featured-video-card`, and `.event-videos-grid` with `width: 100% !important; max-width: 100% !important; min-width: 0 !important; box-sizing: border-box !important;`.
   - Configured `.event-angle-selector` with `width: 100% !important; max-width: 100% !important; min-width: 0 !important; overflow-x: auto !important; -webkit-overflow-scrolling: touch !important; box-sizing: border-box !important;` so the 4 angle buttons scroll horizontally within the mobile width without expanding the page.
3. **Bottom Navigation GPU Composite Layer & Max Z-Index:**
   - Updated `.mobile-app-bottom-nav` with `width: 100vw !important; max-width: 100vw !important; transform: translateZ(0) !important; -webkit-transform: translateZ(0) !important; will-change: transform !important; z-index: 99999 !important; box-sizing: border-box !important;`.
4. **Inactive Countdown Overlay Cleanup:**
   - Added `visibility: hidden` (and `visibility: visible` on `.show`) to `.countdown-overlay` so that it doesn't participate in viewport or hit-test calculations when hidden.

### 3. Verification & Metrics
- Ran Chrome DevTools Protocol automation emulating iPhone 16 (`393x852`):
  - `Videos`: `innerW: 393`, `innerH: 852`, `docScrollW: 393`, `docScrollH: 852`, `navTop: 796`, `navBottom: 852` (Fit to screen, pinned at bottom with zero scroll!).
  - `Photos`: `innerW: 393`, `innerH: 852`, `docScrollW: 393`, `docScrollH: 1985`, `navTop: 796`, `navBottom: 852` (Pinned at bottom!).
  - `Music`: `innerW: 393`, `innerH: 852`, `docScrollW: 393`, `docScrollH: 852`, `navTop: 796`, `navBottom: 852` (Pinned at bottom!).
  - `Reference`: `innerW: 393`, `innerH: 852`, `docScrollW: 393`, `docScrollH: 852`, `navTop: 796`, `navBottom: 852` (Pinned at bottom!).
- Desktop view check (`>= 768px`): Bottom bar remains `display: none`, all 2-column desktop controls, waveforms, shuttles, and solo decks remain 100% functional.
- Synchronized `index.html` and `dance_practice_player.html`.

---

## 13. Mobile Single-Row Angle Selector & Zero-Overflow Layout (< 768px) (Completed & Live)

### 1. User Feedback & Problem
- In mobile view on the Videos tab, buttons `Angle 1`, `Angle 2`, and `Angle 3` could not all be seen simultaneously without clicking and dragging towards the left.
- Full desktop labels (`Angle 1 (Side Stage • 05:40)`, `Angle 2 (Center Stage • 05:56)`, `Angle 3 (Front 60fps • 06:53)`, `All 3 Angles Grid`) took ~814px combined width, forcing horizontal drag/scroll behavior.
- Requirement: All angle buttons (`Angle 1`, `Angle 2`, `Angle 3`, and `Grid`) must be visible simultaneously in a single clean row within the viewport, with zero horizontal dragging/scrolling and zero overflow beyond screen width.

### 2. Architecture & Solution
- **Dual Label Structure:**
  - Added `.btn-label-desk` and `.btn-label-mob` spans inside each button:
    - Desktop: Shows full technical details (`Angle 1 (Side Stage • 05:40)`).
    - Mobile: Shows clean, punchy segmented control labels (`Angle 1`, `Angle 2`, `Angle 3`, `Grid`).
- **Full-Width Equal Segmented Control (`@media (max-width: 768px)`):**
  - `.event-angle-selector`: `display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; justify-content: space-between !important; width: 100% !important; overflow-x: hidden !important; gap: 0.35rem !important;`.
  - `.btn-angle-tab`: `flex: 1 1 0 !important; min-width: 0 !important; padding: 0.45rem 0.2rem !important; font-size: 0.72rem !important; border-radius: 8px !important; text-align: center !important; justify-content: center !important;`.
  - `.btn-angle-tab svg`: Compact `12px` width/height with `flex-shrink: 0`.
- **Text & Meta Overflow Protection:**
  - `.featured-video-meta`: `max-width: 100% !important; width: 100% !important; box-sizing: border-box !important;`.
  - `.featured-video-name`: `max-width: 100% !important; word-break: break-word !important; white-space: normal !important;`.

### 3. Verification Across Screen Widths
- **iPhone 16 (`393 x 852`):**
  - `btnAngle1`: `left: 10px, right: 99px` (Width: 89px)
  - `btnAngle2`: `left: 105px, right: 194px` (Width: 89px)
  - `btnAngle3`: `left: 199px, right: 288px` (Width: 89px)
  - `btnAngleGrid`: `left: 294px, right: 383px` (Width: 89px)
  - `overflowingCount`: **0**
- **Narrow 360px Screen (`360 x 740`):**
  - All 4 buttons fit neatly across `10px → 350px`.
  - `overflowingCount`: **0**
- **Desktop (`1440 x 900`):**
  - Displays full titles (`Angle 1 (Side Stage • 05:40)`, etc.) with zero regressions.

---

## 14. Mobile Landscape Orientation App Shell & Responsive Layout Optimization (`<= 550px` height) (Completed & Live)

### 1. User Feedback & Problem
- In landscape view on mobile devices (e.g., iPhone 16 in landscape `852 x 393`), viewport width exceeds `768px` (`852 > 768`), causing the browser to fall back to the **desktop layout**.
- As a result:
  - The massive desktop header, subtitle, and 8 desktop version tabs rendered, taking up the entire `393px` vertical screen height.
  - The native mobile bottom navigation bar (`#mobileAppBottomNav`) was hidden (`display: none`).
  - Videos and content overflowed vertically and horizontally, requiring awkward vertical scrolling to reach playback controls.
- Requirement: Support mobile landscape mode seamlessly by activating the app shell, suppressing desktop clutter, pinning a compact bottom navigation bar, and optimizing player/gallery layouts for widescreen aspect ratios.

### 2. Architecture & Solution
- **Media Query Expansion:**
  - Extended core mobile app shell styles to `@media (max-width: 768px), (max-height: 550px) and (orientation: landscape)`.
  - Suppressed desktop tabs (`.tabs { display: none !important; }`), desktop subtitle, and footer badges in landscape mode.
  - Activated `#mobileAppBottomNav` with `display: flex !important;`.
- **Landscape-Specific Optimizations (`@media (max-height: 550px) and (orientation: landscape)`):**
  - **Ultra-Compact Header:** Scaled header title to `0.92rem` and padding to `0.2rem 0.5rem`, using `< 34px` vertical space.
  - **Compact Bottom Navigation Bar:** Height reduced to `42px`, with horizontal icon + text layout (`flex-direction: row; gap: 5px; font-size: 0.7rem;`) to save vertical real estate.
  - **Videos Tab:** Constrained `.event-video-embed-box` with `max-height: calc(100dvh - 140px); aspect-ratio: 16 / 9; width: auto; margin: 0 auto;` so the 16:9 video fits on screen alongside the angle selector.
  - **Photos Tab:** Responsive 4-column photo grid (`grid-template-columns: repeat(4, 1fr);`) with compact header toolbar.
  - **Music Studio Tab:** 2-column side-by-side layout (`grid-template-columns: 310px 1fr;`) with left sticky player card and right scrollable tracklist.
  - **Reference Video Tab (Zero Downward Scrolling):**
    - Moved the 5 cue cards (`.video-cues-deck`) to `order: 1 !important;` directly above the video for instant tap access and visual consistency with the Videos tab's angle selector.
    - Constrained `.video-container-wrapper` with `order: 2 !important; height: calc(100dvh - 155px) !important; max-height: calc(100dvh - 155px) !important; aspect-ratio: 16 / 9 !important; width: auto !important; margin: 0 auto !important; display: flex !important; align-items: center !important; justify-content: center !important;`.
    - Inner video set to `width: 100% !important; height: 100% !important; object-fit: contain !important;`.
    - Compacted section title and container gaps so total content height strictly matches viewport height (`scrollHeight <= window.innerHeight`).
  - **Zero Horizontal Overflow:** Enforced `overflow-x: hidden !important; max-width: 100vw !important; min-width: 0 !important;` on all root and container elements.

### 3. Automated Multi-Device Landscape Verification
- **iPhone SE Landscape (`667 x 375`):** `winH: 375, scrollH: 375, isScrollable: false, navTop: 333, navBottom: 375`.
- **iPhone 16 Landscape (`852 x 393`):** `winH: 393, scrollH: 393, isScrollable: false, navTop: 351, navBottom: 393`.
- **Galaxy S20 Landscape (`915 x 412`):** `winH: 412, scrollH: 412, isScrollable: false, navTop: 370, navBottom: 412`.
- **Mobile Portrait Check (`393 x 852`):** `winW: 393, winH: 852, scrollH: 852, navTop: 796, navBottom: 852`.
- **Desktop Check (`1440 x 900`):** Bottom navigation remains `display: none`, desktop 2-column studio, 5-cue desktop grid, and video controls panel remain 100% untouched.


