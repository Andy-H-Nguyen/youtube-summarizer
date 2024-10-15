import streamlit as st
import time
from controllers.de import transcribe_video_orchestrator, save_video_data, check_existing_video_data
from utils.css_utils import inject_css
from utils.user_utils import get_user_id
from utils.video_utils import extract_video_id, show_previous_videos
from utils.transcription_utils import format_transcription

def render_video_summarizer():
    inject_css()

    st.markdown("""
        <div class='main-title'>
            <img src="https://upload.wikimedia.org/wikipedia/commons/4/42/YouTube_icon_%282013-2017%29.png" alt="YouTube icon" />
            YouTube Summarizer
        </div>
    """, unsafe_allow_html=True)

    if 'youtube_url' not in st.session_state:
        st.session_state['youtube_url'] = ''
    if 'transcription' not in st.session_state:
        st.session_state['transcription'] = None
    if 'summary' not in st.session_state:
        st.session_state['summary'] = None

    user_id = get_user_id()

    show_previous_videos(user_id)

    url = st.text_input("Enter YouTube URL:", value=st.session_state.get('youtube_url', ''), placeholder="https://www.youtube.com/watch?v=example", help="Paste the URL of the YouTube video you want to summarize.")

    with st.container():
        video_placeholder = st.empty()
        loading_placeholder = st.empty()
        progress_bar_placeholder = st.empty()

        models = ["Tiny", "Base", "Small", "Medium", "Large"]
        model = st.selectbox("Select Transcription Model:", models, help="Choose a model for transcription.")

        batch_size = st.slider("Batch Size", min_value=5, max_value=60, value=10, step=5, help="Adjust the level of summary detail by controlling batch size.")
        
        video_id = extract_video_id(url)

        st.info("**Note**: Smaller models are faster but less accurate, while larger models are slower but more accurate.", icon="⚙️")

        if url:
            video_placeholder.video(url)
        else:
            video_placeholder.markdown("<div class='placeholder'>Video will appear here once a valid URL is provided</div>", unsafe_allow_html=True)

        tabs = st.tabs(["Transcription", "Summary"])

        if st.button("Transcribe", key="transcribe_button", help="Click to start the transcription process"):
            if url:
                existing_data = check_existing_video_data(user_id, video_id)
                if existing_data:
                    transcript = existing_data['transcription']
                    summary = existing_data['summary']
                else:
                    loading_placeholder.markdown("⏳ Transcribing video, please wait...", unsafe_allow_html=True)
                    progress_bar = progress_bar_placeholder.progress(0)

                    for percent_complete in range(100):
                        time.sleep(0.05)
                        progress_bar.progress(percent_complete + 1)

                    result = transcribe_video_orchestrator(url, model.lower(), batch_size=batch_size)
                    transcript = result['transcription']
                    summary = result['summary']
                    video_name = result['name']

                    save_video_data(user_id, video_id, url, transcript, summary, video_name)
                    st.session_state['processed_videos'].append({
                        'id': video_id,
                        'name': video_name,
                        'url': url,
                        'transcription': transcript,
                        'summary': summary
                    })

                loading_placeholder.empty()
                progress_bar_placeholder.empty()

                with tabs[0]:
                    if transcript:
                        st.success("Transcription completed!")
                        st.markdown("<h3 class='tabs-header'>Transcription Result:</h3>", unsafe_allow_html=True)
                        formatted_transcript = format_transcription(transcript)
                        st.markdown(f"<div class='transcription-box'>{formatted_transcript}</div>", unsafe_allow_html=True)
                    else:
                        st.error("Error occurred while transcribing.")

                with tabs[1]:
                    if summary:
                        st.success("Summary generated!")
                        st.markdown("<h3 class='tabs-header'>Summary Result:</h3>", unsafe_allow_html=True)
                        st.markdown(f"<div class='summary-box'>{summary}</div>", unsafe_allow_html=True)
                    else:
                        st.error("Error occurred while summarizing.")
            else:
                st.error("Please enter a valid YouTube URL.")

    st.markdown("<div class='footer'>Created by Andy Nguyen © 2024</div>", unsafe_allow_html=True)
