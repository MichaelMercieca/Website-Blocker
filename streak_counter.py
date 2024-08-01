import os
import datetime


def print_counter(streak):
    """Print the streak as 3x3 boxes, wrapping after 7 boxes."""
    box = '###\n###\n###'
    separator = '\n---\n'
    streak_lines = []
    for i in range(streak):
        if i > 0 and i % 7 == 0:
            streak_lines.append(separator)
        streak_lines.append(box)
        streak_lines.append('\n')  # Separate boxes vertically
    print(''.join(streak_lines))


class StreakCounter:

    DATE_FORMAT = '%Y-%m-%d'  # Date format for storing in file

    def __init__(self, counter_file_path: str):
        self.counter_file_path = counter_file_path

    def load_counter(self):
        if os.path.exists(self.counter_file_path):
            with open(self.counter_file_path, 'r') as file:
                data = file.read().strip().split(',')
                if len(data) == 2:
                    streak = int(data[0])
                last_updated = datetime.datetime.strptime(data[1], self.DATE_FORMAT)
                return streak, last_updated
        return 0, None

    def save_counter(self, streak: int, last_updated):
        with open(self.counter_file_path, 'w') as file:
            file.write(f"{streak},{last_updated.datetime.datetime.strftime(self.DATE_FORMAT)}")

    def increment_streak(self):
        """Increment the streak value if a new day has started."""
        streak, last_updated = self.load_counter()
        today = datetime.datetime.now().date()

        if last_updated is None or today > last_updated.date():
            streak += 1
            self.save_counter(streak, today)
            return streak, today
        else:
            return streak, last_updated
