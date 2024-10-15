import streamlit as st
from services.firebase_service import check_all_videos_for_user
import re

def extract_video_id(url):
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url)
    if match:
        return match.group(1)
    else:
        return None

def show_previous_videos(user_id):
    st.subheader("Previously Processed Videos:")
    docs = check_all_videos_for_user(user_id)

    if 'processed_videos' not in st.session_state:
        st.session_state['processed_videos'] = []

    if docs:
        for doc in docs:
            video_data = doc.to_dict()
            video_id = doc.id

            if not any(video['id'] == video_id for video in st.session_state['processed_videos']):
                st.session_state['processed_videos'].append({
                    'id': video_id,
                    'name': video_data.get('name', f"Video {video_id}"),
                    'url': video_data['url'],
                    'summary': video_data['summary'],
                    'transcription': video_data['transcription']
                })

    if st.session_state['processed_videos']:
        for video in st.session_state['processed_videos']:
            with st.expander(video['name'], expanded=False):
                st.write(f"**Video URL:** {video['url']}")
                st.video(video['url'])
                st.write(f"**Summary:** {video['summary'][:150]}...")

                if st.button(f"View Full Details for {video['url']}", key=video['id']):
                    st.session_state['youtube_url'] = video['url']
                    st.session_state['transcription'] = video['transcription']
                    st.session_state['summary'] = video['summary']
    else:
        st.write("You haven't processed any videos yet.")
