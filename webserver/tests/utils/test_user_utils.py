import unittest
from unittest.mock import patch
import streamlit as st  # Import streamlit as st
from utils.user_utils import get_user_id

class TestUserUtils(unittest.TestCase):

    @patch('streamlit.session_state', {})
    def test_get_user_id(self):
        # Ensure session state is empty
        self.assertNotIn('user_id', st.session_state, "Session state should not contain user_id initially.")

        # Call get_user_id
        user_id = get_user_id()

        # Assertions
        self.assertTrue(isinstance(user_id, str), "User ID should be a string.")
        self.assertIn('user_id', st.session_state, "User ID should be saved in session state.")
        self.assertEqual(user_id, st.session_state['user_id'], "User ID should match session state value.")

if __name__ == '__main__':
    unittest.main()
