# Humaniti AI Class Quality Assessor

A Streamlit prototype that accepts an online-class recording, transcribes it, samples video frames, scores six teaching-quality dimensions, and classifies the session as Poor, Average, Good, or Excellent.

## Key features

- Upload MP4/MOV/MKV/WEBM/AVI recordings
- Local speech-to-text using Faster Whisper
- Lightweight visual checks using sampled frames
- Deterministic weighted scoring rubric
- Strengths, improvement actions and timestamped evidence
- Downloadable JSON result
- No API key required

## Run locally

1. Install Python 3.10 or 3.11 and FFmpeg.
2. Create a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start the application:

```bash
streamlit run app.py
```

The first transcription run downloads the Whisper model. For offline deployment, pre-download/cache the model in the deployment environment.

## Scoring rubric

- Student engagement: 25%
- Teaching clarity: 20%
- Rapport and interaction: 20%
- Class structure: 15%
- Visual professionalism: 10%
- Learning reinforcement: 10%

Thresholds: Excellent >= 85, Good 70-84, Average 50-69, Poor < 50. These are prototype thresholds and should be calibrated against more human-rated examples.

## Limitations

- Transcript accuracy depends on audio quality and accents.
- Sampled frames may miss short visual events.
- Face presence is only a visibility signal, not identity or emotion analysis.
- The heuristic rubric requires calibration against a larger labelled dataset.
