#!/usr/bin/env python3
"""MCP server for Awtrix3 trixctl commands"""

import os
import subprocess
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("trixctl")

# Get path to trixctl script
TRIXCTL_PATH = Path(__file__).parent / "trixctl"


@mcp.tool()
def trixctl(command: str) -> str:
    """
    Execute trixctl commands for Awtrix3 device control.
    
    Args:
        command: The trixctl command to execute (e.g., "notify Hello", "stats", "power on")
        
    Returns:
        Command output or error message
        
    Examples:
        trixctl("notify Hello World")
        trixctl("stats")
        trixctl("power on")
        trixctl("app create test Testing")
    """
    try:
        # Split command into arguments, preserving quoted strings
        import shlex
        args = shlex.split(command)
        
        # Execute trixctl with the provided arguments
        result = subprocess.run(
            [sys.executable, str(TRIXCTL_PATH)] + args,
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout
        )
        
        if result.returncode == 0:
            return result.stdout.strip() if result.stdout else "Command completed successfully"
        else:
            return f"Error: {result.stderr.strip()}" if result.stderr else f"Command failed with exit code {result.returncode}"
            
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds"
    except Exception as e:
        return f"Error executing command: {str(e)}"


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()