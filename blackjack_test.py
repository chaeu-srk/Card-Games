import pytest

from blackjack import BlackJackDeck, Player, create_game, Table
from cards import Card

class EmptyBjDeck(BlackJackDeck):
    def __init__(self) -> None:
        self.cards = []

    def add_cards(self, cards: list[Card]):
        self.cards.extend(cards)

@pytest.mark.parametrize(
    "bj_combinations_true",
    [
        [Card(1, ""), Card(10, "")],
        [Card(10, ""), Card(1, "")],
        [Card(13, ""), Card(1, "")],
    ],
)
def test_blackjack_combos(bj_combinations_true):
    player = Player(cards = bj_combinations_true)
    assert player.blackjack_check() is True


@pytest.fixture
def game_random_deck() -> Table:
    return create_game()

@pytest.fixture
def empty_deck_game() -> Table:
    deck = EmptyBjDeck()
    player = Player([], "Player")
    dealer = Player([], "Dealer")
    game = Table(player, dealer, deck)
    return game

@pytest.fixture
def player_with_blackjack():
    return Player([Card(1, ""), Card(12, "")])

def test_player_bet_methods():
    pass

def test_player_payout_methods():
    pass

def test_player_bj_payout():
    deck = EmptyBjDeck()
    deck.add_cards([Card(1, ""), Card(3, ""), Card(10, ""), Card(13, ""), Card(10, ""), Card(10, "")])
    game = Table(Player([]), Player([]), deck)

    game.player_bets(100)
    game.initial_deal()
    game.dealer_action()
    game.player_blackjack_win()

    assert game.get_player().get_chips() == 750

def test_reset_table(game_random_deck: Table):
    game = game_random_deck
    game.initial_deal()
    game.player_action("hit")
    game.dealer_action()
    game.reset_table()
    
    player = game.get_player()
    dealer = game.get_dealer()

    assert player.get_cards() == []
    assert dealer.get_cards() == []

def table_reset_with_splits():
    pass

@pytest.fixture
def deck_for_splits():
    deck = EmptyBjDeck()
    deck.add_cards(
        [
            Card(10, ""),
            Card(2, ""),
            Card(12, ""),
            Card(2, ""),
            Card(3, ""),
            Card(3, ""),
            Card(3, ""),
            Card(3, ""),
            Card(3, ""),
        ]
    )
    game = Table(Player([]), Player([]), deck)
    return game

def test_splitable_checks(deck_for_splits: Table):
    game = deck_for_splits
    game.initial_deal()
    assert game.check_splitable() is True
