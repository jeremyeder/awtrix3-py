# Clock Profile Configuration Guide

This guide shows how to transform your Awtrix3 device into a minimal clock display using the clock profile functionality.

## Overview

The clock profile functionality allows you to:
- Strip down your Awtrix3 configuration to a minimal clock display
- Choose between 24-hour and 12-hour time formats
- Control whether seconds are displayed
- Quick configuration via CLI commands or Python library

## Quick Start - CLI Commands

### Basic Minimal Clock (24-hour format)
```bash
# Minimal clock with 24-hour format (HH:mm)
./trixctl clock
```

### 12-Hour Format with Seconds
```bash
# 12-hour format with seconds (hh:mm:ss A)
./trixctl clock --12hr --seconds
```

### Full Settings Clock
```bash
# Keep existing device settings, just change time format
./trixctl clock --12hr --full
```

### Custom Settings with JSON
```bash
# Apply custom settings directly
./trixctl settings '{"brightness": 60, "timeFormat": "HH:mm:ss"}'

# Complex custom configuration
./trixctl settings '{
  "brightness": 100,
  "timeFormat": "hh:mm A",
  "showWeekday": true,
  "centerText": false
}'
```

## Python Library Usage

### Basic Clock Configuration
```python
from awtrix3 import Awtrix3

# Connect to device
awtrix = Awtrix3("192.168.1.128")

# Minimal 24-hour clock
awtrix.clock_profile(format_24hr=True, show_seconds=False)

# 12-hour clock with seconds
awtrix.clock_profile(format_24hr=False, show_seconds=True)

# Keep full settings, just change time format
awtrix.clock_profile(format_24hr=False, minimal=False)
```

### Custom Settings Configuration
```python
# Apply custom settings
awtrix.configure_settings({
    "brightness": 80,
    "timeFormat": "HH:mm",
    "showWeekday": False,
    "centerText": True
})

# Advanced configuration
awtrix.configure_settings({
    "brightness": 120,
    "timeFormat": "hh:mm:ss A",
    "showWeekday": True,
    "showDate": True,
    "showTemp": False,
    "autoTransition": True,
    "transitionTime": 500,
    "scrollSpeed": 80,
    "centerText": false
})
```

## Configuration Flow

### From Full-Featured to Minimal Clock

1. **Backup Current Settings** (recommended)
   ```bash
   ./trixctl backup my-backup.json --include-stats
   ```

2. **Apply Minimal Clock Profile**
   ```bash
   ./trixctl clock
   ```

3. **Restore Later if Needed**
   ```bash
   ./trixctl restore my-backup.json
   ```

### Gradual Configuration Approach

Start minimal and add features:

```bash
# 1. Start with minimal clock
./trixctl clock

# 2. Add specific features via JSON
./trixctl settings '{"showWeekday": true}'

# 3. Adjust brightness
./trixctl settings '{"brightness": 120}'

# 4. Change to 12-hour format
./trixctl settings '{"timeFormat": "hh:mm A"}'
```

## Time Format Options

| Format String | Display Example | Description |
|---------------|----------------|-------------|
| `HH:mm`       | `14:30`        | 24-hour without seconds |
| `HH:mm:ss`    | `14:30:45`     | 24-hour with seconds |
| `hh:mm A`     | `2:30 PM`      | 12-hour without seconds |
| `hh:mm:ss A`  | `2:30:45 PM`   | 12-hour with seconds |

## Minimal vs Full Settings

### Minimal Clock Profile (`minimal=True`)
When using minimal mode, these settings are applied:
- `showWeekday: false` - No weekday display
- `showDate: false` - No date display  
- `showTemp: false` - No temperature display
- `showHumidity: false` - No humidity display
- `showBattery: false` - No battery display
- `autoTransition: true` - Smooth transitions
- `transitionTime: 250` - Fast transitions
- `centerText: true` - Center the time display
- `brightness: 80` - Moderate brightness

### Full Settings Profile (`minimal=False`)
Only changes the time format, keeping all other existing device settings intact.

## Common Configurations

### Ultra-Minimal Clock
```bash
./trixctl settings '{
  "timeFormat": "HH:mm",
  "brightness": 40,
  "showWeekday": false,
  "showDate": false,
  "showTemp": false,
  "centerText": true
}'
```

### Bedroom Clock
```bash
./trixctl settings '{
  "timeFormat": "hh:mm A",
  "brightness": 20,
  "showWeekday": false,
  "showDate": false,
  "showSeconds": false,
  "centerText": true
}'
```

### Office Clock
```bash
./trixctl settings '{
  "timeFormat": "HH:mm",
  "brightness": 100,
  "showWeekday": true,
  "showDate": true,
  "showTemp": true,
  "centerText": false
}'
```

## Troubleshooting

### Backup and Restore
Always backup before major changes:
```bash
# Create backup
./trixctl backup before-clock-config.json

# Apply changes
./trixctl clock --12hr

# Restore if needed
./trixctl restore before-clock-config.json
```

### Invalid JSON Settings
```bash
# This will fail with clear error message
./trixctl settings '{"brightness": invalid}'

# Error: Invalid JSON payload - Expecting value: line 1 column 15 (char 14)
```

### Device Connection Issues
```bash
# Test connection first
./trixctl stats

# If connection fails, check:
# 1. Device IP address is correct
# 2. Device is powered on and connected to WiFi
# 3. No authentication required, or credentials are correct
```

## Advanced Usage

### Scripted Configuration
```bash
#!/bin/bash
# setup-minimal-clock.sh

echo "Setting up minimal clock configuration..."
./trixctl backup "backup-$(date +%Y%m%d-%H%M%S).json"
./trixctl clock --12hr --seconds
echo "Clock configured!"
```

### Configuration Validation
```python
from awtrix3 import Awtrix3

awtrix = Awtrix3("192.168.1.128")

# Get current settings to verify
current_settings = awtrix.get_settings()
print(f"Current time format: {current_settings.get('timeFormat')}")
print(f"Current brightness: {current_settings.get('brightness')}")

# Apply and verify
awtrix.clock_profile(format_24hr=False, show_seconds=True)
updated_settings = awtrix.get_settings()
print(f"Updated time format: {updated_settings.get('timeFormat')}")
```

## Settings Reference

Common settings you can configure:

| Setting | Type | Description | Example Values |
|---------|------|-------------|----------------|
| `timeFormat` | string | Time display format | `"HH:mm"`, `"hh:mm A"` |
| `brightness` | integer | Display brightness (0-255) | `80`, `120`, `40` |
| `showWeekday` | boolean | Show day of week | `true`, `false` |
| `showDate` | boolean | Show date | `true`, `false` |
| `showTemp` | boolean | Show temperature | `true`, `false` |
| `centerText` | boolean | Center text display | `true`, `false` |
| `autoTransition` | boolean | Smooth transitions | `true`, `false` |
| `transitionTime` | integer | Transition duration (ms) | `250`, `500`, `1000` |

## Integration Examples

### Home Automation
```python
# Morning routine - bright clock
if time.hour == 7:
    awtrix.configure_settings({"brightness": 120, "showWeekday": true})

# Evening routine - dim clock  
if time.hour == 22:
    awtrix.configure_settings({"brightness": 30, "showWeekday": false})
```

### Event-Based Configuration
```python
# During meetings - minimal display
awtrix.configure_settings({
    "brightness": 20,
    "timeFormat": "HH:mm",
    "showWeekday": false
})

# After meetings - full display
awtrix.configure_settings({
    "brightness": 100,
    "timeFormat": "HH:mm:ss",
    "showWeekday": true,
    "showDate": true
})
```