import tkinter as tk
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
import sys
import threading
import time
from pystray import Icon, Menu, MenuItem
from PIL import Image

class UsageTracker:
    def __init__(self):
        # Create data directory in user's home folder
        self.data_path = Path.home() / '.laptop_usage'
        self.data_path.mkdir(exist_ok=True)
        self.timer_file = self.data_path / 'timer_data.json'

        # Initialize or load saved time
        self.total_seconds = self.load_timer()
        self.running = True

        # Create main window
        self.root = tk.Tk()
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.attributes('-topmost', True)  # Keep window on top

        # Calculate initial position (bottom-right corner)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 150
        window_height = 30
        x_position = screen_width - window_width - 10
        y_position = screen_height - window_height - 40  # Above taskbar

        self.root.geometry(f'{window_width}x{window_height}+{x_position}+{y_position}')

        # Create timer label
        self.label = tk.Label(
            self.root,
            font=('Consolas', 10),
            bg='black',
            fg='white',
            padx=5,
            pady=2
        )
        self.label.pack(fill='both', expand=True)

        # Make window draggable
        self.label.bind('<Button-1>', self.start_drag)
        self.label.bind('<B1-Motion>', self.on_drag)

        # Create system tray icon
        self.setup_system_tray()

        # Start timer thread
        self.timer_thread = threading.Thread(target=self.update_timer, daemon=True)
        self.timer_thread.start()

        # Save timer periodically
        self.save_timer_periodically()

    def load_timer(self):
        """Load saved timer value from file"""
        try:
            with open(self.timer_file, 'r') as f:
                data = json.load(f)
                return data.get('total_seconds', 0)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0

    def save_timer(self):
        """Save current timer value to file"""
        with open(self.timer_file, 'w') as f:
            json.dump({'total_seconds': self.total_seconds}, f)

    def save_timer_periodically(self):
        """Save timer value every minute"""
        if self.running:
            self.save_timer()
            self.root.after(60000, self.save_timer_periodically)

    def format_time(self, seconds):
        """Convert seconds to days:hours:minutes format"""
        days = seconds // (24 * 3600)
        remaining = seconds % (24 * 3600)
        hours = remaining // 3600
        minutes = (remaining % 3600) // 60
        return f"{int(days):02d}:{int(hours):02d}:{int(minutes):02d}"

    def update_timer(self):
        """Update timer continuously"""
        while self.running:
            self.total_seconds += 1
            self.label.config(text=self.format_time(self.total_seconds))
            time.sleep(1)

    def start_drag(self, event):
        """Record initial position for window dragging"""
        self.x = event.x
        self.y = event.y

    def on_drag(self, event):
        """Handle window dragging"""
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f'+{x}+{y}')

    def setup_system_tray(self):
        """Create system tray icon with menu"""
        # Create a simple icon (you can replace with your own icon file)
        icon_image = Image.new('RGB', (64, 64), color='black')

        def exit_app(icon):
            self.running = False
            self.save_timer()
            icon.stop()
            self.root.quit()

        def reset_timer(icon):
            self.total_seconds = 0
            self.save_timer()

        # Create system tray menu
        menu = Menu(
            MenuItem('Reset Timer', reset_timer),
            MenuItem('Exit', exit_app)
        )

        self.icon = Icon(
            'Usage Tracker',
            icon_image,
            'Laptop Usage Tracker',
            menu
        )

        # Run system tray icon in separate thread
        threading.Thread(target=self.icon.run, daemon=True).start()

    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == '__main__':
    tracker = UsageTracker()
    tracker.run()