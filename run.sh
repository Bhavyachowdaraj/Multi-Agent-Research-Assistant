#!/bin/bash
# ============================================================
# Nexus AI – Quick Setup Script
# Run this once to install dependencies and start the app
# ============================================================

echo ""
echo "  ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗"
echo "  ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝"
echo "  ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗"
echo "  ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║"
echo "  ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║"
echo "  ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝"
echo ""
echo "  AI Research Assistant - Setup"
echo "============================================================"

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate 2>/dev/null || venv\Scripts\activate 2>/dev/null

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt -q

# Check for .env
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env .env
fi

# Load env
export $(grep -v '^#' .env | xargs) 2>/dev/null

if [ -z "$ANTHROPIC_API_KEY" ] || [ "$ANTHROPIC_API_KEY" = "your_anthropic_api_key_here" ]; then
    echo ""
    echo "⚠️  ANTHROPIC_API_KEY not set in .env"
    echo "   The app will run in demo mode."
    echo "   Add your key to .env to enable real AI responses."
    echo "   Get your key at: https://console.anthropic.com"
    echo ""
fi

echo ""
echo "🚀 Starting Nexus AI on http://localhost:5000"
echo "   Press Ctrl+C to stop"
echo ""

python3 app.py
