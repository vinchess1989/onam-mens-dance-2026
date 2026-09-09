import os
import subprocess
import struct
import json
import re

base_dir = r"C:\Users\vinee\Video Editing"
ffmpeg = r"C:\Users\vinee\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin\ffmpeg.exe"

def extract_peaks(mp3_filename, num_points=800):
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

print("Extracting high-resolution beat envelopes...")
manifest = {
    "master_260909": extract_peaks("onam_mens_final_26_0909.mp3", 800),
    "master_260906": extract_peaks("onam_mens_final_26_0906.mp3", 800),
    "comp-1": extract_peaks("Kalyanaraman (5m19s-5m29s).mp3", 200),
    "comp-2": extract_peaks("chettikulangara_only.mp3", 300),
    "comp-pause-1": extract_peaks("cue_option1_sticks.mp3", 150),
    "comp-3": extract_peaks("Sablazki Dance Squad - Short.mp3", 250),
    "comp-4": extract_peaks("shanthamee rathri.mp3", 300),
    "comp-5": extract_peaks("pondicherry dialogue.mp3", 180),
    "comp-pause-2": extract_peaks("cue_option1_sticks.mp3", 150),
    "comp-6": extract_peaks("ivalkoruvan song.mp3", 300),
    "comp-7": extract_peaks("Njanondaliyanum (0m12s-1m06s).mp3", 350),
    "comp-8": extract_peaks("Velmuruka Harohara (2m20s-3m03s).mp3", 320),
    "comp-9": extract_peaks("Applause Crowd Cheering (0m00s-0m10s).mp3", 150),
}

wf_path = os.path.join(base_dir, "waveform_data.json")
with open(wf_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f)
print("Saved waveform_data.json successfully!")
for k, v in manifest.items():
    print(f" - {k:15}: {len(v)} peak points")

# Now read the original index.html or generate_3tab_player.py
index_path = os.path.join(base_dir, "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

# Let's verify and refine the waveform CSS, JS engine, and interactions
# First check if WAVEFORM_DATA is present in html, replace or update it
wf_json_str = json.dumps(manifest)

# If WAVEFORM_DATA already exists, replace it cleanly
if "const WAVEFORM_DATA =" in html:
    html = re.sub(
        r"const WAVEFORM_DATA\s*=\s*\{.*?\};\n",
        f"const WAVEFORM_DATA = {wf_json_str};\n",
        html,
        flags=re.DOTALL
    )
else:
    html = html.replace(
        "    // DATA CONFIGURATION FOR ALL VERSIONS",
        f"    // PRECOMPUTED HIGH-RESOLUTION BEAT & AUDIO WAVEFORM DATA\n    const WAVEFORM_DATA = {wf_json_str};\n\n    // DATA CONFIGURATION FOR ALL VERSIONS"
    )

# Now define improved drawWaveform with clear beat transient spotters
new_draw_waveform_js = """    // HIGH-PRECISION AUDIO WAVEFORM & BEAT TRANSIENT ENGINE
    function drawWaveform(canvasId, peaks, currentTime, totalDuration, activeColor = '#818cf8', inactiveColor = 'rgba(148, 163, 184, 0.35)', beatThreshold = 0.50, isMaster = false) {
      const canvas = document.getElementById(canvasId);
      if (!canvas || !peaks || peaks.length === 0) return;
      const ctx = canvas.getContext('2d');
      
      const dpr = window.devicePixelRatio || 1;
      const rect = canvas.getBoundingClientRect();
      const parentW = canvas.parentElement ? canvas.parentElement.clientWidth : 0;
      const w = Math.floor(canvas.offsetWidth || rect.width || parentW || (isMaster ? 420 : 360));
      const h = Math.floor(canvas.offsetHeight || rect.height || (canvas.parentElement ? canvas.parentElement.clientHeight : 0) || (isMaster ? 56 : 44));
      if (w <= 0 || h <= 0) return;
      
      if (canvas.width !== Math.floor(w * dpr) || canvas.height !== Math.floor(h * dpr)) {
        canvas.width = Math.floor(w * dpr);
        canvas.height = Math.floor(h * dpr);
      }
      ctx.save();
      ctx.scale(dpr, dpr);
      ctx.clearRect(0, 0, w, h);
      
      const centerY = h / 2;
      
      // Center baseline guide
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(0, centerY);
      ctx.lineTo(w, centerY);
      ctx.stroke();
      
      // Master Section Boundary Markers
      if (isMaster && typeof activeRoutine !== 'undefined' && activeRoutine.sections && totalDuration > 0) {
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.16)';
        ctx.setLineDash([2, 3]);
        activeRoutine.sections.forEach(sec => {
          const tStart = (sec.timelineStart !== undefined) ? sec.timelineStart : sec.start;
          if (tStart > 0 && tStart < totalDuration) {
            const secX = (tStart / totalDuration) * w;
            ctx.beginPath();
            ctx.moveTo(secX, 0);
            ctx.lineTo(secX, h);
            ctx.stroke();
          }
        });
        ctx.setLineDash([]);
      }
      
      const progressRatio = totalDuration > 0 ? (currentTime / totalDuration) : 0;
      const progressX = progressRatio * w;
      
      const barCount = peaks.length;
      const barWidth = w / barCount;
      const gap = Math.max(0.3, barWidth * 0.18);
      const actualBarWidth = Math.max(1, barWidth - gap);
      
      for (let i = 0; i < barCount; i++) {
        const x = i * barWidth;
        const peak = peaks[i];
        const barHeight = Math.max(2.5, peak * (h * 0.84));
        const topY = centerY - barHeight / 2;
        
        const isPlayed = x <= progressX;
        const isBeat = peak >= beatThreshold;
        
        if (isBeat) {
          // Luminous Amber Beat Transient
          ctx.fillStyle = isPlayed ? '#fbbf24' : 'rgba(245, 158, 11, 0.75)';
          ctx.fillRect(x, topY, actualBarWidth, barHeight);
          // Glowing top beat cap
          ctx.fillStyle = isPlayed ? '#ffffff' : '#fbbf24';
          const dotW = Math.min(actualBarWidth, 3);
          ctx.fillRect(x + (actualBarWidth - dotW) / 2, Math.max(1, topY - 3), dotW, 2.5);
        } else {
          // Regular audio body bar
          ctx.fillStyle = isPlayed ? activeColor : inactiveColor;
          ctx.fillRect(x, topY, actualBarWidth, barHeight);
        }
      }
      ctx.restore();
    }

    function renderMasterWaveform() {
      const peaks = (currentRoutineKey === 'final260909') ? WAVEFORM_DATA.master_260909 : (WAVEFORM_DATA.master_260906 || WAVEFORM_DATA.master_260909);
      drawWaveform('masterWaveformCanvas', peaks, audio.currentTime, activeRoutine.totalDuration, '#818cf8', 'rgba(148, 163, 184, 0.35)', 0.50, true);
      const masterPlayhead = document.getElementById('masterWaveformPlayhead');
      if (masterPlayhead) {
        const ratio = activeRoutine.totalDuration > 0 ? (audio.currentTime / activeRoutine.totalDuration) : 0;
        masterPlayhead.style.left = `${Math.min(100, ratio * 100)}%`;
      }
    }

    // Global registry of component deck wave renderers
    window.compWaveRenderers = {};
"""

# Replace the existing drawWaveform & renderMasterWaveform block
html = re.sub(
    r"    // HIGH-PRECISION AUDIO WAVEFORM RENDERING ENGINE.*?(?=    // INITIALIZE TIMELINE SEGMENTS)",
    new_draw_waveform_js + "\n",
    html,
    flags=re.DOTALL
)

# Now fix the Master Waveform interaction events and ensure they are attached at DOM load
master_interaction_setup = """    // Master Waveform Click & Hover Seeking Setup
    function setupMasterWaveformEvents() {
      const masterWaveContainer = document.getElementById('masterWaveformContainer');
      const waveHoverTime = document.getElementById('waveformHoverTime');
      if (!masterWaveContainer || !waveHoverTime) return;

      masterWaveContainer.addEventListener('click', (e) => {
        const rect = masterWaveContainer.getBoundingClientRect();
        const ratio = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
        const target = ratio * activeRoutine.totalDuration;
        seekToPrecise(target);
        renderMasterWaveform();
      });

      masterWaveContainer.addEventListener('mousemove', (e) => {
        const rect = masterWaveContainer.getBoundingClientRect();
        const ratio = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
        const hoverTime = ratio * activeRoutine.totalDuration;
        waveHoverTime.style.left = `${ratio * 100}%`;
        waveHoverTime.style.display = 'block';

        const peaks = (currentRoutineKey === 'final260909') ? WAVEFORM_DATA.master_260909 : (WAVEFORM_DATA.master_260906 || WAVEFORM_DATA.master_260909);
        const idx = Math.floor(ratio * (peaks ? peaks.length : 1));
        const isBeat = peaks && peaks[idx] >= 0.50;

        if (isBeat) {
          waveHoverTime.innerHTML = `⚡ BEAT: ${formatTimePrecise(hoverTime)}`;
          waveHoverTime.style.borderColor = '#fbbf24';
          waveHoverTime.style.color = '#fbbf24';
        } else {
          waveHoverTime.innerHTML = formatTimePrecise(hoverTime);
          waveHoverTime.style.borderColor = 'rgba(245, 158, 11, 0.4)';
          waveHoverTime.style.color = '#fbbf24';
        }
      });

      masterWaveContainer.addEventListener('mouseleave', () => {
        waveHoverTime.style.display = 'none';
      });
    }
"""

# Clean up accidental master waveform code from inside btnCountdownToggle
bad_block = """      // Master Waveform Click & Hover Seeking
      const masterWaveContainer = document.getElementById('masterWaveformContainer');
      const waveHoverTime = document.getElementById('waveformHoverTime');
      if (masterWaveContainer) {
        masterWaveContainer.addEventListener('click', (e) => {
          const rect = masterWaveContainer.getBoundingClientRect();
          const ratio = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
          const target = ratio * activeRoutine.totalDuration;
          seekToPrecise(target);
        });

        masterWaveContainer.addEventListener('mousemove', (e) => {
          const rect = masterWaveContainer.getBoundingClientRect();
          const ratio = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
          const hoverTime = ratio * activeRoutine.totalDuration;
          waveHoverTime.style.left = `${ratio * 100}%`;
          waveHoverTime.style.display = 'block';
          waveHoverTime.textContent = formatTimePrecise(hoverTime);
        });

        masterWaveContainer.addEventListener('mouseleave', () => {
          waveHoverTime.style.display = 'none';
        });
      }"""

if bad_block in html:
    html = html.replace(bad_block, "")

# Insert setupMasterWaveformEvents definition before DOMContentLoaded
html = html.replace("    // INITIAL LOAD\n    window.addEventListener('DOMContentLoaded', () => {",
                    master_interaction_setup + "\n    // INITIAL LOAD\n    window.addEventListener('DOMContentLoaded', () => {")

# In switchRoutine, ensure renderMasterWaveform() is called
html = html.replace(
    "renderTrackCards();\n      updateDownloadButtons(routineKey);",
    "renderTrackCards();\n      updateDownloadButtons(routineKey);\n      renderMasterWaveform();"
)

# In seekToPrecise, ensure renderMasterWaveform() is called
html = html.replace(
    "currentTimeText.textContent = formatTimePrecise(sec);",
    "currentTimeText.textContent = formatTimePrecise(sec);\n      renderMasterWaveform();"
)

# In DOMContentLoaded, call setupMasterWaveformEvents and renderMasterWaveform
dom_load_replacement = """    // INITIAL LOAD
    window.addEventListener('DOMContentLoaded', () => {
      renderTimeline();
      renderTrackCards();
      renderComponentStudio();
      setupMasterWaveformEvents();
      updateCountdownUI();
      updateDownloadButtons(currentRoutineKey);
      setTimeout(() => {
        renderMasterWaveform();
      }, 100);
    });"""

html = re.sub(
    r"    // INITIAL LOAD\s+window\.addEventListener\('DOMContentLoaded', \(\) => \{.*?\}\);",
    dom_load_replacement,
    html,
    flags=re.DOTALL
)

# Window resize event to redraw waveforms
resize_code = """    // Window resize handler for waveform canvases
    window.addEventListener('resize', () => {
      renderMasterWaveform();
      if (sectionComponentStudioView.style.display !== 'none') {
        Object.values(window.compWaveRenderers).forEach(fn => fn());
      }
    });
"""
if "window.addEventListener('resize'" not in html:
    html = html.replace("    // KEYBOARD SHORTCUTS", resize_code + "\n    // KEYBOARD SHORTCUTS")

# In btnViewComponents click handler, trigger all component waveforms
btn_view_comp_replacement = """    btnViewComponents.addEventListener('click', () => {
      btnViewComponents.classList.add('active');
      btnViewTimeline.classList.remove('active');
      sectionTimelineView.style.display = 'none';
      sectionComponentStudioView.style.display = 'block';
      setTimeout(() => {
        Object.values(window.compWaveRenderers).forEach(fn => fn());
      }, 50);
    });"""

html = re.sub(
    r"btnViewComponents\.addEventListener\('click', \(\) => \{.*?\}\);",
    btn_view_comp_replacement,
    html,
    flags=re.DOTALL
)

# In renderComponentStudio, register compWaveRenderers[comp.id]
comp_deck_render_code = """        // Attach component waveform drawing and interaction
        const compWfContainer = compCard.querySelector(`#compWaveformContainer-${comp.id}`);
        const compWfPlayhead = compCard.querySelector(`#compWaveformPlayhead-${comp.id}`);
        const compWfHover = compCard.querySelector(`#compWaveformHover-${comp.id}`);
        const compPeaks = WAVEFORM_DATA[comp.id] || [];

        function renderCompWave() {
          drawWaveform(`compWaveformCanvas-${comp.id}`, compPeaks, cAudio.currentTime, comp.duration, comp.color, 'rgba(148, 163, 184, 0.35)', 0.50, false);
          if (compWfPlayhead) {
            const ratio = comp.duration > 0 ? (cAudio.currentTime / comp.duration) : 0;
            compWfPlayhead.style.left = `${Math.min(100, ratio * 100)}%`;
          }
        }

        window.compWaveRenderers[comp.id] = renderCompWave;

        if (compWfContainer) {
          compWfContainer.addEventListener('click', (e) => {
            const rect = compWfContainer.getBoundingClientRect();
            const ratio = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
            const target = ratio * comp.duration;
            cAudio.currentTime = parseFloat(target.toFixed(2));
            cTimeText.textContent = formatTimePrecise(target);
            cScrubber.value = target.toFixed(2);
            renderCompWave();
          });

          compWfContainer.addEventListener('mousemove', (e) => {
            const rect = compWfContainer.getBoundingClientRect();
            const ratio = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
            const hoverTime = ratio * comp.duration;
            compWfHover.style.left = `${ratio * 100}%`;
            compWfHover.style.display = 'block';

            const idx = Math.floor(ratio * (compPeaks ? compPeaks.length : 1));
            const isBeat = compPeaks && compPeaks[idx] >= 0.50;
            if (isBeat) {
              compWfHover.innerHTML = `⚡ BEAT: ${formatTimePrecise(hoverTime)}`;
              compWfHover.style.borderColor = '#fbbf24';
              compWfHover.style.color = '#fbbf24';
            } else {
              compWfHover.innerHTML = formatTimePrecise(hoverTime);
              compWfHover.style.borderColor = 'rgba(56, 189, 248, 0.4)';
              compWfHover.style.color = '#38bdf8';
            }
          });

          compWfContainer.addEventListener('mouseleave', () => {
            compWfHover.style.display = 'none';
          });
        }

        cAudio.addEventListener('timeupdate', () => {
          renderCompWave();
        });

        cAudio.addEventListener('seeked', () => {
          renderCompWave();
        });"""

html = re.sub(
    r"        // Attach component waveform drawing and interaction.*?cScrubber\.addEventListener\('input'",
    comp_deck_render_code + "\n\n        cScrubber.addEventListener('input'",
    html,
    flags=re.DOTALL
)

# In nudgeComponent, update comp waveform
html = html.replace(
    "if (timeText) timeText.textContent = formatTimePrecise(target);",
    "if (timeText) timeText.textContent = formatTimePrecise(target);\n      if (window.compWaveRenderers && window.compWaveRenderers[compId]) window.compWaveRenderers[compId]();"
)

# Save back to index.html, dance_practice_player.html, and generate_3tab_player.py
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
