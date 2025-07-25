#!/usr/bin/env python3

from awtrix3 import Awtrix3

# Initialize client with your Awtrix3 device IP
awtrix = Awtrix3("192.168.1.128")  # Replace with your device IP

# Send a simple notification
awtrix.notify("Let's go Mets!")

# Create a custom app
awtrix.custom_app("weather", "25°C", color="#00FF00")

# Get device stats
stats = awtrix.stats()
print(f"Battery: {stats.get('battery', 'N/A')}%")

# Play a sound
awtrix.play_sound("notification")

# Backup device settings
print("Creating backup...")
backup_data = awtrix.backup_settings("device_backup.json")
print("Backup saved to: device_backup.json")

# You can also get settings without saving to file
settings = awtrix.get_settings()
print(f"Current device has {len(settings)} settings configured")

# Restore from backup (example - don't actually restore in this demo)
# awtrix.restore_settings("device_backup.json")

# Turn off the display
awtrix.power(False)
