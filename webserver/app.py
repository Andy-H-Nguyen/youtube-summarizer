import streamlit as st
from businessLogic import transcribe_video_orchestrator, format_transcription
import time

def main():
    # Set page configuration
    st.set_page_config(page_title="YouTube Summarizer", page_icon="🎥", layout="centered")

    # Custom CSS for enhanced UI/UX design
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    body {
        font-family: 'Roboto', sans-serif;
        background-color: #1c1c1e;
        color: #ffffff;
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
        background-color: #2d2d2f;
        border-radius: 20px;
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.5);
        transition: all 0.4s ease;
    }
    .input-container:hover {
        box-shadow: 0px 12px 40px rgba(0, 0, 0, 0.7);
    }
    input, select {
        font-size: 1.4em;
        padding: 12px;
        border: none;
        border-radius: 10px;
        background-color: #333;
        color: #f1c40f;
        margin-bottom: 25px;
        width: 100%;
    }
    input::placeholder {
        color: #7f8c8d;
    }
    .selectbox label {
        color: #f39c12;
        font-weight: bold;
    }
    .button {
        background-color: #ff6348;
        border: none;
        color: white;
        padding: 18px 36px;
        text-align: center;
        font-size: 1.3em;
        border-radius: 15px;
        cursor: pointer;
        transition: background-color 0.4s ease-in-out, transform 0.4s;
    }
    .button:hover {
        background-color: #ff7f50;
        transform: scale(1.05);
    }
    .footer {
        text-align: center;
        margin-top: 60px;
        font-size: 1.1em;
        color: #bdc3c7;
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
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .progress-bar {
        background-color: #f39c12;
        height: 8px;
        border-radius: 10px;
    }
    .tabs-header {
        text-align: center;
        margin-bottom: 20px;
        color: #bdc3c7;
    }
    </style>
    """, unsafe_allow_html=True)

    # Page title with YouTube icon and header color
    st.markdown("""
        <div class='main-title'>
            <img src="https://upload.wikimedia.org/wikipedia/commons/4/42/YouTube_icon_%282013-2017%29.png" alt="YouTube icon" />
            YouTube Summarizer
        </div>
    """, unsafe_allow_html=True)

    with st.container():
        video_placeholder = st.empty()
        loading_placeholder = st.empty()
        progress_bar_placeholder = st.empty()

        # User input: YouTube URL
        url = st.text_input("Enter YouTube URL:", placeholder="https://www.youtube.com/watch?v=example", help="Paste the URL of the YouTube video you want to summarize.")

        # Model selection dropdown
        models = ["Tiny", "Base", "Small", "Medium", "Large"]
        model = st.selectbox("Select Transcription Model:", models, help="Choose a model for transcription. Larger models are more accurate but slower.")

        # Slider to control the batch size for summary detail level
        batch_size = st.slider("Batch Size", min_value=5, max_value=60, value=10, step=5, help="Adjust the level of summary detail by controlling batch size. Less is more detailed.")

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
