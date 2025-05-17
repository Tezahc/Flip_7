# %%
import random as rng
from typing import Optional, Literal, List
from icecream import ic


class Card:
    def __init__(self, score: int, value: Optional[str] = '', type_: Optional[Literal['number', 'bonus', 'effect']] = None):
        self.score = score or 0
        self.value = value
        self.type = type_ or 'number'

    def __repr__(self):
        return f"val:{self.value}-type:{self.type}-score:{self.score}"

    def __str__(self):
        return f"val:{self.value}-type:{self.type}"


class Deck:
    def __init__(self):
        self.cards = []
        deck_build_list = {
            "numbers" : list(range(13)),
            "bonus" : list(range(2, 11, 2)),
            "effect" : [3]*3
        }

        for type_, list_ in deck_build_list.items():
            if type_ == "numbers":
                self.cards.extend([Card(i) for i in list_ for _ in range(i or 1)])
            elif type_ == "bonus":
                self.cards.extend([Card(0, str(i), 'bonus') for i in list_])
                self.cards.append(Card(0, '*2', 'bonus'))
            elif type_ == "effect":
                self.cards.extend([Card(0, 'stuff', 'effect') for i in list_ for _ in range(i)])

    def __repr__(self):
        return f"{[str(card) for card in self.cards]}"

    def shuffle(self):
        rng.shuffle(self.cards)


class Player:
    def __init__(self, turn: int):
        self.hand: List[Card] = []  # Les cartes qu'il a en main cette manche
        self.turn: int = turn       # Position du joueur / ID
        self.total_score: int = 0   # Score total de la partie
        self.turn_score: int = 0    # Score marqué à la fin du tour

    def add_card_to_hand(self, card: Card):
        """Ajoute une carte à la main du joueur."""
        self.hand.append(card)

    def calculate_turn_score(self):
        """Calcule le score du tour en fonction des cartes en main."""
        self.turn_score = sum(card.score for card in self.hand)

    def update_total_score(self):
        """Met à jour le score total avec le score du tour."""
        self.total_score += self.turn_score
        self.turn_score = 0  # Réinitialise le score du tour

    def clear_hand(self):
        """Vide la main du joueur à la fin du tour."""
        self.hand = []

    def __repr__(self):
        return (f"Player(turn={self.turn}, total_score={self.total_score}, "
                f"turn_score={self.turn_score}, hand={self.hand})")


print('Hello g4m€rZ')
d = Deck()
print(d)


# %%
