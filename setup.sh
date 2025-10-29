#!/bin/bash
# Quick setup script for Discord Meme Bot

set -e

echo "🤖 Discord Meme Bot Setup"
echo "========================="
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "✅ Found Python $PYTHON_VERSION"

# Note about Python 3.13 compatibility
if [[ "$PYTHON_VERSION" == 3.13* ]]; then
    echo "   Note: Python 3.13 detected - audioop-lts will be installed for compatibility"
fi

# Check ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  ffmpeg is not installed."
    echo "   On macOS: brew install ffmpeg"
    echo "   On Ubuntu: sudo apt install ffmpeg"
    exit 1
fi
echo "✅ Found ffmpeg"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv .venv

# Activate and install dependencies
echo "📥 Installing dependencies..."
source .venv/bin/activate
pip install --upgrade pip > /dev/null
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Copy .env.example to .env:"
echo "   cp .env.example .env"
echo ""
echo "2. Edit .env and add your Discord bot token and channel IDs"
echo ""
echo "3. Activate the virtual environment:"
echo "   source .venv/bin/activate"
echo ""
echo "4. Run the bot:"
echo "   python -m bot.main"
echo ""
echo "📖 See README.md for detailed instructions on creating a Discord bot."

