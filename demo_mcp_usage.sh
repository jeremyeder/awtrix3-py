#!/bin/bash
# MCP Usage Demo for Awtrix3-py
# This script demonstrates using the MCP server with Claude Code

set -e

echo "🎮 Awtrix3-py MCP Server Usage Demo"
echo "==================================="
echo ""

echo "📱 Connected to Awtrix3 device via MCP server"
echo "   Using configuration from ~/.trixctl.conf"
echo ""

# Simulate Claude Code CLI prompt
echo "claude-code> /trixctl stats"
sleep 2
echo ""

# Show realistic stats output
echo "📊 Device Statistics"
echo "===================="
echo ""
echo "┌─────────────────────┬────────────────────┐"
echo "│ Metric              │ Value              │"
echo "├─────────────────────┼────────────────────┤"
echo "│ Uptime              │ 2d 14h 32m 18s     │"
echo "│ Free Heap           │ 187,432 bytes      │"
echo "│ Wifi Signal         │ -42 dBm (Excellent)│"
echo "│ Battery Level       │ 87%                │"
echo "│ Temperature         │ 23.4°C             │"
echo "│ Brightness          │ 80                 │"
echo "│ Current App         │ weather            │"
echo "│ Apps in Loop        │ 4                  │"
echo "│ Matrix Size         │ 32x8               │"
echo "│ Firmware Version    │ 0.90               │"
echo "└─────────────────────┴────────────────────┘"
echo ""
sleep 3

echo "✅ Command completed successfully!"
echo ""

echo "claude-code> /trixctl notify \"Demo successful!\""
sleep 1
echo "📨 Notification sent to device"
echo "✅ Command completed successfully!"
echo ""

echo "claude-code> /trixctl app list"
sleep 1
echo "📱 Active Apps in Loop:"
echo "• weather (Current: Clear, 72°F)"
echo "• clock (Digital display)"  
echo "• calendar (Meeting @ 3pm)"
echo "• mets_logo (Let's Go Mets!)"
echo "✅ Command completed successfully!"
echo ""

echo "claude-code> /trixctl power off"
sleep 1
echo "🔌 Device powered off"
echo "✅ Command completed successfully!"
echo ""

echo "claude-code> /trixctl power on"
sleep 1
echo "🔌 Device powered on"
echo "✅ Command completed successfully!"
echo ""

echo "🎯 MCP Integration Benefits:"
echo "• Seamless Claude Code integration"
echo "• No additional setup after initial config"
echo "• Full trixctl command compatibility"
echo "• Real-time device control from chat"
echo "• Professional formatted output"
echo ""

echo "🎉 MCP Demo Complete!"
echo "The Awtrix3 MCP server provides effortless device control"
echo "directly from your Claude Code conversations."