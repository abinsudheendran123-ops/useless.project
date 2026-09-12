# 🏗️ Project Architecture Guide

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         BROWSER (Client)                         │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  MinecraftFrame.tsx (React Component)                    │   │
│  │  ├── UI State Management (useState, useEffect)           │   │
│  │  ├── Battery stats display                               │   │
│  │  ├── Difficulty mode selector                            │   │
│  │  ├── Simulation controls                                 │   │
│  │  └── Event handlers (fetch to API)                       │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────┬───────────────────────────────┘
                                  │ HTTP/REST API Calls
                    ┌─────────────┴──────────────┐
                    │                            │
          ┌─────────▼──────────┐    ┌──────────▼─────────┐
          │   LOCAL DEV        │    │   VERCEL CLOUD     │
          │  (npm run dev)     │    │  (Production)      │
          └─────────┬──────────┘    └────────┬──────────┘
                    │                        │
        ┌───────────▼──────────┐  ┌──────────▼─────────┐
        │  Next.js API Routes  │  │  Python Functions  │
        │  (app/api/*.ts)      │  │  (api/*.py)        │
        └───────────┬──────────┘  └────────┬──────────┘
                    │                      │
        ┌───────────▼──────────────────────▼──────────┐
        │           Battery Logic & Data               │
        │  ├── Roast Database                          │
        │  ├── Creeper Faces                           │
        │  ├── Difficulty Modes (mild/savage/toxic)    │
        │  ├── Simulation State                        │
        │  └── Abuse Score Calculator                  │
        └───────────┬──────────────────────────────────┘
                    │
        ┌───────────▼──────────┐
        │   Optional Features  │
        │  ├── pyttsx3 (TTS)   │
        │  ├── plyer (notify)  │
        │  └── psutil (battery)│
        └──────────────────────┘
```

---

## Data Flow

### Request/Response Cycle

```
1. USER INTERACTION
   └─> Click button/select mode
       └─> React onClick/onChange handler

2. API CALL
   └─> fetch('/api/stats', {...})
       ├─> Method: POST
       ├─> Body: JSON with mode, percent, plugged
       └─> Headers: Content-Type: application/json

3. SERVER PROCESSING
   ├─ LOCAL: Next.js route (app/api/stats/route.ts)
   │  └─> Receives request
   │      └─> Generate battery stats
   │          └─> Calculate roast
   │              └─> Return JSON
   │
   └─ VERCEL: Python function (api/stats.py)
      └─> Receives Vercel event
          └─> Process similar logic
              └─> Return JSON

4. RESPONSE
   └─> Browser receives JSON
       └─> React updates state
           └─> Component re-renders
               └─> UI displays new stats
```

---

## File Dependency Graph

```
┌─────────────────────────────────────────┐
│     globals.css (Tailwind styles)       │
└────────────────────┬────────────────────┘
                     │
        ┌────────────▼────────────┐
        │   app/layout.tsx        │
        │   (Root layout)         │
        └────────────┬────────────┘
                     │
        ┌────────────▼────────────┐
        │   app/page.tsx          │
        │   (Home page)           │
        ├─> useState, useEffect   │
        ├─> isDeadScreen state    │
        └────────────┬────────────┘
                     │
        ┌────────────▼──────────────────┐
        │  components/MinecraftFrame.tsx│
        │  (Main UI Component)          │
        ├─> Renders all UI elements     │
        ├─> Manages battery data        │
        ├─> Handles API calls           │
        └────────┬─────────────────────┘
                 │
      ┌──────────┼──────────┬──────────────┬──────────┐
      │          │          │              │          │
      ▼          ▼          ▼              ▼          ▼
   stats    simulate    reset         speak      notify
   route      route      route          route      route
   (ts)       (ts)       (ts)           (ts)       (ts)
```

---

## Request/Response Examples

### GET Battery Stats

**Request from Browser:**
```javascript
fetch('/api/stats', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ mode: 'savage' })
})
```

**Response from Server:**
```json
{
  "percent": 75,
  "plugged": false,
  "face": "(•‿•) [SURVIVING]",
  "color": "#55ff55",
  "category": "BALANCED",
  "roast": "20% to 80% range. Don't celebrate yet, Steve.",
  "score": 85
}
```

**UI Update:**
```javascript
{
  face = "(•‿•) [SURVIVING]"
  percent = "75%"
  score = "85/100"
  roast = "20% to 80% range..."
  plugged_status = "🔋 ON BATTERY"
}
```

---

## Environment & Configuration

### Development Environment
```
npm run dev
  ↓
Next.js Dev Server (port 3000)
  ├─ Hot reload on file changes
  ├─ Development build
  └─ Routes to app/api/* (TypeScript)
```

### Production Environment (Vercel)
```
git push → GitHub
  ↓
Vercel Webhook Trigger
  ↓
Vercel Build Process
  ├─ npm install
  ├─ next build
  ├─ Compile TypeScript
  ├─ Optimize CSS
  └─ Package Python functions
      ↓
    Vercel Deployment
  ├─ Edge functions (frontend)
  ├─ Serverless functions (backend)
  └─ CDN distribution
```

---

## Component Tree

```
<html>
  └─ <body> (bg-minecraft-dark)
      └─ <RootLayout>
          └─ <HomePage>
              ├─ {isDeadScreen && <DeadScreenOverlay />}
              └─ <MinecraftFrame>
                  ├─ <Header>
                  │  ├─ Title: "MINECRAFT BATTERY HUD"
                  │  └─ Status: "⚡ AC CONNECTED" or "🔋 ON BATTERY"
                  │
                  ├─ <FaceSlot>
                  │  ├─ Emoji face (based on stats.face)
                  │  └─ Durability text
                  │
                  ├─ <StatsGrid>
                  │  ├─ REDSTONE CHARGE: {percent}%
                  │  └─ CELL INTEGRITY: {score}/100
                  │
                  ├─ <RoastBox>
                  │  └─ "{stats.roast}"
                  │
                  ├─ <LogBox>
                  │  └─ [logs.map(log => <LogEntry />)]
                  │
                  ├─ <ModeSelect>
                  │  ├─ Peaceful (Gentle Reminders)
                  │  ├─ Hard (Savage Roasts) [selected]
                  │  └─ Hardcore (Full Creeper Rage)
                  │
                  ├─ <SimulationButtonGrid>
                  │  ├─ 100% Cook
                  │  ├─ 85% Stress
                  │  ├─ 4% Panic
                  │  └─ Live Real
                  │
                  └─ <ActionButtonGrid>
                     ├─ 🔊 Say Roast
                     ├─ 📢 Trigger Popup
                     └─ ⚠️ Toggle Screen Error
```

---

## State Management Flow

```
MinecraftFrame Component State:

┌──────────────────────────┐
│  stats: BatteryStats     │  ◄── Fetched from /api/stats
├──────────────────────────┤
│ {                        │
│   percent: 75,           │
│   plugged: false,        │
│   face: "(•‿•)",         │
│   color: "#55ff55",      │
│   category: "BALANCED",  │
│   roast: "...",          │
│   score: 85              │
│ }                        │
└──────────────────────────┘

┌──────────────────────────┐
│  mode: 'mild' |          │  ◄── User selected
│      'savage' |          │
│      'toxic'             │
└──────────────────────────┘

┌──────────────────────────┐
│  logs: LogEntry[]        │  ◄── Appended on new roast
├──────────────────────────┤
│ [{                       │
│   timestamp: "12:34:56", │
│   category: "BALANCED",  │
│   message: "..."         │
│ }, ...]                  │
└──────────────────────────┘

┌──────────────────────────┐
│  lastRoast: string       │  ◄── Compared to prevent dupes
└──────────────────────────┘
```

---

## API Routing

### Development (Next.js Routes)
```
GET/POST /api/stats        → app/api/stats/route.ts
GET/POST /api/simulate     → app/api/simulate/route.ts
GET/POST /api/reset        → app/api/reset/route.ts
GET/POST /api/speak        → app/api/speak/route.ts
GET/POST /api/notify       → app/api/notify/route.ts
```

### Production (Vercel Routes)
```
GET/POST /api/stats        → api/stats.py (Python)
GET/POST /api/simulate     → api/simulate.py (Python)
GET/POST /api/reset        → api/reset.py (Python)
GET/POST /api/speak        → api/speak.py (Python)
GET/POST /api/notify       → api/notify.py (Python)
```

---

## Roast Database Structure

```
ROAST_DATABASE
├─ mild
│  ├─ overcharge: "100% charged!..."
│  ├─ high: "Past 80%?..."
│  ├─ critical: "Low battery!..."
│  └─ balanced: "Battery levels stable..."
│
├─ savage
│  ├─ overcharge: "100% on AC power!..."
│  ├─ high: "Past 80% and plugged?..."
│  ├─ critical: "Half a heart left!..."
│  └─ balanced: "20% to 80% range..."
│
└─ toxic
   ├─ overcharge: "TSSSSS...UNPLUG!..."
   ├─ high: "LITHIUM TORTURE!..."
   ├─ critical: "0 JUICE!..."
   └─ balanced: "Barely survived..."

CREEPER_FACES
├─ overcharge: "(≖_≖ ) [CHARGED]"
├─ high: "(`･ω･´) [OVERHEATING]"
├─ critical: "(x_x) [0 HEARTS]"
└─ balanced: "(•‿•) [SURVIVING]"
```

---

## Styling Architecture

```
globals.css (Tailwind Directives)
  ├─ @tailwind base
  ├─ @tailwind components (custom .mc-btn, .mc-slot, etc.)
  ├─ @tailwind utilities
  └─ Font imports & Minecraft overrides

tailwind.config.js
  ├─ Content paths (where Tailwind scans)
  ├─ Extend theme
  │  ├─ fontFamily.minecraft
  │  └─ colors.minecraft.*
  └─ Plugins

MinecraftFrame.tsx
  └─ className="mc-btn bg-blue-900 hover:bg-blue-800"
      ├─ mc-btn (from globals.css)
      ├─ bg-blue-900 (Tailwind utility)
      └─ hover:bg-blue-800 (Tailwind responsive)
```

---

## Deployment Pipeline

```
Local Development
  ├─ npm run dev
  ├─ Test features
  └─ git commit

GitHub Repository
  └─ git push origin main

Vercel Webhook
  └─ Triggers on push

Vercel Build
  ├─ Install dependencies
  ├─ npm run build
  │  ├─ Compile TypeScript
  │  ├─ Build Next.js
  │  └─ Optimize assets
  ├─ Prepare Python functions
  │  └─ api/*.py → Serverless functions
  └─ Generate deployment

Vercel Deployment
  ├─ Edge functions (Frontend)
  │  └─ Global CDN distribution
  ├─ Serverless functions (Backend)
  │  └─ Auto-scaling Python runtimes
  └─ Domain configuration

Live at: yourproject.vercel.app
```

---

## Technology Layers

```
User Interface Layer
  └─ React 18 + TypeScript + Tailwind CSS
     └─ Components: MinecraftFrame, etc.

Routing Layer
  └─ Next.js 14 App Router
     └─ Pages: app/page.tsx, app/layout.tsx

API Layer
  └─ Next.js API Routes / Python Functions
     └─ Endpoints: /api/stats, /api/simulate, etc.

Business Logic Layer
  └─ Battery calculations, roast generation, state management

Data Layer
  └─ In-memory state (development)
     └─ Simulated/real battery data

Infrastructure Layer
  └─ Vercel Serverless (Production)
     └─ Next.js + Python runtime
```

---

## Error Handling Flow

```
User Action
  ↓
Try {
  fetch API
    ↓
  Process response
    ↓
  Update UI
} Catch {
  console.error(error)
  ↓
  Show fallback/retry option
}
```

---

## Performance Characteristics

```
Initial Load
├─ HTML/CSS/JS: ~50KB (optimized)
├─ React bundle: ~35KB (code split)
└─ Tailwind CSS: ~15KB (purged)
Total: ~100KB (with compression)

Runtime Performance
├─ API response time: ~50-100ms
├─ UI re-render: <16ms (60fps)
└─ Sync interval: 2.5 seconds

Deployment
├─ Build time: ~1-2 minutes
├─ Deploy time: ~1 minute
└─ Cold start: ~100ms (first request)
```

---

## Scaling Considerations

### Horizontal Scaling
- ✅ Vercel CDN for static assets
- ✅ Serverless auto-scaling for functions
- ✅ No database overhead (stateless)

### Vertical Optimization
- ✅ Code splitting with Next.js
- ✅ CSS purging with Tailwind
- ✅ Image optimization built-in

### Future Database Integration
```
Client → Next.js API → Database (PostgreSQL/MongoDB)
  ├─ User settings
  ├─ Battery history
  └─ Custom roasts
```

---

This architecture is designed for:
- ✅ **Scalability** - Serverless auto-scaling
- ✅ **Performance** - CDN delivery, optimized bundles
- ✅ **Maintainability** - Clear separation of concerns
- ✅ **Extensibility** - Easy to add features
- ✅ **Reliability** - Vercel managed infrastructure
