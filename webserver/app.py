import streamlit as st
from businessLogic import transcribe_video_orchestrator
from streamlit.components.v1 import html

def main():
    st.title("YoutubeSummarizer")
    # User input: YouTube URL
    url = st.text_input("Enter YouTube URL:")

    # User input: model
    models = ["tiny", "base", "small", "medium", "large"]
    model = st.selectbox("Select Model:", models)
    st.write(
        "If you take a smaller model it is faster but not as accurate, whereas a larger model is slower but more accurate.")
    if st.button("Transcribe"):
        if url:
            transcript = transcribe_video_orchestrator(url, model)

            if transcript:
                st.subheader("Transcription:")
                st.markdown(transcript, unsafe_allow_html=True)
            else:
                st.error("Error occurred while transcribing.")
                st.write("Please try again.")

    st.markdown('<div style="margin-top: 450px;"</div>',
                unsafe_allow_html=True)

    st.write(
        "If you need help or have questions about YoutubeSummarizer, feel free to reach out to me.")

    st.write("Please enter your message below:")
    user_message = st.text_area("Your Message:")


if __name__ == "__main__":
    main()
