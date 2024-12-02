import sys
from collections import deque
from itertools import islice
from typing import Deque, TextIO, Tuple


def process_player(raw_player_deck: str) -> Deque[int]:
    player_deck = raw_player_deck.splitlines(False)
    deck = []

    for card in player_deck[1:]:
        deck.append(int(card))

    return deque(deck)


def calculate_player_score(deck: Deque[int]) -> int:
    score = 0
    deck.reverse()

    for index, card in enumerate(deck, 1):
        score += index * card

    return score


def crab_combat(player1_deck: Deque[int], player2_deck: Deque[int]) -> Tuple[str, int]:
    player1_check, player2_check = ([player1_deck.copy()], [player2_deck.copy()])
    games = 0

    while True:
        for player1_recursion_deck in player1_check:
            if player1_deck == player1_recursion_deck:
                for player2_recursion_deck in player2_check:
                    if player2_deck == player2_recursion_deck:
                        if games > 0:
                            return ("P1", calculate_player_score(player1_deck))

        player1_check.append(player1_deck.copy())
        player2_check.append(player2_deck.copy())

        player1_card = player1_deck.popleft()
        player2_card = player2_deck.popleft()

        if player1_card <= len(player1_deck) and player2_card <= len(player2_deck):
            player1_recursive_deck = islice(player1_deck, 0, player1_card)
            player2_recursive_deck = islice(player2_deck, 0, player2_card)

            winner, _ = crab_combat(deque(player1_recursive_deck), deque(player2_recursive_deck))

            if winner == "P1":
                player1_deck.append(player1_card)
                player1_deck.append(player2_card)
            elif winner == "P2":
                player2_deck.append(player2_card)
                player2_deck.append(player1_card)
        else:
            if player1_card > player2_card:
                player1_deck.append(player1_card)
                player1_deck.append(player2_card)
            else:
                player2_deck.append(player2_card)
                player2_deck.append(player1_card)

            if len(player1_deck) == 0:
                return ("P2", calculate_player_score(player2_deck))
            elif len(player2_deck) == 0:
                return ("P1", calculate_player_score(player1_deck))

        games += 1


def handler(raw_game: TextIO) -> int:
    raw_player1, raw_player2 = raw_game.read().split("\n\n")
    _, score = crab_combat(process_player(raw_player1), process_player(raw_player2))

    return score


if __name__ == "__main__":
    print(handler(sys.stdin))
