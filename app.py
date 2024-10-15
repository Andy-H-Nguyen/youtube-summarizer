import os
import streamlit as st
from views.video_view import render_video_summarizer
from streamlit_cookies_manager import EncryptedCookieManager

# Set page configuration

if __name__ == "__main__":
    st.set_page_config(page_title="YouTube Summarizer", page_icon="🎥", layout="centered")
    cookies = EncryptedCookieManager(
        prefix="youtube-summarizer/",
        password=os.environ.get("firebase_client_id", "cookie_secret"),
    )
    if not cookies.ready():
        # Wait for the component to load and send us current cookies.
        st.stop()
    render_video_summarizer(cookies)
