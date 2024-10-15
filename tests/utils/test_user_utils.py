import unittest
from unittest.mock import MagicMock
import uuid
from utils.user_utils import get_user_id

class TestUserUtils(unittest.TestCase):

    def test_get_user_id_existing_cookie(self):
        mock_cookies = MagicMock()
        mock_cookies.get.return_value = "existing-user-id-123"
        user_id = get_user_id(mock_cookies)

        self.assertEqual(user_id, "existing-user-id-123", "It should return the existing user_id from the cookies.")
        mock_cookies.get.assert_called_once_with("user_id")
        mock_cookies.__setitem__.assert_not_called()
        mock_cookies.save.assert_not_called()

    def test_get_user_id_new_cookie(self):
        mock_cookies = MagicMock()
        mock_cookies.get.return_value = None
        user_id = get_user_id(mock_cookies)
        
        self.assertTrue(isinstance(uuid.UUID(user_id), uuid.UUID), "The new user_id should be a valid UUID.")
        mock_cookies.__setitem__.assert_called_once_with("user_id", user_id)
        mock_cookies.save.assert_called_once()

if __name__ == '__main__':
    unittest.main()
