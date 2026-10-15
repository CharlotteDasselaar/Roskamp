from random import randint

import streamlit as st

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

def init_pearls(start_pearl_amount = 3):
    """
    Creates the pearls (trainable entity) for this board in the game.
    This function is used when there is no
    :return:
    """
    st.session_state.current_game[st.session_state.board] = [start_pearl_amount if cell == "" else 0 for cell in st.session_state.board]

    # For every already filled in thing it needs to not have -> add if statement to init

def update_pearls(score):
    # Vind de juiste borden om te updaten
        # Boards waarbij geldt dat er meer x'en zijn dan o's?
    # Wat zijn de juiste zetten?
    # update de juiste zetten van de juiste borden met + of - een getal
    # clear the huidige zetten
    # clear de  huidige borden
    # Voeg huidig toe aan history / pas aan -> is hetzelfde voor al aanwezig of niet
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
        st.session_state.board[idx] = st.session_state.current_player
        winner = check_winner(st.session_state.board)
        if winner:
            st.session_state.winner = winner
        else:
            st.session_state.current_player = "O"
            AI_make_move()



def AI_make_move():
    if not st.session_state.winner and st.session_state.current_player == "O":
        #pass
        # Look into what board there is.
        if not st.session_state.history[st.session_state.board]:
            init_pearls()
        else:
            st.session_state.current_game[st.session_state.board] = st.session_state.history[st.session_state.board]

        # Bereken de som kralen
        pearls = st.session_state.current_game[st.session_state.board]

        # kies een random getal tussen 0 en de som kralen
        pearl_number = randint(0,sum(pearls))
        index_pearl = 8
        # pick een random kraal (vind de index)
        for idx in range(pearls):
            pearl_number -= pearls[idx]
            if pearl_number < 0:
                index_pearl = idx

        if st.session_state.board[index_pearl] != "_":
            st.session_state.board[index_pearl] = st.session_state.current_player
        else:
            raise Exception("Wrong index for AI to make move")

        winner = check_winner(st.session_state.board)
        if winner:
            st.session_state.winner = winner
        else:
            st.session_state.current_player = "X"



def reset_game():
    st.session_state.board = "_" * 9
    st.session_state.current_player = "X"
    st.session_state.winner = None
    st.session_state.current_game = {}

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
            disabled=bool(cell_value or st.session_state.winner),
            use_container_width=True,
        )

# 5. Controls
st.button("Restart Game", on_click=reset_game, type="primary")