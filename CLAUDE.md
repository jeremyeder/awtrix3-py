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

## GitHub Workflow Guidelines

### Issue Status Management
- **Only Jeremy moves issues from Backlog to Ready. Claude only works on Ready issues unless explicitly directed otherwise.**
- Claude workflow: Ready → In Progress → In Review (stop here)
- When picking up a Ready issue, immediately assign yourself and update to "In Progress"
- When work is complete, move to "In Review" and wait for Jeremy's review
- NEVER move issues to Done or merge PRs - Jeremy handles final approval
- **Always close issues when the PR is merged** (not before)

### Issue Creation
- **Claude can create issues to capture great ideas discovered during work. Use sparingly - only for genuinely valuable enhancements or important problems found. Jeremy will triage all new issues.**

### Commit Message Standards
- **Bottom Line Up Front (BLUF)** - Start with concise action summary
- Keep first line under 50 characters for readability  
- Use imperative mood ("Add feature" not "Added feature")
- Include "Addresses #X" to link commits to issues
- Follow with detailed explanation if needed

### Communication Patterns
- Comment on issues with progress updates and completion summaries
- Tag @jeremyeder appropriately for reviews
- Use checkmarks (✅) and code examples in status updates
- Provide clear "ready for review" messaging

### Testing and Validation
- Always test syntax after changes (imports, CLI help, bash completion)
- Validate bash completion with `bash -n`
- Test CLI arguments and help text before committing

### Documentation Requirements
- Update README with new functionality examples
- Create dedicated guides for complex features
- Keep documentation in sync with code changes

### Development Workflow
- You always use feature branches.
