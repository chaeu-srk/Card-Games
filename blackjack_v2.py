from cards import Deck, Card


class BlackJackDeck(Deck):
    """
    creates a 6 deck shoe for blackjack gameplay.
    Deck is shuffled when created

    Methods:
        __init__
        shuffle_deck
        draw_card

    """

    def __init__(self) -> None:
        super().__init__()
        for _ in range(6):
            self.add_64_cards()

        self.shuffle_deck()


class Entity:
    """
    Abstract class for default behaviours
    """

    def __init__(self, cards: list[Card] = [], name: str = "") -> None:
        """
        Constructor method for Entity,
        Args:
            cards: a list that stores the cards the entity holds
            name: name of the entity
        """
        self._cards = cards
        self._name = name

    def get_cards(self) -> list[Card]:
        return self._cards

    def get_name(self) -> str:
        return self._name

    def add_card(self, card: Card) -> None:
        """Gives the entity the passed card."""
        self._cards.append(card)

    def get_card_values(self) -> int:
        """Returns the added up values of the entity's cards"""

        total_value = 0
        for card in self._cards:
            # sets face card values to 10
            if card.value > 10:
                value = 10
            else:
                value = card.value

            total_value += value

        # Turns Ace value to 1 if value is > 11
        if "A" in map(str, self._cards) and total_value <= 11:
            total_value += 10

        return total_value

    def blackjack_check(self) -> bool:
        if len(self._cards) == 2 and self.get_card_values() == 21:
            return True
        return False


class Player(Entity):
    """
    Player entity
    """

    def __init__(
        self, cards: list[Card] = [], name: str = "", chips: int = 500
    ) -> None:
        super().__init__(cards, name)
        self._chips = chips
        self._bet = 0

    def bet(self, bet: int) -> bool:
        """
        stores the amout the player bets
        and subtracts from player chips
        returns False if not enough chips
        """
        if bet > self._chips:
            return False
        
        self._bet = bet
        return True

    def clear_bet(self) -> None:
        """sets bet to 0"""
        self._bet = 0

    def lose_bet(self):
        self._chips -= self._bet
        self.clear_bet()

    def payout(self, blackjack: bool = False) -> None:
        """adds the bet amount to the players chips
        and clears the bet
        if blackjack is true, will change the payout
        """
        if blackjack is True:
            self._chips += self._bet * 1.5

        self._chips += self._bet 
        self.clear_bet()

    def split(self):
        pass


class Table:
    """
    Handles all the interactions between player and dealer
    """
    def __init__(self) -> None:
        self._player = Player(name = "Player")
        self._dealer = Entity(name = "Dealer")

        self._deck = BlackJackDeck()

    def player_draw_card(self) -> None:
        self._player.add_card(self._deck.draw_card())

    def dealer_draw_card(self) -> None:
        self._dealer.add_card(self._deck.draw_card())

    def player_bets(self, bet: int) -> bool:
        return self._player.bet(bet)

    def initial_deal(self) -> None:
        """Dealer and player both draws 2 cards"""
        self.player_draw_card()
        self.dealer_draw_card()
        self.player_draw_card()
        self.dealer_draw_card()
