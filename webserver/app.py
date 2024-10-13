import streamlit as st
from businessLogic import transcribe_video_orchestrator
import time
from businessLogic import format_transcription

def main():
    # Set page configuration
    st.set_page_config(page_title="YouTube Summarizer", page_icon="🎥", layout="centered")

    # Custom CSS for enhanced UI/UX design
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    
    body {
        font-family: 'Roboto', sans-serif;
        background-color: #181818;
        color: #ffffff;
    }
    .main-title {
        color: #e74c3c;
        text-align: center;
        font-size: 3.5em;
        font-weight: bold;
        margin-top: 20px;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.6);
        animation: fadeIn 1.5s ease-in-out;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
    }
    .main-title img {
        height: 50px;
        width: 75px;
    }
    .input-container {
        margin-top: 40px;
        padding: 30px;
        background-color: #252525;
        border-radius: 15px;
        box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    .input-container:hover {
        box-shadow: 0px 6px 25px rgba(0, 0, 0, 0.6);
    }
    input, select {
        font-size: 1.2em;
        padding: 10px;
        border: none;
        border-radius: 8px;
        background-color: #333;
        color: #f1c40f;
        margin-bottom: 20px;
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
        background-color: #f39c12;
        border: none;
        color: white;
        padding: 15px 32px;
        text-align: center;
        font-size: 1.2em;
        border-radius: 12px;
        cursor: pointer;
        transition: background-color 0.3s ease-in-out, transform 0.3s;
    }
    .button:hover {
        background-color: #e67e22;
        transform: scale(1.05);
    }
    .footer {
        text-align: center;
        margin-top: 60px;
        font-size: 0.9em;
        color: #bdc3c7;
    }
    .placeholder {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 400px;
        border: 2px dashed #7f8c8d;
        border-radius: 15px;
        color: #7f8c8d;
        font-size: 1.5em;
        margin-bottom: 20px;
        animation: fadeIn 2s ease-in-out;
    }
    .transcription-box {
        background-color: #34495e;
        padding: 20px;
        border-radius: 10px;
        color: #ecf0f1;
        font-size: 1.1em;
        line-height: 1.6;
        word-wrap: break-word;
        margin-top: 20px;
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
    </style>
    """, unsafe_allow_html=True)

    # Page title with YouTube icon and new header color
    st.markdown("""
        <div class='main-title'>
            <img src="https://upload.wikimedia.org/wikipedia/commons/4/42/YouTube_icon_%282013-2017%29.png" alt="YouTube icon" />
            YouTube Summarizer
        </div>
    """, unsafe_allow_html=True)

    # Use a centered layout for input form and video display
    with st.container():
        video_placeholder = st.empty()  # Placeholder for the video
        loading_placeholder = st.empty()  # Placeholder for loading spinner
        progress_bar_placeholder = st.empty()  # Placeholder for progress bar

        # Inputs: YouTube URL and model selection
        url = st.text_input("Enter YouTube URL:", placeholder="https://www.youtube.com/watch?v=example", help="Paste the URL of the YouTube video you want to summarize.")
        
        models = ["Tiny", "Base", "Small", "Medium", "Large"]
        model = st.selectbox("Select Transcription Model:", models, help="Choose a model for transcription. Larger models are more accurate but slower.")

        # Description of model sizes and speed
        st.info("**Note**: Smaller models are faster but less accurate, while larger models are slower but more accurate.", icon="⚙️")

        if url:
            video_placeholder.video(url)
        else:
            video_placeholder.markdown("<div class='placeholder'>Video will appear here once a valid URL is provided</div>", unsafe_allow_html=True)

        # Tabs for Transcription and Summary
        tabs = st.tabs(["Transcription", "Summary"])

        if st.button("Transcribe", key="transcribe_button", help="Click to start the transcription process"):
            if url:
                # Show loading spinner and progress bar
                loading_placeholder.markdown("⏳ Transcribing video, please wait...", unsafe_allow_html=True)
                progress_bar = progress_bar_placeholder.progress(0)

                # Simulate progress (optional)
                for percent_complete in range(100):
                    time.sleep(0.05)
                    progress_bar.progress(percent_complete + 1)

                # Call transcription (delegating logic to businessLogic)
                result = transcribe_video_orchestrator(url, model.lower())
                transcript = result.get('transcription')
                summary = result.get('summary')

                # Hide loading spinner and progress bar after completion
                loading_placeholder.empty()
                progress_bar_placeholder.empty()
                
                # Display results in the tabs
                with tabs[0]:  # Transcription tab
                    if transcript:
                        st.success("Transcription completed successfully!")
                        st.subheader("Transcription Result:")
                        formatted_transcript = format_transcription(transcript)
                        st.markdown(f"<div class='transcription-box'>{formatted_transcript}</div>", unsafe_allow_html=True)
                    else:
                        st.error("Error occurred while transcribing. Please try again.")

                with tabs[1]:  # Summary tab
                    if summary:
                        st.success("Summary completed successfully!")
                        st.subheader("Summary Result:")
                        st.markdown(f"<div class='transcription-box'>{summary}</div>", unsafe_allow_html=True)
                    else:
                        st.error("Error occurred while summarizing. Please try again.")
            else:
                st.error("Please enter a valid YouTube URL.")

    # Footer with credits
    st.markdown("<div class='footer'>Created by Andy Nguyen © 2024</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
