import pytest

from cards import *
from blackjack import *


@pytest.mark.parametrize("bj_combinations_true", [
    [Card(1, ""), Card(10, "")],
    [Card(10, ""), Card(1, "")],
    [Card(13, ""), Card(1, "")]
])
def test_blackjack_combos(bj_combinations_true):
    player = Person(BlackJackDeck(), bj_combinations_true, "")
    assert player.blackjack_checker() == True

# @pytest.mark.parametrize("bj_combinations_false")

def test_correct_card_symbols():
    ace_card = Card(1, "")
    jack_card = Card(11, "")
    queen_card = Card(12, "")
    king_card = Card(13, "")
    assert ace_card.symbol == "A"
    assert jack_card.symbol == "J"
    assert queen_card.symbol == "Q"
    assert king_card.symbol == "K"
