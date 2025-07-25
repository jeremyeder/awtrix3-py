"""Tests for API integration with mocked responses."""

import json
from unittest.mock import Mock, patch

import pytest
import requests

from awtrix3 import Awtrix3


class TestAPIResponses:
    """Test various API response scenarios."""

    def setup_method(self):
        """Set up test client."""
        self.client = Awtrix3("192.168.1.128")

    @patch("awtrix3.requests.post")
    def test_notify_empty_response(self, mock_post):
        """Test notify with empty response body."""
        mock_response = Mock()
        mock_response.text = ""
        mock_response.json.return_value = None
        mock_post.return_value = mock_response

        result = self.client.notify("Test message")

        assert result is None

    @patch("awtrix3.requests.post")
    def test_notify_json_response(self, mock_post):
        """Test notify with JSON response."""
        mock_response = Mock()
        mock_response.text = '{"status": "success", "id": 123}'
        mock_response.json.return_value = {"status": "success", "id": 123}
        mock_post.return_value = mock_response

        result = self.client.notify("Test message")

        assert result == {"status": "success", "id": 123}

    @patch("awtrix3.requests.get")
    def test_stats_various_fields(self, mock_get):
        """Test stats with various field combinations."""
        stats_data = {
            "battery": 75,
            "uptime": 7200,  # 2 hours
            "ram": 1024,
            "temp": 23.8,
            "wifi_signal": -45,
            "version": "0.97",
            "firmware": "1.1.0",
            "ip": "192.168.1.128",
            "hostname": "my-awtrix",
            "ssid": "HomeNetwork",
            "unknown_field": "test_value",
        }

        mock_response = Mock()
        mock_response.json.return_value = stats_data
        mock_get.return_value = mock_response

        result = self.client.stats()

        assert result == stats_data
        mock_get.assert_called_once_with("http://192.168.1.128/api/stats", auth=None)

    @patch("awtrix3.requests.get")
    def test_list_apps_empty_list(self, mock_get):
        """Test list_apps with empty response."""
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        result = self.client.list_apps()

        assert result == []

    @patch("awtrix3.requests.get")
    def test_list_apps_with_apps(self, mock_get):
        """Test list_apps with multiple apps."""
        apps_data = ["weather", "clock", "calendar", "news"]

        mock_response = Mock()
        mock_response.json.return_value = apps_data
        mock_get.return_value = mock_response

        result = self.client.list_apps()

        assert result == apps_data
        mock_get.assert_called_once_with(
            "http://192.168.1.128/api/loop", auth=None
        )

    @patch("awtrix3.requests.delete")
    def test_delete_app_success_response(self, mock_delete):
        """Test delete_app with success response."""
        mock_response = Mock()
        mock_response.text = '{"status": "deleted", "app": "weather"}'
        mock_response.json.return_value = {"status": "deleted", "app": "weather"}
        mock_delete.return_value = mock_response

        result = self.client.delete_app("weather")

        assert result == {"status": "deleted", "app": "weather"}
        mock_delete.assert_called_once_with(
            "http://192.168.1.128/api/custom", params={"name": "weather"}, auth=None
        )

    @patch("awtrix3.requests.post")
    def test_custom_app_with_additional_params(self, mock_post):
        """Test custom_app with additional parameters."""
        mock_response = Mock()
        mock_response.text = '{"status": "created"}'
        mock_response.json.return_value = {"status": "created"}
        mock_post.return_value = mock_response

        result = self.client.custom_app(
            "weather", "25°C", color="#00FF00", icon="weather", lifetime=30
        )

        assert result == {"status": "created"}
        mock_post.assert_called_once_with(
            "http://192.168.1.128/api/custom",
            params={"name": "weather"},
            json={
                "text": "25°C",
                "color": "#00FF00",
                "icon": "weather",
                "lifetime": 30,
            },
            auth=None,
        )


class TestAPIErrorHandling:
    """Test API error handling scenarios."""

    def setup_method(self):
        """Set up test client."""
        self.client = Awtrix3("192.168.1.128", auth=("user", "pass"))

    @patch("awtrix3.requests.post")
    def test_http_404_error(self, mock_post):
        """Test handling of 404 HTTP error."""
        mock_post.side_effect = requests.exceptions.HTTPError("404 Not Found")

        with pytest.raises(requests.exceptions.HTTPError):
            self.client.notify("test")

    @patch("awtrix3.requests.post")
    def test_connection_error(self, mock_post):
        """Test handling of connection error."""
        mock_post.side_effect = requests.exceptions.ConnectionError(
            "Connection refused"
        )

        with pytest.raises(requests.exceptions.ConnectionError):
            self.client.notify("test")

    @patch("awtrix3.requests.post")
    def test_timeout_error(self, mock_post):
        """Test handling of timeout error."""
        mock_post.side_effect = requests.exceptions.Timeout("Request timed out")

        with pytest.raises(requests.exceptions.Timeout):
            self.client.notify("test")

    @patch("awtrix3.requests.get")
    def test_json_decode_error(self, mock_get):
        """Test handling of JSON decode error."""
        mock_response = Mock()
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_get.return_value = mock_response

        with pytest.raises(json.JSONDecodeError):
            self.client.stats()

    @patch("awtrix3.requests.post")
    def test_authentication_required(self, mock_post):
        """Test API call with authentication."""
        mock_response = Mock()
        mock_response.text = '{"status": "ok"}'
        mock_response.json.return_value = {"status": "ok"}
        mock_post.return_value = mock_response

        result = self.client.notify("test")

        # Verify auth was passed
        mock_post.assert_called_once_with(
            "http://192.168.1.128/api/notify",
            json={"text": "test"},
            auth=("user", "pass"),
        )
        assert result == {"status": "ok"}


class TestAPIEndpoints:
    """Test all API endpoints are called correctly."""

    def setup_method(self):
        """Set up test client."""
        self.client = Awtrix3("test.local")

    @patch("awtrix3.requests.post")
    def test_notify_endpoint(self, mock_post):
        """Test notify endpoint URL and payload."""
        mock_response = Mock()
        mock_response.text = ""
        mock_post.return_value = mock_response

        self.client.notify("Hello")

        mock_post.assert_called_once_with(
            "http://test.local/api/notify", json={"text": "Hello"}, auth=None
        )

    @patch("awtrix3.requests.get")
    def test_stats_endpoint(self, mock_get):
        """Test stats endpoint URL."""
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        self.client.stats()

        mock_get.assert_called_once_with("http://test.local/api/stats", auth=None)

    @patch("awtrix3.requests.post")
    def test_power_endpoint(self, mock_post):
        """Test power endpoint URL and payload."""
        mock_response = Mock()
        mock_response.text = ""
        mock_post.return_value = mock_response

        self.client.power(True)

        mock_post.assert_called_once_with(
            "http://test.local/api/power", json={"power": True}, auth=None
        )

    @patch("awtrix3.requests.post")
    def test_custom_app_endpoint(self, mock_post):
        """Test custom app endpoint URL and payload."""
        mock_response = Mock()
        mock_response.text = ""
        mock_post.return_value = mock_response

        self.client.custom_app("test_app", "Hello World")

        mock_post.assert_called_once_with(
            "http://test.local/api/custom",
            params={"name": "test_app"},
            json={"text": "Hello World"},
            auth=None,
        )

    @patch("awtrix3.requests.delete")
    def test_delete_app_endpoint(self, mock_delete):
        """Test delete app endpoint URL and parameters."""
        mock_response = Mock()
        mock_response.text = ""
        mock_delete.return_value = mock_response

        self.client.delete_app("test_app")

        mock_delete.assert_called_once_with(
            "http://test.local/api/custom", params={"name": "test_app"}, auth=None
        )

    @patch("awtrix3.requests.get")
    def test_list_apps_endpoint(self, mock_get):
        """Test list apps endpoint URL."""
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        self.client.list_apps()

        mock_get.assert_called_once_with("http://test.local/api/loop", auth=None)

    @patch("awtrix3.requests.post")
    def test_play_sound_endpoint(self, mock_post):
        """Test play sound endpoint URL and payload."""
        mock_response = Mock()
        mock_response.text = ""
        mock_post.return_value = mock_response

        self.client.play_sound("beep")

        mock_post.assert_called_once_with(
            "http://test.local/api/sound", json={"sound": "beep"}, auth=None
        )

    @patch("awtrix3.requests.get")
    def test_get_settings_endpoint(self, mock_get):
        """Test get settings endpoint URL."""
        mock_response = Mock()
        mock_response.json.return_value = {"brightness": 80}
        mock_get.return_value = mock_response

        self.client.get_settings()

        mock_get.assert_called_once_with("http://test.local/api/settings", auth=None)


class TestBackupRestoreAPI:
    """Test backup and restore API functionality."""

    def setup_method(self):
        """Set up test client."""
        self.client = Awtrix3("192.168.1.128")

    @patch("awtrix3.requests.get")
    @patch("builtins.open")
    @patch("json.dump")
    def test_backup_settings_to_file(self, mock_json_dump, mock_open, mock_get):
        """Test backup settings to file."""
        # Mock API responses
        settings_response = Mock()
        settings_response.json.return_value = {"brightness": 80, "timeFormat": "HH:mm"}

        stats_response = Mock()
        stats_response.json.return_value = {"version": "0.96", "battery": 85}

        mock_get.side_effect = [settings_response, stats_response]

        # Mock file operations
        mock_file = Mock()
        mock_open.return_value.__enter__.return_value = mock_file

        with patch("datetime.datetime") as mock_datetime:
            mock_datetime.now.return_value.isoformat.return_value = (
                "2024-01-01T12:00:00"
            )

            result = self.client.backup_settings("backup.json")

        assert result == "backup.json"
        mock_open.assert_called_once_with("backup.json", "w")
        mock_json_dump.assert_called_once()

        # Check the backup data structure
        backup_data = mock_json_dump.call_args[0][0]
        assert "backup_timestamp" in backup_data
        assert "backup_version" in backup_data
        assert "device_stats" in backup_data
        assert "settings" in backup_data

    @patch("awtrix3.requests.get")
    def test_backup_settings_return_dict(self, mock_get):
        """Test backup settings returning dict."""
        # Mock API responses
        settings_response = Mock()
        settings_response.json.return_value = {"brightness": 80}

        stats_response = Mock()
        stats_response.json.return_value = {"version": "0.96"}

        mock_get.side_effect = [settings_response, stats_response]

        with patch("datetime.datetime") as mock_datetime:
            mock_datetime.now.return_value.isoformat.return_value = (
                "2024-01-01T12:00:00"
            )

            result = self.client.backup_settings()

        assert isinstance(result, dict)
        assert "backup_timestamp" in result
        assert "settings" in result
        assert result["settings"] == {"brightness": 80}

    @patch("awtrix3.requests.post")
    def test_restore_settings_from_dict(self, mock_post):
        """Test restore settings from dict."""
        mock_response = Mock()
        mock_response.text = '{"status": "ok"}'
        mock_response.json.return_value = {"status": "ok"}
        mock_post.return_value = mock_response

        backup_data = {
            "backup_timestamp": "2024-01-01T12:00:00",
            "backup_version": "1.0",
            "device_stats": {"version": "0.96"},
            "settings": {"brightness": 80, "timeFormat": "HH:mm"},
        }

        result = self.client.restore_settings(backup_data)

        assert result == {"status": "ok"}
        mock_post.assert_called_once_with(
            "http://192.168.1.128/api/settings",
            json={"brightness": 80, "timeFormat": "HH:mm"},
            auth=None,
        )

    @patch("awtrix3.requests.post")
    @patch("builtins.open")
    @patch("json.load")
    def test_restore_settings_from_file(self, mock_json_load, mock_open, mock_post):
        """Test restore settings from file."""
        mock_response = Mock()
        mock_response.text = '{"status": "ok"}'
        mock_response.json.return_value = {"status": "ok"}
        mock_post.return_value = mock_response

        backup_data = {
            "backup_timestamp": "2024-01-01T12:00:00",
            "settings": {"brightness": 90},
        }
        mock_json_load.return_value = backup_data

        mock_file = Mock()
        mock_open.return_value.__enter__.return_value = mock_file

        result = self.client.restore_settings("backup.json")

        assert result == {"status": "ok"}
        mock_open.assert_called_once_with("backup.json", "r")
        mock_post.assert_called_once_with(
            "http://192.168.1.128/api/settings", json={"brightness": 90}, auth=None
        )

    def test_restore_settings_invalid_backup_data(self):
        """Test restore settings with invalid backup data."""
        invalid_data = {"invalid": "data"}  # Missing 'settings' key

        with pytest.raises(
            ValueError, match="Invalid backup data: missing 'settings' key"
        ):
            self.client.restore_settings(invalid_data)
