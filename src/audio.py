from __future__ import annotations
import numpy as np
import librosa


def analyze_audio(path, frame_seconds=2.0):
    y, sr = librosa.load(path, sr=None, mono=True)
    if len(y) == 0: return []
    hop=max(1,int(sr*frame_seconds))
    rms=librosa.feature.rms(y=y, frame_length=min(2048, max(256, 2**int(np.log2(max(sr*.04,256))))), hop_length=hop)[0]
    floor=float(np.percentile(rms,20)); peak=float(np.percentile(rms,90))
    threshold=max(floor*2.2, peak*.12, 0.003)
    out=[]
    for i,energy in enumerate(rms):
        out.append({"minute":int(i*frame_seconds//60),"audio_activity":float(energy >= threshold),"rms":float(energy)})
    return out
