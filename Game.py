import streamlit as st
import random
import time
import pandas as pd

st.set_page_config(page_title="Tic-Tac-Toe", page_icon="🎮")
st.title("Boter Kaas en AIeren")

def init_game_state():
    # 1. Initialize persistent state
    if "board" not in st.session_state:
        st.session_state.board = "_" * 9
    if "current_player" not in st.session_state:
        st.session_state.current_player = "X"
    if "winner" not in st.session_state:
        st.session_state.winner = None
    if "history" not in st.session_state:
        st.session_state.history = {}
    if "current_game" not in st.session_state:
        st.session_state.current_game = {}
    if "AI_moves" not in st.session_state:
        st.session_state.AI_moves = []
    if "random_player" not in st.session_state:
        st.session_state.random_player = False
    if "n_auto_games" not in st.session_state:
        st.session_state.n_auto_games = 1000
    if "game_scored" not in st.session_state:
        st.session_state.game_scored = False

    # Custom CSS for large buttons
    st.markdown(
        """
        <style>
        div[data-testid="stButton"] > button {
            width: 100%;
            
            
            aspect-ratio: 1 / 1;
            height: auto !important;
            padding: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.5rem;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )



def train_simulation(num_games=1000):
    """Simulates N games in milliseconds to train history."""
    for _ in range(num_games):
        b = "_" * 9
        ai_game_states = {}  # board: chosen_move
        winner = None

        while not winner:
            # Player X (Random)
            empty_x = [i for i, c in enumerate(b) if c == "_"]
            b = b[:empty_x[0]] + "X" + b[empty_x[0] + 1:] if len(empty_x) == 1 else (
                lambda idx: b[:idx] + "X" + b[idx + 1:]
            )(random.choice(empty_x))

            winner = check_winner(b)
            if winner:
                break

            # Player O (MENACE AI)
            if b not in st.session_state.history:
                # Dynamic starting beads: more beads early, fewer beads late
                remaining_empty = b.count("_")
                init_val = max(1, remaining_empty // 2)
                st.session_state.history[b] = [init_val if c == "_" else 0 for c in b]

            pearls = st.session_state.history[b]
            legal = [i for i, c in enumerate(b) if c == "_"]

            if sum(pearls) == 0:
                move = random.choice(legal)
            else:
                move = random.choices(range(9), weights=pearls, k=1)[0]

            ai_game_states[b] = move
            b = b[:move] + "O" + b[move + 1:]
            winner = check_winner(b)

        # Distribute rewards
        reward = 3 if winner == "O" else (1 if winner == "Tie" else -1)
        for board_state, move_taken in ai_game_states.items():
            current_pearls = st.session_state.history[board_state]
            current_pearls[move_taken] = max(0, current_pearls[move_taken] + reward)


def change_board(char, idx):
    st.session_state.board = (
        st.session_state.board[:idx] + char + st.session_state.board[idx + 1 :]
    )


def init_pearls(start_pearl_amount=3):
    st.session_state.current_game[st.session_state.board] = [
        start_pearl_amount if cell == "_" else 0
        for cell in st.session_state.board
    ]


def update_pearls(score):
    boards_2_update = [
        b
        for b in st.session_state.current_game
        if b.count("X") > b.count("O")
    ]
    for b in st.session_state.current_game.keys():
        if b in boards_2_update:
            board_tot_moves = b.count("X") + b.count("O")
            index_for_AImoves = (board_tot_moves - 1) // 2
            if index_for_AImoves < len(st.session_state.AI_moves):
                AImove = st.session_state.AI_moves[index_for_AImoves]
                new_value = st.session_state.current_game[b][AImove] + score
                st.session_state.current_game[b][AImove] = max(0, new_value)

    st.session_state.history.update(st.session_state.current_game)


def reset_game():
    st.session_state.board = "_" * 9
    st.session_state.current_player = "X"
    st.session_state.winner = None
    st.session_state.current_game = {}
    st.session_state.AI_moves = []
    st.session_state.games_scored = False


def reset_history():
    st.session_state.history = {}
    reset_game()


def toggle_random_player():
    st.session_state.random_player = not st.session_state.random_player


# 2. Game logic functions
def check_winner(board):
    win_lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6),              # Diagonals
    ]
    for a, b, c in win_lines:
        if board[a] != "_" and board[a] == board[b] == board[c]:
            return board[a]
    if "_" not in board:
        return "Tie"
    return None


def execute_player_move(idx):
    """Executes a move for human or random player (X) without recursive calls."""
    if st.session_state.board[idx] == "_" and not st.session_state.winner:
        change_board("X", idx)
        winner = check_winner(st.session_state.board)
        if winner:
            st.session_state.winner = winner
        else:
            st.session_state.current_player = "O"


def execute_ai_move():
    """Executes a single move for the MENACE AI (O)."""
    if st.session_state.board not in st.session_state.history:
        init_pearls()
    else:
        st.session_state.current_game[st.session_state.board] = list(
            st.session_state.history[st.session_state.board]
        )

    pearls = st.session_state.current_game[st.session_state.board]

    # Fallback to random legal move if bead count dropped to 0
    if sum(pearls) == 0:
        legal_indices = [i for i, c in enumerate(st.session_state.board) if c == "_"]
        index_pearl = random.choice(legal_indices)
    else:
        index_pearl = random.choices(range(len(pearls)), weights=pearls, k=1)[0]

    change_board("O", index_pearl)
    st.session_state.AI_moves.append(index_pearl)

    winner = check_winner(st.session_state.board)
    if winner:
        st.session_state.winner = winner
    else:
        st.session_state.current_player = "X"


# 3. Status Display
def game_render():

    init_game_state()

    if st.session_state.winner:
        if st.session_state.winner == "Tie":
            st.info("🤝 It's a draw!")
        else:
            st.success(f"🎉 Player **{st.session_state.winner}** wins!")
    else:
        st.write(f"Current Turn: **Player {st.session_state.current_player}**")

    # 4. Render 3x3 Board
    for row in range(3):
        cols = st.columns(3, width=90 * 3)
        for col in range(3):
            idx = row * 3 + col
            cell_value = st.session_state.board[idx]
            cols[col].button(
                label=cell_value if cell_value != "_" else " ",
                key=f"cell_{idx}",
                on_click=execute_player_move,
                args=(idx,),
                disabled=bool(
                    cell_value != "_"
                    or st.session_state.winner
                    or st.session_state.random_player
                ),
                use_container_width=True,
            )

    # 5. Controls
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    col_btn1.button("Herstart Spel", on_click=reset_game, type="primary")
    col_btn2.button("Herstart geschiedenis", on_click=reset_history, type="primary", width = 80)
    col_btn3.button(
        "Stop Auto Speler" if st.session_state.random_player else "Start Auto Speler",
        on_click=toggle_random_player,
        type="secondary" if st.session_state.random_player else "primary",
    )

    if st.button(f"⚡ Fast Train \n{st.session_state.n_auto_games} Games"):
        with st.spinner(f"Training {st.session_state.n_auto_games} games in memory..."):
            train_simulation(st.session_state.n_auto_games)
        st.success(f"Trained {st.session_state.n_auto_games} games! Test against the AI now.")

    # 6. Afhandeling van beurten en einde van het spel
    if st.session_state.winner:
        # Stap 1: Pas de kralen exact één keer aan
        if not st.session_state.game_scored:
            if st.session_state.winner == "O":
                update_pearls(3)
            elif st.session_state.winner == "Tie":
                update_pearls(1)
            else:
                update_pearls(-1)
            st.session_state.game_scored = True

        # Stap 2: Automatisch nieuw potje starten
        if st.session_state.random_player:
            time.sleep(0.2)
            reset_game()
            st.rerun()
        else:
            # Menselijke speler: geef 1.5 seconde om de uitslag te zien, daarna schone start
            st.caption("Nieuw potje start automatisch over 0.8 seconde...")
            #if st.button("Direct volgend potje ➡️"):
            #    reset_game()
            #    st.rerun()
            time.sleep(0.8)
            reset_game()
            st.rerun()

    elif st.session_state.current_player == "O":
        # AI is aan de beurt
        time.sleep(0.15)
        execute_ai_move()
        st.rerun()

    elif st.session_state.current_player == "X" and st.session_state.random_player:
        # Automatische tegenspeler is aan de beurt
        time.sleep(0.15)
        empty_indices = [i for i, c in enumerate(st.session_state.board) if c == "_"]
        if empty_indices:
            execute_player_move(random.choice(empty_indices))
            st.rerun()

    # Als current_player == "X" en random_player == False:
    # Doe NIETS! Het script stopt hier en wacht netjes tot de mens een vakje aanklikt.