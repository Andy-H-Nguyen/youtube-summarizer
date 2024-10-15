import streamlit as st

def show_previous_videos(user_id, processed_videos):
    """
    Displays the previously processed videos for a given user.
    """
    st.subheader("Previously Processed Videos")

    # Check if there are any processed videos
    if processed_videos:
        for video in processed_videos:
            # Display each video as an expandable accordion
            with st.expander(video['name'], expanded=False):
                st.write(f"**Video URL:** {video['url']}")
                st.video(video['url'])
                st.write(f"**Summary:** {video['summary'][:150]}...")

                # Button to view full details of the video and its transcription
                if st.button(f"View Full Details for {video['url']}", key=video['id']):
                    # Store the video details in the session state for rendering
                    st.session_state['youtube_url'] = video['url']
                    st.session_state['transcription'] = video['transcription']
                    st.session_state['summary'] = video['summary']
    else:
        st.write("You haven't processed any videos yet.")
