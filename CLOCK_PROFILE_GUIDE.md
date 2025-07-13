# Clock Profile Configuration Guide

## Overview

The clock profile feature allows you to quickly transform your Awtrix3 device into a minimal, distraction-free clock display. This guide covers the configuration flow from a fully-featured display down to a simple clock.

## Quick Start

### CLI Commands

```bash
# Basic minimal clock (24-hour, no seconds)
./trixctl --host 192.168.1.100 clock

# 12-hour format with seconds
./trixctl --host 192.168.1.100 clock --12hr --seconds

# Keep all features but configure as clock
./trixctl --host 192.168.1.100 clock --full --seconds
```

### Python Library

```python
from awtrix3 import Awtrix3

awtrix = Awtrix3("192.168.1.100")

# Minimal 24-hour clock
awtrix.clock_profile()

# 12-hour clock with seconds
awtrix.clock_profile(format_24hr=False, show_seconds=True)

# Custom settings
awtrix.configure_settings({
    "timeFormat": "HH:mm:ss",
    "brightness": 80
})
```

## Configuration Flow

### Step 1: From Full Featured to Minimal

**Default Awtrix3 State:**
- Multiple apps cycling
- Weather displays
- Calendar information
- Notifications
- Transitions and animations
- Various widgets and indicators

**Minimal Clock State:**
- Time display only
- No app transitions
- No additional widgets
- Clean, distraction-free appearance

### Step 2: Clock Format Options

#### Time Format Options

| Format | Description | Example |
|--------|-------------|---------|
| `HH:mm` | 24-hour without seconds | `14:30` |
| `HH:mm:ss` | 24-hour with seconds | `14:30:45` |
| `hh:mm A` | 12-hour without seconds | `2:30 PM` |
| `hh:mm:ss A` | 12-hour with seconds | `2:30:45 PM` |

#### CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `--12hr` | Use 12-hour format | 24-hour |
| `--seconds` | Show seconds | Hidden |
| `--full` | Keep all features | Minimal mode |

### Step 3: Customization

After applying a clock profile, you can fine-tune settings:

```bash
# Custom brightness and format
./trixctl settings '{"brightness": 50, "timeFormat": "HH:mm"}'

# Re-enable specific features
./trixctl settings '{"showWeekday": true, "showCalendar": false}'
```

## Configuration Examples

### Bedroom Clock (Minimal, Dim)
```bash
./trixctl clock
./trixctl settings '{"brightness": 20}'
```

### Kitchen Clock (Readable, With Seconds)
```bash
./trixctl clock --seconds
./trixctl settings '{"brightness": 90}'
```

### Office Clock (12-hour Format)
```bash
./trixctl clock --12hr --seconds
```

### Living Room Display (Keep Some Features)
```bash
./trixctl clock --full
./trixctl settings '{"showWeekday": true, "brightness": 70}'
```

## Minimal Settings Profile

When using `minimal=True` (default), the following settings are applied:

```json
{
  "timeFormat": "HH:mm",
  "dateFormat": "",
  "autoTransition": false,
  "brightness": 80,
  "transitionTime": 0,
  "apps": [],
  "showWeekday": false,
  "showClock": true,
  "showCalendar": false,
  "temperatureUnit": "",
  "batteryLevel": false,
  "scrollSpeed": 0
}
```

## Reverting Changes

To restore full functionality:

```bash
# Reset to default settings (requires device restart)
./trixctl settings '{
  "autoTransition": true,
  "showWeekday": true,
  "showCalendar": true,
  "transitionTime": 500
}'
```

## Python Integration Examples

### Smart Home Integration
```python
# Morning routine: bright clock
awtrix.clock_profile(show_seconds=True)
awtrix.configure_settings({"brightness": 100})

# Night routine: dim clock
awtrix.clock_profile(show_seconds=False)
awtrix.configure_settings({"brightness": 10})
```

### Meeting Room Display
```python
# During meetings: minimal distraction
awtrix.clock_profile(minimal=True)

# Between meetings: full information
awtrix.clock_profile(minimal=False)
awtrix.configure_settings({"showCalendar": True})
```

## Troubleshooting

### Common Issues

**Clock doesn't appear:**
- Verify device connectivity: `./trixctl stats`
- Check power state: `./trixctl power on`

**Format not updating:**
- Some format changes require device restart
- Try power cycling: `./trixctl power off && sleep 2 && ./trixctl power on`

**Settings not persisting:**
- Ensure JSON payload is valid
- Check device firmware version compatibility

### Validation Commands

```bash
# Test connection
./trixctl stats

# Verify clock is configured
./trixctl settings '{"showClock": true}'

# Check current time format
./trixctl notify "Format test: check display"
```

## API Reference

### Library Methods

#### `clock_profile(format_24hr=True, show_seconds=False, minimal=True)`
Configure device as a minimal clock.

**Parameters:**
- `format_24hr` (bool): Use 24-hour format, default True
- `show_seconds` (bool): Show seconds in time display, default False  
- `minimal` (bool): Strip down to minimal settings, default True

#### `configure_settings(settings)`
Update device settings with custom JSON payload.

**Parameters:**
- `settings` (dict): JSON object with device settings

### CLI Commands

#### `trixctl clock [options]`
Configure minimal clock profile.

**Options:**
- `--12hr`: Use 12-hour format (default: 24-hour)
- `--seconds`: Show seconds in time display
- `--full`: Keep all features (default: minimal mode)

#### `trixctl settings <json_payload>`
Configure device settings with custom JSON.

---

**Status**: ✅ Configuration guide complete  
**Last Updated**: 2025-07-13  
**Related**: Issue #7 - Stripped down clock profile