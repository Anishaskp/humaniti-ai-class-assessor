# AI Interaction History

This file records the relevant AI-assisted research, design, development and review interactions used for the challenge. Personal information, credentials and unrelated conversation have been removed.

## Interaction 1: Requirements interpretation

**Prompt:** Review the challenge requirements and identify the minimum viable submission, evaluation priorities and privacy constraints.

**AI response summary:** The application must accept an unseen class recording, return Poor/Average/Good/Excellent, and explain the result with specific observations. The highest-value areas are assessment quality and effective AI use. The submission also requires a hosted application, GitHub source, AI interaction history and a maximum 300-word explanation. Recordings must remain confidential.

**Decision:** Prioritise evidence-based assessment and a working prototype over a complex interface.

## Interaction 2: Rubric design

**Prompt:** Derive a reusable assessment rubric from labelled feedback mentioning rapport, individual questions, homework, introductions, background, visibility, clarity, revision and energy.

**AI response summary:** Group the observations into student engagement, teaching clarity, rapport and interaction, class structure, visual professionalism and learning reinforcement. Use explicit weights and documented classification thresholds.

**Decision:** Implement six weighted dimensions and expose all scores to the user.

## Interaction 3: Architecture

**Prompt:** Propose a solution that can be built in four to five hours and can genuinely process a new recording.

**AI response summary:** Use Streamlit for upload/results, Faster Whisper for local transcription, OpenCV for sampled-frame checks, transcript indicators for teaching events, and deterministic Python scoring. Avoid training a model on the small sample set.

**Decision:** Use a local, API-key-free pipeline to reduce credential and privacy risks.

## Interaction 4: Explainability

**Prompt:** How can the result be made specific rather than generic?

**AI response summary:** Show dimension scores, timestamped transcript evidence, strengths, improvement opportunities, overall reasoning and limitations. Avoid unsupported claims about attention or emotion.

**Decision:** Add timestamped evidence and downloadable JSON.

## Interaction 5: Code review

**Prompt:** Review the prototype for hard-coded outcomes, credential exposure and failure handling.

**AI response summary:** Compute the result from each uploaded recording, keep thresholds in code, exclude media/secrets through .gitignore, surface processing exceptions and document model-download/runtime limitations.

**Decision:** No filename-based classifications, no credentials, and explicit README limitations.
