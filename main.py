import streamlit as st
#from questions import QUESTIONS_BANK
from Game import game_render
from Questions import QUESTIONS_BANK

# 1. State initialisatie voor de quiz
if "current_question_idx" not in st.session_state:
    st.session_state.current_question_idx = 0
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False

# 2. Layout verdelen (Spel links, Vragen rechts)
col_game, col_quiz = st.columns([3, 2], gap="large")

with col_game:
    st.subheader("🎮 Boter Kaas en AIeren")
    game_render()

    # Hier komt je bestaande 3x3 bord-rendering...
with col_quiz:
    st.subheader("💡 Kennistest")

    idx = st.session_state.current_question_idx
    if idx < len(QUESTIONS_BANK):
        q = QUESTIONS_BANK[idx]

        st.markdown(f"**Vraag {idx + 1} van {len(QUESTIONS_BANK)}**")
        st.write(q.prompt)

        # Keuzemenu
        user_choice = st.radio(
            "Kies je antwoord:",
            q.options,
            key=f"q_{q.id}",
            disabled=st.session_state.answered
        )

        if not st.session_state.answered:
            if st.button("Controleren", key=f"btn_{q.id}"):
                selected_idx = q.options.index(user_choice)
                if q.is_correct(selected_idx):
                    st.success("Correct!")
                    st.session_state.quiz_score += 1
                else:
                    st.error("Helaas, onjuist.")

                if q.explanation:
                    st.info(q.explanation)

                st.session_state.answered = True
                st.rerun()
        else:
            if st.button("Volgende vraag ➡️"):
                st.session_state.current_question_idx += 1
                st.session_state.answered = False
                st.rerun()
    else:
        st.success(
            f"Gefeliciteerd! Je hebt alle vragen afgerond. Score: {st.session_state.quiz_score}/{len(QUESTIONS_BANK)}")
        if st.button("Herstart Quiz"):
            st.session_state.current_question_idx = 0
            st.session_state.quiz_score = 0
            st.session_state.answered = False
            st.rerun()
