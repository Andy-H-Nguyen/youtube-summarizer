import streamlit as st

def display_transcription_and_summary(transcript, summary):
    st.success("Transcription completed!")
    st.markdown("<h3 class='tabs-header'>Transcription Result:</h3>", unsafe_allow_html=True)
    st.markdown(f"<div class='transcription-box'>{transcript}</div>", unsafe_allow_html=True)
    
    st.success("Summary generated!")
    st.markdown("<h3 class='tabs-header'>Summary Result:</h3>", unsafe_allow_html=True)
    st.markdown(f"<div class='summary-box'>{summary}</div>", unsafe_allow_html=True)
