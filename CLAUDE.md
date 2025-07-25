# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a production-ready Python client for the Awtrix3 smart pixel clock with dual interfaces:
- **Python library** (`awtrix3.py`) - For programmatic integration
- **CLI tool** (`trixctl`) - For command-line usage

## Architecture

### Core Components

**awtrix3.py** - Single-class HTTP client library with utility functions
- `Awtrix3` class wraps 9 core API endpoints: notify, stats, power, custom_app, delete_app, list_apps, play_sound, get_settings, backup_settings, restore_settings
- Configuration utilities: `generate_config()`, `load_config()`
- Formatting utilities: `format_stats()`, `format_uptime()`
- Simple constructor: `Awtrix3(host, auth=None)`
- All methods use `requests` library for HTTP calls to `http://{host}/api/*`
- Methods return JSON responses or None, raise exceptions on HTTP errors

**trixctl** - Executable CLI wrapper with comprehensive functionality
- Uses `argparse` with nested subcommands for complex operations
- Global `--host` (required), `--username`, `--password`, `--generate-config` options
- Configuration file support (`~/.trixctl.conf`) with environment variable override
- Commands: `notify TEXT`, `stats`, `power on|off`, `app create|delete|list NAME [TEXT]`, `sound NAME`, `backup FILENAME [--include-stats]`, `restore FILENAME [--dry-run] [--force]`
- Professional output formatting with human-readable stats tables

### Dependencies
- **requests** - Only external dependency for HTTP client functionality
- **Python standard library** - argparse, json, sys, configparser, pathlib, datetime for CLI and utilities

## Development Commands

### Setup
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -e .  # Install in development mode
```

### Testing
```bash
# Run comprehensive test suite (85 tests)
python -m pytest

# Run with coverage
python -m pytest --cov=awtrix3 --cov-report=html

# Test CLI without device (mock tests)
python -m pytest tests/test_cli.py

# Test library functionality
python -m pytest tests/test_awtrix3.py

# Test documentation accuracy
python -m pytest tests/test_docs.py
```

### Code Quality
```bash
# Format code
black awtrix3.py tests/

# Check formatting
black --check awtrix3.py tests/

# Lint code
flake8 awtrix3.py tests/

# Sort imports
isort awtrix3.py tests/
```

### CI/CD
- GitHub Actions workflow runs on Python 3.12 and 3.13
- Automated testing, linting, and formatting checks
- All tests must pass before merge

## Design Principles

- **Production ready** - Comprehensive testing, CI/CD, proper error handling
- **Ridiculously simple** - Single-file components, minimal dependencies
- **CLI-first user experience** - trixctl is the primary interface with professional UX
- **Direct API mapping** - No abstraction layers, 1:1 method-to-endpoint mapping
- **PEP8 compliance** - Black formatting, flake8 linting, isort import sorting
- **User journey documentation** - README organized around "I want to..." scenarios
- **Configuration flexibility** - Config files, environment variables, CLI overrides
- **Backup/restore capabilities** - Full device settings management
- **Comprehensive testing** - 100% import success, mocked HTTP tests, documentation validation

## Key Features

### Configuration Management
- `~/.trixctl.conf` file for default settings
- `TRIXCTL_PASSWORD` environment variable for secure auth
- CLI arguments override config file and environment
- `--generate-config` creates self-documented template

### Backup and Restore
- JSON-based backup format with metadata and timestamps
- CLI: `backup FILENAME [--include-stats]` and `restore FILENAME [--dry-run] [--force]`
- Python: `backup_settings(filepath=None)` and `restore_settings(backup_data)`
- Use cases: device migration, configuration experiments, disaster recovery

### Professional Output
- Human-readable stats table with uptime formatting
- Consistent error messages and exit codes
- JSON output for programmatic use
- Bash completion support for faster CLI usage

### Testing Strategy
- Unit tests for all library methods with mocked HTTP
- CLI tests with argument parsing and configuration
- Documentation tests validating all examples work
- API tests ensuring proper HTTP request/response handling
- 85 total tests with comprehensive coverage
