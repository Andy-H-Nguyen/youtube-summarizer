import streamlit as st
from businessLogic import transcribe_video_orchestrator

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
        color: #f39c12;
        text-align: center;
        font-size: 3.5em;
        font-weight: bold;
        margin-top: 20px;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.6);
        animation: fadeIn 1.5s ease-in-out;
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
        transition: background-color 0.3s ease-in-out;
    }
    .button:hover {
        background-color: #e67e22;
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
        height: 400px;  /* Set this to match the video size */
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
    </style>
    """, unsafe_allow_html=True)

    # Page title with animation and shadow effect
    st.markdown("<h1 class='main-title'>YouTube Summarizer</h1>", unsafe_allow_html=True)

    # Use a centered layout for input form and video display
    with st.container():
        # Create a clean layout for the input and video placeholder
        video_placeholder = st.empty()  # Placeholder for the video

        # Inputs: YouTube URL and model selection
        url = st.text_input("Enter YouTube URL:", placeholder="https://www.youtube.com/watch?v=example", help="Paste the URL of the YouTube video you want to summarize.")
        
        models = ["Tiny", "Base", "Small", "Medium", "Large"]
        model = st.selectbox("Select Transcription Model:", models, help="Choose a model for transcription. Larger models are more accurate but slower.")

        # Description of model sizes and speed
        st.info("**Note**: Smaller models are faster but less accurate, while larger models are slower but more accurate.", icon="⚙️")

        if url:
            # Embed video if URL is provided
            video_placeholder.video(url)
        else:
            # Placeholder text before video loads
            video_placeholder.markdown("<div class='placeholder'>Video will appear here once a valid URL is provided</div>", unsafe_allow_html=True)

        # Transcribe button with hover effect and action
        if st.button("Transcribe", key="transcribe_button", help="Click to start the transcription process"):
            if url:
                transcript = transcribe_video_orchestrator(url, model.lower())
                if transcript:
                    st.subheader("Transcription Result:")
                    st.markdown(f"<div class='transcription-box'>{transcript}</div>", unsafe_allow_html=True)
                else:
                    st.error("Error occurred while transcribing. Please try again.")
            else:
                st.error("Please enter a valid YouTube URL.")
    
    # Footer with credits
    st.markdown("<div class='footer'>Created by Andy Nguyen © 2024</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
