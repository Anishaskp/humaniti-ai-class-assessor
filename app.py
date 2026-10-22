import json
import tempfile
from pathlib import Path

import streamlit as st

from analyzer import analyse_recording

st.set_page_config(page_title='Humaniti AI Class Assessor', page_icon='🎓', layout='wide')
st.title('🎓 Humaniti AI Class Quality Assessor')
st.caption('Upload an online-class recording to receive an evidence-based quality assessment.')

with st.sidebar:
    st.header('Assessment rubric')
    st.write('Engagement, clarity, rapport, class structure, visual professionalism, and learning reinforcement.')
    st.info('Recordings are processed only for the current session and are not intentionally persisted by this app.')

uploaded = st.file_uploader('Upload recording', type=['mp4', 'mov', 'mkv', 'webm', 'avi'])
if uploaded:
    st.video(uploaded)
    if st.button('Analyse class', type='primary', use_container_width=True):
        suffix = Path(uploaded.name).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
            f.write(uploaded.getbuffer())
            path = f.name
        try:
            with st.status('Processing the recording...', expanded=True) as status:
                st.write('Extracting audio and generating transcript')
                result = analyse_recording(path)
                status.update(label='Assessment complete', state='complete')

            label = result['classification']
            score = result['overall_score']
            colour = {'Excellent':'green', 'Good':'blue', 'Average':'orange', 'Poor':'red'}[label]
            st.markdown(f'## Overall assessment: :{colour}[{label}]')
            st.metric('Overall score', f'{score}/100')

            cols = st.columns(3)
            for i, (name, value) in enumerate(result['dimension_scores'].items()):
                cols[i % 3].metric(name, f'{value}/100')

            left, right = st.columns(2)
            with left:
                st.subheader('Strengths')
                for item in result['strengths']:
                    st.success(item)
            with right:
                st.subheader('Improvement opportunities')
                for item in result['improvements']:
                    st.warning(item)

            st.subheader('Reasoned assessment')
            st.write(result['reasoning'])

            st.subheader('Evidence detected')
            for item in result['evidence']:
                st.write(f"- **{item['time']}**: {item['observation']}")

            with st.expander('Transcript excerpt'):
                st.text(result['transcript_excerpt'])

            st.download_button(
                'Download assessment JSON',
                json.dumps(result, indent=2),
                file_name='class_assessment.json',
                mime='application/json',
            )
        except Exception as exc:
            st.error(f'Unable to process this recording: {exc}')
            st.exception(exc)
