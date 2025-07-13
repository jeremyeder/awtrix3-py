# Awtrix3 Python Client

A ridiculously simple Python client for the [Awtrix3](https://github.com/Blueforcer/awtrix3) smart pixel clock.

## Installation

```bash
pip install requests
```

## CLI Usage

Use `trixctl` for quick command-line control of your Awtrix3 device:

### I want to send a quick message to my display
```bash
./trixctl --host 192.168.1.100 notify "Meeting in 5 minutes!"
./trixctl --host 192.168.1.100 notify "Coffee ready ☕"
```

### I want to check if my device is working
```bash
./trixctl --host 192.168.1.100 stats
```

### I want to turn my display off at night
```bash
./trixctl --host 192.168.1.100 power off
```

### I want to turn my display back on
```bash
./trixctl --host 192.168.1.100 power on
```

### I want to display ongoing information (like temperature)
```bash
./trixctl --host 192.168.1.100 app temperature "72°F"
./trixctl --host 192.168.1.100 app calendar "Meeting @ 3pm"
```

### I want to play a notification sound
```bash
./trixctl --host 192.168.1.100 sound notification
./trixctl --host 192.168.1.100 sound alarm
```

### I need to authenticate with my device
```bash
./trixctl --host 192.168.1.100 --username admin --password secret notify "Hello!"
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

That's it!