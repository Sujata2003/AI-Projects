import streamlit as st
from math import inf as infinity
from random import choice
import time

# Game variables
HUMAN = -1
COMP = +1

# Initialize the Tic-Tac-Toe board
if 'board' not in st.session_state:
    st.session_state.board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    st.session_state.current_player = HUMAN  # Human starts
    st.session_state.game_over = False
    st.session_state.first_move = 'human'  # Keep track of first turn

# Function to check if a player has won
def wins(state, player):
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    return [player, player, player] in win_state

# Function to evaluate the board for minimax
def evaluate(state):
    if wins(state, COMP):
        return +1
    elif wins(state, HUMAN):
        return -1
    else:
        return 0

# Function to check if the game is over (win or draw)
def game_over(state):
    return wins(state, HUMAN) or wins(state, COMP)

# Function to find empty cells on the board
def empty_cells(state):
    cells = []
    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])
    return cells

# Function to make a valid move
def set_move(x, y, player):
    if [x, y] in empty_cells(st.session_state.board):
        st.session_state.board[x][y] = player
        return True
    return False

# Minimax algorithm to find the best move for the AI
def minimax(state, depth, player):
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best

# Function for AI turn
def ai_turn():
    depth = len(empty_cells(st.session_state.board))
    if depth == 0 or game_over(st.session_state.board):
        return

    if depth == 9:
        x, y = choice([0, 1, 2]), choice([0, 1, 2])
    else:
        move = minimax(st.session_state.board, depth, COMP)
        x, y = move[0], move[1]

    set_move(x, y, COMP)

# Function for human turn
def human_turn(x, y):
    if not st.session_state.game_over and st.session_state.board[x][y] == 0:
        set_move(x, y, HUMAN)
        if wins(st.session_state.board, HUMAN):
            st.session_state.game_over = True
            st.success("You win🧝!")
        elif not empty_cells(st.session_state.board):
            st.session_state.game_over = True
            st.info("It's a draw!")
        else:
            ai_turn()
            if wins(st.session_state.board, COMP):
                st.session_state.game_over = True
                st.warning("AI 🤖 wins! Try again.")

# Function to reset the game
def reset_game():
    st.session_state.board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    st.session_state.game_over = False
    st.session_state.current_player = HUMAN

# Streamlit UI
st.title("👾Tic-Tac-Toe with AI👾")
st.write("You are playing as X")

# Display the Tic-Tac-Toe board
cols = st.columns(3)
for i in range(3):
    for j in range(3):
        if st.session_state.board[i][j] == 0:
            cols[j].button(" ", key=f"{i}{j}", on_click=human_turn, args=(i, j))
        elif st.session_state.board[i][j] == HUMAN:
            cols[j].write("X")
        else:
            cols[j].write("O")

# Reset button to restart the game
if st.button("Reset Game"):
    reset_game()

# Check for game over
if st.session_state.game_over:
    st.write("Game Over")
