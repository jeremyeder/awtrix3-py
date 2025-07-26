"""Unit tests for the Awtrix3 core library."""

from unittest.mock import Mock, patch

import pytest
import requests

from awtrix3 import Awtrix3, format_stats


class TestAwtrix3Init:
    """Test Awtrix3 class initialization."""

    def test_init_with_valid_host(self):
        """Test initialization with valid host."""
        client = Awtrix3("192.168.1.128")
        assert client.base_url == "http://192.168.1.128/api"
        assert client.auth is None

    def test_init_with_http_prefix(self):
        """Test initialization strips http:// prefix."""
        client = Awtrix3("http://192.168.1.128")
        assert client.base_url == "http://192.168.1.128/api"

    def test_init_with_https_prefix(self):
        """Test initialization strips https:// prefix."""
        client = Awtrix3("https://192.168.1.128")
        assert client.base_url == "http://192.168.1.128/api"

    def test_init_with_trailing_slash(self):
        """Test initialization strips trailing slash."""
        client = Awtrix3("192.168.1.128/")
        assert client.base_url == "http://192.168.1.128/api"

    def test_init_with_auth(self):
        """Test initialization with authentication."""
        auth = ("user", "pass")
        client = Awtrix3("192.168.1.128", auth=auth)
        assert client.auth == auth

    def test_init_empty_host_raises_error(self):
        """Test initialization with empty host raises ValueError."""
        with pytest.raises(ValueError, match="Host must be a non-empty string"):
            Awtrix3("")

    def test_init_none_host_raises_error(self):
        """Test initialization with None host raises ValueError."""
        with pytest.raises(ValueError, match="Host must be a non-empty string"):
            Awtrix3(None)

    def test_init_non_string_host_raises_error(self):
        """Test initialization with non-string host raises ValueError."""
        with pytest.raises(ValueError, match="Host must be a non-empty string"):
            Awtrix3(123)


class TestAwtrix3Methods:
    """Test Awtrix3 API methods."""

    def setup_method(self):
        """Set up test client."""
        self.client = Awtrix3("192.168.1.128")

    @patch("awtrix3.requests.post")
    def test_notify_success(self, mock_post):
        """Test successful notification."""
        mock_response = Mock()
        mock_response.json.return_value = {"status": "ok"}
        mock_response.text = '{"status": "ok"}'
        mock_post.return_value = mock_response

        result = self.client.notify("Let's go Mets!")

        mock_post.assert_called_once_with(
            "http://192.168.1.128/api/notify",
            json={"text": "Let's go Mets!"},
            auth=None,
        )
        assert result == {"status": "ok"}

    @patch("awtrix3.requests.get")
    def test_stats_success(self, mock_get):
        """Test successful stats retrieval."""
        mock_response = Mock()
        mock_response.json.return_value = {"battery": 85, "uptime": 12345}
        mock_get.return_value = mock_response

        result = self.client.stats()

        mock_get.assert_called_once_with("http://192.168.1.128/api/stats", auth=None)
        assert result == {"battery": 85, "uptime": 12345}

    @patch("awtrix3.requests.post")
    def test_power_on(self, mock_post):
        """Test power on command."""
        mock_response = Mock()
        mock_response.json.return_value = {"power": True}
        mock_response.text = '{"power": True}'
        mock_post.return_value = mock_response

        result = self.client.power(True)

        mock_post.assert_called_once_with(
            "http://192.168.1.128/api/power", json={"power": True}, auth=None
        )
        assert result == {"power": True}

    @patch("awtrix3.requests.post")
    def test_power_off(self, mock_post):
        """Test power off command."""
        mock_response = Mock()
        mock_response.json.return_value = {"power": False}
        mock_response.text = '{"power": False}'
        mock_post.return_value = mock_response

        result = self.client.power(False)

        mock_post.assert_called_once_with(
            "http://192.168.1.128/api/power", json={"power": False}, auth=None
        )
        assert result == {"power": False}

    @patch("awtrix3.requests.post")
    def test_custom_app_success(self, mock_post):
        """Test successful custom app creation."""
        mock_response = Mock()
        mock_response.json.return_value = {"status": "created"}
        mock_response.text = '{"status": "created"}'
        mock_post.return_value = mock_response

        result = self.client.custom_app("weather", "25°C", color="#00FF00")

        mock_post.assert_called_once_with(
            "http://192.168.1.128/api/custom",
            params={"name": "weather"},
            json={"text": "25°C", "color": "#00FF00"},
            auth=None,
        )
        assert result == {"status": "created"}

    def test_delete_app_empty_name_raises_error(self):
        """Test delete_app with empty name raises ValueError."""
        with pytest.raises(ValueError, match="App name must be a non-empty string"):
            self.client.delete_app("")

        with pytest.raises(ValueError, match="App name must be a non-empty string"):
            self.client.delete_app(None)

    @patch("awtrix3.requests.delete")
    def test_delete_app_success(self, mock_delete):
        """Test successful app deletion."""
        mock_response = Mock()
        mock_response.json.return_value = {"status": "deleted"}
        mock_response.text = '{"status": "deleted"}'
        mock_delete.return_value = mock_response

        result = self.client.delete_app("weather")

        mock_delete.assert_called_once_with(
            "http://192.168.1.128/api/custom", params={"name": "weather"}, auth=None
        )
        assert result == {"status": "deleted"}

    @patch("awtrix3.requests.get")
    def test_list_apps_success(self, mock_get):
        """Test successful app listing."""
        mock_response = Mock()
        mock_response.json.return_value = ["weather", "clock", "calendar"]
        mock_get.return_value = mock_response

        result = self.client.list_apps()

        mock_get.assert_called_once_with("http://192.168.1.128/api/loop", auth=None)
        assert result == ["weather", "clock", "calendar"]

    @patch("awtrix3.requests.post")
    def test_play_sound_success(self, mock_post):
        """Test successful sound playing."""
        mock_response = Mock()
        mock_response.json.return_value = {"status": "playing"}
        mock_response.text = '{"status": "playing"}'
        mock_post.return_value = mock_response

        result = self.client.play_sound("notification")

        mock_post.assert_called_once_with(
            "http://192.168.1.128/api/sound", json={"sound": "notification"}, auth=None
        )
        assert result == {"status": "playing"}

    @patch("awtrix3.requests.post")
    def test_http_error_raises_exception(self, mock_post):
        """Test that HTTP errors are properly raised."""
        mock_post.side_effect = requests.exceptions.HTTPError("404 Not Found")

        with pytest.raises(requests.exceptions.HTTPError):
            self.client.notify("test")


class TestFormatStats:
    """Test the format_stats utility function."""

    def test_format_empty_stats(self):
        """Test formatting empty stats."""
        result = format_stats({})
        assert result == "{}"

    def test_format_none_stats(self):
        """Test formatting None stats."""
        result = format_stats(None)
        assert result == "null"

    def test_format_non_dict_stats(self):
        """Test formatting non-dict stats."""
        result = format_stats("invalid")
        assert result == '"invalid"'

    def test_format_basic_stats(self):
        """Test formatting basic stats in table format."""
        stats = {
            "battery": 85,
            "uptime": 3661,  # 1 hour, 1 minute, 1 second
            "ram": 2048,
            "temp": 25.5,
            "wifi_signal": -42,
            "version": "0.96",
            "firmware": "1.0.0",
            "ip": "192.168.1.128",
            "hostname": "awtrix",
            "ssid": "MyWiFi",
        }

        result = format_stats(stats)

        # Check table structure
        lines = result.split("\n")
        assert lines[0].startswith("Metric")
        assert "Value" in lines[0]
        assert lines[1].startswith("-")

        # Check content
        assert "Battery     85%" in result
        assert "Uptime      1h 1m" in result
        assert "Memory      2048 KB" in result
        assert "Temperature 25.5°C" in result
        assert "WiFi Signal -42 dBm" in result
        assert "Version     0.96" in result
        assert "Firmware    1.0.0" in result
        assert "IP Address  192.168.1.128" in result
        assert "Hostname    awtrix" in result
        assert "WiFi SSID   MyWiFi" in result

    def test_format_uptime_minutes_only(self):
        """Test formatting uptime less than an hour."""
        stats = {"uptime": 300}  # 5 minutes
        result = format_stats(stats)
        assert "Uptime 5m" in result

    def test_format_with_unknown_fields(self):
        """Test formatting with unknown fields."""
        stats = {
            "battery": 85,
            "unknown_field": "value",
            "custom_data": {"nested": "data"},
        }

        result = format_stats(stats)

        assert "Battery 85%" in result
        assert "Additional Data:" in result
        assert '"unknown_field": "value"' in result
        assert '"custom_data"' in result

    def test_format_non_numeric_uptime(self):
        """Test formatting with non-numeric uptime."""
        stats = {"uptime": "invalid"}
        result = format_stats(stats)
        assert "Uptime invalid" in result

    def test_format_single_field(self):
        """Test formatting with single field."""
        stats = {"battery": 75}
        result = format_stats(stats)

        lines = result.split("\n")
        assert lines[0] == "Metric  Value"
        assert lines[1].startswith("-")
        assert lines[2] == "Battery 75%"

    def test_format_handles_formatting_errors(self):
        """Test that formatting errors are handled gracefully."""
        stats = {"battery": None, "version": "0.96"}
        result = format_stats(stats)

        # Should fallback to string representation for None
        assert "Battery None" in result
        assert "Version 0.96" in result
