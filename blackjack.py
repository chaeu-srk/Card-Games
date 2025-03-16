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

    def clear_cards(self) -> None:
        self._cards = []

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
        if "A" in map(repr, self._cards) and total_value <= 11:
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

    def get_chips(self) -> int | float:
        return self._chips

    def get_bet(self) -> int | float:
        return self._bet

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

    def double_bet(self):
        self._bet *= 2

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
        self._player = Player(name="Player")
        self._dealer = Entity(name="Dealer")

        self._deck = BlackJackDeck()

    def get_player(self) -> Player:
        return self._player

    def get_dealer(self) -> Entity:
        return self._dealer

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

    def player_hit(self) -> str | None:
        self.player_draw_card()

        if self._player.get_card_values() > 21:
            return "dealer"

        elif self._player.get_card_values() == 21:
            return self.dealer_action()

        return

    def player_double(self) -> str | None:
        self._player.double_bet()
        hit_result = self.player_hit()

        if hit_result is None:
            return self.dealer_action()

        return hit_result

    def dealer_action(self) -> str | None:
        """
        Return:
            "tied"
            "player"
            "dealer"
            ""
        """
        value = self._dealer.get_card_values()

        if value < 17:
            self.dealer_draw_card()
            return self.dealer_action()

        elif value > 21:
            return "player"

        elif 17 <= value <= 21:
            return self.compare_cards()

        else:
            raise ValueError(f"Invalid dealer card value: {value}")

    def compare_cards(self) -> str | None:
        """
        Returns whoever has the higher card values or tied
        Return:
            "tied", "player", "dealer"
        """
        player_val = self._player.get_card_values()
        dealer_val = self._dealer.get_card_values()

        if player_val == dealer_val:
            return "tied"
        elif player_val > dealer_val:
            return "player"
        elif dealer_val > player_val:
            return "dealer"

    def player_action(self, action: str):
        if action == "hit":
            return self.player_hit()
        elif action == "stand":
            return self.dealer_action()
        elif action == "double":
            return self.player_double()
        elif action == "split":
            pass

    def clear_table_cards(self) -> None:
        self._dealer.clear_cards()
        self._player.clear_cards()

    def player_win(self):
        self._player.payout()
        self.clear_table_cards()

    def player_lose(self):
        self._player.lose_bet()
        self.clear_table_cards()

    def push(self):
        self._player.clear_bet()
        self.clear_table_cards()


class View:
    def __init__(self, game: Table) -> None:
        self.game = game

    def round_start(self):
        print("ROUND START")
        print("----------\n")

    def display_cards(self, entity: Entity, hide_second_card: bool = False):
        value = entity.get_card_values()

        print(f"\n{entity.get_name()} cards:")
        print("-----------")

        for i, card in enumerate(entity.get_cards()):
            if i == 1 and hide_second_card is True:
                print("(********)")
                value = "?"
                break

            print(card)

        print(f"\nValue: {value}\n")

    def ask_for_player_bet(self):
        print(f"Chips: {self.game.get_player().get_chips()}")
        while True:
            bet = int(input("Bet amount: "))
            bet_validity = self.game.player_bets(bet)

            if bet_validity is False:
                print("Not enough chips!")
                continue

            break

    def ask_for_player_action(self):
        action = input("Player action (hit, stand, double, split): ")
        action_result = self.game.player_action(action)

        # Card display option based on action
        if action == "stand":
            self.display_cards(self.game.get_dealer())

        elif action == "double":
            self.display_cards(self.game.get_player())
            self.display_cards(self.game.get_dealer())

        elif action == "hit" and action_result == "dealer":
            self.display_cards(self.game.get_player())
            self.display_cards(self.game.get_dealer())

        else:
            self.display_cards(self.game.get_player())
        

        # display option based on action result
        if action_result is None:
            # Recalls an ask p.action if hit and not bust
            self.ask_for_player_action()

        elif action_result == "player":
            print("player won")
            self.game.player_win()

        elif action_result == "dealer":
            print("dealer won")
            self.game.player_lose()

        elif action_result == "tied":
            print("push")
            self.game.push()

    def ask_play_again(self) -> bool:
        """
        Returns True if player wants to play again
        Returns False if player wants to quit
        """
        while True:
            input_result = input("play again? (y/n): ")
            if input_result == "y":
                return True
            elif input_result == "n":
                return False
            else:
                print("invalid")

    def game_loop(self):
        while True:
            self.round_start()
            self.ask_for_player_bet()

            self.game.initial_deal()
            self.display_cards(self.game.get_dealer(), True)
            self.display_cards(self.game.get_player())
            self.ask_for_player_action()

            if self.ask_play_again() is False:
                break


if __name__ == "__main__":
    game = Table()
    app = View(game)
    print("GAME START >>>\n")
    app.game_loop()
