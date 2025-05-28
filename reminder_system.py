import json
import threading
from datetime import datetime, timedelta
from time import sleep
from plyer import notification
from playsound import playsound
import os

REMINDERS_FILE = 'reminders.json'
AUDIO_FILE = 'file_example_MP3_700KB.mp3'  # You can use any short mp3 file here

def load_reminders():
    if os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_reminder(task, remind_time_str):
    reminders = load_reminders()
    reminders.append({"task": task, "time": remind_time_str})
    with open(REMINDERS_FILE, 'w') as f:
        json.dump(reminders, f, indent=4)

def schedule_reminder(task, remind_time_str):
    remind_time = datetime.strptime(remind_time_str, "%H:%M")
    now = datetime.now()
    # Use today's date for scheduling
    remind_datetime = datetime.combine(now.date(), remind_time.time())
    if remind_datetime < now:
        remind_datetime += timedelta(days=1)  # Schedule for the next day

    delay = (remind_datetime - now).total_seconds()

    def remind():
        sleep(delay)
        notification.notify(
            title="🔔 Reminder!",
            message=task,
            timeout=10
        )
        try:
            playsound(AUDIO_FILE)
        except Exception as e:
            print("Audio alert failed:", e)
        print(f"\n🔔 Reminder: {task} (at {remind_time_str})")

    threading.Thread(target=remind).start()

def main():
    print("📅 Python Reminder System with Notifications + Sound + JSON Storage\n")

    while True:
        task = input("📝 What task do you want to be reminded of? ")
        remind_time = input("⏰ At what time? (format HH:MM in 24-hour, e.g., 14:30): ")

        try:
            datetime.strptime(remind_time, "%H:%M")
        except ValueError:
            print("⚠️ Invalid time format. Please use HH:MM (24-hour).")
            continue

        save_reminder(task, remind_time)
        schedule_reminder(task, remind_time)

        cont = input("➕ Add another reminder? (yes/no): ").strip().lower()
        if cont != 'yes':
            print("✅ All reminders are set. System will keep running.")
            break

if __name__ == "__main__":
    main()

