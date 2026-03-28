#!/bin/bash

# Facebook Automation Quick Start

echo "╔════════════════════════════════════════╗"
echo "║  FACEBOOK AUTOMATION - QUICK START     ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    exit 1
fi

echo "✅ Node.js found"
echo ""

# Step 1: Install dependencies
echo "📦 Step 1: Installing dependencies..."
npm install playwright express dotenv 2>/dev/null
echo "✅ Dependencies installed"
echo ""

# Step 2: Create config
echo "🔧 Step 2: Setting up configuration..."
read -p "Enter Facebook email: " EMAIL
read -sp "Enter Facebook password: " PASSWORD
echo ""

cat > facebook_config.json << EOF
{
  "email": "$EMAIL",
  "password": "$PASSWORD",
  "autoPost": [],
  "monitorInterval": 30000,
  "autoLogin": true,
  "headless": false,
  "enabled": true
}
EOF

echo "✅ Configuration saved"
echo ""

# Step 3: Show usage
echo "🚀 Step 3: Ready to start!"
echo ""
echo "Commands:"
echo "  node facebook_master.js start              - Start automation"
echo "  node facebook_master.js post \"message\"    - Post a message"
echo "  node facebook_master.js config show        - Show config"
echo ""
echo "Quick start:"
echo "  node facebook_master.js start"
echo ""
