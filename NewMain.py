from random import randint

import streamlit as st
import random
from torch.fx.passes.infra.pass_manager import pass_result_wrapper

st.set_page_config(page_title="Tic-Tac-Toe", page_icon="🎮")
st.title("Boter Kaas en AIeren")

# 1. Initialize persistent state
if "board" not in st.session_state:
    st.session_state.board = "_" * 9 # String lenght 9
if "current_player" not in st.session_state:
    st.session_state.current_player = "X" # Character
if "winner" not in st.session_state:
    st.session_state.winner = None
if "history" not in st.session_state:
    st.session_state.history = {} # Dict
if "current_game" not in st.session_state:
    st.session_state.current_game = {} # Dict
if "AI_moves" not in st.session_state:
    st.session_state.AI_moves = []


# Optional CSS to make the buttons appear large and square
st.markdown(
    """
    <style>
    div.stButton > button {
        height: 80px;
        font-size: 36px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def change_board(char, idx):
    """
    Changes board by inserting a character at a certain index.
    :param char:
    :param idx:
    :return:
    """
    st.session_state.board = st.session_state.board[:idx] + char + st.session_state.board[idx + 1:]

def init_pearls(start_pearl_amount = 3):
    """
    Creates the pearls (trainable entity) for this board in the game.
    This function is used when there is no
    :return:
    """
    st.session_state.current_game[st.session_state.board] = [start_pearl_amount if cell == "_" else 0 for cell in st.session_state.board]

    # For every already filled in thing it needs to not have -> add if statement to init

def update_pearls(score):
    # Vind de juiste borden om te updaten
    #boards_2_update = set()
    boards_2_update = [
        board for board in st.session_state.current_game
        if board.count("X") > board.count("O")
    ]
    # Wat zijn de juiste zetten?
    for board in st.session_state.current_game.keys():
        if board in boards_2_update:
            board_tot_moves = board.count("X") + board.count("O")
            # 0 -> x, 1-> 0, 2-> x, 3 -> 1,
            index_for_AImoves = (board_tot_moves - 1) / 2
            AImove = st.session_state.AI_moves[index_for_AImoves]
            st.session_state.current_game[board][AImove] += score

    # update de juiste zetten van de juiste borden met + of - een getal
    # clear the huidige zetten -> reset game
    # clear de  huidige borden -> reset game
    # Voeg huidig toe aan history / pas aan -> is hetzelfde voor al aanwezig of niet
    st.session_state.history.update(st.session_state.current_game)
    pass



# 2. Game logic functions
def check_winner(board): # Here it might go BOOM if turned into string
    win_lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6),  # Diagonals
    ]
    for a, b, c in win_lines:
        if board[a] != "_" and board[a] == board[b] == board[c]:
            return board[a]
    if "_" not in board:
        return "Tie"
    return None


def make_move(idx):
    if st.session_state.board[idx] == "_" and not st.session_state.winner and st.session_state.current_player == "X":
        #st.session_state.board[idx] = st.session_state.current_player
        change_board("X",idx)
        winner = check_winner(st.session_state.board)
        if winner:
            st.session_state.winner = winner
        else:
            st.session_state.current_player = "O"
            AI_make_move()



def AI_make_move():
    if not st.session_state.winner and st.session_state.current_player == "O":
        # Look into what board there is.
        if not st.session_state.board in st.session_state.history:
            init_pearls()
        else:
            st.session_state.current_game[st.session_state.board] = st.session_state.history[st.session_state.board]

        # Bereken de som kralen
        pearls = st.session_state.current_game[st.session_state.board]

        if sum(pearls) == 0:
            raise Exception("No pearl found")
        else:
            index_pearl = random.choices(range(len(pearls)), weights=pearls, k=1)[0]

        if st.session_state.board[index_pearl] == "_":
            #st.session_state.board[index_pearl] = st.session_state.current_player
            change_board(st.session_state.current_player, index_pearl)
            st.session_state.AI_moves.append(index_pearl)
        else:
            raise Exception("Wrong index for AI to make move")

        winner = check_winner(st.session_state.board)
        if winner:
            st.session_state.winner = winner
        else:
            st.session_state.current_player = "X" #



def reset_game():
    st.session_state.board = "_" * 9
    st.session_state.current_player = "X"
    st.session_state.winner = None
    st.session_state.current_game = {}
    st.session_state.AI_moves = []

def reset_history():
    st.session_state.history = {}
    reset_game()


# 3. Status display
if st.session_state.winner:
    if st.session_state.winner == "Tie":
        st.info("🤝 It's a draw!")
        # + 1 for all moves by AI in this round -> RUN UPDATE PEARLS
        update_pearls(1)
    else: # Check of speler of AI heeft gewonnen ->
        st.success(f"🎉 Player **{st.session_state.winner}** wins!")
        # AI wint
            # +3 als AI wint
        # Speler wint
            # -1 als speler wint
    # Update de kralen
else:
    st.write(f"Current Turn: **Player {st.session_state.current_player}**")


# 4. Render the 3x3 board
for row in range(3):
    cols = st.columns(3, width = 90 * 3)
    for col in range(3):
        idx = row * 3 + col
        cell_value = st.session_state.board[idx]

        # Display an empty space if unmarked so the button retains height
        cols[col].button(
            label=cell_value if cell_value else " ",
            key=f"cell_{idx}",
            on_click=make_move,
            args=(idx,),
            disabled=bool(cell_value != "_" or st.session_state.winner),
            use_container_width=True,
        )

# 5. Controls
st.button("Restart Game", on_click=reset_game, type="primary")