# %%
import random as rng
import pandas as pd
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

    def draw_card(self):
        if self.cards:
            return self.cards.pop()
        else:
            return None
            # TODO: _rebuild_deck(self) # -> créer Discard

    def stats(self):
        df = pd.DataFrame([{'value': card.value, 'score': card.score, 'type': card.type} for card in self.cards])

        return df.value.value_counts().reset_index()


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

    def check_duplicate(self, value):
        """Vérifie si le joueur a déjà une carte en main."""
        # TODO, pour la carte à effet 2e chance, ajouter un argument 'type' ou quoi qui checkera si le joueur a déjà cette carte
        return any(card.value == value for card in self.hand)

    def __repr__(self):
        return (f"Player(turn={self.turn}, total_score={self.total_score}, "
                f"turn_score={self.turn_score}, hand={self.hand})")


class GameEngine:
    def __init__(self, players: List[Player]):
        self.players = players
        self.deck = Deck()
        self.current_player_index = 0
        self.game_over = False

    def initialize_game(self):
        """Initialise le jeu en distribuant les cartes aux joueurs."""
        self.deck.shuffle()
        for player in self.players:
            card = self.deck.draw_card()
            if card:
                player.add_card_to_hand(card)
            # TODO: gérer le draw d'une carte à effet -> draw3 ou stop

    def next_turn(self):
        """Passe au tour du joueur suivant."""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def play_turn(self):
        """Joue un tour pour le joueur actuel."""
        current_player = self.players[self.current_player_index]
        print(f"Tour du joueur {current_player.turn}")

        # C'est ici qu'il faudra intégrer toute l'intelligence du moteur :
        # tirer une carte si les chances de break sont acceptables
        # choisir à qui attribuer un stop ou un draw 3

        # Action de base : draw une carte
        # check doublon : break (sauf si second_chance)

        # règle des flip 7 : fin de la manche pour tout le monde

        card_drawn = self.deck.draw_card()
        if card_drawn:
            print(f"le joueur {current_player} a tiré la carte {card_drawn}")

            if current_player.check_duplicate(card_drawn.value):
                print(f"Joueur {current_player} a déjà une carte de valeur {card_drawn.value}. "
                      f"Son tour s'arrête et il marque 0 point pour cette manche.")
                current_player.turn_score = 0
            else:
                current_player.add_card_to_hand(card_drawn)
                current_player.calculate_turn_score()

        # Passer au joueur suivant
        self.next_turn()

    def check_game_over(self):
        """Vérifie si le jeu est terminé."""
        # Si un seul des joueurs a au moins 200 points, c'est la fin de game
        if any(p.total_score >= 200 for p in self.players):
            self.game_over = True
            self.determine_winner()

    def determine_winner(self):
        """Détermine le gagnant du jeu."""
        winner = max(self.players, key=lambda player: player.total_score)
        print(f"Le gagnant est le joueur {winner.turn} avec un score de {winner.total_score}")

    def run_game(self):
        """Exécute la boucle principale du jeu."""
        self.initialize_game()
        while not self.game_over:
            self.play_turn()
            self.check_game_over()


# Exemple d'utilisation
players_ = [Player(turn=i) for i in range(2)]  # Créer 2 joueurs
game_engine = GameEngine(players_)
game_engine.run_game()


print('Hello g4m€rZ')
d = Deck()
print(d)


# %%
