from __future__ import annotations
import cv2
import time
from collections import defaultdict
from math import hypot


def analyze_video(source, threshold_seconds=30, max_seconds=600, sample_every=5):
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise RuntimeError("Could not open video source. Check the file or camera index.")
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    if fps <= 0: fps = 25.0
    tracks = {}
    windows = defaultdict(lambda: {"faces": 0, "motion": 0.0, "samples": 0})
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    prev_gray = None; idx = 0; first_wall = time.monotonic()
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 640
    try:
        while idx / fps < max_seconds:
            ok, frame = cap.read()
            if not ok: break
            if idx % sample_every:
                idx += 1; continue
            t = idx / fps
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            small = cv2.resize(gray, (max(1, int(width * .5)), max(1, int(gray.shape[0] * .5))))
            boxes = detector.detectMultiScale(small, scaleFactor=1.1, minNeighbors=5, minSize=(24, 24))
            centers = [(int(x*2 + w), int(y*2 + h)) for x,y,w,h in boxes]
            active = set()
            for center in centers:
                choices = [(hypot(center[0]-tr["center"][0], center[1]-tr["center"][1]), key) for key,tr in tracks.items() if key not in active and t-tr["last"] <= 2.0]
                dist, key = min(choices) if choices else (1e9, None)
                if dist > max(70, min(frame.shape[:2]) * .18): key = None
                if key is None:
                    key = f"track_{len(tracks)+1:03d}"
                    tracks[key] = {"first": t, "last": t, "seen": 0, "center": center}
                tr=tracks[key]; tr["last"]=t; tr["seen"]+=1; tr["center"]=center; active.add(key)
            minute = int(t // 60)
            rec=windows[minute]; rec["faces"] += len(centers); rec["samples"] += 1
            if prev_gray is not None:
                delta=cv2.absdiff(small, prev_gray)
                rec["motion"] += float(delta.mean()) / 32.0
            prev_gray=small; idx += 1
            if isinstance(source, int) and time.monotonic()-first_wall >= max_seconds: break
    finally:
        cap.release()
    duration = min(idx / fps, max_seconds)
    attendance=[]
    for key,tr in tracks.items():
        span=max(0.0,tr["last"]-tr["first"])
        attendance.append({"track_id":key,"first_seen_seconds":round(tr["first"],1),"last_seen_seconds":round(tr["last"],1),"observed_span_seconds":round(span,1),"sampled_frames":tr["seen"],"attended":bool(span >= threshold_seconds and tr["seen"] >= 3)})
    out=[]
    for minute,rec in sorted(windows.items()):
        n=max(rec["samples"],1)
        out.append({"minute":minute,"visual_presence":round(rec["faces"]/n,3),"visual_activity":round(min(rec["motion"]/n,1.0),3)})
    return {"duration":duration,"attendance":attendance,"windows":out}
