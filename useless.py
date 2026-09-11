import time
import random
import psutil
from plyer import notification

ROASTS = {
    "overcharged": [
        "Unplug me! You're literally cooking my lithium cells.",
        "100%? What are you hoarding electrons for, the apocalypse?",
        "I'm full. Stop force-feeding me electricity.",
        "80% was enough, but no, you had to keep going. Goodbye, battery lifespan."
    ],
    "plugged_above_80": [
        "I'm at {percent}%. The 20-80 rule means nothing to you, does it?",
        "Sitting at {percent}% on AC power... you like degraded chemistry, don't you?",
        "Unplug the brick. We're past 80%, you psycho."
    ],
    "critical_low": [
        "{percent}% left. Living dangerously, are we?",
        "Down to {percent}%. Find a socket or say goodbye to that unsaved work.",
        "I'm gasping for juice at {percent}%. You wouldn't treat your phone like this."
    ],
    "plugged_in_late": [
        "Oh, so NOW you care? Plugged in at {percent}% like a hero.",
        "Barely made it. Don't expect a thank-you note."
    ]
}

class BatteryRoaster:
    def __init__(self, check_interval=10):
        self.check_interval = check_interval
        self.alerted_over_80 = False
        self.alerted_100 = False
        self.alerted_critical = False
        self.last_plugged_state = None

    def send_roast(self, title: str, message: str):
        print(f"\n[ALERT SENT] {title}: {message}")
        notification.notify(
            title=title,
            message=message,
            app_name="Battery Roaster",
            timeout=5
        )

    def evaluate(self):
        battery = psutil.sensors_battery()
        if battery is None:
            print("No battery detected on this machine.")
            return

        percent = int(battery.percent)
        is_plugged = battery.power_plugged
        print(f"Status check: {percent}% | Plugged in: {is_plugged}")

        # Plugged in when critically low
        if self.last_plugged_state is False and is_plugged and percent <= 15:
            msg = random.choice(ROASTS["plugged_in_late"]).format(percent=percent)
            self.send_roast("🔌 Saved at the Buzzer", msg)

        # Charging past safety bounds
        if is_plugged:
            if percent == 100 and not self.alerted_100:
                msg = random.choice(ROASTS["overcharged"]).format(percent=percent)
                self.send_roast("⚡ Bloatware Warning", msg)
                self.alerted_100 = True

            elif percent >= 80 and not self.alerted_over_80:
                msg = random.choice(ROASTS["plugged_above_80"]).format(percent=percent)
                self.send_roast("🔋 Cell Abuse Detected", msg)
                self.alerted_over_80 = True

            if percent > 20:
                self.alerted_critical = False

        # Discharging / Low Battery
        else:
            self.alerted_over_80 = False
            self.alerted_100 = False

            if percent <= 15 and not self.alerted_critical:
                msg = random.choice(ROASTS["critical_low"]).format(percent=percent)
                self.send_roast("🪫 Critical Neglect", msg)
                self.alerted_critical = True

        self.last_plugged_state = is_plugged

    def run(self):
        print("--- Battery Roaster is now running ---")
        print("Press Ctrl + C in the terminal to stop it.\n")
        while True:
            self.evaluate()
            time.sleep(self.check_interval)

if __name__ == "__main__":
    roaster = BatteryRoaster(check_interval=10)
    roaster.run()