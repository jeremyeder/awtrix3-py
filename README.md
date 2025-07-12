# Awtrix3 Python Client

A ridiculously simple Python client for the [Awtrix3](https://github.com/Blueforcer/awtrix3) smart pixel clock.

## Installation

```bash
pip install requests
```

## Usage

```python
from awtrix3 import Awtrix3

# Connect to your device
awtrix = Awtrix3("192.168.1.100")  # Replace with your device IP

# Send notification
awtrix.notify("Hello World!")

# Create custom app
awtrix.custom_app("temp", "22°C", color="#FF0000")

# Get device stats
stats = awtrix.stats()

# Play sound
awtrix.play_sound("notification")

# Power control
awtrix.power(False)  # Turn off
awtrix.power(True)   # Turn on
```

## Authentication

If your device requires authentication:

```python
awtrix = Awtrix3("192.168.1.100", auth=("username", "password"))
```

## Methods

- `notify(text)` - Send simple text notification
- `stats()` - Get device statistics  
- `power(on=True)` - Power control
- `custom_app(name, text, **kwargs)` - Create/update custom app
- `play_sound(name)` - Play a sound

That's it!