# Awtrix3 Python Client

A ridiculously simple Python client for the [Awtrix3](https://github.com/Blueforcer/awtrix3) smart pixel clock.

## Installation

### From PyPI (Recommended)

```bash
pip install awtrix3
```

### From Source

```bash
git clone https://github.com/jeremyeder/awtrix3-py.git
cd awtrix3-py
pip install -e .
```

## CLI Usage

Use `trixctl` for quick command-line control of your Awtrix3 device:

> **Note**: After installing from PyPI, the `trixctl` command will be available globally. If installing from source, you can use `./trixctl` or `python -m awtrix3`.

### Configuration Setup (Optional but Recommended)

Create a config file to avoid repeating common options:

```bash
# Generate a config file template
trixctl --generate-config

# Edit the generated ~/.trixctl.conf file
# Set your device IP and username (if needed)
```

For secure password handling, use an environment variable:
```bash
export TRIXCTL_PASSWORD="your_password"
```

### I want to send a quick message to my display
```bash
# With config file (host already set)
trixctl notify "Let's go Mets!"
trixctl notify "Let's go Mets!"

# Without config file
trixctl --host 192.168.1.128 notify "Let's go Mets!"
```

### I want to check if my device is working
```bash
trixctl stats
```

### I want to turn my display off at night
```bash
trixctl power off
```

### I want to turn my display back on
```bash
trixctl power on
```

### I want to display ongoing information (like temperature)
```bash
trixctl app create temperature "72°F"
trixctl app create calendar "Meeting @ 3pm"
```

### I want to manage my custom apps
```bash
# List all apps currently in the display loop
trixctl app list

# Delete a specific custom app
trixctl app delete temperature
```

### I want to play a notification sound
```bash
trixctl sound notification
trixctl sound alarm
```

### I want to backup my device settings
```bash
# Create backup file
trixctl backup my_device.json

# Preview what a restore would do
trixctl restore my_device.json --dry-run

# Restore settings from backup
trixctl restore my_device.json
```

### I want to configure my device as a minimal clock
```bash
# Minimal 24-hour clock (strips down to essentials)
trixctl clock

# 12-hour format with seconds  
trixctl clock --12hr --seconds

# Keep all settings, just change time format
trixctl clock --12hr --full
```

### I want to apply custom device settings
```bash
# Set brightness and time format
trixctl settings '{"brightness": 60, "timeFormat": "HH:mm:ss"}'

# Complex configuration
trixctl settings '{
  "brightness": 100,
  "timeFormat": "hh:mm A",
  "showWeekday": true,
  "centerText": false
}'
```

### I need to authenticate with my device
```bash
# Set username in config file and password via environment:
export TRIXCTL_PASSWORD="secret"
trixctl notify "Let's go Mets!"

# Or override everything via CLI:
trixctl --host 192.168.1.128 --username admin --password secret notify "Let's go Mets!"
```

### Bash Completion (Linux/Mac)

Enable tab completion for faster command entry.

**macOS Prerequisites:**
macOS ships with an old bash version (3.2 from 2007). For best completion experience, install modern bash via Homebrew:

```bash
# Install modern bash and completion support
brew install bash bash-completion@2

# Add to your shell profile (~/.bash_profile or ~/.zshrc):
export PATH="/opt/homebrew/bin:$PATH"
```

**Installation:**

```bash
# System-wide installation (requires sudo):
sudo cp trixctl-completion.bash /etc/bash_completion.d/trixctl

# User-specific installation:
mkdir -p ~/.bash_completion.d
cp trixctl-completion.bash ~/.bash_completion.d/trixctl
echo 'source ~/.bash_completion.d/trixctl' >> ~/.bashrc
source ~/.bashrc
```

Now you can use tab completion:
```bash
trixctl <TAB>          # Shows all commands and options
trixctl power <TAB>    # Shows 'on' and 'off'
trixctl --host <TAB>   # Shows common IP suggestions
```

## Python Library Usage

For developers who want to integrate Awtrix3 into their Python applications:

```python
from awtrix3 import Awtrix3

# Connect to your device
awtrix = Awtrix3("192.168.1.128")

# Send notification
awtrix.notify("Let's go Mets!")

# Create custom app
awtrix.custom_app("temperature", "72°F")

# Manage custom apps
apps = awtrix.list_apps()              # Get all apps in loop
awtrix.delete_app("temperature")       # Delete specific app

# Get device stats
stats = awtrix.stats()

# Play sound
awtrix.play_sound("notification")

# Power control
awtrix.power(False)  # Turn off
awtrix.power(True)   # Turn on

# Backup and restore settings
awtrix.backup_settings("backup.json")  # Save to file
settings = awtrix.get_settings()       # Get current settings
awtrix.restore_settings("backup.json") # Restore from file

# Clock profile configuration
awtrix.clock_profile(format_24hr=True, show_seconds=False)  # Minimal 24hr clock
awtrix.clock_profile(format_24hr=False, show_seconds=True)  # 12hr with seconds

# Custom settings configuration
awtrix.configure_settings({"brightness": 80, "timeFormat": "HH:mm"})
```

### Authentication

If your device requires authentication:

```python
awtrix = Awtrix3("192.168.1.128", auth=("username", "password"))
```

### Available Methods

- `notify(text)` - Send simple text notification
- `stats()` - Get device statistics  
- `power(on=True)` - Power control
- `custom_app(name, text, **kwargs)` - Create/update custom app
- `delete_app(name)` - Delete a custom app by name
- `list_apps()` - Get list of apps currently in the loop
- `play_sound(name)` - Play a sound
- `get_settings()` - Get current device settings
- `backup_settings(filepath=None)` - Backup device settings to file or dict
- `restore_settings(backup_data)` - Restore settings from backup file or dict
- `clock_profile(format_24hr=True, show_seconds=False, minimal=True)` - Configure minimal clock display
- `configure_settings(settings)` - Apply custom device settings with JSON payload

## MCP Server Integration

This project includes a Model Context Protocol (MCP) server that enables `/trixctl` commands directly from Claude Code CLI.

### Installation Demo

![MCP Installation Demo](demo_mcp_install.gif)

### Usage Demo

![MCP Usage Demo](demo_mcp_usage.gif)

### Setup for Claude Desktop

1. Install MCP dependencies:
```bash
pip install -e .[mcp]
```

2. Add to Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):
```json
{
  "mcpServers": {
    "trixctl": {
      "command": "python",
      "args": ["/absolute/path/to/awtrix3-py/mcp_server.py"]
    }
  }
}
```

### Usage in Claude Code
```
/trixctl notify "Hello World"
/trixctl stats
/trixctl power on
/trixctl app create test "Testing MCP"
/trixctl backup /tmp/backup.json
```

The MCP server provides full compatibility with the trixctl CLI and uses your existing `~/.trixctl.conf` configuration.

## Attribution

Thanks to [@blueforcer](https://github.com/Blueforcer) for creating the amazing [Awtrix3](https://github.com/Blueforcer/awtrix3) project that inspired this client, and to [@claude](https://claude.ai) for the implementation assistance.

That's it!