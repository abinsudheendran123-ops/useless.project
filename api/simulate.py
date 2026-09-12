"""
Minecraft Battery HUD - Simulate API
Simulates a battery state for testing
"""

import json

# In-memory storage for simulation state
simulation_state = {}


def handler(request):
    """Vercel serverless function handler"""
    try:
        global simulation_state
        data = json.loads(request.body) if request.body else {}
        
        simulation_state = {
            "percent": data.get("percent", 50),
            "plugged": data.get("plugged", False),
            "mode": data.get("mode", "savage")
        }

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"status": "simulated", "state": simulation_state})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
