from __future__ import annotations
from collections import defaultdict


def fuse(visual_windows, audio_windows, duration):
    audio=defaultdict(list)
    for row in audio_windows: audio[row["minute"]].append(row["audio_activity"])
    out=[]
    for v in visual_windows:
        minute=v["minute"]
        a=sum(audio[minute])/len(audio[minute]) if audio[minute] else 0.0
        presence=min(v["visual_presence"]/3.0,1.0)
        motion=v["visual_activity"]
        # Coarse group-level activity proxy, not an attention or learning measure.
        score=0.45*presence+0.30*motion+0.25*a
        out.append({"minute":minute,"visual_presence":v["visual_presence"],"visual_activity":motion,"audio_activity":round(a,3),"engagement_proxy":round(score,3)})
    return out
