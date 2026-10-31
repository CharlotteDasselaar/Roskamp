from dataclasses import dataclass, field
from typing import List, Optional

list_ntrain = [1000, 2000, 5000, 7000]
# 0: --> geen verschil duidelijk
# 1: -->  verschil duidelijk
# 2: --> maakt geen fouten tegen random speler
# 4: --> duidelijk dat tegen speler niet gaat werken.


# Vanaf wanneer is het te winnen voor de random speler en wanneer voor de speler himself?

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
            "Zoals je ziet maakt de AI snel zijn volgende zet. Je kunt hierna weer een zet zetten, zoals je daarnet hebt gedaan. "
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
            "Als je dacht dat de AI slecht in elkaar zat, dan heb je wel heel weinig vertrouwen in de maker! "
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
            "Druk eerst op de knop om de geschiedenis te wissen (schone lei) en maak daarna de tabel zichtbaar. "
            "Speel nu een paar wedstrijdjes met de tabel open. Wat gebeurt er?"
        ),
        unlock_button="geschiedenis",
        options=[
            "De geschiedenislijst wordt steeds langer en de cijfers in de tweede kolom veranderen nooit.",
            "De geschiedenislijst wordt steeds langer en de cijfers in de tweede kolom kunnen na wat wedstrijdjes veranderen.",
            "De geschiedenislijst wordt steeds korter en de cijfers in de tweede kolom veranderen nooit.",
            "De geschiedenislijst wordt steeds korter en de cijfers in de tweede kolom veranderen nooit meer.",
            "De geschiedenislijst wordt steeds korter en de cijfers in de tweede kolom kunnen na wat wedstrijdjes veranderen."
        ],
        correct_idx=1,
        explanation=(
            "De geschiedenislijst wordt steeds langer: de AI leert meer situaties kennen. "
            "De cijfers in de tweede kolom veranderen ook steeds; wat dat betekent ontdek je zo!"
        )
    ),
    Question(
        id=6,
        prompt=(
            "De eerste kolom geeft aan welk bord de AI heeft gezien. "
            "De tweede kolom geeft het aantal kralen aan per vakje van dat speelveld. Wat is een 'bord'?"
        ),
        options=[
            "De stand van de wedstrijd: waar nu de kruisjes, rondjes of lege vakjes staan.",
            "Een bord is een synoniem voor een kraal.",
            "Het bord is het lege speelveld zonder de stand van het spel.",
            "Het bord is een ander woord voor kruisje."
        ],
        correct_idx=0,
        explanation="Een bord is de actuele stand van de wedstrijd: waar kruisjes, rondjes en lege vakjes staan."
    ),
    Question(
        id=7,
        prompt="Wat is een 'kraal'?",
        options=[
            "De eenheid waarin wordt gemeten hoe vaak de AI een vakje heeft gekozen.",
            "Een manier om de kans van het kiezen van een vakje door de AI te bepalen.",
            "Een synoniem voor bord.",
            "Het percentage dat de AI wint."
        ],
        correct_idx=1,
        explanation="De kralen bepalen de kansverdeling: hoe meer kralen een vakje heeft, hoe groter de trekkans."
    ),
    Question(
        id=8,
        prompt=(
            "Maak af: Als er kralen worden toegevoegd voor een bepaald vakje, wordt de kans dat de AI dat vakje kiest "
            "[groter/kleiner/hetzelfde]. Als er kralen worden weggehaald, wordt die kans [groter/kleiner/hetzelfde]."
        ),
        options=[
            "groter, groter",
            "groter, kleiner",
            "groter, hetzelfde",
            "kleiner, groter",
            "kleiner, kleiner",
            "kleiner, hetzelfde",
            "hetzelfde, groter",
            "hetzelfde, kleiner",
            "hetzelfde, hetzelfde"
        ],
        correct_idx=1,
        explanation="Meer kralen = grotere kans om gekozen te worden. Minder kralen = kleinere kans."
    ),
    Question(
        id=9,
        prompt=(
            "In 1961 bouwde een onderzoeker een werkend AI-brein zónder computer, puur met luciferdoosjes en "
            "honderden gekleurde kralen. Elk doosje staat voor een specifieke situatie op het bord. In die doosjes zitten "
            "kralen die elk een vakje voorstellen; door blind een kraal te trekken kiest het systeem zijn zet. "
            "Het echte leren gebeurt na afloop: verliest de AI, dan worden gebruikte kralen weggehaald (straf). "
            "Wint de AI, dan worden er juist kralen bijgelegd (beloning).\n\n"
            "Welk type AI is Boter, Kaas en AIeren dus?"
        ),
        options=[
            "Deep learning",
            "Supervised Learning",
            "Unsupervised Learning",
            "Reinforcement Learning"
        ],
        correct_idx=3,
        explanation="Reinforcement Learning draait om het leren van gewenst gedrag via beloningen en straffen."
    ),

    # ----------------------------------------------------
    # DEEL 3: Eerste Training & Spelregels van het Systeem
    # ----------------------------------------------------

Question(
        id=10,
        prompt=(
            "Voordat we gaan trainen, doen we eerst een nulmeting! Druk op de knop 'Start Auto Speler'. "
            "De computer speelt nu als willekeurige speler (X) tegen jouw nog ongetrainde AI (O). "
            "Laat ze even 5 tot 10 potjes tegen elkaar spelen (en zet hem daarna weer op Stop). "
            "Wat valt je op aan de resultaten van de AI?"
        ),
        options=[
            "De AI wint veruit de meeste potjes van de willekeurige speler.",
            "De AI wint ongeveer de helft van de tijd, mogelijk zelfs minder!",
            "Bijna elk potje eindigt direct in een gelijkspel."
        ],
        correct_idx=1,
        explanation=(
            "Klopt! Omdat jouw AI nog helemaal ongetraind is, gokt hij blind. Omdat de AI als tweede speler (O) "
            "begint, heeft de beginnende speler (X) bij willekeurige zetten een voordeel (X wint normaal ~58% van de potjes). "
            "De AI is op dit moment dus nog een verliezer. Tijd om daar verandering in te brengen!"
        )
    ),

    Question(
        id=11,
        prompt=(
            "We beginnen deze AI steeds beter te snappen! Als beloning mag je op de 'Snel trainen'-knop drukken. "
            f"Hierdoor speelt de AI supersnel {list_ntrain[0]} wedstrijdjes tegen een willekeurige speler. "
            "Hoe vaker je traint, hoe beter de AI wordt!"
        ),
        enable_autotrain= list_ntrain[0],
        options=[f"Wat leuk! Start de {list_ntrain[0]} potjes."],
        correct_idx=0,
        explanation="De simulatie draait op de achtergrond en past direct alle kralen aan!"
    ),
Question(
        id=12,
        prompt=(
            "Laten we kijken wat die 1000 potjes training hebben opgeleverd! "
            "Druk op 'Start Auto Speler' en laat ze weer 3 tot 5 potjes tegen elkaar spelen (zet hem daarna weer op Stop). "
            "Merk je al een enorm verschil in de uitslagen?"
        ),
        options=[
            "Ja, de AI is opeens oppermachtig en wint bijna elk potje!",
            "Nee, er is eigenlijk nog niet heel veel verschil; de AI verliest nog steeds geregeld.",
            "De AI speelt vanaf nu alleen nog maar gelijkspel."
        ],
        correct_idx=1,
        explanation=(
            "Er is (als het goed is) nog niet heel veel veranderd! 1000 potjes klinkt als heel veel voor een mens, "
            "maar voor een AI is dit nog maar een warming-up. Omdat er honderden verschillende bordstanden zijn, "
            "heeft de AI veel situaties pas één of twee keer gezien. Hij heeft dus echt nog veel meer data en vlieguren nodig!"
        )
    ),
    Question(
        id=13,
        prompt=(
            "Stel je voor dat de AI vakje C2 kiest en de speler direct wint. "
            "Elk leeg vakje begint met 3 kralen en bij elk verlies verliest de AI 1 kraal voor die zet. "
            "Hoeveel wedstrijdjes moet de AI op deze manier verliezen totdat deze blunderzet nooit meer gedaan kan worden?"
        ),
        image_path="Bord voor vraag.png",
        options=["0", "4", "2", "3"],
        correct_idx=3,
        explanation=(
            "Je start met 3 kralen voor C2. Bij elk verlies gaat er 1 kraal af. "
            "Na 3 keer verliezen met die zet zijn er 0 kralen over, waardoor hij nooit meer getrokken kan worden."
        )
    ),
    Question(
        id=14,
        prompt=(
            "Kies de juiste woorden: De AI wint een wedstrijd. Hierna krijgt de AI een beloning van 3 kralen voor "
            "[elke zet / de laatste zet] die hij [die wedstrijd / gedurende het hele trainingsproces] gemaakt heeft."
        ),
        options=[
            "elke zet, die wedstrijd",
            "elke zet, gedurende het hele trainingsproces",
            "de laatste zet, die wedstrijd",
            "de laatste zet, gedurende het hele trainingsproces"
        ],
        correct_idx=0,
        explanation="Alle zetten die hebben bijgedragen aan de winst van díe specifieke wedstrijd krijgen de beloning."
    ),
    Question(
        id=15,
        prompt=(
            f"Tijd voor een upgrade! Druk op de snel-train-knop om de AI nog eens {list_ntrain[1]} wedstrijdjes "
            "te laten spelen tegen de willekeurige speler."
        ),
        enable_autotrain= list_ntrain[1],
        options=[f"Top, train {list_ntrain[1]} potjes!"],
        correct_idx=0,
        explanation="De AI leert nu razendsnel patronen herkennen van duizenden wedstrijden tegelijk."
    ),
    Question(
        id=16,
        prompt=(
            "We hebben de AI al flink getraind. Zet de Random Speler weer eens aan en speel zelf een paar potje). "
            "Merk je al dat de AI vooruitgaat?"
        ),
        options=[
            "Ik kan de AI niet verslaan en de random speler ook niet!",
            "Tegen de random speler gaat het best wel wat beter, maar ikzelf win nog redelijk makkelijk",
            "Zowel ik als speler als de random speler verslaan de AI makkelijk",
            "Ik kan de AI speler amper verslaan, maar de random speler doet het wel zo nu en dan hele."
        ],
        correct_idx=1,
        explanation="In principe zou de random speler het best wel wat beter moeten doen op dit punt, maar je zou zelf nog redelijk makkelijk moeten kunnen winnen. Dat is misschien gek... binnenkort kijken we waarom dit is!"
    ),
    Question(
        id=17,
        prompt=(
            "Als de AI gelijk speelt, worden de kralen van de gemaakte zetten verhoogd met 1. "
            "Wat zou een goede reden zijn om een beloning te geven terwijl de AI niet wint? "
            "Leg het kort uit in je eigen woorden:"
        ),
        has_text_input=True,
        revealed_text=(
            "Spelers zijn in het begin veel beter dan de AI. De beginnende AI is als een kleuter die willekeurig "
            "dingen roept; als die kleuter gelijk speelt tegen jou is dat al heel knap! Met een kleine beloning (+1) "
            "leert de AI dat gelijkspelen véél beter is dan verliezen."
        ),
        options=[
            "Mijn uitleg sloot hier goed bij aan!",
            "Ik had iets heel anders opgeschreven."
        ],
        correct_idx=0,
        explanation="Door gelijkspel te belonen leert de AI niet alleen hoe hij wint, maar vooral hoe hij niet verliest."
    ),

    # ----------------------------------------------------
    # DEEL 4: Data & Kansen Berekenen (Gevorderd)
    # ----------------------------------------------------
    Question(
        id=18,
        prompt=(
            "In de code zien de kralen er zo uit: 021003241. "
            "De volgorde staat voor de vakjes: A1, A2, A3, B1, B2, B3, C1, C2, C3. "
            "Welk vakje heeft nu 4 kralen?"
        ),
        options=["C3", "A3", "B1", "C2"],
        correct_idx=3,
        explanation="Het 8e getal in de reeks is een 4, en de 8e positie hoort bij vakje C2."
    ),
    Question(
        id=19,
        prompt=f"Laten we de AI weer een trainingsboost geven. Druk op de snel-train-knop voor {list_ntrain[2]} potjes!",
        enable_autotrain= list_ntrain[2],
        options=[f"Simuleer {list_ntrain[2]} potjes!"],
        correct_idx=0,
        explanation=f"{list_ntrain[2]} potjes worden in een fractie van een seconde doorgerekend."
    ),
    Question(
        id=20,
        prompt="Speel weer een potje tegen de AI. Merk je dat hij zijn verdediging beter op orde heeft?",
        options=[
            "Ik win altijd! De random player verliest altijd.",
            "De AI wordt beter, maar ik kan er nog steeds van winnen. Hij wint (vrijwel) altijd tegen de random speler.",
            "Nee, er is helemaal geen verbetering geweest deze hele tijd."
        ],
        correct_idx=1,
        explanation="In principe hoort het tweede antwoord het juiste antwoord te zijn. Speel anders nog een paar keer of dit klopt."
    ),
    Question(
        id=21,
        prompt=(
            "Bij de start van de training begint het bord in code als volgt: 3,3,3,3,3,3,3,3,3. "
            "Elk getal staat voor de kralen van één vakje (van A1 t/m C3). "
            "Stel dat de AI mag beginnen: wat is de kans dat de AI vakje C1 kiest?"
        ),
        options=["3/3", "3/9", "1/3", "1/9"],
        correct_idx=3,
        explanation="Totaal aantal kralen = 9 x 3 = 27. Vakje C1 heeft 3 kralen. De kans is 3/27, wat gelijk is aan 1/9."
    ),
    Question(
        id=22,
        prompt=(
            "De kralen van een bord zien er zo uit: 303020003 (3 voor A1, 3 voor A3, 2 voor B2 en 3 voor C3). "
            "Wat is de kans dat de AI vakje B2 kiest? (Geschreven als breuk)"
        ),
        options=["0", "2/11", "4/54", "3/11"],
        correct_idx=1,
        explanation="B2 heeft 2 kralen. Het totaal aantal kralen is 3 + 3 + 2 + 3 = 11. De kans is dus 2/11."
    ),
    Question(
        id=23,
        prompt=f"Tijd om nog een laatste ronde zoveel mogelijk {list_ntrain[3]} wedstrijdjes te trainen! Mogelijk kan je dan zelfs als speler niet winnen!",
        enable_autotrain=list_ntrain[3],
        options=[f"Train nog {list_ntrain[3]} potjes! We gaan het proberen! Dit kan even duren"],
        correct_idx=0,
        explanation="Laten we kijken hoe dit gaat..."
    ),
    Question(
        id=24,
        prompt="Test de AI nogmaals uit. Hoe gaat het spel nu?",
        options=[
            "Ik kan niet winnen van de AI... hij blijft me verslaan",
            "De AI speelt niet heel veel meer beter dan de vorige keer."
        ],
        correct_idx=1,
        explanation="De AI zou nog verslaanbaar moeten zijn, zelfs na zoveel trainingssessies. Ergens is dat best vervelend, hoe zou dat nu komen?"
    ),

    # ----------------------------------------------------
    # DEEL 5: Optimalisatie & Expert Vragen
    # ----------------------------------------------------

    Question(
        id=25,
        prompt=(
            "Met de optie 'Random Speler' kun je de AI snel trainen. "
            "Wat zijn hier de voor- en nadelen van?"
        ),
        options=[
            "Voordeel: tegenstander wordt ook slimmer; Nadeel: kost de computer veel energie.",
            "Voordeel: heel snel en automatisch; Nadeel: kost de computer extreem veel energie.",
            "Voordeel: heel snel en automatisch; Nadeel: de willekeurige speler leert de AI niet verdedigen tegen slimme menselijke tactieken.",
            "Voordeel: tegenstander wordt ook slimmer; Nadeel: willekeurige speler is niet zo slim als een mens."
        ],
        correct_idx=2,
        explanation=(
            "Antwoord C: De AI traint razendsnel tegen willekeurige zetten, maar leert daardoor "
            "nog niet hoe hij moet anticiperen op een mens die doelgericht een val opzet."
            "Dit is ook de reden dat je na zoveel trainen nogsteeds van deze AI zou winnen."
            "Je zou de AI goed kunnen trainen door zelf heeeel veel potjes ertegen te spelen, maar dat kost wel veel tijd ook."
            )
    ),

    Question(
        id=26,
        prompt=(
            "Expert-vraag: Nu blijven de beloningen (+3) en straffen (-1) gedurende het hele proces hetzelfde. "
            "Wat zou een goede verbetering zijn voor het trainingsproces?"
        ),
        options=[
            "Na meerdere wedstrijden gaan de beloningen en straffen dichter naar nul.",
            "Na meerdere wedstrijden worden de beloningen en straffen juist extremer.",
            "Na meerdere wedstrijden moeten de straffen veranderen in (kleine) beloningen.",
            "Na meerdere wedstrijden moeten de beloningen veranderen in (lichte) straffen."
        ],
        correct_idx=0,
        explanation=(
            "Antwoord A klopt! Aan het einde van de training staat de strategie al grotendeels vast. "
            "Door beloningen en straffen kleiner te maken (vergelijkbaar met 'learning rate decay'), "
            "voorkom je dat een toevallig verliespotje meteen een bewezen sterke tactiek overhoop gooit."
        )
    ),


    Question(
        id=27,
        prompt=(
            "Expert-vraag (geen zorgen als je geen programmeur bent!): "
            "Bekijk de onderstaande code. Wat gebeurt hier ongeveer? Typ een korte samenvatting:"
        ),
        ##Change into photo
        image_path = "Foto code voor vraag.png",
        has_text_input=True,
        revealed_text=(
            "Als er een winnaar/eindstand is en de score nog niet is verwerkt: "
            "als de AI ('O') wint krijgen de gebruikte kralen +3, bij gelijkspel +1, en als de speler wint "
            "krijgt de AI straf (-1 kraal). Daarna wordt gemarkeerd dat de stand is verwerkt."
        ),
        options=[
            "Dit kwam goed overeen met mijn uitleg!",
            "Ik vond de code te ingewikkeld / zat er naast."
        ],
        correct_idx=0,
        explanation="De code zet het Reinforcement Learning principe (winst = belonen, verlies = straffen) om in actie."
    ),
    Question(
        id=28,
        prompt=(
            "Dit systeem met luciferdoosjes en kralen werkt fantastisch voor boter-kaas-en-eieren. "
            "Waarom lukt het niet om een AI op exact déze manier te leren schaken?"
        ),
        options=[
            "Schaken heeft te veel oneerlijke regels voor kralen.",
            "Er zijn meer mogelijke schaakborden dan atomen in het heelal; je hebt miljarden kamers vol doosjes nodig.",
            "Bij schaken kun je niet met belonen en straffen werken.",
            "Een computer kan geen willekeurige zetten simuleren bij schaken."
        ],
        correct_idx=1,
        explanation=(
            "Antwoord B! Dit heet de 'combinatorische explosie'. Boter-kaas-en-eieren heeft maar enkele honderden "
            "unieke bordstanden. Schaken heeft er naar schatting 10^43. Moderne schaak-AI's (zoals AlphaZero) "
            "gebruiken daarom neurale netwerken (Deep Learning) die patronen herkennen in plaats van elke situatie apart op te slaan."
        )
    ),

    # ----------------------------------------------------
    # DEEL 6: Finale & Vrij Experimenteren
    # ----------------------------------------------------
    Question(
        id=29,
        prompt=(
            "Gefeliciteerd, je hebt de hele quiz en het trainingsproces doorlopen! "
            "De snel-train-knop staat vanaf nu permanent open. Experimenteer gerust verder om te zien of je "
            "de AI helemaal onverslaanbaar kunt maken."
        ),
        permanent_autotrain=True,
        options=[
            "Ik ben tevreden en wil vrij verder spelen!",
            "Ik wil alles resetten en helemaal opnieuw beginnen."
        ],
        correct_idx=0,
        explanation="Je kunt nu onbeperkt doortrainen of via de reset-knop weer met een leeg brein beginnen."
    )
]