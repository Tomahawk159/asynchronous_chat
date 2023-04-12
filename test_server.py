import unittest
from unittest.mock import MagicMock

from server import process_client_message, send_msg_client


class ServerTestCase(unittest.TestCase):
    def test_process_client_message_valid_message(self):
        message = {"action": "presence", "user": {"account_name": "guest"}}
        expected_response = {"response": 200}
        response = process_client_message(message)
        self.assertEqual(response, expected_response)

    def test_process_client_message_invalid_message(self):
        message = {"action": "login", "user": {"account_name": "guest"}}
        expected_response = {"response": 400, "error": "Bad Request"}
        response = process_client_message(message)
        self.assertEqual(response, expected_response)

    def test_send_msg_client(self):
        client = MagicMock()
        response = {"response": 200}
        send_msg_client(client, response)
        client.send.assert_called_once_with(b'{"response": 200}')


if __name__ == "__main__":
    unittest.main()
