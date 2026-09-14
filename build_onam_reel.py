import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRATCH_DIR = os.path.join(BASE_DIR, "scratch")
os.makedirs(SCRATCH_DIR, exist_ok=True)

V1 = os.path.join(BASE_DIR, "WhatsApp Video 2026-09-12 at 17.55.13.mp4") # Angle 1 (60fps)
V2 = os.path.join(BASE_DIR, "WhatsApp Video 2026-09-12 at 19.17.08.mp4") # Angle 2 (30fps)
AUDIO_SRC = os.path.join(BASE_DIR, "Onam Mood - Sahasam (Full HD 1080p).mp4")

OUT_AUDIO = os.path.join(SCRATCH_DIR, "onam_mood_mastered_2min.wav")
OUT_REEL_VERTICAL = os.path.join(BASE_DIR, "onam_dance_reel_2min.mp4")
OUT_REEL_WIDESCREEN = os.path.join(BASE_DIR, "onam_dance_reel_widescreen_2min.mp4")

# 1. Master the 2-minute Onam Mood audio (01:25 to 03:25)
print("=== Step 1: Mastering 2-Min Onam Mood Audio ===")
audio_cmd = [
    "ffmpeg", "-y", "-ss", "00:01:25.000", "-t", "120.000",
    "-i", AUDIO_SRC,
    "-vn",
    "-af", "afade=t=in:ss=0:d=1.0,afade=t=out:st=117.5:d=2.5,loudnorm=I=-14:TP=-1.5:LRA=11",
    "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2",
    OUT_AUDIO
]
res = subprocess.run(audio_cmd, capture_output=True, text=True)
if res.returncode != 0:
    print("Audio error:", res.stderr)
    sys.exit(1)
print(f"Mastered audio saved: {OUT_AUDIO}")

# 2. Clips definition (exact durations sum to 120.0s)
# Each item: (clip_index, source_video, start_time, src_duration, speed_factor, out_duration, description)
# Note: out_duration = src_duration / speed_factor. For 0.5x speed, out_duration = src_duration * 2
CLIPS = [
    # 1. Intro entrance & sunglasses pose (8s)
    {"src": V1, "ss": 26.5, "dur": 4.0, "speed": 0.5, "out_dur": 8.0, "desc": "Intro Sunglasses Pose"},
    # 2. Chettikulangara opening steps & claps (10s)
    {"src": V2, "ss": 118.0, "dur": 5.0, "speed": 0.5, "out_dur": 10.0, "desc": "Chettikulangara Claps & Steps"},
    # 3. Chettikulangara synchronized group spin (12s)
    {"src": V1, "ss": 54.0, "dur": 6.0, "speed": 0.5, "out_dur": 12.0, "desc": "Chettikulangara Group Spin"},
    # 4. Sablazki squad swagger walk (10s)
    {"src": V1, "ss": 86.0, "dur": 5.0, "speed": 0.5, "out_dur": 10.0, "desc": "Sablazki Squad Swagger"},
    # 5. Shanthamee graceful lyrical wave (10s)
    {"src": V2, "ss": 185.0, "dur": 5.0, "speed": 0.5, "out_dur": 10.0, "desc": "Shanthamee Graceful Wave"},
    # 6. Ivalkoruvan beat drop & mid-air jump (12s)
    {"src": V1, "ss": 144.5, "dur": 6.0, "speed": 0.5, "out_dur": 12.0, "desc": "Ivalkoruvan Beat Drop Jump"},
    # 7. Ivalkoruvan energetic leg kicks (10s)
    {"src": V2, "ss": 235.0, "dur": 5.0, "speed": 0.5, "out_dur": 10.0, "desc": "Ivalkoruvan Leg Kicks"},
    # 8. Njanondaliyanum wave choreography (12s)
    {"src": V1, "ss": 185.0, "dur": 6.0, "speed": 0.5, "out_dur": 12.0, "desc": "Njanondaliyanum Wave Move"},
    # 9. Velmuruka fast turns & head tilts (12s)
    {"src": V2, "ss": 318.0, "dur": 6.0, "speed": 0.5, "out_dur": 12.0, "desc": "Velmuruka Fast Turns"},
    # 10. Velmuruka climax energy twirls (12s)
    {"src": V1, "ss": 252.0, "dur": 6.0, "speed": 0.5, "out_dur": 12.0, "desc": "Velmuruka Climax Twirls"},
    # 11. Grand celebration & backstage smiles/high fives (12s)
    {"src": V1, "ss": 270.0, "dur": 6.0, "speed": 0.5, "out_dur": 12.0, "desc": "Backstage Celebration & Smiles"},
]

total_out = sum(c["out_dur"] for c in CLIPS)
print(f"Total planned reel duration: {total_out:.1f}s (exactly {int(total_out)}s)")

# 3. Render individual segments in 1920x1080 30fps
print("=== Step 2: Rendering Slow-Mo Video Segments ===")
segment_files = []
for i, c in enumerate(CLIPS):
    seg_path = os.path.join(SCRATCH_DIR, f"seg_{i:02d}.mp4")
    segment_files.append(seg_path)
    
    if os.path.exists(seg_path) and os.path.getsize(seg_path) > 1000:
        print(f"[{i+1}/{len(CLIPS)}] Using existing segment: {c['desc']}")
        continue

    # Speed multiplier: 0.5x -> setpts=2.0*PTS
    pts_factor = 1.0 / c["speed"]
    vf = f"setpts={pts_factor}*PTS,fps=30,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black"
    
    cmd = [
        "ffmpeg", "-y", "-ss", f"{c['ss']:.3f}", "-t", f"{c['dur']:.3f}",
        "-i", c["src"],
        "-an",
        "-vf", vf,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-t", f"{c['out_dur']:.3f}",
        seg_path
    ]
    print(f"[{i+1}/{len(CLIPS)}] Rendering {c['desc']} ({c['out_dur']}s)...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error rendering clip {i}:", res.stderr)
        sys.exit(1)

# Write concat list
concat_list = os.path.join(SCRATCH_DIR, "concat_clips.txt")
with open(concat_list, "w", encoding="utf-8") as f:
    for seg in segment_files:
        safe_path = seg.replace("\\", "/")
        f.write(f"file '{safe_path}'\n")

# Copy font locally to avoid drive letter colon in ffmpeg filtergraph
font_local = "scratch/arialbd.ttf"
if not os.path.exists(font_local):
    import shutil
    shutil.copyfile("C:/Windows/Fonts/arialbd.ttf", font_local)

filter_complex = (
    "[0:v]split=2[v_bg][v_fg];"
    "[v_bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5,colorchannelmixer=0.55:0:0:0:0:0.55:0:0:0:0:0.55:0[bg_dim];"
    "[v_fg]scale=1080:608:force_original_aspect_ratio=decrease,pad=1080:616:0:4:0xf59e0b[fg_border];"
    "[bg_dim][fg_border]overlay=(W-w)/2:(H-h)/2[composite];"
    f"[composite]drawtext=fontfile='{font_local}':text='OULU ONAM 2026':fontcolor=white:fontsize=44:x=(w-text_w)/2:y=280:box=1:boxcolor=black@0.65:boxborderw=18,"
    f"drawtext=fontfile='{font_local}':text='MENS DANCE ROUTINE':fontcolor=0xfbbf24:fontsize=56:x=(w-text_w)/2:y=360:box=1:boxcolor=black@0.65:boxborderw=20,"
    f"drawtext=fontfile='{font_local}':text='SLOW-MOTION HIGHLIGHTS':fontcolor=0x38bdf8:fontsize=36:x=(w-text_w)/2:y=450:box=1:boxcolor=black@0.5:boxborderw=14,"
    f"drawtext=fontfile='{font_local}':text='ONAM MOOD - SAHASAM':fontcolor=white:fontsize=40:x=(w-text_w)/2:y=1420:box=1:boxcolor=black@0.7:boxborderw=18,"
    f"drawtext=fontfile='{font_local}':text='Official 2026 Rehearsal & Stage Studio':fontcolor=0x94a3b8:fontsize=30:x=(w-text_w)/2:y=1500:box=1:boxcolor=black@0.5:boxborderw=14"
    "[v_out]"
)

vertical_cmd = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", concat_list,
    "-i", OUT_AUDIO,
    "-filter_complex", filter_complex,
    "-map", "[v_out]", "-map", "1:a",
    "-c:v", "libx264", "-preset", "medium", "-crf", "23",
    "-c:a", "aac", "-b:a", "192k",
    "-movflags", "+faststart",
    "-shortest",
    OUT_REEL_VERTICAL
]

res = subprocess.run(vertical_cmd, capture_output=True, text=True)
if res.returncode != 0:
    print("Vertical reel error:", res.stderr)
    sys.exit(1)

print(f"Vertical 9:16 reel created: {OUT_REEL_VERTICAL}")
print("=== All Reels Rendered Successfully! ===")
