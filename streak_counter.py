import os
import datetime

DATE_FORMAT = '%Y-%m-%d'  # Date format for storing in file
counter_file_path = 'counter_file.txt'


def print_counter(streak):
    """Print the streak as 3x3 boxes, wrapping after 7 boxes."""
    box = '###'             # x3
    separator_h = '|'       # x3
    separator_v = ' ---'
    streak_lines = []
    boxes_in_row = 0

    for i in range(streak):
        if i > 0 and i % 7 == 0:
            boxes_in_row = 7
        elif i == (streak-1):
            boxes_in_row = i % 7

        # Printing
        if boxes_in_row != 0:
            # Horizontal
            for j in range(3):
                streak_lines.append(separator_h)
                for k in range(boxes_in_row):
                    streak_lines.append(box)
                    streak_lines.append(separator_h)
                streak_lines.append('\n')
            # Separate boxes vertically
            for j in range(boxes_in_row):
                streak_lines.append(separator_v)
            streak_lines.append('\n')

            boxes_in_row = 0        # reset to prevent printing extra

    print(''.join(streak_lines))


def load_counter():
    if os.path.exists(counter_file_path):
        with open(counter_file_path, 'r') as file:
            data = file.read().strip().split(',')
            if len(data) == 2:
                streak = int(data[0])
                last_updated = datetime.datetime.strptime(data[1], DATE_FORMAT)
                return streak, last_updated
    return 0, None


def save_counter(streak: int, last_updated):
    with open(counter_file_path, 'w') as file:
        file.write(f"{streak},{last_updated}")


def increment_streak():
    """Increment the streak value if a new day has started."""
    streak, last_updated = load_counter()
    today = datetime.datetime.now()

    if last_updated is None or today > last_updated.date():
        streak += 1
        save_counter(streak, today)
        return streak, today
    else:
        return streak, last_updated
