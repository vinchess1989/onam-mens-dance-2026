import os
import subprocess
import struct
import json
import re

base_dir = r"C:\Users\vinee\Video Editing"
ffmpeg = r"C:\Users\vinee\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin\ffmpeg.exe"

def extract_peaks(mp3_filename, num_points=3000):
    p = os.path.join(base_dir, mp3_filename)
    if not os.path.exists(p):
        print(f"Warning: File not found: {p}")
        return []
    cmd = [
        ffmpeg, "-hide_banner", "-v", "error",
        "-i", p,
        "-ac", "1",
        "-ar", "8000",
        "-f", "s16le",
        "-"
    ]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    raw = proc.stdout
    num_samples = len(raw) // 2
    if num_samples == 0:
        return []
    samples = struct.unpack(f"<{num_samples}h", raw)
    
    block_size = max(1, num_samples // num_points)
    peaks = []
    for i in range(num_points):
        start = i * block_size
        end = min(num_samples, start + block_size)
        if start >= num_samples:
            break
        bin_samples = samples[start:end]
        if bin_samples:
            m = max(abs(s) for s in bin_samples)
            peaks.append(round(m / 32768.0, 3))
        else:
            peaks.append(0.0)
            
    max_p = max(peaks) if peaks and max(peaks) > 0 else 1.0
    return [round(p / max_p, 3) for p in peaks]

print("Extracting ultra-high-density beat envelopes (3000 pts master, 600-1200 pts components)...")
manifest = {
    "master_260909": extract_peaks("onam_mens_final_26_0909.mp3", 3000),
    "master_260906": extract_peaks("onam_mens_final_26_0906.mp3", 3000),
    "comp-1": extract_peaks("Kalyanaraman (5m19s-5m29s).mp3", 600),
    "comp-2": extract_peaks("chettikulangara_only.mp3", 1000),
    "comp-pause-1": extract_peaks("cue_option1_sticks.mp3", 600),
    "comp-3": extract_peaks("Sablazki Dance Squad - Short.mp3", 800),
    "comp-4": extract_peaks("shanthamee rathri.mp3", 1000),
    "comp-5": extract_peaks("pondicherry dialogue.mp3", 600),
    "comp-pause-2": extract_peaks("cue_option1_sticks.mp3", 600),
    "comp-6": extract_peaks("ivalkoruvan song.mp3", 1000),
    "comp-7": extract_peaks("Njanondaliyanum (0m12s-1m06s).mp3", 1200),
    "comp-8": extract_peaks("Velmuruka Harohara (2m20s-3m03s).mp3", 1200),
    "comp-9": extract_peaks("Applause Crowd Cheering (0m00s-0m10s).mp3", 600),
}

wf_path = os.path.join(base_dir, "waveform_data.json")
with open(wf_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f)
print("Saved high-density waveform_data.json successfully!")
for k, v in manifest.items():
    print(f" - {k:15}: {len(v)} peak points")

index_path = os.path.join(base_dir, "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. CSS for Waveform Inspector Modal & Zoom Controls
css_inspector = """
    /* FULL-SCREEN WAVEFORM INSPECTOR & ZOOM ENGINE */
    .waveform-inspector-modal {
      position: fixed;
      inset: 0;
      z-index: 2500;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 1.5rem;
      animation: fadeInModal 0.2s ease;
    }

    @keyframes fadeInModal {
      from { opacity: 0; }
      to { opacity: 1; }
    }

    .inspector-backdrop {
      position: absolute;
      inset: 0;
      background: rgba(5, 8, 18, 0.88);
      backdrop-filter: blur(18px);
      -webkit-backdrop-filter: blur(18px);
    }

    .inspector-window {
      position: relative;
      z-index: 10;
      width: 100%;
      max-width: 1440px;
      background: rgba(15, 23, 42, 0.95);
      border: 1px solid rgba(245, 158, 11, 0.35);
      border-radius: var(--radius-lg);
      box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.8), 0 0 35px rgba(245, 158, 11, 0.15);
      display: flex;
      flex-direction: column;
      gap: 0.85rem;
      padding: 1.5rem 1.75rem;
      overflow: hidden;
    }

    .inspector-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      flex-wrap: wrap;
      padding-bottom: 0.65rem;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }

    .inspector-header-left {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      flex-wrap: wrap;
    }

    .inspector-badge {
      font-size: 0.75rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      padding: 0.2rem 0.65rem;
      border-radius: 999px;
      background: rgba(245, 158, 11, 0.15);
      border: 1px solid rgba(245, 158, 11, 0.35);
      color: #fbbf24;
    }

    .inspector-title {
      font-size: 1.35rem;
      font-weight: 700;
      color: #fff;
    }

    .inspector-time-pill {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.9rem;
      font-weight: 700;
      color: #38bdf8;
      background: rgba(0, 0, 0, 0.35);
      padding: 0.2rem 0.6rem;
      border-radius: 6px;
      border: 1px solid rgba(56, 189, 248, 0.3);
    }

    .inspector-header-controls {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      flex-wrap: wrap;
    }

    .zoom-pill-group {
      display: flex;
      align-items: center;
      gap: 0.25rem;
      background: rgba(0, 0, 0, 0.4);
      padding: 0.25rem 0.4rem;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border-glass);
    }

    .zoom-label {
      font-size: 0.75rem;
      font-weight: 700;
      color: #94a3b8;
      margin: 0 0.4rem;
      text-transform: uppercase;
    }

    .btn-zoom-preset {
      background: transparent;
      border: none;
      color: #cbd5e1;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.75rem;
      font-weight: 700;
      padding: 0.25rem 0.5rem;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.15s ease;
    }

    .btn-zoom-preset:hover {
      background: rgba(255, 255, 255, 0.1);
      color: #fff;
    }

    .btn-zoom-preset.active {
      background: #fbbf24;
      color: #090c15;
      font-weight: 800;
    }

    .btn-zoom-step {
      width: 26px;
      height: 26px;
      border-radius: 4px;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--border-glass);
      color: #fff;
      font-size: 0.95rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.15s ease;
    }

    .btn-zoom-step:hover {
      background: rgba(245, 158, 11, 0.25);
      border-color: #fbbf24;
      color: #fbbf24;
    }

    .btn-inspector-close {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--border-glass);
      color: #e2e8f0;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .btn-inspector-close:hover {
      background: rgba(239, 68, 68, 0.25);
      border-color: rgba(239, 68, 68, 0.5);
      color: #f87171;
      transform: scale(1.08);
    }

    .inspector-hint-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      font-size: 0.76rem;
      color: #94a3b8;
      background: rgba(0, 0, 0, 0.25);
      padding: 0.35rem 0.75rem;
      border-radius: 6px;
      flex-wrap: wrap;
    }

    .inspector-canvas-wrapper {
      display: flex;
      flex-direction: column;
      width: 100%;
      background: rgba(10, 15, 30, 0.9);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: var(--radius-md);
      overflow: hidden;
      box-shadow: inset 0 2px 14px rgba(0, 0, 0, 0.6);
    }

    #inspectorRulerCanvas {
      width: 100%;
      height: 24px;
      display: block;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      background: rgba(15, 23, 42, 0.5);
    }

    .inspector-main-canvas-box {
      position: relative;
      width: 100%;
      height: 250px;
      cursor: crosshair;
      user-select: none;
    }

    #inspectorWaveformCanvas {
      width: 100%;
      height: 100%;
      display: block;
    }

    .inspector-playhead {
      position: absolute;
      top: 0;
      bottom: 0;
      width: 2px;
      background: #ffffff;
      box-shadow: 0 0 10px #ffffff, 0 0 4px var(--primary);
      pointer-events: none;
      transform: translateX(-50%);
      left: 0%;
      z-index: 10;
    }

    .inspector-playhead-tag {
      position: absolute;
      top: 4px;
      transform: translateX(-50%);
      background: #fbbf24;
      color: #090c15;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.7rem;
      font-weight: 800;
      padding: 0.1rem 0.35rem;
      border-radius: 4px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.4);
      white-space: nowrap;
    }

    .inspector-hover-line {
      position: absolute;
      top: 0;
      bottom: 0;
      width: 1px;
      background: rgba(56, 189, 248, 0.75);
      pointer-events: none;
      transform: translateX(-50%);
      display: none;
      z-index: 8;
    }

    .inspector-hover-tooltip {
      position: absolute;
      top: 6px;
      transform: translateX(-50%);
      background: rgba(0, 0, 0, 0.9);
      border: 1px solid #38bdf8;
      color: #38bdf8;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.75rem;
      font-weight: 700;
      padding: 0.15rem 0.5rem;
      border-radius: 4px;
      white-space: nowrap;
      pointer-events: none;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.6);
    }

    .inspector-hover-tooltip.is-beat {
      border-color: #fbbf24;
      color: #fbbf24;
      background: rgba(20, 15, 5, 0.92);
      box-shadow: 0 0 12px rgba(245, 158, 11, 0.4);
    }

    /* MINIMAP OVERVIEW */
    .inspector-minimap-container {
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
      width: 100%;
    }

    .minimap-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.7rem;
      font-family: 'JetBrains Mono', monospace;
      color: #94a3b8;
      font-weight: 700;
      text-transform: uppercase;
    }

    .inspector-minimap-box {
      position: relative;
      width: 100%;
      height: 40px;
      background: rgba(10, 15, 30, 0.75);
      border: 1px solid var(--border-glass);
      border-radius: var(--radius-sm);
      overflow: hidden;
      cursor: pointer;
    }

    #inspectorMinimapCanvas {
      width: 100%;
      height: 100%;
      display: block;
    }

    .inspector-minimap-viewport {
      position: absolute;
      top: 0;
      bottom: 0;
      left: 0%;
      width: 100%;
      background: rgba(245, 158, 11, 0.18);
      border: 1.5px solid #fbbf24;
      border-radius: 4px;
      box-shadow: 0 0 12px rgba(245, 158, 11, 0.25);
      cursor: grab;
    }

    .inspector-minimap-viewport:active {
      cursor: grabbing;
    }

    .inspector-minimap-playhead {
      position: absolute;
      top: 0;
      bottom: 0;
      width: 2px;
      background: #ffffff;
      transform: translateX(-50%);
      left: 0%;
      pointer-events: none;
      z-index: 5;
    }

    /* TRANSPORT BAR */
    .inspector-transport-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      background: rgba(0, 0, 0, 0.35);
      padding: 0.65rem 1rem;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border-glass);
      flex-wrap: wrap;
    }

    .transport-left {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    .btn-transport-play {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
      border: none;
      color: #090c15;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 1.1rem;
      font-weight: 800;
      box-shadow: 0 2px 10px rgba(245, 158, 11, 0.4);
      transition: all 0.2s ease;
    }

    .btn-transport-play:hover {
      transform: scale(1.08);
    }

    .transport-time {
      font-family: 'JetBrains Mono', monospace;
      display: flex;
      align-items: baseline;
      gap: 0.35rem;
    }

    .transport-cur-time {
      font-size: 1.15rem;
      font-weight: 800;
      color: #fbbf24;
    }

    .transport-total-time {
      font-size: 0.85rem;
      color: #94a3b8;
      font-weight: 600;
    }

    .transport-nudges {
      display: flex;
      align-items: center;
      gap: 0.35rem;
      flex-wrap: wrap;
    }

    .btn-inspect-expand {
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      background: rgba(245, 158, 11, 0.15);
      border: 1px solid rgba(245, 158, 11, 0.35);
      color: #fbbf24;
      font-size: 0.72rem;
      font-weight: 700;
      padding: 0.2rem 0.55rem;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.15s ease;
      text-decoration: none;
    }

    .btn-inspect-expand:hover {
      background: rgba(245, 158, 11, 0.3);
      color: #fff;
      transform: translateY(-1px);
    }
"""

if "/* FULL-SCREEN WAVEFORM INSPECTOR & ZOOM ENGINE */" not in html:
    html = html.replace("  </style>", css_inspector + "\n  </style>", 1)

# 2. Update Master Waveform Header with "⛶ Inspect Full Width & Zoom" button
master_wf_title_target = """      <div class="waveform-panel-title">
        <span>📊 Beat Transient & Audio Waveform (Click to Seek 0.01s)</span>
        <span style="color:#fbbf24; font-size:0.7rem;">⚡ Spikes = Beat Drops & Clave Clicks</span>
      </div>"""

master_wf_title_replacement = """      <div class="waveform-panel-title">
        <div style="display:flex; align-items:center; gap:0.5rem;">
          <span>📊 Beat Transient & Audio Waveform</span>
          <button class="btn-inspect-expand" onclick="openWaveformInspector('master')" title="Inspect waveform across full screen with up to 16x zoom">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"/></svg>
            <span>⛶ Inspect Full Width & Zoom</span>
          </button>
        </div>
        <span style="color:#fbbf24; font-size:0.7rem;">⚡ Spikes = Beat Drops & Clave Clicks</span>
      </div>"""

if master_wf_title_target in html:
    html = html.replace(master_wf_title_target, master_wf_title_replacement)

# 3. Update Component Deck Header with "⛶ Inspect & Zoom" button
comp_wf_header_target = """                <div class="comp-waveform-header">
                  <span>Waveform & Beat Transients</span>
                  <span style="color:${comp.color};">Click graph to seek</span>
                </div>"""

comp_wf_header_replacement = """                <div class="comp-waveform-header">
                  <div style="display:flex; align-items:center; gap:0.45rem;">
                    <span>Waveform & Beat Transients</span>
                    <button class="btn-inspect-expand" onclick="openWaveformInspector('comp', '${comp.id}')" title="Inspect this component waveform across full screen with up to 16x zoom">
                      <svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor"><path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"/></svg>
                      <span>⛶ Inspect & Zoom</span>
                    </button>
                  </div>
                  <span style="color:${comp.color};">Click graph to seek</span>
                </div>"""

if comp_wf_header_target in html:
    html = html.replace(comp_wf_header_target, comp_wf_header_replacement)

# 4. Insert Modal HTML right before </body>
modal_html = """  <!-- FULL-SCREEN WAVEFORM INSPECTOR MODAL WITH MULTI-LEVEL ZOOM (1x to 16x) -->
  <div id="waveformInspectorModal" class="waveform-inspector-modal" role="dialog" aria-modal="true" style="display: none;">
    <div class="inspector-backdrop" onclick="closeWaveformInspector()"></div>
    <div class="inspector-window">
      <!-- Header -->
      <div class="inspector-header">
        <div class="inspector-header-left">
          <span class="inspector-badge" id="inspectorTrackBadge">Master Controller</span>
          <h2 class="inspector-title" id="inspectorTrackTitle">Final Mix 260909 (Full Routine)</h2>
          <span class="inspector-time-pill" id="inspectorTimeReadout">00:00.00 / 04:12.66</span>
        </div>
        <div class="inspector-header-controls">
          <div class="zoom-pill-group">
            <span class="zoom-label">Zoom:</span>
            <button class="btn-zoom-preset active" data-zoom="1">1x</button>
            <button class="btn-zoom-preset" data-zoom="2">2x</button>
            <button class="btn-zoom-preset" data-zoom="4">4x</button>
            <button class="btn-zoom-preset" data-zoom="8">8x</button>
            <button class="btn-zoom-preset" data-zoom="16">16x</button>
            <button class="btn-zoom-step" id="btnZoomOut" title="Zoom Out (-)">−</button>
            <button class="btn-zoom-step" id="btnZoomIn" title="Zoom In (+)">+</button>
          </div>
          <button class="btn-inspector-close" onclick="closeWaveformInspector()" title="Close Inspector (Esc)">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
          </button>
        </div>
      </div>

      <!-- Hint bar -->
      <div class="inspector-hint-bar">
        <span>💡 <b>Mouse Wheel</b> over waveform to Zoom In/Out • <b>Click</b> anywhere to Seek (0.01s Precision) • <b>Drag</b> to Pan when zoomed</span>
        <span id="inspectorBeatInfo" style="color: #fbbf24; font-weight: 700;">⚡ Amber Spikes = Drum Drops & Clave Beats</span>
      </div>

      <!-- Main Waveform & Ruler Area -->
      <div class="inspector-canvas-wrapper" id="inspectorCanvasWrapper">
        <canvas id="inspectorRulerCanvas" height="24"></canvas>
        <div class="inspector-main-canvas-box" id="inspectorMainBox">
          <canvas id="inspectorWaveformCanvas" height="250"></canvas>
          <div class="inspector-playhead" id="inspectorPlayhead">
            <div class="inspector-playhead-tag" id="inspectorPlayheadTag">00:00.00</div>
          </div>
          <div class="inspector-hover-line" id="inspectorHoverLine">
            <div class="inspector-hover-tooltip" id="inspectorHoverTooltip">00:00.00</div>
          </div>
        </div>
      </div>

      <!-- Minimap / Overview Strip -->
      <div class="inspector-minimap-container">
        <div class="minimap-header">
          <span>TRACK OVERVIEW (Full Duration)</span>
          <span id="inspectorVisibleRangeText">Viewing: 00:00.00 - 04:12.66 (100%)</span>
        </div>
        <div class="inspector-minimap-box" id="inspectorMinimapBox">
          <canvas id="inspectorMinimapCanvas" height="40"></canvas>
          <div class="inspector-minimap-viewport" id="inspectorMinimapViewport"></div>
          <div class="inspector-minimap-playhead" id="inspectorMinimapPlayhead"></div>
        </div>
      </div>

      <!-- Playback & Micro-Nudge Transport -->
      <div class="inspector-transport-bar">
        <div class="transport-left">
          <button class="btn-transport-play" id="inspectorBtnPlay" title="Play/Pause (Space)">▶</button>
          <div class="transport-time">
            <span class="transport-cur-time" id="inspectorTransportTime">00:00.00</span>
            <span class="transport-total-time" id="inspectorTransportTotal">/ 04:12.66</span>
          </div>
        </div>

        <div class="transport-nudges">
          <span style="font-size:0.75rem; color:#94a3b8; font-weight:700; margin-right:4px;">NUDGE:</span>
          <button class="btn-nudge" onclick="inspectorNudge(-1.00)">-1.0s</button>
          <button class="btn-nudge" onclick="inspectorNudge(-0.10)">-0.1s</button>
          <button class="btn-nudge fine" onclick="inspectorNudge(-0.01)">-0.01s</button>
          <button class="btn-nudge fine" onclick="inspectorNudge(0.01)">+0.01s</button>
          <button class="btn-nudge" onclick="inspectorNudge(0.10)">+0.1s</button>
          <button class="btn-nudge" onclick="inspectorNudge(1.00)">+1.0s</button>
        </div>

        <div class="transport-right" id="inspectorExtraActions">
          <!-- Dynamic action button (e.g. Sync to Mix) -->
        </div>
      </div>
    </div>
  </div>
"""

if '<div id="waveformInspectorModal"' not in html:
    html = html.replace("</body>", modal_html + "\n</body>", 1)

# 5. Inject WAVEFORM_DATA updated JSON
wf_json_str = json.dumps(manifest)
html = re.sub(
    r"const WAVEFORM_DATA\s*=\s*\{.*?\};\n",
    f"const WAVEFORM_DATA = {wf_json_str};\n",
    html,
    flags=re.DOTALL
)

# 6. JavaScript Inspector Engine
inspector_engine_js = """
    // =========================================================================
    // FULL-SCREEN WAVEFORM INSPECTOR & MULTI-LEVEL ZOOM ENGINE (1x to 16x)
    // =========================================================================
    const inspectorState = {
      isOpen: false,
      sourceType: 'master', // 'master' or 'comp'
      compId: null,
      peaks: [],
      duration: 0,
      color: '#fbbf24',
      title: '',
      audioEl: null,
      zoomLevel: 1.0, // 1.0, 2.0, 4.0, 8.0, 16.0
      panRatio: 0.0,  // 0.0 to (1.0 - 1.0 / zoomLevel)
      isDraggingPan: false,
      dragStartX: 0,
      dragStartPan: 0,
      isDraggingMinimap: false,
      animFrameId: null
    };

    function openWaveformInspector(sourceType, compId = null) {
      inspectorState.sourceType = sourceType;
      inspectorState.compId = compId;
      inspectorState.zoomLevel = 1.0;
      inspectorState.panRatio = 0.0;
      inspectorState.isOpen = true;

      const modal = document.getElementById('waveformInspectorModal');
      const badge = document.getElementById('inspectorTrackBadge');
      const title = document.getElementById('inspectorTrackTitle');
      const extraActions = document.getElementById('inspectorExtraActions');

      if (sourceType === 'master') {
        inspectorState.peaks = (currentRoutineKey === 'final260909') ? WAVEFORM_DATA.master_260909 : (WAVEFORM_DATA.master_260906 || WAVEFORM_DATA.master_260909);
        inspectorState.duration = activeRoutine.totalDuration;
        inspectorState.color = '#818cf8';
        inspectorState.title = `${activeRoutine.name} (Full Routine)`;
        inspectorState.audioEl = audio;

        badge.textContent = 'Master Controller';
        badge.style.background = 'rgba(245, 158, 11, 0.15)';
        badge.style.borderColor = 'rgba(245, 158, 11, 0.35)';
        badge.style.color = '#fbbf24';
        title.textContent = inspectorState.title;
        extraActions.innerHTML = '';
      } else {
        const comp = COMPONENT_TRACKS.find(c => c.id === compId);
        if (!comp) return;
        inspectorState.peaks = WAVEFORM_DATA[compId] || [];
        inspectorState.duration = comp.duration;
        inspectorState.color = comp.color;
        inspectorState.title = `${comp.title} (${comp.badge})`;
        inspectorState.audioEl = compAudioElements[compId];

        badge.textContent = `Component Track • Part ${comp.part}`;
        badge.style.background = 'rgba(56, 189, 248, 0.15)';
        badge.style.borderColor = 'rgba(56, 189, 248, 0.35)';
        badge.style.color = '#38bdf8';
        title.textContent = inspectorState.title;
        extraActions.innerHTML = `
          <button class="btn-comp-action btn-comp-sync" onclick="syncComponentToMaster('${comp.id}')" title="Sync & seek master mix to current timepoint">
            <span>⚡ Sync to Master Mix</span>
          </button>
        `;
      }

      modal.style.display = 'flex';
      updateZoomButtonsUI();
      updateInspectorTransportUI();

      setTimeout(() => {
        renderInspectorRuler();
        renderInspectorWaveform();
        renderInspectorMinimap();
      }, 50);

      startInspectorLoop();
    }

    function closeWaveformInspector() {
      inspectorState.isOpen = false;
      const modal = document.getElementById('waveformInspectorModal');
      modal.style.display = 'none';
      if (inspectorState.animFrameId) {
        cancelAnimationFrame(inspectorState.animFrameId);
        inspectorState.animFrameId = null;
      }
    }

    function setInspectorZoom(zoom, centerRatio = 0.5) {
      const oldZoom = inspectorState.zoomLevel;
      const newZoom = Math.max(1.0, Math.min(16.0, zoom));
      if (newZoom === oldZoom && newZoom !== 1.0) return;

      // Maintain center anchor
      const visibleFractionOld = 1.0 / oldZoom;
      const visibleFractionNew = 1.0 / newZoom;
      const currentCenter = inspectorState.panRatio + (visibleFractionOld * centerRatio);
      let newPan = currentCenter - (visibleFractionNew * centerRatio);
      newPan = Math.max(0.0, Math.min(1.0 - visibleFractionNew, newPan));

      inspectorState.zoomLevel = newZoom;
      inspectorState.panRatio = (newZoom === 1.0) ? 0.0 : newPan;

      updateZoomButtonsUI();
      renderInspectorRuler();
      renderInspectorWaveform();
      renderInspectorMinimap();
    }

    function updateZoomButtonsUI() {
      document.querySelectorAll('.btn-zoom-preset').forEach(btn => {
        const z = parseFloat(btn.dataset.zoom);
        btn.classList.toggle('active', Math.abs(z - inspectorState.zoomLevel) < 0.01);
      });
    }

    function updateInspectorTransportUI() {
      const cur = inspectorState.audioEl ? inspectorState.audioEl.currentTime : 0;
      const total = inspectorState.duration;
      const btnPlay = document.getElementById('inspectorBtnPlay');
      const readout = document.getElementById('inspectorTimeReadout');
      const curReadout = document.getElementById('inspectorTransportTime');
      const totalReadout = document.getElementById('inspectorTransportTotal');

      if (readout) readout.textContent = `${formatTimePrecise(cur)} / ${formatTimePrecise(total)}`;
      if (curReadout) curReadout.textContent = formatTimePrecise(cur);
      if (totalReadout) totalReadout.textContent = `/ ${formatTimePrecise(total)}`;

      if (btnPlay) {
        const isPaused = inspectorState.audioEl ? inspectorState.audioEl.paused : true;
        btnPlay.textContent = isPaused ? '▶' : '⏸';
      }
    }

    function inspectorNudge(delta) {
      if (!inspectorState.audioEl) return;
      const cur = inspectorState.audioEl.currentTime;
      const target = Math.max(0, Math.min(inspectorState.duration, cur + delta));
      inspectorState.audioEl.currentTime = parseFloat(target.toFixed(2));
      updateInspectorTransportUI();
      renderInspectorWaveform();
      renderInspectorMinimap();

      if (inspectorState.sourceType === 'master') {
        seekToPrecise(target);
      } else if (inspectorState.compId) {
        nudgeComponent(inspectorState.compId, 0);
      }
    }

    function startInspectorLoop() {
      function loop() {
        if (!inspectorState.isOpen) return;
        if (inspectorState.audioEl && !inspectorState.audioEl.paused) {
          updateInspectorTransportUI();
          renderInspectorWaveformPlayhead();
          renderInspectorMinimapPlayhead();
        }
        inspectorState.animFrameId = requestAnimationFrame(loop);
      }
      inspectorState.animFrameId = requestAnimationFrame(loop);
    }

    // =========================================================================
    // INSPECTOR CANVAS RENDERERS
    // =========================================================================
    function renderInspectorRuler() {
      const canvas = document.getElementById('inspectorRulerCanvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const dpr = window.devicePixelRatio || 1;
      const w = Math.floor(canvas.offsetWidth || canvas.parentElement.clientWidth || 1200);
      const h = Math.floor(canvas.offsetHeight || 24);

      if (canvas.width !== w * dpr || canvas.height !== h * dpr) {
        canvas.width = w * dpr;
        canvas.height = h * dpr;
      }
      ctx.save();
      ctx.scale(dpr, dpr);
      ctx.clearRect(0, 0, w, h);

      const totalDur = inspectorState.duration;
      if (totalDur <= 0) { ctx.restore(); return; }

      const visibleFraction = 1.0 / inspectorState.zoomLevel;
      const startT = inspectorState.panRatio * totalDur;
      const endT = startT + visibleFraction * totalDur;
      const visibleDur = endT - startT;

      // Determine tick intervals
      let majorStep = 10;
      let minorStep = 2;
      if (visibleDur <= 5) { majorStep = 0.5; minorStep = 0.1; }
      else if (visibleDur <= 15) { majorStep = 1; minorStep = 0.25; }
      else if (visibleDur <= 30) { majorStep = 2; minorStep = 0.5; }
      else if (visibleDur <= 60) { majorStep = 5; minorStep = 1; }
      else if (visibleDur <= 120) { majorStep = 10; minorStep = 2; }
      else { majorStep = 30; minorStep = 5; }

      ctx.fillStyle = '#94a3b8';
      ctx.font = '9px "JetBrains Mono", monospace';
      ctx.textAlign = 'left';
      ctx.textBaseline = 'middle';

      const firstMinor = Math.floor(startT / minorStep) * minorStep;
      for (let t = firstMinor; t <= endT; t += minorStep) {
        if (t < startT) continue;
        const x = ((t - startT) / visibleDur) * w;
        const isMajor = Math.abs(t % majorStep) < (minorStep * 0.4) || Math.abs((t % majorStep) - majorStep) < (minorStep * 0.4);

        ctx.strokeStyle = isMajor ? 'rgba(255, 255, 255, 0.4)' : 'rgba(255, 255, 255, 0.15)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(x, isMajor ? 0 : 8);
        ctx.lineTo(x, h);
        ctx.stroke();

        if (isMajor && x + 40 < w) {
          ctx.fillText(formatTimePrecise(t), x + 4, 10);
        }
      }

      ctx.restore();
    }

    function renderInspectorWaveform() {
      const canvas = document.getElementById('inspectorWaveformCanvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const dpr = window.devicePixelRatio || 1;
      const w = Math.floor(canvas.offsetWidth || canvas.parentElement.clientWidth || 1200);
      const h = Math.floor(canvas.offsetHeight || 250);

      if (canvas.width !== w * dpr || canvas.height !== h * dpr) {
        canvas.width = w * dpr;
        canvas.height = h * dpr;
      }
      ctx.save();
      ctx.scale(dpr, dpr);
      ctx.clearRect(0, 0, w, h);

      const peaks = inspectorState.peaks;
      const totalDur = inspectorState.duration;
      if (!peaks || peaks.length === 0 || totalDur <= 0) { ctx.restore(); return; }

      const visibleFraction = 1.0 / inspectorState.zoomLevel;
      const startT = inspectorState.panRatio * totalDur;
      const endT = startT + visibleFraction * totalDur;
      const visibleDur = endT - startT;

      const centerY = h / 2;

      // Center baseline guide
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(0, centerY);
      ctx.lineTo(w, centerY);
      ctx.stroke();

      // Section markers for master mix
      if (inspectorState.sourceType === 'master' && activeRoutine && activeRoutine.sections) {
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
        ctx.setLineDash([3, 3]);
        activeRoutine.sections.forEach(sec => {
          const tStart = (sec.timelineStart !== undefined) ? sec.timelineStart : sec.start;
          if (tStart >= startT && tStart <= endT) {
            const secX = ((tStart - startT) / visibleDur) * w;
            ctx.beginPath();
            ctx.moveTo(secX, 0);
            ctx.lineTo(secX, h);
            ctx.stroke();

            // Label
            ctx.fillStyle = sec.color;
            ctx.font = 'bold 10px "Plus Jakarta Sans", sans-serif';
            ctx.fillText(sec.title, secX + 4, 18);
          }
        });
        ctx.setLineDash([]);
      }

      // Slice the visible peaks
      const startPeakIdx = Math.floor(inspectorState.panRatio * peaks.length);
      const endPeakIdx = Math.min(peaks.length, Math.ceil((inspectorState.panRatio + visibleFraction) * peaks.length));
      const visiblePeaks = peaks.slice(startPeakIdx, endPeakIdx);

      const barCount = visiblePeaks.length;
      const barWidth = w / Math.max(1, barCount);
      const gap = Math.max(0.3, barWidth * 0.18);
      const actualBarWidth = Math.max(1, barWidth - gap);

      const curTime = inspectorState.audioEl ? inspectorState.audioEl.currentTime : 0;
      const progressX = ((curTime - startT) / visibleDur) * w;

      for (let i = 0; i < barCount; i++) {
        const x = i * barWidth;
        const peak = visiblePeaks[i];
        const barHeight = Math.max(3, peak * (h * 0.86));
        const topY = centerY - barHeight / 2;

        const isPlayed = x <= progressX;
        const isBeat = peak >= 0.50;

        if (isBeat) {
          ctx.fillStyle = isPlayed ? '#fbbf24' : 'rgba(245, 158, 11, 0.8)';
          ctx.fillRect(x, topY, actualBarWidth, barHeight);

          // Glowing top beat cap
          ctx.fillStyle = isPlayed ? '#ffffff' : '#fbbf24';
          const dotW = Math.min(actualBarWidth, 4);
          ctx.fillRect(x + (actualBarWidth - dotW) / 2, Math.max(2, topY - 3.5), dotW, 3);
        } else {
          ctx.fillStyle = isPlayed ? inspectorState.color : 'rgba(148, 163, 184, 0.35)';
          ctx.fillRect(x, topY, actualBarWidth, barHeight);
        }
      }

      ctx.restore();
      renderInspectorWaveformPlayhead();
    }

    function renderInspectorWaveformPlayhead() {
      const playhead = document.getElementById('inspectorPlayhead');
      const tag = document.getElementById('inspectorPlayheadTag');
      if (!playhead || !inspectorState.audioEl) return;

      const curTime = inspectorState.audioEl.currentTime;
      const totalDur = inspectorState.duration;
      const visibleFraction = 1.0 / inspectorState.zoomLevel;
      const startT = inspectorState.panRatio * totalDur;
      const endT = startT + visibleFraction * totalDur;
      const visibleDur = endT - startT;

      if (curTime >= startT && curTime <= endT && visibleDur > 0) {
        const ratio = (curTime - startT) / visibleDur;
        playhead.style.display = 'block';
        playhead.style.left = `${ratio * 100}%`;
        if (tag) tag.textContent = formatTimePrecise(curTime);
      } else {
        playhead.style.display = 'none';
      }
    }

    function renderInspectorMinimap() {
      const canvas = document.getElementById('inspectorMinimapCanvas');
      const viewport = document.getElementById('inspectorMinimapViewport');
      const rangeText = document.getElementById('inspectorVisibleRangeText');
      if (!canvas || !viewport) return;

      const ctx = canvas.getContext('2d');
      const dpr = window.devicePixelRatio || 1;
      const w = Math.floor(canvas.offsetWidth || canvas.parentElement.clientWidth || 1200);
      const h = Math.floor(canvas.offsetHeight || 40);

      if (canvas.width !== w * dpr || canvas.height !== h * dpr) {
        canvas.width = w * dpr;
        canvas.height = h * dpr;
      }
      ctx.save();
      ctx.scale(dpr, dpr);
      ctx.clearRect(0, 0, w, h);

      const peaks = inspectorState.peaks;
      if (peaks && peaks.length > 0) {
        const barCount = Math.min(peaks.length, 300);
        const step = peaks.length / barCount;
        const barWidth = w / barCount;
        const centerY = h / 2;

        for (let i = 0; i < barCount; i++) {
          const peak = peaks[Math.floor(i * step)];
          const barHeight = Math.max(2, peak * (h * 0.8));
          const topY = centerY - barHeight / 2;
          ctx.fillStyle = (peak >= 0.50) ? '#f59e0b' : 'rgba(148, 163, 184, 0.4)';
          ctx.fillRect(i * barWidth, topY, Math.max(1, barWidth - 0.5), barHeight);
        }
      }
      ctx.restore();

      // Viewport rectangle
      const visibleFraction = 1.0 / inspectorState.zoomLevel;
      viewport.style.left = `${inspectorState.panRatio * 100}%`;
      viewport.style.width = `${visibleFraction * 100}%`;

      const totalDur = inspectorState.duration;
      const startT = inspectorState.panRatio * totalDur;
      const endT = startT + visibleFraction * totalDur;
      const pct = Math.round(visibleFraction * 100);
      if (rangeText) {
        rangeText.textContent = `Viewing: ${formatTimePrecise(startT)} - ${formatTimePrecise(endT)} (${pct}% • ${inspectorState.zoomLevel}x)`;
      }

      renderInspectorMinimapPlayhead();
    }

    function renderInspectorMinimapPlayhead() {
      const playhead = document.getElementById('inspectorMinimapPlayhead');
      if (!playhead || !inspectorState.audioEl || inspectorState.duration <= 0) return;
      const ratio = inspectorState.audioEl.currentTime / inspectorState.duration;
      playhead.style.left = `${Math.min(100, Math.max(0, ratio * 100))}%`;
    }

    // =========================================================================
    // INSPECTOR INTERACTION HANDLERS (SEEK, PAN, ZOOM, MINIMAP)
    // =========================================================================
    function setupInspectorInteractions() {
      const mainBox = document.getElementById('inspectorMainBox');
      const hoverLine = document.getElementById('inspectorHoverLine');
      const hoverTooltip = document.getElementById('inspectorHoverTooltip');
      const minimapBox = document.getElementById('inspectorMinimapBox');
      const btnPlay = document.getElementById('inspectorBtnPlay');

      // 1. Play / Pause Transport Button
      if (btnPlay) {
        btnPlay.addEventListener('click', () => {
          if (!inspectorState.audioEl) return;
          if (inspectorState.audioEl.paused) {
            inspectorState.audioEl.play().catch(() => {});
          } else {
            inspectorState.audioEl.pause();
          }
          updateInspectorTransportUI();
        });
      }

      // 2. Zoom Buttons
      document.querySelectorAll('.btn-zoom-preset').forEach(btn => {
        btn.addEventListener('click', () => {
          const z = parseFloat(btn.dataset.zoom);
          setInspectorZoom(z);
        });
      });

      document.getElementById('btnZoomIn').addEventListener('click', () => {
        setInspectorZoom(inspectorState.zoomLevel * 1.5);
      });

      document.getElementById('btnZoomOut').addEventListener('click', () => {
        setInspectorZoom(inspectorState.zoomLevel / 1.5);
      });

      // 3. Mouse Wheel Zoom (Centered at mouse cursor position!)
      if (mainBox) {
        mainBox.addEventListener('wheel', (e) => {
          e.preventDefault();
          const rect = mainBox.getBoundingClientRect();
          const cursorRatio = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
          const factor = e.deltaY < 0 ? 1.25 : 0.8;
          setInspectorZoom(inspectorState.zoomLevel * factor, cursorRatio);
        }, { passive: false });

        // Hover Line & Beat Tooltip
        mainBox.addEventListener('mousemove', (e) => {
          if (inspectorState.isDraggingPan) {
            const dx = e.clientX - inspectorState.dragStartX;
            const rect = mainBox.getBoundingClientRect();
            const visibleFraction = 1.0 / inspectorState.zoomLevel;
            const deltaRatio = -(dx / rect.width) * visibleFraction;
            let newPan = inspectorState.dragStartPan + deltaRatio;
            newPan = Math.max(0.0, Math.min(1.0 - visibleFraction, newPan));
            inspectorState.panRatio = newPan;
            renderInspectorRuler();
            renderInspectorWaveform();
            renderInspectorMinimap();
            return;
          }

          const rect = mainBox.getBoundingClientRect();
          const cursorXRatio = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
          const visibleFraction = 1.0 / inspectorState.zoomLevel;
          const startT = inspectorState.panRatio * inspectorState.duration;
          const endT = startT + visibleFraction * inspectorState.duration;
          const hoverTime = startT + cursorXRatio * (endT - startT);

          hoverLine.style.display = 'block';
          hoverLine.style.left = `${cursorXRatio * 100}%`;

          // Detect beat peak under cursor
          const peaks = inspectorState.peaks;
          const totalFraction = inspectorState.panRatio + cursorXRatio * visibleFraction;
          const peakIdx = Math.floor(totalFraction * (peaks ? peaks.length : 1));
          const isBeat = peaks && peaks[peakIdx] >= 0.50;

          if (isBeat) {
            hoverTooltip.innerHTML = `⚡ BEAT: ${formatTimePrecise(hoverTime)}`;
            hoverTooltip.classList.add('is-beat');
          } else {
            hoverTooltip.innerHTML = formatTimePrecise(hoverTime);
            hoverTooltip.classList.remove('is-beat');
          }
        });

        mainBox.addEventListener('mouseleave', () => {
          if (!inspectorState.isDraggingPan) {
            hoverLine.style.display = 'none';
          }
        });

        // Click to Seek (0.01s Precision)
        mainBox.addEventListener('mousedown', (e) => {
          if (e.button !== 0) return;
          inspectorState.isDraggingPan = true;
          inspectorState.dragStartX = e.clientX;
          inspectorState.dragStartPan = inspectorState.panRatio;
          mainBox.style.cursor = 'grabbing';
        });

        window.addEventListener('mouseup', (e) => {
          if (inspectorState.isDraggingPan) {
            const dist = Math.abs(e.clientX - inspectorState.dragStartX);
            inspectorState.isDraggingPan = false;
            mainBox.style.cursor = 'crosshair';

            // If mouse moved less than 4px, treat as a click to seek!
            if (dist < 4 && inspectorState.isOpen) {
              const rect = mainBox.getBoundingClientRect();
              if (e.clientX >= rect.left && e.clientX <= rect.right && e.clientY >= rect.top && e.clientY <= rect.bottom) {
                const cursorXRatio = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
                const visibleFraction = 1.0 / inspectorState.zoomLevel;
                const startT = inspectorState.panRatio * inspectorState.duration;
                const endT = startT + visibleFraction * inspectorState.duration;
                const targetTime = startT + cursorXRatio * (endT - startT);

                if (inspectorState.audioEl) {
                  inspectorState.audioEl.currentTime = parseFloat(targetTime.toFixed(2));
                  updateInspectorTransportUI();
                  renderInspectorWaveform();
                  renderInspectorMinimap();

                  if (inspectorState.sourceType === 'master') {
                    seekToPrecise(targetTime);
                  } else if (inspectorState.compId) {
                    const scrubber = document.getElementById(`compScrubber-${inspectorState.compId}`);
                    const timeText = document.getElementById(`compTimeReadout-${inspectorState.compId}`);
                    if (scrubber) scrubber.value = targetTime.toFixed(2);
                    if (timeText) timeText.textContent = formatTimePrecise(targetTime);
                    if (window.compWaveRenderers && window.compWaveRenderers[inspectorState.compId]) {
                      window.compWaveRenderers[inspectorState.compId]();
                    }
                  }
                }
              }
            }
          }
        });
      }

      // 4. Minimap Drag & Jump
      if (minimapBox) {
        minimapBox.addEventListener('click', (e) => {
          const rect = minimapBox.getBoundingClientRect();
          const clickRatio = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
          const visibleFraction = 1.0 / inspectorState.zoomLevel;
          let newPan = clickRatio - visibleFraction / 2;
          newPan = Math.max(0.0, Math.min(1.0 - visibleFraction, newPan));
          inspectorState.panRatio = newPan;
          renderInspectorRuler();
          renderInspectorWaveform();
          renderInspectorMinimap();
        });
      }

      // 5. Global Keyboard Shortcuts for Inspector
      window.addEventListener('keydown', (e) => {
        if (!inspectorState.isOpen) return;

        if (e.key === 'Escape') {
          closeWaveformInspector();
        } else if (e.code === 'Space') {
          e.preventDefault();
          btnPlay.click();
        } else if (e.key === '+' || e.key === '=') {
          e.preventDefault();
          setInspectorZoom(inspectorState.zoomLevel * 1.5);
        } else if (e.key === '-' || e.key === '_') {
          e.preventDefault();
          setInspectorZoom(inspectorState.zoomLevel / 1.5);
        } else if (e.key === '0') {
          setInspectorZoom(1.0);
        } else if (e.key === 'ArrowLeft') {
          e.preventDefault();
          inspectorNudge(-0.10);
        } else if (e.key === 'ArrowRight') {
          e.preventDefault();
          inspectorNudge(0.10);
        }
      });
    }
"""

# Replace or add inspector engine to JS before DOMContentLoaded
if "// FULL-SCREEN WAVEFORM INSPECTOR & MULTI-LEVEL ZOOM ENGINE" not in html:
    html = html.replace("    // Master Waveform Click & Hover Seeking Setup", inspector_engine_js + "\n    // Master Waveform Click & Hover Seeking Setup")

# In DOMContentLoaded, call setupInspectorInteractions()
if "setupInspectorInteractions();" not in html:
    html = html.replace("setupMasterWaveformEvents();", "setupMasterWaveformEvents();\n      setupInspectorInteractions();")

# Save files
for path in ["index.html", "dance_practice_player.html"]:
    p = os.path.join(base_dir, path)
    with open(p, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Updated {path} successfully!")

gen_py = os.path.join(base_dir, "generate_3tab_player.py")
with open(gen_py, "w", encoding="utf-8") as f:
    f.write(f'''import os

html_content = {repr(html)}

for p in ["dance_practice_player.html", "index.html"]:
    with open(p, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Updated {{p}} successfully")
''')
print("Updated generate_3tab_player.py successfully!")
