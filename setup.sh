#!/bin/bash
# Minecraft Battery HUD - Quick Setup for macOS/Linux

echo ""
echo "==================================="
echo " 🎮 Minecraft Battery HUD Setup 🎮"
echo "==================================="
echo ""

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found! Download from: https://nodejs.org"
    exit 1
fi
echo "✅ Node.js found"

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python not found! Download from: https://python.org"
    exit 1
fi
echo "✅ Python found"

# Install Node dependencies
echo ""
echo "📦 Installing Node.js dependencies..."
npm install || { echo "❌ Failed to install Node dependencies"; exit 1; }
echo "✅ Node dependencies installed"

# Install Python dependencies
echo ""
echo "🐍 Installing Python dependencies..."
python3 -m pip install -r requirements.txt || { echo "❌ Failed to install Python dependencies"; exit 1; }
echo "✅ Python dependencies installed"

# Optional: Install advanced features
echo ""
echo ""
echo "🎵 Optional: Advanced Features"
echo "   - Text-to-Speech: pyttsx3"
echo "   - Desktop Notifications: plyer"
echo "   - Battery Monitoring: psutil"
echo ""
read -p "Install advanced features? (y/n): " install_optional
if [[ $install_optional == "y" || $install_optional == "Y" ]]; then
    echo "Installing advanced features..."
    python3 -m pip install psutil pyttsx3 plyer
    echo "✅ Advanced features installed"
fi

# Create .env.local
if [ ! -f .env.local ]; then
    echo ""
    echo "📝 Creating .env.local..."
    cp .env.example .env.local
    echo "✅ .env.local created"
fi

# Summary
echo ""
echo "==================================="
echo "   ✅ Setup Complete!"
echo "==================================="
echo ""
echo "🚀 To start the development server:"
echo "   npm run dev"
echo ""
echo "📖 Then open: http://localhost:3000"
echo ""
echo "📚 For deployment guide, see: DEPLOYMENT.md"
echo "📘 For more info, see: README.md"
echo ""
echo "==================================="
echo ""
