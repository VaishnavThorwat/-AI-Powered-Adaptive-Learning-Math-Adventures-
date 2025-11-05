import time
import csv
import os

class PerformanceTracker:
    def __init__(self, log_file="session_log.csv"):
        self.reset()
        self.log_file = log_file
        self._init_log_file()

    def reset(self):
        self.attempts = []  # List of dicts: {'correct':True, 'time':float}

    def _init_log_file(self):
        """Create CSV file with header if it doesn't exist."""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'name', 'question_no', 'question', 'correct', 'time_taken', 'difficulty', 'level', 'event'])

    def add_attempt(self, correct, t, name=None, question_no=None, question=None, difficulty=None, level=None, event="attempt"):
        """Add a new attempt to tracker and log it persistently."""
        entry = {'correct': correct, 'time': t}
        self.attempts.append(entry)

        # Write the log entry to CSV
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                time.strftime("%Y-%m-%d %H:%M:%S"),
                name if name else "Unknown",
                question_no if question_no is not None else "",
                question if question else "",
                correct,
                round(t, 2),
                difficulty if difficulty else "",
                level if level else "",
                event
            ])

    def last_n(self, n):
        return self.attempts[-n:] if len(self.attempts) >= n else []

    def get_stats(self, n):
        last = self.last_n(n)
        if not last:
            return None, None
        avg_time = sum(x['time'] for x in last) / n
        all_correct = all(x['correct'] for x in last)
        return all_correct, avg_time
