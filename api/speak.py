"""
Minecraft Battery HUD - Speak API
Text-to-speech endpoint (local environment only)
"""

import json
import os

# pyttsx3 is optional - only used in local environments
try:
    import pyttsx3
    import threading
    HAS_TTS = True
except ImportError:
    HAS_TTS = False


def speak_text(text):
    """Speak text using text-to-speech"""
    if not HAS_TTS:
        return False

    def _speak():
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 160)
            engine.say(text)
            engine.runAndWait()
        except Exception:
            pass

    threading.Thread(target=_speak, daemon=True).start()
    return True


def handler(request):
    """Vercel serverless function handler"""
    try:
        # Speech features only work in local environments
        # Vercel serverless functions don't have audio output
        if os.environ.get("VERCEL"):
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "status": "skipped",
                    "message": "Text-to-speech not available in Vercel environment. Use locally for full features."
                })
            }

        data = json.loads(request.body) if request.body else {}
        roast = data.get("roast", "Battery alert!")

        if speak_text(roast):
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"status": "speaking"})
            }
        else:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Text-to-speech not available"})
            }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
