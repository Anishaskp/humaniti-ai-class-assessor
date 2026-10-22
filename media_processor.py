import cv2
from faster_whisper import WhisperModel

_model = None

def transcribe(video_path):
    global _model
    if _model is None:
        _model = WhisperModel('small', device='cpu', compute_type='int8')
    segments, _ = _model.transcribe(video_path, vad_filter=True, beam_size=3)
    output, full = [], []
    for s in segments:
        item = {'start': float(s.start), 'end': float(s.end), 'text': s.text.strip()}
        output.append(item)
        full.append(item['text'])
    return output, ' '.join(full)

def inspect_video(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0
    duration = frame_count / fps if fps else 0
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    sample_times = [duration * i / 11 for i in range(1, 11)] if duration else [0]
    face_hits, sharpness = 0, []
    for sec in sample_times:
        cap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
        ok, frame = cap.read()
        if not ok:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if len(face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(40, 40))) > 0:
            face_hits += 1
        sharpness.append(cv2.Laplacian(gray, cv2.CV_64F).var())
    cap.release()
    samples = max(1, len(sharpness))
    stable = sum(1 for x in sharpness if x > 60) / samples
    return {
        'duration_seconds': round(duration, 1),
        'sampled_frames': samples,
        'face_presence_ratio': round(face_hits / samples, 2),
        'frame_stability': round(stable, 2),
    }
