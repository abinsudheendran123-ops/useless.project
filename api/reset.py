"""
Minecraft Battery HUD - Reset API
Resets simulation to real battery stats
"""

import json

simulation_state = {}


def handler(request):
    """Vercel serverless function handler"""
    try:
        global simulation_state
        simulation_state = {}

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"status": "reset"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
