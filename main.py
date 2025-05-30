import streamlit as st
import random
import time

# Grid size
GRID_SIZE = 10

# Emoji representations
SNAKE_EMOJI = "🟩"
FOOD_EMOJI = "🍎"
EMPTY_EMOJI = "⬜"

# Initialize state
if "snake" not in st.session_state:
    st.session_state.snake = [(5, 5)]
    st.session_state.food = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
    st.session_state.direction = "RIGHT"
    st.session_state.score = 0
    st.session_state.game_over = False

def place_food():
    while True:
        food = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
        if food not in st.session_state.snake:
            return food

def move_snake():
    head_x, head_y = st.session_state.snake[-1]

    direction = st.session_state.direction
    if direction == "UP":
        new_head = (head_x, head_y - 1)
    elif direction == "DOWN":
        new_head = (head_x, head_y + 1)
    elif direction == "LEFT":
        new_head = (head_x - 1, head_y)
    else:  # RIGHT
        new_head = (head_x + 1, head_y)

    # Check collisions
    if (
        new_head in st.session_state.snake
        or new_head[0] < 0 or new_head[0] >= GRID_SIZE
        or new_head[1] < 0 or new_head[1] >= GRID_SIZE
    ):
        st.session_state.game_over = True
        return

    st.session_state.snake.append(new_head)

    # Eat food
    if new_head == st.session_state.food:
        st.session_state.score += 1
        st.session_state.food = place_food()
    else:
        st.session_state.snake.pop(0)

def render_grid():
    grid = ""
    for y in range(GRID_SIZE):
        row = ""
        for x in range(GRID_SIZE):
            if (x, y) == st.session_state.food:
                row += FOOD_EMOJI
            elif (x, y) in st.session_state.snake:
                row += SNAKE_EMOJI
            else:
                row += EMPTY_EMOJI
        grid += row + "\n"
    st.markdown(grid)

# Title and score
st.title("🐍 Streamlit Snake Game")
st.write(f"**Score:** {st.session_state.score}")

# Movement buttons
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("⬆️ Up") and st.session_state.direction != "DOWN":
        st.session_state.direction = "UP"
with col1:
    if st.button("⬅️ Left") and st.session_state.direction != "RIGHT":
        st.session_state.direction = "LEFT"
with col3:
    if st.button("➡️ Right") and st.session_state.direction != "LEFT":
        st.session_state.direction = "RIGHT"
with col2:
    if st.button("⬇️ Down") and st.session_state.direction != "UP":
        st.session_state.direction = "DOWN"

# Move snake and render grid
if not st.session_state.game_over:
    move_snake()
    render_grid()
    time.sleep(0.2)
    st.experimental_rerun()
else:
    st.error("💀 Game Over!")
    if st.button("🔄 Restart"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()
