from random import shuffle


class Card:

    def __init__(self, value: int, suit: str) -> None:
        self.value = value
        self.suit = suit

        face_card_values = {
            1: "A",
            11: "J",
            12: "Q",
            13: "K",
        }

        if value > 10 or value == 1:
            self.symbol = face_card_values[value]
        else:
            self.symbol = value

    def __str__(self) -> str:
        return str(self.symbol)

    def __int__(self) -> int:
        return self.value

    def __repr__(self) -> str:
        return f"({self.symbol}, {self.suit})"


class Deck:
    def __init__(self) -> None:
        self.cards = []

    def add_64_cards(self) -> None:
        """
        Creates a standard deck with 64 cards.
        """
        for suit in ["Diamond", "Heart", "Spade", "Club"]:
            for x in range(1, 14):
                self.cards.append(Card(x, suit))

    def shuffle_deck(self) -> None:
        shuffle(self.cards)

    def draw_one_card(self) -> Card:
        return self.cards.pop(0)


if __name__ == "__main__":
    card = [Card(12, ""), Card(1, "")]
    print("A" in map(str, card))
