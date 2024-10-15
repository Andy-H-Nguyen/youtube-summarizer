import streamlit as st
from views.video_view import render_video_summarizer

# Set page configuration

if __name__ == "__main__":
    st.set_page_config(page_title="YouTube Summarizer", page_icon="🎥", layout="centered")
    render_video_summarizer()
