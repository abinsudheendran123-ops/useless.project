import threading
import time
from datetime import datetime
from flask import Flask, render_template_string, jsonify, request
import psutil
from plyer import notification
import pyttsx3

app = Flask(__name__)

simulated_state = None
current_mode = "savage"
abuse_score = 100

ROAST_DATABASE = {
    "mild": {
        "overcharge": "100% charged! You're storing more energy than a chest full of Redstone.",
        "high": "Past 80%? Even iron golems know when to take a rest.",
        "critical": "Low battery! You're about to respawn at your bed with unsaved loot.",
        "balanced": "Battery levels stable. Safe from Creeper detonations."
    },
    "savage": {
        "overcharge": "100% on AC power! You're literally smelting your battery like raw iron in a blast furnace.",
        "high": "Past 80% and still plugged in? You're playing on Hardcore mode with zero armor.",
        "critical": "Half a heart left! Plug in the charger before you take fall damage and drop all your code.",
        "balanced": "20% to 80% range. Don't celebrate yet, Steve. You're still one bad move from a wipe."
    },
    "toxic": {
        "overcharge": "TSSSSS... UNPLUG THE CABLE BEFORE YOUR LAPTOP BLOWS UP LIKE A CHARGED CREEPER!",
        "high": "LITHIUM CELL TORTURE DETECTED. YOU PLAY LIKE A NOOB WHO DIGS STRAIGHT DOWN!",
        "critical": "0 JUICE REMAINING. SAY GOODBYE TO YOUR INVENTORY AND YOUR UNSAVED WORK!",
        "balanced": "You barely survived the night. Stop acting like you know how to manage power."
    }
}

CREEPER_FACES = {
    "overcharge": "(≖_≖ ) [CHARGED]",
    "high": "(`･ω･´) [OVERHEATING]",
    "critical": "(x_x) [0 HEARTS]",
    "balanced": "(•‿•) [SURVIVING]"
}

def speak_text(text):
    def _speak():
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 160)
            engine.say(text)
            engine.runAndWait()
        except Exception:
            pass
    threading.Thread(target=_speak, daemon=True).start()

def get_battery_stats():
    global simulated_state, abuse_score
    if simulated_state:
        pct = simulated_state["percent"]
        plugged = simulated_state["plugged"]
    else:
        battery = psutil.sensors_battery()
        pct = int(battery.percent) if battery else 50
        plugged = battery.power_plugged if battery else False

    if plugged and pct == 100:
        cat = "overcharge"
        color = "#ff5555"
        abuse_score = max(20, abuse_score - 2)
    elif plugged and pct >= 80:
        cat = "high"
        color = "#ffaa00"
        abuse_score = max(40, abuse_score - 1)
    elif not plugged and pct <= 15:
        cat = "critical"
        color = "#aa0000"
        abuse_score = max(10, abuse_score - 3)
    else:
        cat = "balanced"
        color = "#55ff55"
        abuse_score = min(100, abuse_score + 1)

    face = CREEPER_FACES[cat]
    roast = ROAST_DATABASE[current_mode][cat]

    return {
        "percent": pct,
        "plugged": plugged,
        "face": face,
        "color": color,
        "category": cat.upper(),
        "roast": roast,
        "score": abuse_score
    }

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Minecraft Battery HUD</title>
    <link href="https://fonts.cdnfonts.com/css/minecraft-4" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Minecraft', 'Courier New', monospace; image-rendering: pixelated; }
        body {
            background: #141110 url('https://images.unsplash.com/photo-1627856013091-fed6e4e30025?auto=format&fit=crop&w=1200&q=80') center/cover no-repeat;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .mc-frame {
            background: #c6c6c6;
            border: 4px solid #fff;
            border-right-color: #555;
            border-bottom-color: #555;
            box-shadow: 0 0 0 4px #000, 0 20px 40px rgba(0,0,0,0.8);
            width: 480px;
            padding: 20px;
            position: relative;
        }

        .mc-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            color: #3f3f3f;
            font-size: 16px;
            font-weight: bold;
            text-shadow: 2px 2px #fff;
        }

        .mc-slot {
            background: #8b8b8b;
            border: 3px solid #373737;
            border-right-color: #fff;
            border-bottom-color: #fff;
            padding: 16px;
            margin-bottom: 14px;
            text-align: center;
        }

        .pixel-face {
            font-size: 26px;
            color: #55ff55;
            text-shadow: 2px 2px #000;
            margin-bottom: 6px;
        }

        .stat-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 14px;
        }

        .stat-card {
            background: #8b8b8b;
            border: 3px solid #373737;
            border-right-color: #fff;
            border-bottom-color: #fff;
            padding: 10px;
            text-align: center;
        }

        .stat-title {
            font-size: 11px;
            color: #2b2b2b;
            text-shadow: 1px 1px #fff;
            margin-bottom: 4px;
        }

        .stat-val {
            font-size: 22px;
            color: #fff;
            text-shadow: 2px 2px #000;
        }

        .roast-slot {
            background: #2b2b2b;
            border: 3px solid #000;
            border-right-color: #555;
            border-bottom-color: #555;
            color: #ffff55;
            padding: 14px;
            margin-bottom: 14px;
            font-size: 13px;
            line-height: 1.4;
            text-shadow: 1px 1px #000;
            min-height: 50px;
        }

        .mc-log {
            background: #000;
            border: 3px solid #555;
            padding: 8px;
            height: 75px;
            overflow-y: auto;
            color: #aaa;
            font-size: 11px;
            margin-bottom: 14px;
        }

        .mc-btn {
            background: #727272;
            border: 3px solid #fff;
            border-right-color: #373737;
            border-bottom-color: #373737;
            color: #fff;
            text-shadow: 2px 2px #000;
            padding: 8px 12px;
            font-size: 12px;
            cursor: pointer;
            text-transform: uppercase;
        }

        .mc-btn:active {
            border: 3px solid #373737;
            border-right-color: #fff;
            border-bottom-color: #fff;
        }

        .btn-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 6px;
            margin-bottom: 10px;
        }

        .action-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
        }

        .btn-redstone { background: #aa0000; }
        .btn-lapis { background: #0000aa; }
        
        select {
            width: 100%;
            background: #8b8b8b;
            border: 3px solid #373737;
            border-right-color: #fff;
            border-bottom-color: #fff;
            color: #fff;
            padding: 6px;
            font-size: 12px;
            text-shadow: 1px 1px #000;
            margin-bottom: 14px;
        }

        /* Full Screen Red Error Overlay */
        #full-error-screen {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(139, 0, 0, 0.95);
            z-index: 999999;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: #fff;
            text-align: center;
            cursor: pointer;
            box-shadow: inset 0 0 120px #000;
        }
    </style>
</head>
<body>

<!-- Full Screen Red Error Overlay -->
<div id="full-error-screen" onclick="toggleDeadCorner()">
    <div style="font-size: 64px; color: #ff2222; text-shadow: 4px 4px #000; margin-bottom: 16px;">☠ DISPLAY BLINDNESS ☠</div>
    <div style="font-size: 24px; color: #ffff55; text-shadow: 2px 2px #000; margin-bottom: 24px;">BATTERY HARDWARE FAILURE // SCREEN DESTROYED</div>
    <div style="font-size: 16px; line-height: 1.8; color: #fff; max-width: 650px; text-shadow: 2px 2px #000; margin-bottom: 30px;">
        ALL SYSTEM STATUS METRICS ARE HIDDEN & INACCESSIBLE.<br>
        CANNOT READ OS TRAY OR PERCENTAGE LEVELS.<br>
        ONLY EMERGENCY AUDIO SYNTHESIS IS ACTIVE.
    </div>
    <button class="mc-btn" style="background:#555; padding:12px 24px; font-size:14px;">[ CLICK ANYWHERE TO RESTORE HUD ]</button>
</div>

<div class="mc-frame">
    <div class="mc-header">
        <span>MINECRAFT BATTERY HUD</span>
        <span id="pwr-status" style="font-size: 12px;">AC: CHECKING</span>
    </div>

    <div class="mc-slot">
        <div id="mc-face" class="pixel-face">...</div>
        <div id="mc-durability" style="font-size: 11px; color: #fff; text-shadow: 1px 1px #000;">DURABILITY: CALCULATING</div>
    </div>

    <div class="stat-grid">
        <div class="stat-card">
            <div class="stat-title">REDSTONE CHARGE</div>
            <div id="pct-val" class="stat-val">--%</div>
        </div>
        <div class="stat-card">
            <div class="stat-title">CELL INTEGRITY</div>
            <div id="abuse-val" class="stat-val">--/100</div>
        </div>
    </div>

    <div class="roast-slot" id="roast-box">
        Connecting to Redstone circuit...
    </div>

    <div class="mc-log" id="mc-log">
        <div>[SYSTEM] World spawned. Monitoring laptop sensors...</div>
    </div>

    <select id="mode-select" onchange="changeMode(this.value)">
        <option value="mild">Difficulty: Peaceful (Gentle Reminders)</option>
        <option value="savage" selected>Difficulty: Hard (Savage Roasts)</option>
        <option value="toxic">Difficulty: Hardcore (Full Creeper Rage)</option>
    </select>

    <div class="btn-grid">
        <button class="mc-btn" onclick="sim(100, true)">100% Cook</button>
        <button class="mc-btn" onclick="sim(85, true)">85% Stress</button>
        <button class="mc-btn" onclick="sim(4, false)">4% Panic</button>
        <button class="mc-btn" onclick="resetSim()">Live Real</button>
    </div>

    <div class="action-grid">
        <button class="mc-btn btn-lapis" onclick="triggerSpeak()">🔊 Say Roast</button>
        <button class="mc-btn btn-redstone" onclick="triggerNotify()">Trigger Popup</button>
        <button class="mc-btn" style="background: #1e1e1e; grid-column: span 2; border-color: #ff5555; color: #ff5555;" onclick="toggleDeadCorner()">⚠️ Toggle Screen Error (Blind Mode)</button>
    </div>
</div>

<script>
    let lastRoast = "";
    let isDeadScreen = false;

    async function sync() {
        const res = await fetch('/api/stats');
        const d = await res.json();

        document.getElementById('mc-face').innerText = d.face;
        document.getElementById('mc-face').style.color = d.color;
        document.getElementById('pct-val').innerText = d.percent + '%';
        document.getElementById('abuse-val').innerText = d.score + '/100';
        document.getElementById('mc-durability').innerText = `DURABILITY: ${d.score}%`;

        document.getElementById('pwr-status').innerText = d.plugged ? '⚡ AC CONNECTED' : '🔋 ON BATTERY';
        document.getElementById('pwr-status').style.color = d.plugged ? '#00aa00' : '#ff5555';

        document.getElementById('roast-box').innerText = '"' + d.roast + '"';

        if (d.roast !== lastRoast) {
            lastRoast = d.roast;
            const log = document.getElementById('mc-log');
            const t = new Date().toLocaleTimeString();
            log.innerHTML += `<div>[${t}] ${d.category}: ${d.roast}</div>`;
            log.scrollTop = log.scrollHeight;
        }
    }

    async function sim(p, plug) {
        await fetch('/api/simulate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({percent: p, plugged: plug})
        });
        sync();
    }

    async function resetSim() {
        await fetch('/api/reset', { method: 'POST' });
        sync();
    }

    async function changeMode(mode) {
        await fetch('/api/mode', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({mode: mode})
        });
        sync();
    }

    async function triggerSpeak() { await fetch('/api/speak'); }
    async function triggerNotify() { await fetch('/api/notify'); }

    function toggleDeadCorner() {
        const overlay = document.getElementById('full-error-screen');
        isDeadScreen = !isDeadScreen;
        overlay.style.display = isDeadScreen ? 'flex' : 'none';
    }

    setInterval(sync, 2500);
    sync();
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/api/stats")
def stats():
    return jsonify(get_battery_stats())

@app.route("/api/mode", methods=["POST"])
def set_mode():
    global current_mode
    current_mode = request.get_json().get("mode", "savage")
    return jsonify({"status": "updated", "mode": current_mode})

@app.route("/api/simulate", methods=["POST"])
def simulate():
    global simulated_state
    simulated_state = request.get_json()
    return jsonify({"status": "simulated"})

@app.route("/api/reset", methods=["POST"])
def reset():
    global simulated_state
    simulated_state = None
    return jsonify({"status": "reset"})

@app.route("/api/notify")
def notify():
    data = get_battery_stats()
    notification.notify(
        title=f"Minecraft Battery Alert [{data['category']}]",
        message=data["roast"],
        app_name="Minecraft Battery HUD",
        timeout=5
    )
    return jsonify({"status": "sent"})

@app.route("/api/speak")
def speak():
    data = get_battery_stats()
    speak_text(data["roast"])
    return jsonify({"status": "speaking"})

if __name__ == "__main__":
    print("Serving Minecraft Battery HUD on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
    