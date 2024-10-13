import streamlit as st
from businessLogic import transcribe_video_orchestrator
from streamlit.components.v1 import html

def main():
    # Set page configuration
    st.set_page_config(page_title="YouTube Summarizer", page_icon="🎥", layout="centered")

    # Custom CSS for modern look
    st.markdown("""
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f5f5f5;
    }
    .main-title {
        text-align: center;
        color: #2c3e50;
        font-size: 3em;
        font-weight: bold;
        margin-top: 20px;
    }
    .input-container {
        margin-top: 40px;
        padding: 20px;
        background-color: #ffffff;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
    }
    .selectbox label {
        color: #2980b9;
        font-weight: bold;
    }
    .footer {
        text-align: center;
        margin-top: 60px;
        font-size: 0.9em;
        color: #7f8c8d;
    }
    </style>
    """, unsafe_allow_html=True)

    # Page title
    st.markdown("<h1 class='main-title'>YouTube Summarizer</h1>", unsafe_allow_html=True)

    # Input container
    with st.container():
        st.markdown("<div class='input-container'>", unsafe_allow_html=True)
        
        # User input: YouTube URL
        url = st.text_input("Enter YouTube URL:", placeholder="https://www.youtube.com/watch?v=example")
        
        # User input: model selection
        models = ["Tiny", "Base", "Small", "Medium", "Large"]
        model = st.selectbox("Select Transcription Model:", models)
        st.write("**Note**: Smaller models are faster but less accurate, while larger models are slower but more accurate.")

        if st.button("Transcribe"):
            if url:
                transcript = transcribe_video_orchestrator(url, model.lower())  # Assuming model.lower() maps correctly

                if transcript:
                    st.subheader("Transcription Result:")
                    st.markdown(f"<div style='background-color:#ecf0f1; padding:10px; border-radius:5px;'>{transcript}</div>", unsafe_allow_html=True)
                else:
                    st.error("Error occurred while transcribing. Please try again.")
            else:
                st.error("Please enter a valid YouTube URL.")
        
        st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("<div class='footer'>Created by YourName © 2024</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
