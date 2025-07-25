# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a minimal Python client for the Awtrix3 smart pixel clock with dual interfaces:
- **Python library** (`awtrix3.py`) - For programmatic integration
- **CLI tool** (`trixctl`) - For command-line usage

## Architecture

### Core Components

**awtrix3.py** - Single-class HTTP client library
- `Awtrix3` class wraps 7 core API endpoints: notify, stats, power, custom_app, delete_app, list_apps, play_sound
- Simple constructor: `Awtrix3(host, auth=None)`
- All methods use `requests` library for HTTP calls to `http://{host}/api/*`
- Methods return JSON responses or None, raise exceptions on HTTP errors

**trixctl** - Executable CLI wrapper
- Uses `argparse` with subcommands mapping 1:1 to library methods
- Global `--host` (required), `--username`, `--password` options
- Imports and instantiates `Awtrix3` class, prints JSON results
- Commands: `notify TEXT`, `stats`, `power on|off`, `app create|delete|list`, `sound NAME`, `backup|restore`

### Dependencies
- **requests** - Only external dependency for HTTP client functionality
- **Python standard library** - argparse, json, sys for CLI

## Development Commands

### Setup
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install requests
```

### Testing
```bash
# Test CLI (requires real Awtrix3 device)
trixctl --host 192.168.1.128 stats

# Test library
python example.py  # Edit IP address first
```

### Making Executable
```bash
chmod +x trixctl  # Already done in repo
```

## Design Principles

- **Ridiculously simple** - Single-file components, minimal dependencies
- **CLI-first user experience** - trixctl is the primary interface
- **Direct API mapping** - No abstraction layers, 1:1 method-to-endpoint mapping
- **PEP8 compliance** - Standard Python formatting and naming conventions
- **User journey documentation** - README organized around "I want to..." scenarios