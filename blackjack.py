from typing import Literal
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


class Player:
    def __init__(self, cards: list[Card], name: str = "", chips: int = 500) -> None:
        """
        Constructor method for Entity,
        Args:
            cards: a list that stores the cards the entity holds
            name: name of the entity
        """
        self._cards = cards
        self._name = name

        self._chips = chips
        self._bet = 0

    def get_cards(self) -> list[Card]:
        return self._cards

    def get_name(self) -> str:
        return self._name

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

    def get_chips(self) -> int:
        return self._chips

    def double_chips(self):
        self._chips *= 2

    def get_bet(self) -> int:
        return self._bet

    def add_card(self, card: Card) -> None:
        """Gives the entity the passed card."""
        self._cards.append(card)

    def clear_cards(self) -> None:
        self._cards = []

    def blackjack_check(self) -> bool:
        if len(self._cards) == 2 and self.get_card_values() == 21:
            return True
        return False

    def check_can_double_split(self) -> bool:
        if (self._chips - self._bet) < self._bet:
            return False
        else:
            return True

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

    def add_bet(self, bet: int) -> bool:
        if bet > self._chips:
            return False

        self._bet += bet
        return True

    def reduce_chips(self, num: int):
        self._chips -= num

    def add_chips(self, num: int):
        self._chips += num

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
            chips = self._bet * 1.5
            self._chips += int(chips)

        self._chips += self._bet
        self.clear_bet()


class Table:
    """
    Handles all the interactions between player and dealer
    """

    def __init__(self, player: Player, dealer: Player, deck: Deck) -> None:
        self._player = player
        self._dealer = dealer

        self._deck = deck

    def get_player(self) -> Player:
        return self._player

    def get_dealer(self) -> Player:
        return self._dealer

    def get_deck(self) -> Deck:
        return self._deck

    def draw_card(self, player: Player) -> None:
        player.add_card(self._deck.draw_card())

    def player_draw_card(self) -> None:
        self._player.add_card(self._deck.draw_card())

    def dealer_draw_card(self) -> None:
        self._dealer.add_card(self._deck.draw_card())

    def player_bets(self, bet: int) -> bool:
        return self._player.bet(bet)

    def initial_deal(self) -> None | Literal["blackjack"]:
        """
        The inital deal when a round starts
        deals two cards to the player and dealer

        if returns blackjack if player got blackjack
        """
        self.player_draw_card()
        self.dealer_draw_card()
        self.player_draw_card()
        self.dealer_draw_card()

        if self.get_player().blackjack_check():
            return "blackjack"

    def player_hit(self) -> None | Literal["bust", "dealer_action"]:
        """
        Returns:
            "bust"
            "dealer_action"
            None
        """
        self.player_draw_card()

        if self._player.get_card_values() > 21:
            return "bust"

        elif self._player.get_card_values() == 21:
            return "dealer_action"

        return None

    def split_hit(self, split: Player) -> None | Literal["bust", "dealer_action"]:
        """
        Returns:
            "bust"
            "dealer_action"
            None
        """
        self.draw_card(split)

        if split.get_card_values() > 21:
            return "bust"

        elif split.get_card_values() == 21:
            return "dealer_action"

        return None

    def player_double(self) -> None | Literal["dealer_action", "bust"]:
        """
        Returns:
            "bust"
            "dealer_action"
        """
        self._player.double_bet()
        hit_result = self.player_hit()

        if hit_result is None:
            return "dealer_action"

        return hit_result

    def split_double(self, split: Player):
        split.double_chips()
        hit_result = self.split_hit(split)

        if hit_result is None:
            return "dealer_action"

        return hit_result

    def create_split(self):
        return [
            Player(
                [self.get_player().get_cards()[0]], "split 1", self._player.get_bet()
            ),
            Player(
                [self.get_player().get_cards()[1]], "split 2", self._player.get_bet()
            ),
        ]

    def split_action(
        self, split: Player, action: str
    ) -> None | Literal["bust", "dealer_action", "invalid"]:
        if action == "hit":
            return self.split_hit(split)

        elif action == "stand":
            return "dealer_action"

        elif action == "double":
            if not self.get_player().check_can_double_split():
                return "invalid"
            return self.split_double(split)

        # elif action == "split":
        #     if not self.get_player().check_can_double_split():
        #         return "invalid"
        #     return "split"
        else:
            return "invalid"

    def dealer_action(self) -> None | Literal["player", "dealer", "tied", "compare"]:
        """
        Return:
            "compare"
            "tied"
            "player"
            "dealer"
        """
        value = self._dealer.get_card_values()

        if value < 17:
            self.dealer_draw_card()
            return self.dealer_action()

        elif value > 21:
            return "player"

        elif 17 <= value <= 21:
            return "compare"

        else:
            raise ValueError(f"Invalid dealer card value: {value}")

    def split_dealer_action(self) -> None | Literal["compare", "player"]:
        value = self._dealer.get_card_values()
        if value < 17:
            self.dealer_draw_card()
            return self.split_dealer_action()

        elif 17 <= value <= 21:
            return "compare"

        elif value > 21:
            return "player"

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
            self._player.payout()
            return "player"

        elif dealer_val > player_val:
            self._player.lose_bet()
            return "dealer"

    def split_compare_cards(self, split: Player) -> Literal["tied", "player", "dealer"]:
        """
        Returns whoever has the higher card values or tied
        Return:
            "tied", "player", "dealer"
        """
        split_val = split.get_card_values()
        dealer_val = self._dealer.get_card_values()

        if split_val == dealer_val:
            return "tied"
        elif split_val > dealer_val:
            return "player"
        elif dealer_val > split_val:
            return "dealer"
        else:
            raise ValueError

    def collect_split_results(self, splits: list[Player]):
        split_results = []
        for split in splits:
            if split.get_card_values() > 21:
                split_results.append("bust")
                break

            split_results.append(self.split_compare_cards(split))

        return split_results

    def player_action(
        self, action: str | Literal["hit", "stand", "double", "split"]
    ) -> None | Literal["dealer_action", "bust", "invalid", "split", "blackjack"]:
        """
        returns the result of the player action:

        if none is returned player_action is to be recalled
        if dealer_action then dealer_action is to be called
        if split then create_splits should be called and split_action should be used for the splits
        if bust then dealer action should be called then player_lose
        """
        if self.get_player().blackjack_check():
            return "blackjack"

        elif action == "hit":
            return self.player_hit()

        elif action == "stand":
            return "dealer_action"

        elif action == "double":
            if not self.get_player().check_can_double_split():
                return "invalid"
            return self.player_double()

        elif action == "split":
            if (
                not self.get_player().check_can_double_split()
                or not self.check_splitable()
            ):
                return "invalid"
            return "split"

        else:
            return "invalid"

    def reset_table(self) -> None:
        """
        clears player's cards
        clears player's bet
        clears dealer's bet
        """
        self._dealer.clear_cards()
        self._player.clear_cards()
        self._player.clear_bet()

    def player_blackjack_win(self) -> None:
        self._player.payout(True)
        self.reset_table()

    def player_win(self) -> None:
        """
        player wins their bet and table is reset
        """
        self._player.payout()
        self.reset_table()

    def player_lose(self) -> None:
        """
        player loses their bet and table is reset
        """
        self._player.lose_bet()
        self.reset_table()

    def split_lose(self, split: Player):
        self._player.reduce_chips(split.get_chips())

    def split_win(self, split: Player):
        self._player.add_chips(split.get_chips())

    def push(self):
        self.reset_table()

    def check_splitable(self) -> bool:
        """
        True if can split
        """
        card_1 = self._player.get_cards()[0]
        card_2 = self._player.get_cards()[1]

        if int(card_1) == int(card_2):
            return True
        return False


class View:
    def __init__(self, game: Table) -> None:
        self.game = game
        self.splits = []

    def round_start(self):
        print("ROUND START")
        print("----------\n")

    def display_cards(self, entity: Player, hide_second_card: bool = False):
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

            if self.game.get_player().bet(bet) is False:
                print("Not enough chips!")
                continue

            break

    def ask_for_player_action(self, game: Table):
        if game.get_player().blackjack_check():
            dealer_result = self.game.dealer_action()
            self.display_cards(game.get_dealer())

            if game.get_dealer().blackjack_check():
                print("PUSH")
                self.game.push()
                return
            else:
                print("BLACKJACK")
                self.game.player_blackjack_win()
                return

        while True:
            action = input("Player action (hit, stand, double, split): ")
            action_result = game.player_action(action)

            if action_result == "invalid":
                continue
            elif action_result is None:
                self.display_cards(game.get_player())
                continue
            elif action == "double":
                self.display_cards(game.get_player())
                break
            else:
                break

        if action_result == "dealer_action":
            dealer_result = self.game.dealer_action()
            self.display_cards(game.get_dealer())

        elif action_result == "bust":
            self.display_cards(game.get_player())
            print("BUST")
            dealer_result = self.game.dealer_action()
            self.display_cards(game.get_dealer())
            self.game.player_lose()
            return
        elif action_result == "split":
            return self.split_loop()
        else:
            raise ValueError

        if dealer_result == "compare":
            game_result = self.game.compare_cards()
        else:
            game_result = dealer_result

        if game_result == "player":
            self.game.player_win()

            print("WON")
        elif game_result == "dealer":
            self.game.player_lose()

            print("LOST")

        elif game_result == "tied":
            self.game.reset_table()

            print("PUSH")

    def split_loop(self):
        splits = self.game.create_split()

        for split in splits:
            self.split_ask_player_action(split)

        self.game.split_dealer_action()
        self.display_cards(self.game.get_dealer())
        split_results = self.game.collect_split_results(splits)

        for i, result in enumerate(split_results):
            print(f"Split {i}: {result}")

    def split_ask_player_action(self, split: Player):
        self.display_cards(split)
        while True:
            action = input("Player action (hit, stand, double, split): ")
            action_result = self.game.split_action(split, action)

            if action_result == "invalid":
                continue

            # action result is to recall
            elif action_result is None:
                self.display_cards(split)
                continue

            else:
                return action_result

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

    def initial_deal(self):
        if self.game.initial_deal() == "blackjack":
            dealer_result = self.game.dealer_action()
            self.display_cards(self.game.get_dealer())

            if dealer_result == "compare":
                print("PUSH")
                self.game.push()
            else:
                print("BLACKJACK")
                self.game.player_blackjack_win()

    def game_loop(self):
        while True:
            self.round_start()
            self.ask_for_player_bet()

            self.game.initial_deal()
            self.display_cards(self.game.get_dealer(), True)
            self.display_cards(self.game.get_player())

            self.ask_for_player_action(self.game)

            if self.ask_play_again() is False:
                break


def create_game() -> Table:
    player = Player([], "Player")
    dealer = Player([], "Dealer")
    deck = BlackJackDeck()

    game = Table(player, dealer, deck)
    return game


def custom_game():
    player = Player([], "Player")
    dealer = Player([], "Dealer")
    deck = Deck()
    deck.add_cards(
        [
            Card(1, ""),
            Card(1, ""),
            Card(10, ""),
            Card(13, ""),
            Card(13, ""),
            Card(13, ""),
            Card(13, ""),
        ]
    )

    game = Table(player, dealer, deck)
    return game


if __name__ == "__main__":
    game = create_game()
    app = View(game)

    print("GAME START >>>\n")
    app.game_loop()

# BUGS
# getting 21 after hitting does not display cards
# cannot split on two face cards. Card.value is > 10 so checks dont pass
