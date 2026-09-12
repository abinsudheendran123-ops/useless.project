"""
Minecraft Battery HUD - Stats API
Returns current battery statistics
"""

import json
import os
from datetime import datetime

# Simulated state storage (in production, use a database)
SIMULATED_STATE = None
CURRENT_MODE = "savage"
ABUSE_SCORE = 100

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


def get_battery_stats(percent=None, plugged=None, mode="savage"):
    """Calculate battery statistics and roasts"""
    global ABUSE_SCORE

    # Use simulated state if available, otherwise use provided values
    if percent is None:
        percent = 50
    if plugged is None:
        plugged = False

    # Determine category based on battery state
    if plugged and percent == 100:
        category = "overcharge"
        color = "#ff5555"
        ABUSE_SCORE = max(20, ABUSE_SCORE - 2)
    elif plugged and percent >= 80:
        category = "high"
        color = "#ffaa00"
        ABUSE_SCORE = max(40, ABUSE_SCORE - 1)
    elif not plugged and percent <= 15:
        category = "critical"
        color = "#aa0000"
        ABUSE_SCORE = max(10, ABUSE_SCORE - 3)
    else:
        category = "balanced"
        color = "#55ff55"
        ABUSE_SCORE = min(100, ABUSE_SCORE + 1)

    face = CREEPER_FACES[category]
    roast = ROAST_DATABASE[mode][category]

    return {
        "percent": percent,
        "plugged": plugged,
        "face": face,
        "color": color,
        "category": category.upper(),
        "roast": roast,
        "score": ABUSE_SCORE
    }


def handler(request):
    """Vercel serverless function handler"""
    try:
        data = json.loads(request.body) if request.body else {}
        mode = data.get("mode", "savage")
        percent = data.get("percent")
        plugged = data.get("plugged")

        # For Vercel environment, return simulated data
        # In production with local usage, you'd use psutil here
        stats = get_battery_stats(
            percent=percent if percent is not None else 75,
            plugged=plugged if plugged is not None else False,
            mode=mode
        )

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(stats)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
