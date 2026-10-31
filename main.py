import os
from pathlib import Path
import streamlit as st
from Game import game_render, train_simulation
from Questions import QUESTIONS_BANK

BASE_DIR = Path(__file__).resolve().parent

# 1. State initialisatie voor de quiz
def init_quiz():
    if "current_question_idx" not in st.session_state:
        st.session_state.current_question_idx = 0
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
    if "answered" not in st.session_state:
        st.session_state.answered = False
    if "text_submitted" not in st.session_state:
        st.session_state.text_submitted = False
    if "last_correct" not in st.session_state:
        st.session_state.last_correct = None

def reset_quiz():
    st.session_state.current_question_idx = 0
    st.session_state.quiz_score = 0
    st.session_state.answered = False
    st.session_state.text_submitted = False
    st.session_state.last_correct = None

init_quiz()

# 2. Layout verdelen (Spel links, Vragen rechts)
col_game, col_quiz = st.columns([5, 4], gap="small")

with col_game:
    st.subheader("🎮 Boter Kaas en AIeren")
    game_render()

with col_quiz:
    st.subheader("💡 Kennistest")

    idx = st.session_state.current_question_idx
    if idx < len(QUESTIONS_BANK):
        q = QUESTIONS_BANK[idx]

        st.markdown(f"**Vraag {idx + 1} van {len(QUESTIONS_BANK)}**")
        st.write(q.prompt)

        # Afbeelding tonen indien aanwezig
        if getattr(q, "image_path", None):
            img_path = BASE_DIR / q.image_path
            if img_path.exists():
                st.image(str(img_path), use_container_width=True)
            elif os.path.exists(q.image_path):
                st.image(q.image_path, use_container_width=True)

        # Code snippet tonen indien aanwezig
        if getattr(q, "code_snippet", None):
            st.code(q.code_snippet, language="python")

        # ==========================================================
        # SCENARIO A: Open reflectievraag (zelf typen + vergelijken)
        # ==========================================================
        if getattr(q, "has_text_input", False):
            user_text = st.text_area(
                "Typ hier jouw antwoord:",
                key=f"text_input_{q.id}",
                disabled=st.session_state.text_submitted,
                placeholder="Typ hier kort wat jij denkt..."
            )

            # Stap 1: Antwoord nog niet onthuld
            if not st.session_state.text_submitted:
                if st.button("Controleer", key=f"btn_submit_text_{q.id}"):
                    if user_text.strip() == "":
                        st.warning("Typ eerst even een kort antwoord voordat je controleert!")
                    else:
                        st.session_state.text_submitted = True
                        st.rerun()

            # Stap 2: Antwoord is verstuurd -> Toon modelantwoord en laat speler zelf kiezen
            else:
                st.info(f"📋 **Het juiste antwoord:**\n\n{q.revealed_text}")

                user_choice = st.radio(
                    "Klopt dit met wat jij had opgeschreven?",
                    q.options,
                    key=f"eval_radio_{q.id}",
                    disabled=st.session_state.answered
                )

                if not st.session_state.answered:
                    if st.button("Bevestig evaluatie", key=f"btn_eval_{q.id}"):
                        selected_idx = q.options.index(user_choice)
                        is_correct = q.is_correct(selected_idx)
                        st.session_state.last_correct = is_correct

                        if is_correct:
                            st.session_state.quiz_score += 1

                        if getattr(q, "enable_autotrain", None):
                            train_simulation(q.enable_autotrain)

                        st.session_state.answered = True
                        st.rerun()
                else:
                    if st.session_state.last_correct:
                        st.success("🎉 Goed ingeschat!")
                    else:
                        st.warning("Geeft helemaal niks, hier leer je juist van!")

                    if q.explanation:
                        st.caption(q.explanation)

                    if st.button("Volgende vraag ➡️", key=f"next_{q.id}"):
                        st.session_state.current_question_idx += 1
                        st.session_state.answered = False
                        st.session_state.text_submitted = False
                        st.session_state.last_correct = None
                        st.rerun()

        # ==========================================================
        # SCENARIO B: Standaard Meerkeuzevraag
        # ==========================================================
        else:
            user_choice = st.radio(
                "Kies je antwoord:",
                q.options,
                key=f"q_{q.id}",
                disabled=st.session_state.answered
            )

            if not st.session_state.answered:
                if st.button("Controleren", key=f"btn_{q.id}"):
                    selected_idx = q.options.index(user_choice)
                    is_correct = q.is_correct(selected_idx)

                    st.session_state.last_correct = is_correct
                    if is_correct:
                        st.session_state.quiz_score += 1

                    if getattr(q, "enable_autotrain", None):
                        train_simulation(q.enable_autotrain)

                    st.session_state.answered = True
                    st.rerun()
            else:
                if st.session_state.last_correct:
                    st.success("🎉 Correct!")
                else:
                    st.error("❌ Dit is niet het antwoord wat we zochten.")

                if q.explanation:
                    st.info(q.explanation)

                if st.button("Volgende vraag ➡️", key=f"next_{q.id}"):
                    st.session_state.current_question_idx += 1
                    st.session_state.answered = False
                    st.session_state.last_correct = None
                    st.rerun()

    else:
        st.write("Je bent klaar met de quiz!\nSpeel vooral nog een paar potjes tegen je getrainde AI.")
        if st.button("Terug naar start"):
            reset_quiz()
            st.rerun()