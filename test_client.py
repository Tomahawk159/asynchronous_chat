import json
import time
import unittest
from unittest.mock import patch, MagicMock

from client import create_server_message, process_server_message


class ClientTest(unittest.TestCase):
    def test_create_server_message(self):
        action = "presence"
        name = "guest"
        expected_message = {
            "action": action,
            "time": time.time(),
            "user": {"account_name": name},
        }

        actual_message = create_server_message(action, name)

        self.assertEqual(expected_message, actual_message)

    def test_send_msg_server(self):
        transport = MagicMock()
        response = {"response": 200, "message": "Welcome to the chat!"}
        json_response = json.dumps(response)
        transport.recv.return_value = json_response.encode()

        with patch("client.json.loads") as mock_json_loads:
            process_server_message(transport)
            transport.recv.assert_called_once_with(4096)
            mock_json_loads.assert_called_once_with(json_response)


if __name__ == "__main__":
    unittest.main()
