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

#### Prerequisites

**macOS users**: The system bash is too old for completion features. Install modern bash via Homebrew:
```bash
brew install bash
# Then restart your terminal or source your shell config
```

**Linux users**: Usually works with the system bash.

#### Installation

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

## Attribution

Thanks to [@blueforcer](https://github.com/Blueforcer) for creating the amazing [Awtrix3](https://github.com/Blueforcer/awtrix3) project that inspired this client, and to [@claude](https://claude.ai) for the implementation assistance.

That's it!