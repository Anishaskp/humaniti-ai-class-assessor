import re
from collections import defaultdict

from media_processor import transcribe, inspect_video

WEIGHTS = {
    'Student engagement': 0.25,
    'Teaching clarity': 0.20,
    'Rapport and interaction': 0.20,
    'Class structure': 0.15,
    'Visual professionalism': 0.10,
    'Learning reinforcement': 0.10,
}

PATTERNS = {
    'questions': r'\?|\b(what|why|how|can you|could you|tell me|who knows|anyone)\b',
    'names': r'\b[A-Z][a-z]{2,}\b',
    'intro': r'\b(welcome|introduce|introduction|how are you|good morning|good evening)\b',
    'clarity': r'\b(first|next|because|example|means|understand|explain|remember)\b',
    'revision': r'\b(revision|recap|previous class|last class|review)\b',
    'homework': r'\b(homework|assignment|practice|complete this|before next class)\b',
    'closing': r'\b(summary|today we learned|see you|thank you|next class)\b',
    'encouragement': r'\b(good|excellent|well done|great|correct|nice try)\b',
}

def matches(text, key):
    return len(re.findall(PATTERNS[key], text, flags=re.I))

def clamp(v):
    return max(0, min(100, int(round(v))))

def analyse_recording(video_path):
    segments, transcript = transcribe(video_path)
    visual = inspect_video(video_path)
    words = max(1, len(transcript.split()))
    minutes = max(1.0, visual['duration_seconds'] / 60)

    qpm = matches(transcript, 'questions') / minutes
    encouragement = matches(transcript, 'encouragement')
    intro = matches(transcript, 'intro')
    clarity = matches(transcript, 'clarity')
    revision = matches(transcript, 'revision')
    homework = matches(transcript, 'homework')
    closing = matches(transcript, 'closing')

    scores = {
        'Student engagement': clamp(45 + min(35, qpm * 12) + min(20, encouragement * 2)),
        'Teaching clarity': clamp(48 + min(42, clarity * 2.2) + (10 if words > 250 else 0)),
        'Rapport and interaction': clamp(42 + min(25, intro * 8) + min(33, encouragement * 3)),
        'Class structure': clamp(38 + min(18, intro * 9) + min(20, revision * 8) + min(24, closing * 10)),
        'Visual professionalism': clamp(45 + visual['face_presence_ratio'] * 35 + visual['frame_stability'] * 20),
        'Learning reinforcement': clamp(35 + min(35, revision * 12) + min(30, homework * 15)),
    }
    overall = clamp(sum(scores[k] * WEIGHTS[k] for k in WEIGHTS))
    classification = 'Excellent' if overall >= 85 else 'Good' if overall >= 70 else 'Average' if overall >= 50 else 'Poor'

    strengths, improvements = [], []
    observations = {
        'Student engagement': ('Questions and encouragement create opportunities for learner participation.', 'Increase individual questioning and invite responses from quieter learners.'),
        'Teaching clarity': ('The transcript contains structured explanations and clarity checks.', 'Use clearer step-by-step explanations and regularly check understanding.'),
        'Rapport and interaction': ('The session includes welcoming or encouraging language.', 'Spend more time on rapport building and personalised interaction.'),
        'Class structure': ('The class shows identifiable opening, teaching, revision, or closing stages.', 'Add a clear introduction, recap, summary, and conclusion.'),
        'Visual professionalism': ('The presenter is visible in a stable portion of the sampled frames.', 'Maintain consistent camera visibility, framing, and background.'),
        'Learning reinforcement': ('Revision, practice, or homework is included.', 'Conclude with revision and a clear homework or practice activity.'),
    }
    for name, value in scores.items():
        (strengths if value >= 70 else improvements).append(observations[name][0 if value >= 70 else 1])
    strengths = strengths[:4] or ['The recording was processed successfully and contained assessable teaching content.']
    improvements = improvements[:4] or ['Continue using evidence-based interaction and conclude with measurable learning reinforcement.']

    evidence = []
    for seg in segments:
        text = seg['text'].strip()
        if any(re.search(PATTERNS[k], text, re.I) for k in ['questions','intro','revision','homework','encouragement']):
            evidence.append({'time': format_time(seg['start']), 'observation': text[:220]})
        if len(evidence) == 6:
            break
    if not evidence:
        evidence.append({'time': '00:00', 'observation': 'No strong transcript event was detected; review transcript quality and audio clarity.'})

    reasoning = (
        f'The class is assessed as {classification} with an overall score of {overall}/100. '
        f'The strongest measured area is {max(scores, key=scores.get).lower()} ({max(scores.values())}/100), '
        f'while the main opportunity is {min(scores, key=scores.get).lower()} ({min(scores.values())}/100). '
        'The result combines transcript-derived indicators with lightweight visual checks and a deterministic weighted rubric, '
        'so the final label is not selected solely by a language model.'
    )
    return {
        'classification': classification,
        'overall_score': overall,
        'dimension_scores': scores,
        'strengths': strengths,
        'improvements': improvements,
        'reasoning': reasoning,
        'evidence': evidence,
        'transcript_excerpt': transcript[:3000],
        'technical_notes': visual,
    }

def format_time(seconds):
    seconds = int(seconds)
    return f'{seconds // 60:02d}:{seconds % 60:02d}'
