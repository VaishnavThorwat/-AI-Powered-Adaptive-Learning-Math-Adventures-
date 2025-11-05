# AI-Powered Adaptive Learning: Math Adventures Prototype

## Problem Statement

Design a system that helps children (ages 5-10) practice basic math (addition, subtraction, multiplication, or division). 
- Generate simple math puzzles. 
- Track performance (correctness, response time). 
- Automatically adjust the next puzzleʼs difficulty. 
- Display a basic end-of-session performance summary.

---

## Overview

Math Adventures is an interactive, AI-driven learning game that makes arithmetic practice engaging and personalized. It dynamically adjusts question difficulty based on the learner’s performance to help them improve progressively.


---

## Features

* Dynamic puzzle generation for arithmetic operations
* Adaptive difficulty adjustment using performance data
* Real-time tracking of accuracy and speed
* Personalized recommendations for the next difficulty level
* Simple Streamlit interface for interactive learning

---

## How It Works

1. The player enters their name and chooses a starting difficulty.
2. They solve 15 math questions that vary based on performance.
3. The system tracks correctness and time for each question.
4. After every few questions, difficulty is automatically adjusted.
5. At the end, the player receives a summary and a recommended difficulty for the next session.

---

## File Structure

| File                  | Description                                                  |
| --------------------- | ------------------------------------------------------------ |
| `main.py`             | Streamlit app that handles the user interface and game flow. |
| `puzzle_generator.py` | Creates math problems for different modes and levels.        |
| `Tracker.py`          | Tracks performance, accuracy, and response times and also log them in CSV file.            |
| `adaptive_engine.py`  | Controls logic for adaptive difficulty and recommendations.  |
| `requirement.txt`     | This file lists all Python dependencies your project needs to run.|
---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/VaishnavThorwat/AI-Powered-Adaptive-Learning-Math-Adventures.git
   cd AI-Powered-Adaptive-Learning-Math-Adventures
   ```

2. Install dependencies:

   ```bash
   pip install streamlit
   ```

3. Run the application:

   ```bash
   streamlit run main.py
   ```
---

## Technologies Used

* Python
* Streamlit

---

## Author

**Vaishnav Thorwat**
GitHub: [VaishnavThorwat](https://github.com/VaishnavThorwat)


