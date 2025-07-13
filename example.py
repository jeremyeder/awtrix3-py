#!/usr/bin/env python3

from awtrix3 import Awtrix3

# Initialize client with your Awtrix3 device IP
awtrix = Awtrix3("192.168.1.100")  # Replace with your device IP

# Send a simple notification
awtrix.notify("Hello from Python!")

# Create a custom app
awtrix.custom_app("weather", "25°C", color="#00FF00")

# Get device stats
stats = awtrix.stats()
print(f"Battery: {stats.get('battery', 'N/A')}%")

# Play a sound
awtrix.play_sound("notification")

# Configure as minimal clock (24-hour, no seconds)
print("Setting up minimal clock...")
awtrix.clock_profile(format_24hr=True, show_seconds=False, minimal=True)

# Alternative: 12-hour clock with seconds
# awtrix.clock_profile(format_24hr=False, show_seconds=True, minimal=True)

# Custom settings configuration
custom_settings = {
    "brightness": 60,
    "timeFormat": "HH:mm",
    "showClock": True
}
awtrix.configure_settings(custom_settings)

# Turn off the display
awtrix.power(False)