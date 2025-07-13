# Awtrix3 Python Client

A ridiculously simple Python client for the [Awtrix3](https://github.com/Blueforcer/awtrix3) smart pixel clock.

## Installation

```bash
git clone https://github.com/jeremyeder/awtrix3-py.git
cd awtrix3-py
pip install requests
```

## CLI Usage

Use `trixctl` for quick command-line control of your Awtrix3 device:

### Configuration Setup (Optional but Recommended)

Create a config file to avoid repeating common options:

```bash
# Generate a config file template
./trixctl --generate-config

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
./trixctl notify "Meeting in 5 minutes!"
./trixctl notify "Coffee ready ☕"

# Without config file
./trixctl --host 192.168.1.100 notify "Meeting in 5 minutes!"
```

### I want to check if my device is working
```bash
./trixctl stats
```

### I want to turn my display off at night
```bash
./trixctl power off
```

### I want to turn my display back on
```bash
./trixctl power on
```

### I want to display ongoing information (like temperature)
```bash
./trixctl app temperature "72°F"
./trixctl app calendar "Meeting @ 3pm"
```

### I want to play a notification sound
```bash
./trixctl sound notification
./trixctl sound alarm
```

### I want to configure my display as a simple clock

Turn your Awtrix3 into a minimal, distraction-free clock:

```bash
# Strip everything down to a basic 24-hour clock (14:30)
./trixctl clock

# 12-hour format with AM/PM (2:30 PM)
./trixctl clock --12hr

# Show seconds in the time display (14:30:45)
./trixctl clock --seconds

# 12-hour format with seconds (2:30:45 PM)
./trixctl clock --12hr --seconds

# Keep other features enabled (weather, apps, etc.)
./trixctl clock --full
```

### I want to apply custom device settings

Send raw JSON configuration to your device:

```bash
# Set custom brightness and time format
./trixctl settings '{"brightness": 80, "timeFormat": "HH:mm"}'

# Disable multiple features at once
./trixctl settings '{"showWeather": false, "showBattery": false, "autoTransition": false}'
```

### I need to authenticate with my device
```bash
# Set username in config file and password via environment:
export TRIXCTL_PASSWORD="secret"
./trixctl notify "Hello!"

# Or override everything via CLI:
./trixctl --host 192.168.1.100 --username admin --password secret notify "Hello!"
```

### Bash Completion (Linux/Mac)

Enable tab completion for faster command entry:

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
./trixctl <TAB>          # Shows all commands and options
./trixctl power <TAB>    # Shows 'on' and 'off'
./trixctl --host <TAB>   # Shows common IP suggestions
```

## Python Library Usage

For developers who want to integrate Awtrix3 into their Python applications:

```python
from awtrix3 import Awtrix3

# Connect to your device
awtrix = Awtrix3("192.168.1.100")

# Send notification
awtrix.notify("Hello World!")

# Create custom app
awtrix.custom_app("temperature", "72°F")

# Get device stats
stats = awtrix.stats()

# Play sound
awtrix.play_sound("notification")

# Power control
awtrix.power(False)  # Turn off
awtrix.power(True)   # Turn on

# Configure as minimal clock
awtrix.clock_profile(format_24hr=True, show_seconds=False, minimal=True)

# Custom settings
awtrix.configure_settings({"brightness": 60, "showWeather": False})
```

### Authentication

If your device requires authentication:

```python
awtrix = Awtrix3("192.168.1.100", auth=("username", "password"))
```

### Available Methods

- `notify(text)` - Send simple text notification
- `stats()` - Get device statistics  
- `power(on=True)` - Power control
- `custom_app(name, text, **kwargs)` - Create/update custom app
- `play_sound(name)` - Play a sound
- `get_settings()` - Get current device settings
- `configure_settings(settings)` - Apply custom settings via JSON payload
- `clock_profile(format_24hr=True, show_seconds=False, minimal=True)` - Configure minimal clock display

## Attribution

Thanks to [@blueforcer](https://github.com/Blueforcer) for creating the amazing [Awtrix3](https://github.com/Blueforcer/awtrix3) project that inspired this client, and to [@claude](https://claude.ai) for the implementation assistance.

That's it!