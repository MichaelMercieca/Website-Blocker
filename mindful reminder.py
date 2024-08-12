import tkinter as tk
# from tkinter import messagebox
import time
import threading


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

    # Wait for 10 seconds before showing the close button
    popup.after(10000, lambda: show_close_button(popup))

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


# Create the main application window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Start the scheduler in a separate thread
threading.Thread(target=schedule_popup, daemon=True).start()

# Start the main application loop
root.mainloop()
