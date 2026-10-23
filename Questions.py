# Hier komen de questions
# Init some questions correct thing
# Init page number

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Question:
    id: int
    prompt: str
    options: List[str]
    correct_idx: int
    explanation: Optional[str] = None

    def is_correct(self, selected_idx: int) -> bool:
        return selected_idx == self.correct_idx


QUESTIONS_BANK = [
    Question(
        id=1,
        prompt="Waarmee traint het MENACE-algoritme?",
        options=["Neurale netwerken", "Kralen/luciferdoosjes", "Backpropagation"],
        correct_idx=1,
        explanation="Donald Michie gebruikte in 1961 luciferdoosjes gevuld met gekleurde kralen."
    ),
    Question(
        id=2,
        prompt="Wat gebeurt er als de AI verliest?",
        options=["Hij krijgt een extra kraal", "Er wordt een kraal weggehaald", "Niets"],
        correct_idx=1,
        explanation="Als straf voor de verloren zet verliest het doosje de gespeelde kraal."
    ),
]