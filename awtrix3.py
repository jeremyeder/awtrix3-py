import json

import requests

__version__ = "0.1.0"
__all__ = [
    "Awtrix3",
    "format_stats",
    "format_uptime",
    "generate_config",
    "load_config",
    "main",
]


class Awtrix3:
    def __init__(self, host, auth=None):
        if not host or not isinstance(host, str):
            raise ValueError("Host must be a non-empty string")
        # Clean up host URL (remove http/https if present)
        host = host.replace("http://", "").replace("https://", "").strip("/")
        self.base_url = f"http://{host}/api"
        self.auth = auth

    def notify(self, text):
        """Send a simple text notification"""
        data = {"text": text}
        response = requests.post(f"{self.base_url}/notify", json=data, auth=self.auth)
        response.raise_for_status()
        return response.json() if response.text else None

    def stats(self):
        """Get device statistics"""
        response = requests.get(f"{self.base_url}/stats", auth=self.auth)
        response.raise_for_status()
        return response.json()

    def power(self, on=True):
        """Turn device on/off"""
        data = {"power": on}
        response = requests.post(f"{self.base_url}/power", json=data, auth=self.auth)
        response.raise_for_status()
        return response.json() if response.text else None

    def custom_app(self, name, text, **kwargs):
        """Create/update a custom app"""
        data = {"text": text, **kwargs}
        response = requests.post(
            f"{self.base_url}/custom", params={"name": name}, json=data, auth=self.auth
        )
        response.raise_for_status()
        # API returns plain text "OK", not JSON
        try:
            return response.json() if response.text.strip() else None
        except json.JSONDecodeError:
            return {"status": response.text.strip()} if response.text.strip() else None

    def play_sound(self, sound_name):
        """Play a sound by name"""
        data = {"sound": sound_name}
        response = requests.post(f"{self.base_url}/sound", json=data, auth=self.auth)
        response.raise_for_status()
        return response.json() if response.text else None

    def delete_app(self, name):
        """Delete a custom app by name"""
        if not name or not isinstance(name, str):
            raise ValueError("App name must be a non-empty string")
        response = requests.post(
            f"{self.base_url}/custom", params={"name": name}, auth=self.auth
        )
        response.raise_for_status()
        # API returns plain text "OK", not JSON
        try:
            return response.json() if response.text.strip() else None
        except json.JSONDecodeError:
            return {"status": response.text.strip()} if response.text.strip() else None

    def list_apps(self):
        """Get list of apps currently in the loop"""
        response = requests.get(f"{self.base_url}/loop", auth=self.auth)
        response.raise_for_status()
        return response.json()

    def get_settings(self):
        """Get current device settings for backup"""
        response = requests.get(f"{self.base_url}/settings", auth=self.auth)
        response.raise_for_status()
        return response.json()

    def backup_settings(self, filepath=None):
        """Backup device settings to JSON file

        Args:
            filepath (str): Path to save backup file. If None, returns settings dict.

        Returns:
            dict: Settings data if filepath is None
            str: Filepath where backup was saved if filepath provided
        """
        import json
        from datetime import datetime

        settings = self.get_settings()

        # Add metadata to backup
        backup_data = {
            "backup_timestamp": datetime.now().isoformat(),
            "backup_version": "1.0",
            "device_stats": self.stats(),
            "settings": settings,
        }

        if filepath is None:
            return backup_data

        with open(filepath, "w") as f:
            json.dump(backup_data, f, indent=2)

        return filepath

    def restore_settings(self, backup_data):
        """Restore device settings from backup data

        Args:
            backup_data (dict or str): Backup data dict or filepath to backup JSON

        Returns:
            dict: Result of settings update
        """
        import json

        if isinstance(backup_data, str):
            # Load from file
            with open(backup_data, "r") as f:
                backup_data = json.load(f)

        if "settings" not in backup_data:
            raise ValueError("Invalid backup data: missing 'settings' key")

        settings = backup_data["settings"]

        # Apply settings using existing configure_settings method if available
        if hasattr(self, "configure_settings"):
            return self.configure_settings(settings)
        else:
            # Fall back to direct API call
            response = requests.post(
                f"{self.base_url}/settings", json=settings, auth=self.auth
            )
            response.raise_for_status()
            return response.json() if response.text else None


def format_stats(stats_data):
    """Format stats data in a minimal aligned table style"""
    import json

    if not stats_data or not isinstance(stats_data, dict):
        return json.dumps(stats_data, indent=2)

    # Collect table rows
    rows = []
    known_fields = set()

    # Define field mappings and formatting
    field_mappings = [
        ("battery", "Battery", lambda x: f"{x}%"),
        ("uptime", "Uptime", lambda x: format_uptime(x)),
        ("ram", "Memory", lambda x: f"{x} KB"),
        ("temp", "Temperature", lambda x: f"{x}°C"),
        ("wifi_signal", "WiFi Signal", lambda x: f"{x} dBm"),
        ("version", "Version", lambda x: str(x)),
        ("firmware", "Firmware", lambda x: str(x)),
        ("ip", "IP Address", lambda x: str(x)),
        ("hostname", "Hostname", lambda x: str(x)),
        ("ssid", "WiFi SSID", lambda x: str(x)),
    ]

    # Process known fields
    for field_key, field_label, formatter in field_mappings:
        if field_key in stats_data:
            try:
                formatted_value = formatter(stats_data[field_key])
                rows.append((field_label, formatted_value))
                known_fields.add(field_key)
            except (TypeError, ValueError):
                # Fallback to string representation if formatting fails
                rows.append((field_label, str(stats_data[field_key])))
                known_fields.add(field_key)

    if not rows:
        return json.dumps(stats_data, indent=2)

    # Calculate column widths
    max_label_width = max(len(row[0]) for row in rows)

    # Build table
    output = []
    output.append(f"{'Metric':<{max_label_width}} Value")
    output.append("-" * (max_label_width + 20))

    for label, value in rows:
        output.append(f"{label:<{max_label_width}} {value}")

    # Handle any unknown fields
    additional_data = {k: v for k, v in stats_data.items() if k not in known_fields}
    if additional_data:
        output.append("")
        output.append("Additional Data:")
        output.append(json.dumps(additional_data, indent=2))

    return "\n".join(output)


def format_uptime(uptime_seconds):
    """Format uptime seconds into human-readable format"""
    if isinstance(uptime_seconds, (int, float)):
        hours = int(uptime_seconds // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    else:
        return str(uptime_seconds)


def generate_config():
    """Generate a self-documented config file template"""
    import os
    import sys
    from pathlib import Path

    config_content = """# trixctl Configuration File
# This file contains default settings for the trixctl command.
# CLI arguments will override these settings.
#
# For security, passwords should be set via environment variable:
# export TRIXCTL_PASSWORD="your_password"

[device]
# IP address or hostname of your Awtrix3 device
# Example: host = 192.168.1.128
host =

# Username for device authentication (if required)
# Example: username = admin
username =

[settings]
# Default output format (json is currently the only option)
output_format = json

# Example usage:
# trixctl notify "Let's go Mets!"    # Uses config file host
# trixctl --host 192.168.1.128 notify "Let's go Mets!"  # Override with CLI arg
"""

    config_path = Path.home() / ".trixctl.conf"

    try:
        with open(config_path, "w") as f:
            f.write(config_content)
        # Set secure permissions (owner read/write only)
        os.chmod(config_path, 0o600)
        print(f"Generated config file: {config_path}")
        print("Edit the file to set your default device settings.")
        print("Use TRIXCTL_PASSWORD environment variable for password.")
    except Exception as e:
        print(f"Error generating config: {e}", file=sys.stderr)
        sys.exit(1)


def load_config():
    """Load configuration from ~/.trixctl.conf"""
    import configparser
    import sys
    from pathlib import Path

    config_path = Path.home() / ".trixctl.conf"
    config = {}

    if config_path.exists():
        try:
            parser = configparser.ConfigParser()
            parser.read(config_path)

            if "device" in parser:
                device = parser["device"]
                if device.get("host"):
                    config["host"] = device.get("host")
                if device.get("username"):
                    config["username"] = device.get("username")

        except Exception as e:
            print(
                f"Warning: Error reading config file {config_path}: {e}",
                file=sys.stderr,
            )

    return config


def main():
    """Main CLI entry point"""
    import argparse
    import json
    import os
    import sys

    parser = argparse.ArgumentParser(
        description="Control Awtrix3 device",
        epilog=(
            "\nThanks to @blueforcer for Awtrix3 inspiration "
            "and @claude for implementation.\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--host", help="Device IP address (overrides config file)")
    parser.add_argument("--username", help="Auth username (overrides config file)")
    parser.add_argument(
        "--password", help="Auth password (overrides config file and env var)"
    )
    parser.add_argument(
        "--generate-config",
        action="store_true",
        help="Generate a config file template at ~/.trixctl.conf",
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # notify command
    notify_parser = subparsers.add_parser("notify", help="Send notification")
    notify_parser.add_argument("text", help="Notification text")

    # stats command
    subparsers.add_parser("stats", help="Get device statistics")

    # power command
    power_parser = subparsers.add_parser("power", help="Power control")
    power_parser.add_argument("state", choices=["on", "off"], help="Power state")

    # app command with subcommands
    app_parser = subparsers.add_parser("app", help="Manage custom apps")
    app_subparsers = app_parser.add_subparsers(dest="app_command", help="App commands")

    # app create command
    app_create_parser = app_subparsers.add_parser("create", help="Create custom app")
    app_create_parser.add_argument("name", help="App name")
    app_create_parser.add_argument("text", help="App text")

    # app delete command
    app_delete_parser = app_subparsers.add_parser("delete", help="Delete custom app")
    app_delete_parser.add_argument("name", help="App name to delete")

    # app list command
    app_subparsers.add_parser("list", help="List apps in current loop")

    # sound command
    sound_parser = subparsers.add_parser("sound", help="Play sound")
    sound_parser.add_argument("name", help="Sound name")

    # backup command
    backup_parser = subparsers.add_parser("backup", help="Backup device settings")
    backup_parser.add_argument("filename", help="Backup filename (JSON)")
    backup_parser.add_argument(
        "--include-stats", action="store_true", help="Include device stats in backup"
    )

    # restore command
    restore_parser = subparsers.add_parser("restore", help="Restore device settings")
    restore_parser.add_argument("filename", help="Backup filename (JSON)")
    restore_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be restored without applying",
    )
    restore_parser.add_argument(
        "--force", action="store_true", help="Restore without confirmation"
    )

    args = parser.parse_args()

    # Handle generate-config command
    if getattr(args, "generate_config", False):
        generate_config()
        return

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Load config file
    config = load_config()

    # Determine values with priority: CLI args > env vars > config file
    host = args.host or config.get("host")
    username = args.username or config.get("username")
    password = args.password or os.environ.get("TRIXCTL_PASSWORD")

    if not host:
        print(
            "Error: No host specified. Use --host, set it in config file, "
            "or run --generate-config",
            file=sys.stderr,
        )
        sys.exit(1)

    # Setup auth
    auth = None
    if username and password:
        auth = (username, password)

    # Create client
    client = Awtrix3(host, auth=auth)

    try:
        if args.command == "notify":
            result = client.notify(args.text)
        elif args.command == "stats":
            result = client.stats()
        elif args.command == "power":
            result = client.power(args.state == "on")
        elif args.command == "app":
            if not args.app_command:
                print(
                    "Error: app command requires a subcommand (create, delete, list)",
                    file=sys.stderr,
                )
                sys.exit(1)
            elif args.app_command == "create":
                result = client.custom_app(args.name, args.text)
            elif args.app_command == "delete":
                result = client.delete_app(args.name)
            elif args.app_command == "list":
                result = client.list_apps()
        elif args.command == "sound":
            result = client.play_sound(args.name)
        elif args.command == "backup":
            # Create backup
            print("Creating backup of device settings...")
            backup_file = client.backup_settings(args.filename)
            print(f"Backup saved to: {backup_file}")

            if args.include_stats:
                print("Backup includes device statistics")

            result = {"status": "success", "backup_file": backup_file}

        elif args.command == "restore":
            # Load and validate backup file
            try:
                with open(args.filename, "r") as f:
                    backup_data = json.load(f)
            except FileNotFoundError:
                print(
                    f"Error: Backup file '{args.filename}' not found", file=sys.stderr
                )
                sys.exit(1)
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON in backup file - {e}", file=sys.stderr)
                sys.exit(1)

            # Show what will be restored
            if "backup_timestamp" in backup_data:
                print(f"Backup created: {backup_data['backup_timestamp']}")
            if (
                "device_stats" in backup_data
                and "version" in backup_data["device_stats"]
            ):
                version = backup_data["device_stats"].get("version", "unknown")
                print(f"Backup from device version: {version}")

            settings_count = len(backup_data.get("settings", {}))
            print(f"Settings to restore: {settings_count} items")

            if args.dry_run:
                print("\n--- DRY RUN MODE - Nothing will be changed ---")
                print("Settings that would be restored:")
                for key in backup_data.get("settings", {}):
                    print(f"  - {key}")
                result = {"status": "dry_run", "settings_count": settings_count}
            else:
                # Confirm restoration unless --force is used
                if not args.force:
                    confirm = input(
                        f"\nRestore {settings_count} settings to device? (y/N): "
                    )
                    if confirm.lower() not in ["y", "yes"]:
                        print("Restore cancelled")
                        sys.exit(0)

                print("Restoring settings...")
                result = client.restore_settings(backup_data)
                print("Settings restored successfully!")

        if result:
            if args.command == "stats":
                print(format_stats(result))
            elif args.command in ["backup", "restore"]:
                # Backup/restore commands handle their own output
                pass
            else:
                print(json.dumps(result, indent=2))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
