from time import sleep
from cards import Card, Deck


class BlackJackDeck(Deck):
    """
    creates a 6 deck shoe for blackjack gameplay.
    """

    def __init__(self) -> None:
        super().__init__()
        for _ in range(6):
            self.add_64_cards()

        self.shuffle_deck()


class Person:
    """
    Default behaviour for players
    """

    def __init__(self, deck: BlackJackDeck, cards: list[Card], name: str) -> None:
        self.cards = cards
        self.deck = deck
        self.chips = 500
        self.name = name
        self.bet_amount = 0

    def draw_card(self):
        self.cards.append(self.deck.draw_one_card())

    def bet(self, amount: int) -> bool:
        if amount > self.chips:
            return False

        self.chips -= amount
        self.bet_amount = amount
        return True

    def payout(self):
        self.chips += 2 * self.bet_amount
        self.bet_amount = 0

    def blackjack_payout(self):
        self.chips += 2.5 * self.bet_amount
        self.bet_amount = 0

    def reset_bet(self):
        self.bet_amount = 0

    def win_hand(self):
        self.chips += self.bet_amount

    def blackjack_checker(self) -> bool:
        if len(self.cards) > 2 and self.calculate_card_values() == 21:
            return True
        return False

    def calculate_card_values(self) -> int:
        total_value = 0

        for card in self.cards:
            # sets face card values to 10
            if card.value > 10:
                value = 10
            else:
                value = card.value

            total_value += value

        if "A" in map(str, self.cards) and total_value <= 11:
            total_value += 10

        return total_value

    def get_player_cards(self):
        return self.cards


class Game:
    def __init__(self):
        self.deck = BlackJackDeck()
        self.player = Person(self.deck, [], "Player")
        self.dealer = Person(self.deck, [], "Dealer")

    def initial_deal(self):
        self.player.draw_card()
        self.dealer.draw_card()
        self.player.draw_card()
        self.dealer.draw_card()

    def player_bets(self, bet_amount: str) -> bool:
        """
        Returns True if bet is valid and sets bet_amount var in player
        Returns False otherwise and does not set bet_amount
        """
        return self.player.bet(bet_amount)

    # def initial_display(self):
    #     print("\nDEALER CARDS:")
    #     print("-------------")
    #     print(repr(self.dealer.cards[0]))
    #     print("(********)")
    #     print("value: ???")

    #     print("\nPLAYER CARDS:")
    #     print("-------------")
    #     for card in self.player.cards:
    #         print(repr(card))
    #     print(f"value: {self.player.calculate_card_values()}\n")

    def check_player_blackjack(self):
        if self.player.blackjack_checker() is True:
            self.win_round()

    def player_hit(self):
        """
        player draws cards
        outcomes ->
            player gets 21 and wins
            player busts and loses
        """
        self.player.draw_card()

        # Player Busts
        if self.player.calculate_card_values() > 21:
            self.lose_round()

        # Player gets 21
        elif self.player.calculate_card_values() == 21:
            self.win_round()

    def player_double(self):
        self.player.bet_amount *= 2

    def player_split(self):
        pass

    def clear_cards(self) -> None:
        self.player.cards.clear()
        self.dealer.cards.clear()

    def dealer_action(self):
        pass

    def win_round(self):
        """
        payout player -> reset cards
        """
        self.player.payout()
        self.clear_cards()

    def lose_round(self):
        """
        reset player_bet -> reset cards
        """
        self.player.reset_bet()
        self.clear_cards()


class View:
    def __init__(self):
        self.game = Game()

    def start_game(self):
        print("GAME START >>> \n")

    def player_chips(self):
        print(f"Chips: {self.game.player.chips}")

    def ask_player_bet(self):
        while True:
            # TODO: Handle incorrect input types
            bet_amount = int(input("Bet amount: "))
            if self.game.player_bets(bet_amount) is True:
                break
            print("Not enought chips!\n")

    def round_start(self):
        print("\nROUND START >>>\n")
        self.game.initial_deal()
        sleep(1)
        
        delay = 0.7
        self.dealer_cards(delay)
        self.player_cards(delay)

    def dealer_cards(self, delay: int):
        print("DEALER CARDS")
        print("------------")
        sleep(delay)
        print(f"{repr(self.game.dealer.cards[0])}")
        sleep(delay)
        print("(********)")
        sleep(delay)
        print("value: ???")
        sleep(delay)
        print("\n")

    def player_cards(self, delay: int):
        print("PLAYER CARDS")
        print("------------")
        sleep(delay)
        print(f"{repr(self.game.player.cards[0])}")
        sleep(delay)
        print(f"{repr(self.game.player.cards[1])}")
        sleep(delay)
        print(f"value: {self.game.player.calculate_card_values()}")
        print("\n")

    def player_action(self):
        msg = "action (hit, stand, double, split): "
        while True:
            selection = input(msg)
            if selection == "hit":
                pass
            elif selection == "stand":
                pass
            elif selection == "double":
                pass
            elif selection == "split":
                pass
            print("Not a action")


def mainloop():
    view = View()
    view.start_game()
    view.player_chips()
    view.ask_player_bet()
    view.round_start()


if __name__ == "__main__":
    mainloop()
