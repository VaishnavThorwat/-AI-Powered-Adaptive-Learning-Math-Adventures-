import random

def generate_puzzle(mode, level):
    if mode == "Easy":
        return generate_easy(level)
    elif mode == "Medium":
        return generate_medium(level)
    elif mode == "Hard":
        return generate_hard(level)

def generate_easy(level):
    # Keep generating until we get a positive answer
    while True:
        if level == 1:
            a, b = random.randint(1, 10), random.randint(1, 10)
        elif level == 2:
            a, b = random.randint(10, 50), random.randint(10, 50)
        else:
            a, b = random.randint(10, 100), random.randint(10, 100)

        op = random.choice(['+', '-'])

        # For subtraction, make sure a >= b to avoid negative result
        if op == '-':
            if a < b:
                a, b = b, a  # Swap to make sure result is positive

        question = f"{a} {op} {b}"
        answer = eval(question)

        # Make sure answer is positive
        if answer > 0:
            return question, answer


def generate_medium(level):
    # Keep generating until we get a positive integer answer
    while True:
        if level == 1:
            a, b = random.randint(2, 12), random.randint(2, 12)
        elif level == 2:
            a, b = random.randint(10, 30), random.randint(2, 12)
        else:
            a, b = random.randint(10, 50), random.randint(10, 20)

        op = random.choice(['*', '/'])

        if op == '/':
            # Make a divisible by b to get integer result
            a = a * b

        question = f"{a} {op} {b}"
        answer = eval(question)

        # Make sure answer is positive integer
        if answer > 0 and answer == int(answer):
            return question, int(answer)


def generate_hard(level):
    # Keep generating until we get a positive answer
    while True:
        if level == 1:
            a, b, c = random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)
        elif level == 2:
            a, b, c = random.randint(1, 20), random.randint(1, 20), random.randint(1, 20)
        else:
            a, b, c = random.randint(1, 50), random.randint(1, 30), random.randint(1, 10)

        op1 = random.choice(['+', '-', '*'])
        op2 = random.choice(['+', '-', '*'])

        question = f"{a} {op1} {b} {op2} {c}"
        answer = eval(question)

        # Make sure answer is positive
        if answer > 0:
            return question, answer