# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a minimal Python client for the Awtrix3 smart pixel clock with dual interfaces:
- **Python library** (`awtrix3.py`) - For programmatic integration
- **CLI tool** (`trixctl`) - For command-line usage

## Architecture

### Core Components

**awtrix3.py** - Single-class HTTP client library
- `Awtrix3` class wraps 5 core API endpoints: notify, stats, power, custom_app, play_sound
- Simple constructor: `Awtrix3(host, auth=None)`
- All methods use `requests` library for HTTP calls to `http://{host}/api/*`
- Methods return JSON responses or None, raise exceptions on HTTP errors

**trixctl** - Executable CLI wrapper
- Uses `argparse` with subcommands mapping 1:1 to library methods
- Global `--host` (required), `--username`, `--password` options
- Imports and instantiates `Awtrix3` class, prints JSON results
- Commands: `notify TEXT`, `stats`, `power on|off`, `app NAME TEXT`, `sound NAME`

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
./trixctl --host 192.168.1.100 stats

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

## Working Guidelines

- When picking up a GitHub issue, update its status to "In progress" to indicate active work
- Whenever I ask to pick up a GitHub issue, make sure to update its status to In progress so I know you are working on it
- Once ready for review, move the issue to In Review status
- NEVER move an issue to Done or merge a PR myself
- Whenever I ask to review the backlog, assume I want to:
  * Move any ready-to-execute issues to Ready status
  * Comment and tag the user when backlog issues are not ready for execution
- Always update the issue status when starting work:
  * If an issue is in Backlog, move it to Ready first
  * Then move the issue to In Progress
  * When ready for review, move to In Review
  * Wait for human review and further instructions before closing or merging