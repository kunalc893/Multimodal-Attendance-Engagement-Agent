def suggestions(windows):
    if not windows: return ["Try a short interactive check-in to establish a participation baseline."]
    out=[]
    recent=windows[-3:]
    avg=sum(r["engagement_proxy"] for r in recent)/len(recent)
    if avg < .25: out.append("Recent group activity is low; consider a brief pause, question, or pair discussion.")
    elif avg > .7: out.append("Recent group activity is high; maintain the current pace and leave time for questions.")
    if len(windows)>=2 and windows[-1]["engagement_proxy"] < windows[0]["engagement_proxy"]*.65:
        out.append("The activity proxy declined over the session; consider changing format or checking for questions.")
    if not any(r["audio_activity"] > .05 for r in windows):
        out.append("Little audio energy was detected; check microphone placement or use a non-audio participation check.")
    if not out: out.append("No strong change was detected. Use your classroom context to decide whether any adjustment is needed.")
    return out
