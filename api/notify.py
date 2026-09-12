"""
Minecraft Battery HUD - Notify API
Desktop notification endpoint (local environment only)
"""

import json
import os

# plyer is optional - only used in local environments
try:
    from plyer import notification
    HAS_NOTIFY = True
except ImportError:
    HAS_NOTIFY = False


def send_notification(title, message):
    """Send desktop notification"""
    if not HAS_NOTIFY:
        return False

    try:
        notification.notify(
            title=title,
            message=message,
            app_name="Minecraft Battery HUD",
            timeout=5
        )
        return True
    except Exception:
        return False


def handler(request):
    """Vercel serverless function handler"""
    try:
        # Notifications only work in local environments
        # Vercel serverless functions don't have desktop access
        if os.environ.get("VERCEL"):
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "status": "skipped",
                    "message": "Desktop notifications not available in Vercel environment. Use locally for full features."
                })
            }

        data = json.loads(request.body) if request.body else {}
        category = data.get("category", "ALERT")
        roast = data.get("roast", "Battery alert!")

        if send_notification(f"Minecraft Battery [{category}]", roast):
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"status": "sent"})
            }
        else:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Notification failed"})
            }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
