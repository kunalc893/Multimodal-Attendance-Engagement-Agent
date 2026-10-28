# Multimodal Attendance & Engagement Agent (Local MVP)

A privacy-conscious starter app for classroom session analytics. Video and audio are processed on your computer. The app shows anonymous face tracks for presence duration, visual activity, optional audio activity, and rule-based teaching suggestions.

## Run in VS Code on Windows

1. Install **Python 3.10 or newer** and **Visual Studio Code** with the Microsoft Python extension.
2. Open the `multimodal_attendance` folder in VS Code (**File → Open Folder**).
3. In the VS Code terminal, run:

   ```powershell
   .\setup.bat
   ```

   Or double-click `setup.bat` in File Explorer. It creates a `.venv` virtual environment and installs the required packages. Internet access is needed for the initial install; media is processed locally afterward.
4. Start the app by running `run_app.bat`, or press **F5** in VS Code and choose **Run Streamlit app**.
5. Open the URL printed by Streamlit in the terminal, usually `http://localhost:8501`.

If VS Code does not select `.venv` automatically, press `Ctrl+Shift+P` → **Python: Select Interpreter** → choose `.venv\Scripts\python.exe` → open a new terminal.

## Manual setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Choose a recorded MP4/AVI video or use a local camera. Optional audio can be supplied as a WAV/MP3/FLAC file. Camera analysis is limited to 10 minutes per session. Audio is analyzed using RMS energy; the app does not transcribe speech or identify speakers.

## Workflow

1. Choose a video source and optional audio file; set the minimum sustained-presence duration.
2. The vision module detects faces in sampled frames and associates them with temporary anonymous tracks.
3. A track counts as present after it is observed for the configured duration.
4. Visual movement and audio activity are summarized over time windows.
5. The signals produce a heuristic group activity proxy. Rule-based suggestions offer possible teaching adjustments.
6. Review attendance, trends, and suggestions in the dashboard. Download CSV or choose to save a JSON report locally.

## Architecture

`app.py` (Streamlit UI) → `src/vision.py` (OpenCV face detection and tracking) and `src/audio.py` (audio activity) → `src/fusion.py` (signal fusion) → `src/advisor.py` (rule-based suggestions) → `data/` (reports saved by the user).

Face tracks do not identify people. This MVP does not provide reliable head-pose estimation, direct microphone recording, inactivity-duration measurement, or speech recognition. The activity score is heuristic and group-level; it is not a measure of attention, learning, or individual performance.

## Privacy and responsible use

- The app makes no cloud calls and uses no face embeddings or identity recognition.
- Temporary media files are deleted after analysis.
- Reports are saved only when the user selects **Save report locally**.
- Follow your institution's notice and consent process before recording. Do not use results for grading, discipline, or other high-stakes decisions.
- Face detection and audio energy can be affected by lighting, occlusion, room noise, and accessibility needs.

## Limitations and validation

The Haar detector can miss faces due to lighting, pose, or occlusion. Track IDs can change when people cross in the frame. Audio energy does not confirm speech; fans or room noise may count as activity. Syntax compilation passed with Python 3.12. Runtime packages were not installed in this environment, so the full Streamlit app was not launched here. `setup.bat` installs the packages. Validate accuracy and performance with representative classroom recordings and the target computer.

## Interactive demo

[Open the sample-data demo](demo.html). It does not record or upload media.
