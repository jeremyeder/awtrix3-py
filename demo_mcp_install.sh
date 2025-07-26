#!/bin/bash
# MCP Installation Demo for Awtrix3-py
# This script demonstrates the installation process for the MCP server integration

set -e

echo "🚀 Awtrix3-py MCP Server Installation Demo"
echo "=========================================="
echo ""

# Simulate a fresh environment
echo "📦 Step 1: Installing MCP dependencies..."
sleep 1
echo "$ pip install -e .[mcp]"
sleep 2
echo "Looking in indexes: https://pypi.org/simple"
echo "Obtaining file:///Users/demo/awtrix3-py"
echo "  Installing build dependencies ... done"
echo "  Checking if build is necessary ... done" 
echo "  Getting requirements to build wheel ... done"
echo "  Installing backend dependencies ... done"
echo "  Preparing metadata (pyproject.toml) ... done"
echo "Collecting mcp>=1.0.0 (from awtrix3[mcp])"
echo "  Downloading mcp-1.0.0-py3-none-any.whl (45 kB)"
echo "     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 45.2/45.2 kB 1.2 MB/s eta 0:00:00"
echo "Installing collected packages: mcp, awtrix3"
echo "  Running setup.py develop for awtrix3"
echo "Successfully installed awtrix3 mcp-1.0.0"
echo ""
sleep 2

echo "✅ MCP dependencies installed successfully!"
echo ""

echo "⚙️  Step 2: Configuring Claude Desktop..."
sleep 1
echo "$ mkdir -p ~/Library/Application\ Support/Claude"
sleep 1

# Show the configuration file creation
echo "$ cat > ~/Library/Application\ Support/Claude/claude_desktop_config.json << 'EOF'"
sleep 1
echo "{"
echo "  \"mcpServers\": {"
echo "    \"trixctl\": {"
echo "      \"command\": \"python\","
echo "      \"args\": [\"/Users/demo/awtrix3-py/mcp_server.py\"]"
echo "    }"
echo "  }"
echo "}"
echo "EOF"
sleep 2
echo ""

echo "📁 Configuration file created at:"
echo "   ~/Library/Application Support/Claude/claude_desktop_config.json"
echo ""

echo "🔍 Step 3: Verifying MCP server..."
sleep 1
echo "$ python mcp_server.py --help"
sleep 1
echo "MCP server for Awtrix3 trixctl commands"
echo "Provides /trixctl command integration for Claude Code"
echo ""

echo "✅ MCP server is ready!"
echo ""

echo "🎯 Next Steps:"
echo "1. Restart Claude Desktop application"
echo "2. Open Claude Code CLI"  
echo "3. Use /trixctl commands directly!"
echo ""

echo "💡 Example usage:"
echo "   /trixctl stats"
echo "   /trixctl notify \"Hello from MCP!\""
echo "   /trixctl power on"
echo ""

echo "🎉 Installation Complete!"
echo "The MCP server is now ready for use with Claude Code."