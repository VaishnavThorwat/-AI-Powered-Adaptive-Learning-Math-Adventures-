import streamlit as st
import time
from puzzle_generator import generate_puzzle
from Tracker import PerformanceTracker
from adaptive_engine import should_level_up, should_level_down, recommend_next_difficulty


# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    if 'stage' not in st.session_state:
        st.session_state.stage = 'name_entry'  # name_entry, difficulty_select, quiz, results
    if 'name' not in st.session_state:
        st.session_state.name = ""
    if 'difficulty' not in st.session_state:
        st.session_state.difficulty = None
    if 'level' not in st.session_state:
        st.session_state.level = 1
    if 'tracker' not in st.session_state:
        st.session_state.tracker = PerformanceTracker()
    if 'question_count' not in st.session_state:
        st.session_state.question_count = 0
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'current_answer' not in st.session_state:
        st.session_state.current_answer = None
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None


def reset_game():
    """Reset all game state"""
    st.session_state.stage = 'name_entry'
    st.session_state.name = ""
    st.session_state.difficulty = None
    st.session_state.level = 1
    st.session_state.tracker = PerformanceTracker()
    st.session_state.question_count = 0
    st.session_state.current_question = None
    st.session_state.current_answer = None
    st.session_state.start_time = None


def generate_new_question():
    """Generate a new question and start timer"""
    question, answer = generate_puzzle(st.session_state.difficulty, st.session_state.level)
    st.session_state.current_question = question
    st.session_state.current_answer = answer
    st.session_state.start_time = time.time()


# Initialize
init_session_state()

st.title("🧮 Adaptive Math Puzzle Game")

# Stage 1: Name Entry
if st.session_state.stage == 'name_entry':
    st.markdown("### Welcome! Let's get started")
    name = st.text_input("Enter your name:", key="name_input", placeholder="Your name...")

    if st.button("Continue", type="primary", disabled=not name.strip()):
        st.session_state.name = name.strip()
        st.session_state.stage = 'difficulty_select'
        st.rerun()

# Stage 2: Difficulty Selection
elif st.session_state.stage == 'difficulty_select':
    st.markdown(f"### Hello, {st.session_state.name}! 👋")
    st.markdown("Choose your starting difficulty level:")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🟢 Easy", use_container_width=True, type="secondary"):
            st.session_state.difficulty = "Easy"
            st.session_state.stage = 'quiz'
            generate_new_question()
            st.rerun()

    with col2:
        if st.button("🟡 Medium", use_container_width=True, type="secondary"):
            st.session_state.difficulty = "Medium"
            st.session_state.stage = 'quiz'
            generate_new_question()
            st.rerun()

    with col3:
        if st.button("🔴 Hard", use_container_width=True, type="secondary"):
            st.session_state.difficulty = "Hard"
            st.session_state.stage = 'quiz'
            generate_new_question()
            st.rerun()

# Stage 3: Quiz
elif st.session_state.stage == 'quiz':
    # Generate question if needed
    if st.session_state.current_question is None:
        generate_new_question()

    # Progress bar
    progress = st.session_state.question_count / 15
    st.progress(progress, text=f"Question {st.session_state.question_count + 1} of 15")

    # Display current stats (without level)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Player", st.session_state.name)
    with col2:
        st.metric("Difficulty", st.session_state.difficulty)

    st.divider()

    # Display question
    st.markdown(f"### Question {st.session_state.question_count + 1}")
    st.markdown(f"# {st.session_state.current_question} = ?")

    # Display timer
    timer_placeholder = st.empty()
    elapsed_time = time.time() - st.session_state.start_time
    timer_placeholder.markdown(f"⏱️ **Time: {elapsed_time:.1f}s**")

    # Answer input
    user_input = st.text_input(
        "Your Answer:",
        key=f"answer_{st.session_state.question_count}",
        placeholder="Enter your answer..."
    )

    # Action buttons
    col1, col2 = st.columns([1, 1])

    with col1:
        submit = st.button("✓ Submit", type="primary", use_container_width=True, disabled=not user_input)

    with col2:
        skip = st.button("→ Skip", use_container_width=True)

    # Handle submit
    if submit and user_input:
        end_time = time.time()
        time_taken = end_time - st.session_state.start_time

        try:
            user_value = float(user_input)
            is_correct = (user_value == st.session_state.current_answer)
        except ValueError:
            is_correct = False

        # Record attempt using tracker
        st.session_state.tracker.add_attempt(is_correct, time_taken)

        # Show feedback
        if is_correct:
            st.success(f"✓ Correct! Time: {time_taken:.2f} seconds")
        else:
            st.error(
                f"✗ Wrong! The correct answer was: {st.session_state.current_answer} | Time: {time_taken:.2f} seconds")

        # Move to next question
        st.session_state.question_count += 1

        # Check if quiz is complete
        if st.session_state.question_count >= 15:
            st.session_state.stage = 'results'
            time.sleep(1.5)  # Brief pause to show feedback
            st.rerun()

        # Adaptive difficulty every 3 questions using tracker.get_stats()
        if st.session_state.question_count % 3 == 0 and st.session_state.question_count > 0:
            all_correct, avg_time = st.session_state.tracker.get_stats(3)

            if all_correct is not None:
                # Level up if all correct and fast
                if should_level_up(st.session_state.difficulty, st.session_state.level,
                                   st.session_state.tracker) and st.session_state.level < 3:
                    st.session_state.level += 1
                    st.info("🎯 Questions getting slightly harder - you're doing great!")
                # Level down if struggling
                elif should_level_down(st.session_state.tracker) and st.session_state.level > 1:
                    st.session_state.level -= 1
                    st.info("📝 Adjusting difficulty to help you succeed!")

        # Generate next question
        st.session_state.current_question = None
        st.session_state.current_answer = None
        time.sleep(1.5)  # Brief pause to show feedback
        st.rerun()

    # Handle skip
    if skip:
        st.session_state.question_count += 1

        if st.session_state.question_count >= 15:
            st.session_state.stage = 'results'
        else:
            st.session_state.current_question = None
            st.session_state.current_answer = None

        st.rerun()

# Stage 4: Results
elif st.session_state.stage == 'results':
    st.balloons()

    # Use tracker.attempts directly
    attempts = st.session_state.tracker.attempts
    correct_count = sum(1 for a in attempts if a['correct'])
    total_time = sum(a['time'] for a in attempts)
    avg_time = total_time / len(attempts) if attempts else 0
    accuracy = (correct_count / len(attempts) * 100) if attempts else 0

    st.markdown(f"# 🎉 Quiz Complete, {st.session_state.name}!")

    st.divider()

    # Display results in columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Score", f"{correct_count}/15", f"{accuracy:.1f}%")

    with col2:
        st.metric("Average Time", f"{avg_time:.2f}s")

    with col3:
        st.metric("Total Time", f"{total_time:.1f}s")

    st.divider()

    # Performance summary with recent performance insight
    st.markdown("### 📊 Performance Summary")

    # Overall performance
    if accuracy >= 80:
        st.success("Outstanding performance! 🌟")
    elif accuracy >= 60:
        st.info("Good job! Keep practicing! 💪")
    else:
        st.warning("Keep trying! Practice makes perfect! 📚")

    # Show recent performance using last_n()
    last_5 = st.session_state.tracker.last_n(5)
    if last_5:
        recent_correct = sum(1 for a in last_5 if a['correct'])
        recent_avg_time = sum(a['time'] for a in last_5) / len(last_5)

        st.markdown("#### 🔥 Last 5 Questions")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Accuracy:** {recent_correct}/5 ({recent_correct * 20:.0f}%)")
        with col2:
            st.write(f"**Avg Time:** {recent_avg_time:.2f}s")

    st.divider()

    # Recommendation using adaptive_engine function
    recommended_difficulty = recommend_next_difficulty(accuracy, avg_time, st.session_state.difficulty)

    st.markdown("### 💡 Recommendation")

    if recommended_difficulty != st.session_state.difficulty:
        if recommended_difficulty == "Hard":
            st.info(f"🚀 You're doing great! Try **{recommended_difficulty}** mode next for a bigger challenge!")
        elif recommended_difficulty == "Easy":
            st.info(
                f"🎯 Consider trying **{recommended_difficulty}** mode to build your confidence and improve your foundation!")
        else:
            st.info(f"📈 Try **{recommended_difficulty}** mode next - it's the perfect next step for you!")
    else:
        st.info(
            f"✨ **{recommended_difficulty}** mode is perfect for you! Try it again to improve your speed and accuracy!")

    st.divider()

    # Detailed breakdown - always visible
    st.markdown("### 📋 Detailed Breakdown")

    for i, attempt in enumerate(attempts, 1):
        status = "✓ Correct" if attempt['correct'] else "✗ Wrong"
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**Question {i}:** {status}")
        with col2:
            st.write(f"{attempt['time']:.2f}s")

    st.divider()

    # Play again button
    if st.button("🔄 Play Again", type="primary", use_container_width=True):
        reset_game()
        st.rerun()
