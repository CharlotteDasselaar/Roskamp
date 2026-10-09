import streamlit as st

st.set_page_config(page_title="Tic-Tac-Toe", page_icon="🎮")
st.title("Tic-Tac-Toe")

# 1. Initialize persistent state
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
if "current_player" not in st.session_state:
    st.session_state.current_player = "X"
if "winner" not in st.session_state:
    st.session_state.winner = None
if "history" not in st.session_state:
    st.session_state.history = {}

# Optional CSS to make the buttons appear large and square
st.markdown(
    """
    <style>
    div.stButton > button {
        height: 80px;
        font-size: 36px;
        font-weight: bold;
        color: #1E88E5; /* 'color' in plaats van 'font-color' */
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# 2. Game logic functions
def check_winner(board):
    win_lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6),  # Diagonals
    ]
    for a, b, c in win_lines:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if "" not in board:
        return "Tie"
    return None


def make_move(idx):
    if st.session_state.board[idx] == "" and not st.session_state.winner: # and st.session_state.current_player == "X":
        st.session_state.board[idx] = st.session_state.current_player
        winner = check_winner(st.session_state.board)
        if winner:
            st.session_state.winner = winner
        else:
            st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"

def AI_make_move(idx):
    if st.session_state.board[idx] == "" and not st.session_state.winner and st.session_state.current_player == "O":
        # Look into what board there is.

        # Check the kralen

        # Bereken de som kralen

        # kies een random getal tussen 0 en de som kralen

        # pick een random kraal (vind de index)

        # Kies het vakje van de kraal


def reset_game():
    st.session_state.board = [""] * 9
    st.session_state.current_player = "X"
    st.session_state.winner = None


# 3. Status display
if st.session_state.winner:
    if st.session_state.winner == "Tie":
        st.info("🤝 It's a draw!")
        # + 1 for all moves by AI in this round
    else: # Check of speler of AI heeft gewonnen ->
        st.success(f"🎉 Player **{st.session_state.winner}** wins!")
        # AI wint
            # +3 als AI wint
        # Speler wint
            # -1 als speler wint
    # Update de kralen

def update_pearls():
    pass

else:
    st.write(f"Current Turn: **Player {st.session_state.current_player}**")

# 4. Render the 3x3 board
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        idx = row * 3 + col
        cell_value = st.session_state.board[idx]

        # Display an empty space if unmarked so the button retains height
        cols[col].button(
            label=cell_value if cell_value else " ",
            key=f"cell_{idx}",
            on_click=make_move,
            args=(idx,),
            disabled=bool(cell_value or st.session_state.winner),
            use_container_width=True,
        )

# 5. Controls
st.button("Restart Game", on_click=reset_game, type="primary")