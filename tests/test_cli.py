"""Tests for the CLI functionality."""

import os
from unittest.mock import Mock, mock_open, patch

import pytest

from awtrix3 import generate_config, load_config, main


class TestCLIArgumentParsing:
    """Test CLI argument parsing."""

    @patch("awtrix3.Awtrix3")
    @patch("sys.argv", ["trixctl", "--host", "192.168.1.128", "notify", "test"])
    def test_notify_command_parsing(self, mock_awtrix_class):
        """Test notify command argument parsing."""
        mock_client = Mock()
        mock_awtrix_class.return_value = mock_client
        mock_client.notify.return_value = {"status": "ok"}

        with patch("builtins.print"):
            main()

        mock_awtrix_class.assert_called_once_with("192.168.1.128", auth=None)
        mock_client.notify.assert_called_once_with("test")

    @patch("awtrix3.Awtrix3")
    @patch("sys.argv", ["trixctl", "--host", "192.168.1.128", "stats"])
    def test_stats_command_parsing(self, mock_awtrix_class):
        """Test stats command argument parsing."""
        mock_client = Mock()
        mock_awtrix_class.return_value = mock_client
        mock_client.stats.return_value = {"battery": 85}

        with patch("builtins.print"):
            main()

        mock_awtrix_class.assert_called_once_with("192.168.1.128", auth=None)
        mock_client.stats.assert_called_once()

    @patch("awtrix3.Awtrix3")
    @patch("sys.argv", ["trixctl", "--host", "192.168.1.128", "power", "on"])
    def test_power_command_parsing(self, mock_awtrix_class):
        """Test power command argument parsing."""
        mock_client = Mock()
        mock_awtrix_class.return_value = mock_client
        mock_client.power.return_value = {"power": True}

        with patch("builtins.print"):
            main()

        mock_awtrix_class.assert_called_once_with("192.168.1.128", auth=None)
        mock_client.power.assert_called_once_with(True)

    @patch("awtrix3.Awtrix3")
    @patch("sys.argv", ["trixctl", "--host", "192.168.1.128", "power", "off"])
    def test_power_off_command_parsing(self, mock_awtrix_class):
        """Test power off command argument parsing."""
        mock_client = Mock()
        mock_awtrix_class.return_value = mock_client
        mock_client.power.return_value = {"power": False}

        with patch("builtins.print"):
            main()

        mock_client.power.assert_called_once_with(False)

    @patch("awtrix3.Awtrix3")
    @patch(
        "sys.argv",
        ["trixctl", "--host", "192.168.1.128", "app", "create", "weather", "25°C"],
    )
    def test_app_create_command_parsing(self, mock_awtrix_class):
        """Test app create command argument parsing."""
        mock_client = Mock()
        mock_awtrix_class.return_value = mock_client
        mock_client.custom_app.return_value = {"status": "created"}

        with patch("builtins.print"):
            main()

        mock_client.custom_app.assert_called_once_with("weather", "25°C")

    @patch("awtrix3.Awtrix3")
    @patch(
        "sys.argv", ["trixctl", "--host", "192.168.1.128", "app", "delete", "weather"]
    )
    def test_app_delete_command_parsing(self, mock_awtrix_class):
        """Test app delete command argument parsing."""
        mock_client = Mock()
        mock_awtrix_class.return_value = mock_client
        mock_client.delete_app.return_value = {"status": "deleted"}

        with patch("builtins.print"):
            main()

        mock_client.delete_app.assert_called_once_with("weather")

    @patch("awtrix3.Awtrix3")
    @patch("sys.argv", ["trixctl", "--host", "192.168.1.128", "app", "list"])
    def test_app_list_command_parsing(self, mock_awtrix_class):
        """Test app list command argument parsing."""
        mock_client = Mock()
        mock_awtrix_class.return_value = mock_client
        mock_client.list_apps.return_value = ["weather", "clock"]

        with patch("builtins.print"):
            main()

        mock_client.list_apps.assert_called_once()

    @patch("awtrix3.Awtrix3")
    @patch("sys.argv", ["trixctl", "--host", "192.168.1.128", "sound", "notification"])
    def test_sound_command_parsing(self, mock_awtrix_class):
        """Test sound command argument parsing."""
        mock_client = Mock()
        mock_awtrix_class.return_value = mock_client
        mock_client.play_sound.return_value = {"status": "playing"}

        with patch("builtins.print"):
            main()

        mock_client.play_sound.assert_called_once_with("notification")


class TestCLIAuthentication:
    """Test CLI authentication handling."""

    @patch("awtrix3.Awtrix3")
    @patch(
        "sys.argv",
        [
            "trixctl",
            "--host",
            "192.168.1.128",
            "--username",
            "admin",
            "--password",
            "secret",
            "notify",
            "test",
        ],
    )
    def test_authentication_from_args(self, mock_awtrix_class):
        """Test authentication from command line arguments."""
        mock_client = Mock()
        mock_awtrix_class.return_value = mock_client
        mock_client.notify.return_value = {"status": "ok"}

        with patch("builtins.print"):
            main()

        mock_awtrix_class.assert_called_once_with(
            "192.168.1.128", auth=("admin", "secret")
        )

    @patch("awtrix3.Awtrix3")
    @patch(
        "sys.argv",
        ["trixctl", "--host", "192.168.1.128", "--username", "admin", "notify", "test"],
    )
    @patch.dict(os.environ, {"TRIXCTL_PASSWORD": "env_secret"})
    def test_authentication_from_env(self, mock_awtrix_class):
        """Test authentication from environment variable."""
        mock_client = Mock()
        mock_awtrix_class.return_value = mock_client
        mock_client.notify.return_value = {"status": "ok"}

        with patch("builtins.print"):
            main()

        mock_awtrix_class.assert_called_once_with(
            "192.168.1.128", auth=("admin", "env_secret")
        )


class TestCLIErrorHandling:
    """Test CLI error handling."""

    @patch("sys.argv", ["trixctl", "notify", "test"])
    @patch("awtrix3.load_config", return_value={})
    def test_missing_host_error(self, mock_load_config):
        """Test error when host is missing."""
        with patch("builtins.print") as mock_print:
            with pytest.raises(SystemExit):
                main()

        # Check that error message was printed
        mock_print.assert_called()
        args = mock_print.call_args_list
        error_found = any("No host specified" in str(call) for call in args)
        assert error_found, f"Expected 'No host specified' error not found in: {args}"

    @patch("sys.argv", ["trixctl", "--host", "192.168.1.128", "app"])
    def test_app_missing_subcommand_error(self):
        """Test error when app subcommand is missing."""
        with patch("builtins.print") as mock_print:
            with pytest.raises(SystemExit):
                main()

        # Check that error message was printed
        args = mock_print.call_args_list
        error_found = any("requires a subcommand" in str(call) for call in args)
        assert error_found

    @patch("awtrix3.Awtrix3")
    @patch("sys.argv", ["trixctl", "--host", "192.168.1.128", "notify", "test"])
    def test_api_exception_handling(self, mock_awtrix_class):
        """Test handling of API exceptions."""
        mock_client = Mock()
        mock_awtrix_class.return_value = mock_client
        mock_client.notify.side_effect = Exception("Connection failed")

        with patch("builtins.print") as mock_print:
            with pytest.raises(SystemExit):
                main()

        # Check that error was printed
        args = mock_print.call_args_list
        error_found = any("Connection failed" in str(call) for call in args)
        assert error_found


class TestConfigGeneration:
    """Test configuration file generation."""

    @patch("sys.argv", ["trixctl", "--generate-config"])
    def test_generate_config_creates_file(self):
        """Test that generate-config creates a config file."""
        with patch("builtins.open", mock_open()) as mock_file:
            with patch("os.chmod") as mock_chmod:
                with patch("builtins.print"):
                    main()

        # Check that file was opened for writing
        mock_file.assert_called()
        handle = mock_file()
        handle.write.assert_called()

        # Check that secure permissions were set
        mock_chmod.assert_called()

    def test_generate_config_function(self):
        """Test the generate_config function directly."""
        with patch("builtins.open", mock_open()) as mock_file:
            with patch("os.chmod"):
                with patch("builtins.print"):
                    generate_config()

        # Verify file operations
        mock_file.assert_called_once()
        handle = mock_file()
        handle.write.assert_called_once()

        # Check content contains expected sections
        written_content = handle.write.call_args[0][0]
        assert "[device]" in written_content
        assert "[settings]" in written_content
        assert "192.168.1.128" in written_content


class TestConfigLoading:
    """Test configuration file loading."""

    def test_load_config_missing_file(self):
        """Test loading config when file doesn't exist."""
        with patch("pathlib.Path.exists", return_value=False):
            config = load_config()

        assert config == {}

    def test_load_config_valid_file(self):
        """Test loading valid config file."""
        config_content = """
[device]
host = 192.168.1.128
username = admin
"""

        with patch("pathlib.Path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=config_content)):
                config = load_config()

        assert config == {"host": "192.168.1.128", "username": "admin"}

    def test_load_config_handles_errors(self):
        """Test that config loading handles errors gracefully."""
        with patch("pathlib.Path.exists", return_value=True):
            with patch("builtins.open", side_effect=IOError("Permission denied")):
                with patch("builtins.print"):  # Suppress warning output
                    config = load_config()

        assert config == {}


class TestHelpOutput:
    """Test CLI help output."""

    @patch("sys.argv", ["trixctl", "--help"])
    def test_main_help_output(self):
        """Test main help output contains expected information."""
        with pytest.raises(SystemExit):
            with patch("sys.stdout") as mock_stdout:
                main()

        # Should exit with code 0 for help
        assert mock_stdout.write.called

    @patch("sys.argv", ["trixctl", "app", "--help"])
    def test_app_subcommand_help(self):
        """Test app subcommand help output."""
        with pytest.raises(SystemExit):
            with patch("sys.stdout") as mock_stdout:
                main()

        # Should show app subcommands
        assert mock_stdout.write.called
