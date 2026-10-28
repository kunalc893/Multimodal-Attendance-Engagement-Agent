from __future__ import annotations
import json
import os
from datetime import datetime
from pathlib import Path
import tempfile
import pandas as pd
import streamlit as st
from src.vision import analyze_video
from src.audio import analyze_audio
from src.fusion import fuse
from src.advisor import suggestions

st.set_page_config(page_title="Classroom Session Insights", layout="wide")
st.title("Multimodal Attendance & Engagement")
st.caption("Local processing • Anonymous tracks • Heuristic insights")

with st.sidebar:
    st.header("Session setup")
    source = st.radio("Video source", ["Recorded video", "Local camera"])
    video_file = st.file_uploader("Choose a video", type=["mp4", "avi", "mov", "mkv"]) if source == "Recorded video" else None
    camera_index = st.number_input("Camera index", min_value=0, max_value=8, value=0) if source == "Local camera" else 0
    audio_file = st.file_uploader("Optional audio file", type=["wav", "mp3", "flac", "ogg"])
    threshold = st.slider("Sustained presence threshold (seconds)", 5, 120, 30, step=5)
    st.caption("Media is processed temporarily. Reports are saved only at your request.")

if "result" not in st.session_state:
    st.session_state.result = None

if st.button("Analyze session", type="primary", disabled=(source == "Recorded video" and video_file is None)):
    progress = st.progress(0, text="Preparing inputs…")
    temp_paths = []
    try:
        if source == "Recorded video":
            suffix = Path(video_file.name).suffix or ".mp4"
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
                tmp.write(video_file.getbuffer()); video_path = tmp.name
            temp_paths.append(video_path)
        else:
            video_path = int(camera_index)
        progress.progress(10, text="Analyzing video…")
        vision = analyze_video(video_path, threshold_seconds=threshold)
        progress.progress(70, text="Analyzing audio…")
        if audio_file:
            with tempfile.NamedTemporaryFile(suffix=Path(audio_file.name).suffix, delete=False) as tmp:
                tmp.write(audio_file.getbuffer()); audio_path = tmp.name
                temp_paths.append(audio_path)
            audio = analyze_audio(audio_path)
        else:
            audio = []
        progress.progress(90, text="Fusing session signals…")
        windows = fuse(vision["windows"], audio, vision["duration"])
        st.session_state.result = {"vision": vision, "windows": windows, "suggestions": suggestions(windows), "created_at": datetime.now().astimezone().isoformat()}
        progress.progress(100, text="Done")
    except Exception as exc:
        st.error(f"Analysis failed: {exc}")
    finally:
        for temp_path in temp_paths:
            try: os.unlink(temp_path)
            except OSError: pass

result = st.session_state.result
if result:
    v = result["vision"]
    c1, c2, c3 = st.columns(3)
    c1.metric("Session duration", f"{v['duration'] / 60:.1f} min")
    c2.metric("Anonymous tracks", len(v["attendance"]))
    c3.metric("Tracks meeting threshold", sum(x["attended"] for x in v["attendance"]))
    st.subheader("Attendance log")
    att = pd.DataFrame(v["attendance"])
    if not att.empty:
        st.dataframe(att, use_container_width=True)
        st.download_button("Download attendance CSV", att.to_csv(index=False), "attendance.csv", "text/csv")
    else:
        st.info("No face tracks detected in sampled frames.")
    st.subheader("Session trends")
    frame = pd.DataFrame(result["windows"])
    if not frame.empty:
        st.line_chart(frame.set_index("minute")[ ["engagement_proxy", "visual_activity", "audio_activity"] ])
        st.dataframe(frame, use_container_width=True)
    st.subheader("Teaching suggestions")
    for item in result["suggestions"]:
        st.write("• " + item)
    if st.button("Save report locally"):
        out = Path("data/reports"); out.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = out / f"session_{stamp}.json"
        path.write_text(json.dumps(result, indent=2), encoding="utf-8")
        st.success(f"Saved to {path}")
else:
    st.info("Choose a video source and select Analyze session to begin. For a quick demo, use a short prerecorded clip.")







