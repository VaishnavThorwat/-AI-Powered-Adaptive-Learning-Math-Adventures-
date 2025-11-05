# adaptive_engine.py

def should_level_up(mode, level, tracker):
    # Thresholds for each mode and level
    thresholds = {'Easy': [5, 10], 'Medium': [7, 13], 'Hard': [9, 15]}

    # Validate mode and prevent index out of range
    if mode not in thresholds or level < 1 or level > len(thresholds[mode]):
        return False

    # Get stats for last 3 questions
    correct, avg_time = tracker.get_stats(3)

    # If not all correct, don't level up
    if not correct:
        return False

    # Get time limit for current mode and level
    limit = thresholds[mode][level - 1]

    # Level up if average time is less than limit
    return avg_time < limit


def should_level_down(tracker):
    # Get last 3 attempts
    last = tracker.last_n(3)

    # If no attempts or all correct, don't level down
    if not last or all(x['correct'] for x in last):
        return False

    # Count wrong answers
    wrong_count = sum(not x['correct'] for x in last)

    # Level down if 2 or more wrong in last 3
    return wrong_count >= 2


def recommend_next_difficulty(accuracy, avg_time, current_difficulty):
    # List of difficulty levels in order
    difficulty_order = ["Easy", "Medium", "Hard"]

    # Find current difficulty index
    current_index = difficulty_order.index(current_difficulty)

    # Case 1: Excellent performance - high accuracy and fast time
    if accuracy >= 80 and avg_time < 10:
        # If not already on Hard, suggest next level
        if current_index < 2:
            return difficulty_order[current_index + 1]

    # Case 2: Strong performance on Hard mode
    elif current_difficulty == "Hard" and accuracy >= 70:
        return "Hard"

    # Case 3: Struggling - low accuracy or very slow
    elif accuracy < 50 or avg_time > 20:
        # If not already on Easy, suggest easier level
        if current_index > 0:
            return difficulty_order[current_index - 1]

    # Case 4: Good performance on Medium - ready for Hard
    elif current_difficulty == "Medium" and accuracy >= 75 and avg_time < 12:
        return "Hard"

    # Case 5: Good performance on Easy - ready for Medium
    elif current_difficulty == "Easy" and accuracy >= 70 and avg_time < 15:
        return "Medium"

    # Default: Stay at current level
    return current_difficulty
