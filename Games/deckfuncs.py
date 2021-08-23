import random


def get_deck(shuffle=True):
    values = ["A"] + list(range(2, 11)) + ["J", "Q", "K"]
    suits = ["C", "H", "S", "D"]
    deck = [str(value) + suit for value in values for suit in suits]
    if shuffle:
        random.shuffle(deck)
    return deck
