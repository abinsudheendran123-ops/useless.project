# 📋 Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Run Setup Script

**Windows:**
```bash
setup.bat
```

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

### Step 2: Start Development Server
```bash
npm run dev
```

### Step 3: Open in Browser
Navigate to: **http://localhost:3000**

---

## 🎮 What You Get

✨ **Beautiful Minecraft-Themed UI**
- Authentic pixel-perfect design
- Responsive on mobile & desktop
- Dark mode optimized

⚡ **Battery Monitoring**
- Real-time battery percentage
- Charging status
- 3 difficulty modes for roasts:
  - 🟢 Peaceful (Gentle)
  - 🟡 Hard (Savage)
  - 🔴 Hardcore (Toxic)

🔊 **Fun Features**
- Text-to-speech roasts
- Desktop notifications
- Battery state simulation
- Live activity log

---

## 📝 Features Overview

### Difficulty Modes

#### 🟢 Peaceful Mode
*Gentle battery reminders*
```
"100% charged! You're storing more energy than a chest full of Redstone."
"Battery levels stable. Safe from Creeper detonations."
```

#### 🟡 Hard Mode (Default)
*Savage Minecraft roasts*
```
"100% on AC power! You're literally smelting your battery like raw iron."
"Half a heart left! Plug in the charger before you drop all your code."
```

#### 🔴 Hardcore Mode
*Full creeper chaos*
```
"TSSSSS... UNPLUG THE CABLE BEFORE YOUR LAPTOP BLOWS UP!"
"LITHIUM CELL TORTURE DETECTED. YOU PLAY LIKE A NOOB!"
```

### Simulation Buttons
- **100% Cook** - Simulate fully charged on AC
- **85% Stress** - Simulate high battery usage
- **4% Panic** - Simulate critical battery
- **Live Real** - Use actual battery stats

### Advanced Features
- **Say Roast** 🔊 - Hear your battery roast aloud
- **Trigger Popup** 📢 - Get desktop notifications
- **Blind Mode** ⚠️ - Full screen error overlay

---

## 🔧 Development

### Project Structure
```
app/                 # React components
├── page.tsx         # Home page
├── layout.tsx       # Layout with Tailwind
└── api/             # API routes
    ├── stats/       # Get battery stats
    ├── simulate/    # Simulate battery
    ├── reset/       # Reset simulation
    ├── speak/       # Text-to-speech
    └── notify/      # Notifications

components/         # Reusable React components
├── MinecraftFrame.tsx
```

### Technologies Used
- **React 18** - UI library
- **Next.js 14** - Framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Python** - Backend APIs

---

## 🌐 Deploy to Vercel

### Option 1: Via GitHub (Easiest)
1. Push to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Click "Import Project"
4. Select your repo
5. Deploy! 🎉

### Option 2: Via Vercel CLI
```bash
npm install -g vercel
vercel
```

### See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed guide

---

## 🐛 Troubleshooting

### "npm: command not found"
- Install Node.js: https://nodejs.org

### "python: command not found"
- Install Python: https://python.org

### "Port 3000 already in use"
```bash
# Use different port
npm run dev -- -p 3001
# Then open http://localhost:3001
```

### Text-to-Speech not working
```bash
# Install pyttsx3
pip install pyttsx3
# Then restart: npm run dev
```

### Desktop Notifications not working
```bash
# Install plyer
pip install plyer
# Then restart: npm run dev
```

---

## 📚 Learning Resources

- [Next.js Docs](https://nextjs.org/docs) - Framework guide
- [React Docs](https://react.dev) - Component library
- [Tailwind CSS](https://tailwindcss.com) - Styling
- [Python](https://python.org/doc) - Backend APIs
- [Vercel](https://vercel.com/docs) - Deployment

---

## 🎮 Have Fun!

That's it! You now have a fully functional Minecraft-themed battery monitor ready to deploy. 

### Next Steps:
1. ✅ Run locally with `npm run dev`
2. ✅ Try different difficulty modes
3. ✅ Customize roasts in code
4. ✅ Deploy to Vercel
5. ✅ Share with friends! 🎉

---

**Made with ❤️ using React, Tailwind CSS, and Python**

Questions? Check out [DEPLOYMENT.md](DEPLOYMENT.md) or [README.md](README.md)
