# %%
import random as rng
from typing import Optional, Literal
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


print('Hello g4m€rZ')
d = Deck()
print(d)


# %%
