import psutil
import os
import sys
import tkinter as tk
# from tkinter import messagebox
import time
import threading


def check_duplicate_process():
    # Get the current script's name
    current_script = os.path.basename(__file__)
    current_pid = os.getpid()

    # Iterate over all running processes
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # Skip the current process if it is this program being run
            if proc.pid == current_pid:
                continue

            # Check if the process is running the same script
            proc_name = proc.name()
            proc_cmdline = proc.cmdline()

            if (proc_name == 'python' or proc_name == 'pythonw') and len(proc_cmdline) > 1:
                if current_script in proc_cmdline[1]:
                    print('Another instance of this script is already running. Exiting.')
                    sys.exit(0)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # In case a process ends while we are iterating, or we do not have permission to access it
            continue


def show_popup():
    # Create a new fullscreen window
    popup = tk.Tk()
    popup.attributes("-fullscreen", True)

    # Create and place the label
    label = tk.Label(
        popup,
        text="Stop to breath mindfully. If you are working, continue afterwards. "
             "If you are distracted, come back to the present moment and realise you are meant for more.",
        font=("Helvetica", 24),
        wraplength=popup.winfo_screenwidth()
    )
    label.pack(expand=True)

    # Wait for 12 seconds before showing the close button
    popup.after(12000, lambda: show_close_button(popup))

    # Run the popup's main loop
    popup.mainloop()


def show_close_button(popup):
    # Create and place the close button
    button = tk.Button(popup, text="Close", command=popup.destroy, font=("Helvetica", 18))
    button.pack(pady=20)


def schedule_popup():
    while True:
        # Wait for 8 minutes (480 seconds)
        time.sleep(480)
        # Show the popup in the main thread
        root.after(0, show_popup)


# Main execution
if __name__ == "__main__":
    check_duplicate_process()  # Check if another instance is running

    # Create the main application window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Start the scheduler in a separate thread
    threading.Thread(target=schedule_popup, daemon=True).start()

    # Start the main application loop
    root.mainloop()
