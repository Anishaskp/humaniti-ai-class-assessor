# Brief Explanation

I built an AI-assisted class quality assessment prototype that accepts an online-class recording and classifies the session as **Poor, Average, Good, or Excellent**, while providing specific evidence explaining the result.

I first converted the supplied evaluator observations into a structured rubric covering student engagement, teaching clarity, rapport and interaction, class structure, visual professionalism, and learning reinforcement. The application transcribes the recording using a local speech-to-text model and samples video frames for limited visual checks such as presenter visibility and frame quality. Transcript indicators and visual signals are converted into dimension scores, and a deterministic weighted scoring layer produces the final classification.

This design avoids asking a language model to return an unsupported label. The interface displays the overall score, dimension-level scores, strengths, improvement opportunities, timestamped transcript evidence, and a downloadable JSON assessment. It also avoids hard-coded outcomes and genuinely processes each uploaded recording.

I chose Streamlit because the challenge needs a simple assessment application rather than a production platform. I did not train a custom classifier because the labelled sample set is small and the available development window is limited. The reference examples were instead used to shape the rubric and expected observations.

The main limitations are transcription accuracy, sensitivity to recording quality, and sampled-frame analysis potentially missing short events. The initial scoring thresholds are heuristic and should be calibrated against a larger set of independently human-rated classes. Visual processing is intentionally limited and does not attempt identity, emotion, or attention recognition.
