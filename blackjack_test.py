import pytest

from cards import *
from blackjack import *


@pytest.mark.parametrize("bj_combinations_true", [
    [Card(1, ""), Card(10, "")],
    [Card(10, ""), Card(1, "")],
    [Card(13, ""), Card(1, "")]
])
def test_blackjack_combos(bj_combinations_true):
    player = Player(BlackJackDeck(), bj_combinations_true)
    assert player.blackjack_checker() == True

# @pytest.mark.parametrize("bj_combinations_false")
