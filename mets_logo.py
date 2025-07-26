#!/usr/bin/env python3

from awtrix3 import Awtrix3

# Initialize client - replace with your Awtrix3 device IP
# You can also use: python mets_logo.py --host YOUR_IP if you have trixctl configured
awtrix = Awtrix3("192.168.1.128")  # Replace with your device IP

# Create Mets logo custom app
# Using baseball icon (2099) with Mets colors
awtrix.custom_app(
    "mets_logo", 
    "Let's Go Mets!",  # Let's Go Mets!
    icon=2099,  # Baseball icon
    color="#FF6600",  # Mets orange
    background="#002D72",  # Mets blue
    duration=5000  # Show for 5 seconds
)

print("Mets logo displayed on Awtrix3!")
print("Use 'trixctl app delete mets_logo' to remove it")