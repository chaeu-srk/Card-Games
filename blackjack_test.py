import pytest

from blackjack import *
from cards import *


@pytest.mark.parametrize(
    "bj_combinations_true",
    [
        [Card(1, ""), Card(10, "")],
        [Card(10, ""), Card(1, "")],
        [Card(13, ""), Card(1, "")],
    ],
)
def test_blackjack_combos(bj_combinations_true):
    player = Person(BlackJackDeck(), bj_combinations_true, "")
    assert player.blackjack_checker() == True


@pytest.mark.skip
def test_correct_card_symbols():
    ace_card = Card(1, "")
    jack_card = Card(11, "")
    queen_card = Card(12, "")
    king_card = Card(13, "")
    assert ace_card.symbol == "A"
    assert jack_card.symbol == "J"
    assert queen_card.symbol == "Q"
    assert king_card.symbol == "K"


soft_value_cases = [
    ([Card(1, ""), Card(3, "")], 14),
    ([Card(5, ""), Card(1, "")], 16),
    ([Card(1, ""), Card(1, ""), Card(1, "")], 13),
    ([Card(1, ""), Card(13, "")], 21),
    ([Card(12, ""), Card(5, ""), Card(1, "")], 16),
    ([Card(13, ""), Card(12, "")], 20),
]


@pytest.mark.parametrize("soft_value_cases", soft_value_cases)
def test_soft_values(soft_value_cases):
    player = Person(BlackJackDeck(), soft_value_cases[0], "")
    assert player.calculate_card_values() == soft_value_cases[1]
