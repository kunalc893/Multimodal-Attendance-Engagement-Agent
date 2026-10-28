# Objectives, Architecture, and Implementation Status

## Objectives

- Automate attendance logs using sustained presence rather than single-frame detection.
- Summarize group-level visual and optional audio activity over time windows.
- Provide transparent, non-directive teaching suggestions based on activity trends.
- Process media locally and avoid saving raw media.

## System architecture and workflow

1. **Input**: Streamlit accepts a recorded video or local camera, plus an optional audio recording.
2. **Vision**: OpenCV Haar cascade detects faces in sampled frames. A centroid tracker associates detections across gaps of up to two seconds.
3. **Attendance**: A track qualifies after it has been observed for the configured duration and at least three sampled frames. Track IDs are anonymous and session-specific.
4. **Audio**: Librosa estimates activity from RMS energy. It does not determine whether a signal is speech.
5. **Fusion**: Per-minute visual presence, movement, and audio activity produce a 0–1 group activity proxy.
6. **Suggestion agent**: Simple rules turn trends into teaching suggestions. No generative AI model or cloud service is used.
7. **Dashboard and storage**: Streamlit shows logs, trends, and suggestions. CSV can be downloaded; JSON is written to `data/reports/` only when requested.

## Scope and follow-up work

| Requirement | Current MVP status |
| --- | --- |
| Objectives, architecture, workflow | Documented here and in README |
| Recorded video / camera | Implemented; camera uses OpenCV capture |
| Audio input | Audio-file upload implemented; direct microphone recording is pending |
| Face detection and anonymous tracking | Implemented with OpenCV Haar cascade and centroid association |
| Sustained presence and time logs | Duration threshold implemented; times are elapsed session seconds |
| Head pose | Not implemented; landmark-based estimation and validation are needed |
| Movement / inactivity | Movement proxy implemented; inactivity duration threshold is pending |
| Speech / interaction detection | Not implemented; RMS is an acoustic activity proxy only |
| Multimodal fusion and trends | Implemented as an explicitly heuristic group activity proxy |
| Teaching suggestions | Rule-based suggestions implemented; no trained or generative AI model |
| Dashboard / reports | Streamlit dashboard, CSV download, and opt-in JSON report implemented |
| Offline / local processing | No network calls in the app; internet is needed for initial package installation |
| Accuracy and performance validation | Syntax compilation passed with Python 3.12; validation on representative media and target hardware is pending |

## Validation before deployment

Compare consented, representative classroom recordings against manually annotated entry and exit times. Measure attendance precision/recall and timing error, missed/false detections across lighting, occlusion, and camera positions, audio false-positive rate in noisy rooms, and processing time per video minute on the target computer. Do not treat the activity proxy as a student-level measure of attention, learning, or performance.

## Progress demo

[Open the interactive dashboard demo](demo.html). It uses fictional sample data and is not connected to the analysis pipeline.
