import streamlit as st
from businessLogic import transcribe_video_orchestrator, format_transcription, check_existing_video_data, save_video_data, check_all_videos_for_user
import time
import uuid
import re

# Extract the video ID from a YouTube URL
def extract_video_id(url):
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url)
    if match:
        return match.group(1)
    else:
        return None

# Generate or retrieve the user's unique ID (UUID)
def get_user_id():
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = str(uuid.uuid4())
    return st.session_state['user_id']

# Show previously processed videos for the user
def show_previous_videos(user_id):
    st.subheader("Previously Processed Videos:")
    docs = check_all_videos_for_user(user_id)

    if 'processed_videos' not in st.session_state:
        st.session_state['processed_videos'] = []

    if docs:
        for doc in docs:
            video_data = doc.to_dict()
            video_id = doc.id

            # Check if the video is already in session state, avoid duplication
            if not any(video['id'] == video_id for video in st.session_state['processed_videos']):
                st.session_state['processed_videos'].append({
                    'id': video_id,
                    'name': video_data.get('name', f"Video {video_id}"),
                    'url': video_data['url'],
                    'summary': video_data['summary'],
                    'transcription': video_data['transcription']
                })

    # Display videos with accordions
    if st.session_state['processed_videos']:
        for video in st.session_state['processed_videos']:
            with st.expander(video['name'], expanded=False):
                st.write(f"**Video URL:** {video['url']}")
                st.video(video['url'])
                st.write(f"**Summary:** {video['summary'][:150]}...")

                # Button to load the full video and transcription
                if st.button(f"View Full Details for {video['url']}", key=video['id']):
                    st.session_state['youtube_url'] = video['url']
                    st.session_state['transcription'] = video['transcription']
                    st.session_state['summary'] = video['summary']

                    # No need for rerun, Streamlit will automatically rerender
                    # Just clear and update the inputs manually below

    else:
        st.write("You haven't processed any videos yet.")

def main():
    # Set page configuration and fix white flash
    st.set_page_config(page_title="YouTube Summarizer", page_icon="🎥", layout="centered")

    # Custom CSS for enhanced UI/UX design with a dark background to avoid white flashes
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;700&display=swap');
    body {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #1f1f1f 0%, #3a3a3a 100%);
        color: #ffffff;
        margin: 0;
        padding: 0;
        overflow-x: hidden;
    }
    .main-title {
        color: #ff4757;
        text-align: center;
        font-size: 3.8em;
        font-weight: bold;
        margin-top: 30px;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.7);
        animation: fadeIn 1.5s ease-in-out;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 15px;
    }
    .main-title img {
        height: 55px;
        width: 80px;
    }
    .input-container {
        margin-top: 40px;
        padding: 35px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
        animation: fadeIn 2s ease-in-out;
    }
    .input-container:hover {
        box-shadow: 0px 12px 40px rgba(0, 0, 0, 0.6);
        transform: scale(1.02);
    }
    input, select {
        font-size: 1.4em;
        padding: 12px;
        border: none;
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 0.2);
        color: #ffffff;
        margin-bottom: 25px;
        width: 100%;
    }
    input::placeholder {
        color: #cccccc;
    }
    .button {
        background: linear-gradient(135deg, #ff6348 0%, #ff7f50 100%);
        border: none;
        color: white;
        padding: 18px 36px;
        text-align: center;
        font-size: 1.3em;
        border-radius: 15px;
        cursor: pointer;
        transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
    }
    .button:hover {
        transform: scale(1.05);
        box-shadow: 0px 8px 30px rgba(255, 99, 72, 0.6);
    }
    .footer {
        text-align: center;
        margin-top: 60px;
        font-size: 1.1em;
        color: #bdc3c7;
        animation: fadeIn 2s ease-in-out;
    }
    .placeholder {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 704px;
        height: 528px;
        border: 2px dashed #7f8c8d;
        border-radius: 20px;
        color: #7f8c8d;
        font-size: 1.6em;
        margin-bottom: 25px;
        animation: fadeIn 2s ease-in-out;
    }
    .transcription-box, .summary-box {
        background-color: #353535;
        padding: 25px;
        border-radius: 15px;
        color: #ecf0f1;
        font-size: 1.2em;
        line-height: 1.8;
        margin-top: 25px;
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.3);
        word-wrap: break-word;
        animation: fadeIn 2s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)

    # Display page title with YouTube icon and header
    st.markdown("""
        <div class='main-title'>
            <img src="https://upload.wikimedia.org/wikipedia/commons/4/42/YouTube_icon_%282013-2017%29.png" alt="YouTube icon" />
            YouTube Summarizer
        </div>
    """, unsafe_allow_html=True)

    # Initialize session state for the video URL, transcription, and summary
    if 'youtube_url' not in st.session_state:
        st.session_state['youtube_url'] = ''
    if 'transcription' not in st.session_state:
        st.session_state['transcription'] = None
    if 'summary' not in st.session_state:
        st.session_state['summary'] = None

    user_id = get_user_id()

    # Show previously processed videos
    show_previous_videos(user_id)

    # Use st.session_state['youtube_url'] as the default value for the URL input field
    url = st.text_input("Enter YouTube URL:", value=st.session_state.get('youtube_url', ''), placeholder="https://www.youtube.com/watch?v=example", help="Paste the URL of the YouTube video you want to summarize.")

    with st.container():
        video_placeholder = st.empty()
        loading_placeholder = st.empty()
        progress_bar_placeholder = st.empty()

        # Model selection dropdown
        models = ["Tiny", "Base", "Small", "Medium", "Large"]
        model = st.selectbox("Select Transcription Model:", models, help="Choose a model for transcription. Larger models are more accurate but slower.")

        # Slider to control the batch size for summary detail level
        batch_size = st.slider("Batch Size", min_value=5, max_value=60, value=10, step=5, help="Adjust the level of summary detail by controlling batch size.")
        
        # Video ID for checking existing data
        video_id = extract_video_id(url)

        st.info("**Note**: Smaller models are faster but less accurate, while larger models are slower but more accurate.", icon="⚙️")

        # Display the video or placeholder
        if url:
            video_placeholder.video(url)
        else:
            video_placeholder.markdown("<div class='placeholder'>Video will appear here once a valid URL is provided</div>", unsafe_allow_html=True)

        tabs = st.tabs(["Transcription", "Summary"])

        # Transcription button action
        if st.button("Transcribe", key="transcribe_button", help="Click to start the transcription process"):
            if url:
                existing_data = check_existing_video_data(user_id, video_id)
                if existing_data:
                    # Use existing data
                    transcript = existing_data['transcription']
                    summary = existing_data['summary']
                else:
                    loading_placeholder.markdown("⏳ Transcribing video, please wait...", unsafe_allow_html=True)
                    progress_bar = progress_bar_placeholder.progress(0)

                    # Simulate progress (optional)
                    for percent_complete in range(100):
                        time.sleep(0.05)
                        progress_bar.progress(percent_complete + 1)

                    # Call transcription (passing batch_size as summary detail level)
                    result = transcribe_video_orchestrator(url, model.lower(), batch_size=batch_size)
                    transcript = result.get('transcription')
                    summary = result.get('summary')
                    video_name = result.get('name')

                    # Save video data, including video name, and update UI immediately
                    save_video_data(user_id, video_id, url, transcript, summary, video_name)
                    # Add new video data to session state for real-time update
                    st.session_state['processed_videos'].append({
                        'id': video_id,
                        'name': video_name,
                        'url': url,
                        'transcription': transcript,
                        'summary': summary
                    })

                # Hide loading spinner and progress bar
                loading_placeholder.empty()
                progress_bar_placeholder.empty()

                # Display transcription and summary in tabs
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

if __name__ == "__main__":
    main()
