# Backup and Restore Guide

## Overview

The backup and restore functionality allows you to save and restore Awtrix3 device settings and configurations. This is useful for:

- **Device migration**: Transfer settings between devices
- **Configuration backup**: Save working configurations before experiments
- **Disaster recovery**: Restore settings after device reset
- **Batch deployment**: Apply same settings to multiple devices

## Quick Start

### CLI Usage

```bash
# Create a backup
trixctl --host 192.168.1.128 backup my_device_backup.json

# Restore from backup (with confirmation)
trixctl --host 192.168.1.128 restore my_device_backup.json

# Restore with dry-run (preview only)
trixctl --host 192.168.1.128 restore my_device_backup.json --dry-run

# Force restore without confirmation
trixctl --host 192.168.1.128 restore my_device_backup.json --force
```

### Python Library Usage

```python
from awtrix3 import Awtrix3

awtrix = Awtrix3("192.168.1.128")

# Create backup to file
awtrix.backup_settings("backup.json")

# Get settings without saving to file
settings = awtrix.backup_settings()  # Returns dict

# Restore from file
awtrix.restore_settings("backup.json")

# Restore from dict
awtrix.restore_settings(settings)
```

## Backup Format

Backup files are JSON format with the following structure:

```json
{
  "backup_timestamp": "2025-07-13T12:34:56.789Z",
  "backup_version": "1.0",
  "device_stats": {
    "version": "0.96",
    "battery": 85,
    "uptime": 12345,
    "ip": "192.168.1.128"
  },
  "settings": {
    "brightness": 80,
    "timeFormat": "HH:mm",
    "showClock": true,
    "autoTransition": false
  }
}
```

### Backup Components

- **backup_timestamp**: When backup was created (ISO 8601 format)
- **backup_version**: Backup format version for compatibility
- **device_stats**: Device information at backup time (for reference)
- **settings**: Complete device configuration settings

## CLI Commands

### Backup Command

```bash
trixctl backup <filename> [options]
```

**Arguments:**
- `filename`: JSON file to save backup (required)

**Options:**
- `--include-stats`: Include device statistics in backup

**Examples:**
```bash
# Basic backup
trixctl backup daily_backup.json

# Backup with device stats
trixctl backup full_backup.json --include-stats
```

### Restore Command

```bash
trixctl restore <filename> [options]
```

**Arguments:**
- `filename`: JSON backup file to restore (required)

**Options:**
- `--dry-run`: Preview what would be restored without applying changes
- `--force`: Skip confirmation prompt

**Examples:**
```bash
# Interactive restore (asks for confirmation)
trixctl restore backup.json

# Preview restore without applying
trixctl restore backup.json --dry-run

# Automatic restore without prompts
trixctl restore backup.json --force
```

## Python Library API

### Class Methods

#### `get_settings()`
Get current device settings as dict.

```python
settings = awtrix.get_settings()
```

#### `backup_settings(filepath=None)`
Create backup of device settings.

**Parameters:**
- `filepath` (str, optional): Path to save backup file

**Returns:**
- `dict`: Backup data if filepath is None
- `str`: Filepath where backup was saved if filepath provided

```python
# Save to file
backup_file = awtrix.backup_settings("backup.json")

# Get as dict
backup_data = awtrix.backup_settings()
```

#### `restore_settings(backup_data)`
Restore device settings from backup.

**Parameters:**
- `backup_data` (dict or str): Backup data dict or filepath to backup JSON

**Returns:**
- `dict`: Result of settings update

```python
# Restore from file
result = awtrix.restore_settings("backup.json")

# Restore from dict
result = awtrix.restore_settings(backup_dict)
```

## Use Cases

### Device Migration

```bash
# Backup old device
trixctl --host 192.168.1.128 backup old_device.json

# Restore to new device  
trixctl --host 192.168.1.129 restore old_device.json
```

### Configuration Experiments

```bash
# Backup current config
trixctl backup before_experiment.json

# Make experimental changes...
trixctl settings '{"brightness": 20}'

# Restore if needed
trixctl restore before_experiment.json
```

### Batch Device Setup

```python
# Create template configuration
template_settings = {
    "brightness": 80,
    "timeFormat": "HH:mm", 
    "autoTransition": False
}

devices = ["192.168.1.128", "192.168.1.129", "192.168.1.130"]

for ip in devices:
    awtrix = Awtrix3(ip)
    awtrix.restore_settings({"settings": template_settings})
    print(f"Configured device: {ip}")
```

### Automated Backups

```python
from datetime import datetime
import os

def daily_backup(device_ip):
    awtrix = Awtrix3(device_ip)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backup_{timestamp}.json"
    
    awtrix.backup_settings(backup_file)
    print(f"Daily backup saved: {backup_file}")
    
    # Cleanup old backups (keep last 7 days)
    # ... cleanup logic here

daily_backup("192.168.1.128")
```

## Error Handling

### Common Errors

**File Not Found:**
```
Error: Backup file 'missing.json' not found
```

**Invalid JSON:**
```
Error: Invalid JSON in backup file - Expecting ',' delimiter: line 5 column 8
```

**Missing Settings:**
```
ValueError: Invalid backup data: missing 'settings' key
```

**Network Issues:**
```
Error: HTTPConnectionPool(host='192.168.1.128', port=80): 
Max retries exceeded with url: /api/settings
```

### Best Practices

1. **Test restores**: Use `--dry-run` before actual restore
2. **Backup before changes**: Always backup before major configuration changes
3. **Version compatibility**: Check device stats in backup for version compatibility
4. **Secure storage**: Store backups securely, especially if they contain sensitive settings
5. **Regular backups**: Automate regular backups for important devices

## Bash Completion

Tab completion is available for backup/restore commands:

```bash
trixctl backup <TAB>          # Completes with .json files
trixctl backup file.json --<TAB>  # Shows --include-stats
trixctl restore <TAB>         # Completes with .json files  
trixctl restore file.json --<TAB> # Shows --dry-run --force
```

## Limitations

- **Settings only**: Current implementation backs up settings, not files (icons, melodies)
- **API dependent**: Requires `/api/settings` endpoint availability
- **No encryption**: Backup files are plain JSON (encrypt separately if needed)
- **No compression**: Large configurations create large backup files

## Future Enhancements

Potential improvements for future versions:

- File system backup (icons, melodies, custom apps)
- Encrypted backup support
- Backup compression
- Incremental backups
- Remote backup storage integration
- Backup scheduling and automation

---

**Status**: ✅ Implemented and ready for use  
**Version**: 1.0  
**Last Updated**: 2025-07-13