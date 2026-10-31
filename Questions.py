from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Question:
    id: int
    prompt: str
    options: List[str] = field(default_factory=list)
    correct_idx: Optional[int] = None
    explanation: Optional[str] = None

    # --- Extra features voor de interactieve flow ---
    until_correct: bool = False            # Pas doorgaan als het antwoord goed is
    has_text_input: bool = False           # Toon een open tekstveld voor de gebruiker
    revealed_text: Optional[str] = None    # Uitleg die zichtbaar wordt na het typen
    unlock_button: Optional[str] = None    # Ontgrendelt een knop in de app (bv. 'geschiedenis')
    enable_autotrain: Optional[int] = None # Toont de sneltrein-knop met N simulaties
    permanent_autotrain: bool = False      # Houdt sneltrainen permanent actief
    image_path: Optional[str] = None       # Toont een afbeelding bij de vraag
    code_snippet: Optional[str] = None     # Toont een opgemaakt codeblok

    def is_correct(self, selected_idx: int) -> bool:
        if self.correct_idx is None:
            return True
        return selected_idx == self.correct_idx


QUESTIONS_BANK = [
    # ----------------------------------------------------
    # DEEL 1: Introductie & Zelf Ervaren
    # ----------------------------------------------------
    Question(
        id=1,
        prompt=(
            "Welkom bij boter kaas en AIeren! Bij dit spel ga je leren hoe dit type AI werkt. "
            "Jij bent de speler en bent het kruisje (X), de AI is het rondje (O). "
            "Druk eens op een vakje om dat te kiezen. Is het gelukt?"
        ),
        options=[
            "Ja! Ik kan een vakje aantikken en dan staat daar een kruisje.",
            "Het lukt me helaas nog niet."
        ],
        correct_idx=0,
        until_correct=True,
        explanation="Als het niet lukt, vraag een buur om je te helpen. Lukt het dan nog niet, haal de spreker erbij."
    ),
    Question(
        id=2,
        prompt=(
            "Zoals je ziet maakt de AI snel zijn volgende zet. Je kunt hierna weer zetten zoals daarnet. "
            "Speel zo eens een potje uit. Is het mogelijk om van de AI te winnen?"
        ),
        options=[
            "Nee, de AI is onverslaanbaar.",
            "Ik kan van de AI winnen.",
            "Ik loop even helemaal vast."
        ],
        correct_idx=1,
        until_correct=True,
        explanation="Als je vastloopt of niet kunt winnen, vraag even aan iemand naast je of roep de spreker."
    ),
    Question(
        id=3,
        prompt="Het is dus heel makkelijk om van de AI te winnen. Wat betekent dat denk je?",
        options=[
            "De AI is verkeerd in elkaar gezet, maar wel al getraind.",
            "De AI is goed in elkaar gezet en al getraind.",
            "De AI is verkeerd in elkaar gezet en niet getraind.",
            "De AI is goed in elkaar gezet, maar nog niet getraind."
        ],
        correct_idx=3,
        explanation=(
            "Als je dacht dat de AI slecht in elkaar zat, heb je wel weinig vertrouwen in de maker! "
            "Het probleem is simpelweg dat de AI nog niet getraind is; na het trainen zou hij goed moeten spelen."
        )
    ),
    Question(
        id=4,
        prompt=(
            "De AI zou dus werken als je hem traint. 'Trainen' is een begrip dat vaak rondgaat bij AI. "
            "Maar wat wordt er eigenlijk bedoeld met 'trainen' als het over AI gaat? "
            "Leg het hieronder uit in je eigen woorden (een paar zinnen is genoeg):"
        ),
        has_text_input=True,
        revealed_text=(
            "Het trainen van een AI is een proces waarbij de AI steeds voorbeelden krijgt. "
            "In dit spel zijn dat gespeelde wedstrijdjes. De AI leert van deze voorbeelden en wordt "
            "steeds een stukje beter in zijn specifieke taak."
        ),
        options=[
            "Ja, dat komt inderdaad genoeg overeen met mijn antwoord.",
            "Nee, ik had echt iets totaal anders opgeschreven."
        ],
        correct_idx=0,
        explanation="Als je het nog lastig vindt, kun je altijd even om extra toelichting vragen!"
    ),

    # ----------------------------------------------------
    # DEEL 2: Onder de Motorkap (Geschiedenis & Kralen)
    # ----------------------------------------------------
    Question(
        id=5,
        prompt=(
            "We weten nu dat de AI getraind moet worden met meerdere potjes. We hebben een nieuwe knop ontgrendeld! "
            "Hiermee krijg je een tabel te zien met de onderliggende data van het spel. "
            "Druk eerst op de knop om de geschiedenis te wissen (schone lei