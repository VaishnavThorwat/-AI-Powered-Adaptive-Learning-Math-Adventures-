import time

class PerformanceTracker:
    def __init__(self):
        self.reset()

    def reset(self):
        self.attempts = []  # List of dicts: {'correct':True, 'time':float}

    def add_attempt(self, correct, t):
        self.attempts.append({'correct': correct, 'time': t})

    def last_n(self, n):
        return self.attempts[-n:] if len(self.attempts) >= n else []

    def get_stats(self, n):
        last = self.last_n(n)
        if not last:
            return None, None
        avg_time = sum(x['time'] for x in last) / n
        all_correct = all(x['correct'] for x in last)
        return all_correct, avg_time
