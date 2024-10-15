import uuid
import streamlit as st

# Generate or retrieve the user's unique ID (UUID)
def get_user_id():
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = str(uuid.uuid4())
    return st.session_state['user_id']
