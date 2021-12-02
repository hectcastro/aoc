import sys
from collections import deque
from typing import Deque, TextIO


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


def handler(raw_game: TextIO) -> int:
    raw_player1, raw_player2 = raw_game.read().split("\n\n")
    player1_deck, player2_deck = (
        process_player(raw_player1),
        process_player(raw_player2),
    )

    while any([len(player1_deck) != 0, len(player2_deck) != 0]):
        if len(player1_deck) == 0 or len(player2_deck) == 0:
            break

        player1_card = player1_deck.popleft()
        player2_card = player2_deck.popleft()

        if player1_card > player2_card:
            player1_deck.append(player1_card)
            player1_deck.append(player2_card)
        else:
            player2_deck.append(player2_card)
            player2_deck.append(player1_card)

    return calculate_player_score(player1_deck)


if __name__ == "__main__":
    print(handler(sys.stdin))
