# 🚀 Deployment Guide - Minecraft Battery HUD

## Quick Start - Deploy to Vercel in 3 Steps

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit: Minecraft Battery HUD"
git remote add origin https://github.com/YOUR_USERNAME/minecraft-battery-hud.git
git branch -M main
git push -u origin main
```

### Step 2: Connect to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Sign in with GitHub
3. Click "New Project"
4. Select your repository
5. Click "Import"

### Step 3: Deploy
Vercel automatically detects Next.js + Python setup and deploys! 🎉

---

## Local Development Setup

### Prerequisites
- **Node.js 18+** - [Download](https://nodejs.org)
- **Python 3.11+** - [Download](https://python.org)
- **Git** - [Download](https://git-scm.com)

### Installation

1. **Clone/Setup the project:**
```bash
cd c:\Users\abins\Downloads\project
```

2. **Install Node.js dependencies:**
```bash
npm install
```

3. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

4. **For full local features (optional):**
```bash
# Text-to-speech and notifications
pip install psutil pyttsx3 plyer
```

5. **Run development server:**
```bash
npm run dev
```

6. **Open in browser:**
   - Navigate to `http://localhost:3000`

---

## Vercel Deployment Configuration

The `vercel.json` file is already configured for:
- ✅ Next.js 14 framework detection
- ✅ Python 3.11 serverless functions
- ✅ Automatic build and start commands
- ✅ Environment variable support

### Environment Variables on Vercel

Add these in Vercel Dashboard → Settings → Environment Variables:

```
VERCEL=true
REACT_APP_API_URL=https://your-project.vercel.app
```

---

## Project Structure

```
📦 minecraft-battery-hud/
│
├── 📂 app/                          # Next.js App Router
│   ├── 📄 layout.tsx                # Root layout
│   ├── 📄 page.tsx                  # Home page
│   └── 📂 api/                      # Next.js API routes
│       ├── stats/route.ts           # Battery stats
│       ├── simulate/route.ts        # Simulation
│       ├── reset/route.ts           # Reset
│       ├── speak/route.ts           # Text-to-speech
│       └── notify/route.ts          # Notifications
│
├── 📂 components/                   # React components
│   └── 📄 MinecraftFrame.tsx        # Main UI component
│
├── 📂 api/                          # Python serverless functions
│   ├── 📄 stats.py                  # Battery stats (Python)
│   ├── 📄 simulate.py               # Simulation (Python)
│   ├── 📄 reset.py                  # Reset (Python)
│   ├── 📄 speak.py                  # Text-to-speech (Python)
│   └── 📄 notify.py                 # Notifications (Python)
│
├── 📂 public/                       # Static files
│
├── 📄 globals.css                   # Global Tailwind styles
├── 📄 tailwind.config.js            # Tailwind config
├── 📄 next.config.js                # Next.js config
├── 📄 postcss.config.js             # PostCSS config
├── 📄 tsconfig.json                 # TypeScript config
├── 📄 vercel.json                   # Vercel deployment config
├── 📄 package.json                  # Node dependencies
├── 📄 requirements.txt               # Python dependencies
└── 📄 README.md                     # Project documentation
```

---

## Build & Production

### Build for Production
```bash
npm run build
npm run start
```

### Vercel Builds Automatically
Once deployed to Vercel:
- Every push to `main` branch triggers automatic deployment
- Build logs available in Vercel Dashboard
- Automatic preview deployments for pull requests

---

## Features & Limitations

### ✅ Works Everywhere (Vercel + Local)
- Minecraft-themed UI
- Battery percentage simulation
- Multiple difficulty modes
- Responsive design

### 🏠 Local-Only Features
These require running locally with Python packages installed:
- **Real Battery Monitoring** (psutil)
- **Text-to-Speech** (pyttsx3)
- **Desktop Notifications** (plyer)

### ☁️ Vercel-Only Limitation
Serverless functions on Vercel don't have:
- Direct OS access (battery info)
- Audio output devices
- Desktop notification system

---

## Troubleshooting

### Build Fails on Vercel
**Error:** `Python runtime not found`
- ✅ Solution: `vercel.json` is already configured for Python 3.11
- Make sure all `api/*.py` files are present

### Functions Return 500 Error
**Error:** `Internal Server Error`
- Check Vercel Function Logs: Dashboard → Deployments → Logs
- Verify Python dependencies in `requirements.txt`
- Ensure Python files don't have syntax errors

### API Returns "Not Found"
**Error:** `404 - Not Found`
- Ensure API routes in `app/api/*/route.ts` exist
- Check route names match requests in `MinecraftFrame.tsx`
- Verify Vercel build includes all files

### Features Not Working Locally
**Issue:** Speech/notifications return "skipped"
- Run: `pip install pyttsx3 plyer psutil`
- Restart dev server: `npm run dev`
- May need to run as administrator on Windows

---

## Performance Tips

### Optimize Next.js Build
```bash
npm run build
# Check build size
ls -lh .next/
```

### Monitor Vercel Analytics
- Dashboard → Analytics
- Track deployment times, response times, logs
- Use this to identify bottlenecks

### Python Function Optimization
- Keep functions stateless (no global variables)
- Use native libraries when possible
- Cache expensive computations

---

## Security Best Practices

### Environment Variables
- Never commit `.env.local`
- Use Vercel Dashboard for secrets
- Rotate API keys regularly

### Python Code Safety
- Validate all inputs
- Use type hints
- Avoid `eval()` or `exec()`

### CORS Configuration
```javascript
// Already set in Next.js routes
// For Python Vercel functions, add:
headers: {
  'Access-Control-Allow-Origin': '*'
}
```

---

## Next Steps After Deployment

1. **Custom Domain**
   - Add domain in Vercel Settings
   - Point DNS records to Vercel

2. **Analytics & Monitoring**
   - Enable Vercel Analytics
   - Set up error tracking (Sentry)

3. **CI/CD Pipeline**
   - Add GitHub Actions for testing
   - Automatic deployment on merge

4. **Enhancements**
   - Add database (PostgreSQL)
   - Authentication (NextAuth.js)
   - User profiles for battery history

---

## Support & Resources

- 📖 [Next.js Docs](https://nextjs.org/docs)
- 📚 [Vercel Docs](https://vercel.com/docs)
- 🐍 [Python Serverless Guide](https://vercel.com/docs/functions/serverless-functions/python)
- 🎨 [Tailwind CSS](https://tailwindcss.com)
- 💬 [Vercel Community](https://vercel.com/community)

---

## Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Vercel project connected
- [ ] Environment variables set
- [ ] Build completed successfully
- [ ] Website loads at `yourproject.vercel.app`
- [ ] Battery stats displaying
- [ ] Mode selection working
- [ ] Simulation buttons functional
- [ ] Custom domain configured (optional)

---

## Made with ❤️ - Ready to Deploy! 🚀
