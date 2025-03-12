import time
import ctypes
import schedule
import threading
import sys
from datetime import datetime

# Windows API constants
SW_MINIMIZE = 6


# Function to minimize all windows (equivalent to Windows key + D)
def minimize_all_windows():
    try:
        # Using Windows API to minimize all windows
        ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0)  # Press Windows key
        ctypes.windll.user32.keybd_event(0x44, 0, 0, 0)  # Press D key
        ctypes.windll.user32.keybd_event(0x44, 0, 2, 0)  # Release D key
        ctypes.windll.user32.keybd_event(0x5B, 0, 2, 0)  # Release Windows key

        # Log the action with current time
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"[{current_time}] All windows minimized!")

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


# Function to run the scheduler in a separate thread
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


def main():
    print("Window Minimizer Started")
    print("This script will minimize all windows every 8 minutes")
    print("Press Ctrl+C to exit")

    # Schedule the task to run every 8 minutes
    schedule.every(8).minutes.do(minimize_all_windows)

    # Run once at startup
    minimize_all_windows()

    # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True  # This ensures the thread will exit when the main program exits
    scheduler_thread.start()

    # Keep the main thread running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting window minimizer...")
        sys.exit(0)


if __name__ == "__main__":
    main()