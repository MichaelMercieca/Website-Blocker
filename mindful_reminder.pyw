import psutil
import os
import sys
import tkinter as tk
# from tkinter import messagebox
import time
import threading
import keyboard

os.chdir(os.path.dirname(os.path.abspath(__file__)))


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
    popup.attributes("-topmost", True)
    popup.lift()
    popup.focus_force()

    def block_windows_key():
        # Block the Windows key
        keyboard.block_key('windows')
        keyboard.block_key('left windows')
        keyboard.block_key('right windows')

    def do_nothing():
        # Function to do nothing (used to disable keys)
        pass

    # Override the close button (X) in the window
    popup.protocol("WM_DELETE_WINDOW", do_nothing)
    # Override the Alt+F4 keypress
    popup.bind("<Alt-F4>", lambda event: do_nothing())
    # Override the Escape key press
    popup.bind("<Escape>", lambda event: do_nothing())
    # block Windows key
    block_windows_key()

    # Create and place the label
    label = tk.Label(
        popup,
        text="Stop to breath mindfully. If you are working, continue afterwards. "
             "If you are distracted, come back to the present moment and realise you are meant for more.",
        font=("Helvetica", 24),
        wraplength=popup.winfo_screenwidth()
    )
    label.pack(expand=True)

    # Wait for 15 seconds before showing the close button
    popup.after(15000, lambda: show_close_button(popup))

    # Run the popup's main loop
    popup.mainloop()


def show_close_button(popup):
    # Create and place the close button
    button = tk.Button(popup, text="Close", command=popup.destroy, font=("Helvetica", 18))
    button.pack(pady=20)


def schedule_popup():
    while True:
        # Wait for 7 minutes (420 seconds)
        time.sleep(420)
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

# import psutil
# import os
# import sys
# import tkinter as tk
# import time
# import threading
# import keyboard
#
#
# # Configuration variables for easy adjustment
# REGULAR_POPUP_INTERVAL = 7 * 60  # Time between regular popups (in seconds) - 7 minutes
# REGULAR_POPUP_DISPLAY_TIME = 15  # Time before close button appears in regular popups (in seconds)
# LONG_POPUP_INTERVAL = 40 * 60  # Time between long popups (in seconds) - 40 minutes
# LONG_POPUP_DISPLAY_TIME = 5 * 60  # Time before close button appears in long popup (in seconds)
# MINDFUL_MESSAGE = "Stop to breathe mindfully. If you are working, continue afterwards. " \
#                   "If you are distracted, come back to the present moment and realise you are meant for more."
#
#
# def check_duplicate():
#     """Check if another instance of this script is already running, and exit if found."""
#     current_script = os.path.basename(__file__)
#     current_pid = os.getpid()
#
#     for proc in psutil.process_iter():
#         try:
#             if proc.pid == current_pid:
#                 continue
#
#             process_name = proc.name()
#             process_cmdline = proc.cmdline()
#
#             if (process_name == "python" or process_name == "pythonw") and len(process_cmdline) > 1:
#                 if current_script in process_cmdline[1]:
#                     print("Another instance of this script is already running. Exiting.")
#                     sys.exit(0)
#         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#             continue
#
#
# def show_popup(is_long_popup=False, remaining_time=None):
#     """Show a popup window, either regular or long, with an optional countdown."""
#     popup = tk.Tk()
#     popup.attributes("-fullscreen", True)
#     popup.attributes("-topmost", True)
#     popup.lift()
#     popup.focus_force()
#
#     def block_windows_key():
#         # Block the Windows key
#         keyboard.block_key('windows')
#         keyboard.block_key('left windows')
#         keyboard.block_key('right windows')
#
#     def do_nothing():
#         # Function to do nothing (used to disable keys)
#         pass
#
#     # Override the close button (X) in the window
#     popup.protocol("WM_DELETE_WINDOW", do_nothing)
#     # Override the Alt+F4 keypress
#     popup.bind("<Alt-F4>", lambda event: do_nothing())
#     # Override the Escape key press
#     popup.bind("<Escape>", lambda event: do_nothing())
#     # block Windows key
#     block_windows_key()
#
#     # Mindfulness message
#     label = tk.Label(popup, text=MINDFUL_MESSAGE, font=("Helvetica", 24), wraplength=popup.winfo_screenwidth())
#     label.pack(expand=True)
#
#     if remaining_time is not None:  # Regular popup with countdown
#         countdown_label = tk.Label(popup, font=("Helvetica", 18))
#         countdown_label.pack(expand=True)
#         update_regular_popup(popup, countdown_label, remaining_time)
#     else:  # Long popup
#         countdown_label = tk.Label(popup, font=("Helvetica", 18))
#         countdown_label.pack(expand=True)
#         countdown_timer(popup, countdown_label, LONG_POPUP_DISPLAY_TIME)
#
#     if is_long_popup:
#         popup.after(LONG_POPUP_DISPLAY_TIME * 1000, lambda: show_close_button(popup))
#     else:
#         popup.after(REGULAR_POPUP_DISPLAY_TIME * 1000, lambda: show_close_button(popup))
#
#     popup.mainloop()
#
#
# def update_regular_popup(popup, countdown_label, remaining_time):
#     """Update the regular popup to show the time remaining until the long popup."""
#     if remaining_time > 0:
#         countdown_label.config(text=f"Time until long popup: {remaining_time} minutes remaining.")
#         remaining_time -= 1
#         popup.after(60000, lambda: update_regular_popup(popup, countdown_label, remaining_time))  # Update every minute
#     else:
#         show_close_button(popup)
#
#
# def countdown_timer(popup, countdown_label, remaining_time):
#     """Countdown for the long popup before the close button appears."""
#     if remaining_time > 0:
#         countdown_label.config(text=f"Long Popup Countdown: {remaining_time} seconds remaining.")
#         remaining_time -= 1
#         popup.after(1000, lambda: countdown_timer(popup, countdown_label, remaining_time))  # Update every second
#     else:
#         show_close_button(popup)
#
#
# def show_close_button(popup):
#     """Display the close button on the popup after a delay."""
#     button = tk.Button(popup, text="Close", command=popup.destroy, font=("Helvetica", 18))
#     button.pack(pady=20)
#
#
# def schedule_popup():
#     """Main loop that handles the scheduling of both regular and long popups."""
#     cycle_counter = 0
#     while True:
#         for _ in range(int(LONG_POPUP_INTERVAL / REGULAR_POPUP_INTERVAL)):  # Regular popups before the long one
#             time.sleep(REGULAR_POPUP_INTERVAL)  # Wait for 7 minutes
#             remaining_time = (LONG_POPUP_INTERVAL - (cycle_counter + 1) * REGULAR_POPUP_INTERVAL) // 60  # Minutes until long popup
#             cycle_counter += 1
#             root.after(0, show_popup, False, remaining_time)  # Show regular popup
#
#         # Show the long popup
#         root.after(0, show_popup, True)
#         time.sleep(LONG_POPUP_DISPLAY_TIME)  # Wait for 5 minutes (time on screen for long popup)
#
#
# if __name__ == "__main__":
#     check_duplicate()  # Check if another instance is running
#
#     root = tk.Tk()
#     root.withdraw()  # Hide the root window
#
#     threading.Thread(target=schedule_popup, daemon=True).start()  # Start the scheduler in a separate thread
#     root.mainloop()  # Start the main application loop
