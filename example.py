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

# Turn off the display
awtrix.power(False)