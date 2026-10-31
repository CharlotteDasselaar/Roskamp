import streamlit as st
#from questions import QUESTIONS_BANK
from Game import game_render
from Game import train_simulation
from Questions import QUESTIONS_BANK
import os
from pathlib import Path

# 1. State initialisatie voor de quiz
def init_quiz():
    if "current_question_idx" not in st.session_state:
        st.session_state.current_question_idx = 0
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
    if "answered" not in st.session_state:
        st.session_state.answered = False

def reset_quiz():
    st.session_state.current_question_idx = 0
    st.session_state.quiz_score = 0
    st.session_state.answered = False
init_quiz()
# 2. Layout verdelen (Spel links, Vragen rechts)
col_game, col_quiz = st.columns([5, 4], gap="xsmall")

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

        BASE_DIR = Path(__file__).resolve().parent

        if getattr(q, "image_path", None):
            img_full_path = BASE_DIR / q.image_path
            if img_full_path.exists():
                st.image(str(img_full_path), use_container_width=True)
            else:
                st.warning(f"Afbeelding niet gevonden: {q.image_path}")

        # Keuzemenu
        user_choice = st.radio(
            "Kies je antwoord:",
            q.options,
            key=f"q_{q.id}",
            disabled=st.session_state.answered
        )

        # 1. Zorg dat last_correct geïnitialiseerd is bij je session_state
        if "last_correct" not in st.session_state:
            st.session_state.last_correct = None

        # 2. Vraag-afhandeling
        if not st.session_state.answered:
            if st.button("Controleren", key=f"btn_{q.id}"):
                selected_idx = q.options.index(user_choice)
                is_correct = q.is_correct(selected_idx)

                # Sla resultaat op in state
                st.session_state.last_correct = is_correct
                if is_correct:
                    st.session_state.quiz_score += 1

                if q.enable_autotrain:
                    train_simulation(q.enable_autotrain)
                    st.info("De AI wordt nu getrained!")

                st.session_state.answered = True
                st.rerun()

        else:
            # Toon HIER de feedback, zodat deze zichtbaar blijft
            if st.session_state.last_correct:
                st.success("🎉 Correct!")
            else:
                st.error("❌ Dit is niet het antwoord wat we zochten.")

            if q.explanation:
                st.info(q.explanation)

            if st.button("Volgende vraag ➡️"):
                st.session_state.current_question_idx += 1
                st.session_state.answered = False
                st.session_state.last_correct = None
                st.rerun()
    else:
        st.write(f"Je bent klaar met de quiz.\nSpeel vooral nog met je goede AI systeem!")
        if st.button("Terug naar start"):
            reset_quiz()
            st.rerun()

