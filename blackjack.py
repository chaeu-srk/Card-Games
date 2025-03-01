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

    def check_player_blackjack(self):
        if self.player.blackjack_checker() is True:
            self.win_round()

    def player_hit(self):
        """
        player draws cards
        outcomes ->
            player gets 21 and wins
            player busts and loses
        returns ->
            Card values
        """
        self.player.draw_card()
        return self.player.calculate_card_values()

        # Player Busts
        # if self.player.calculate_card_values() > 21:
        #     self.lose_round()

        # # Player gets 21
        # elif self.player.calculate_card_values() == 21:
        #     self.win_round()

    def player_double(self):
        self.player.bet_amount *= 2

    def player_split(self):
        pass

    def clear_cards(self) -> None:
        self.player.cards.clear()
        self.dealer.cards.clear()

    def dealer_action(self):
        """
        Return: hit, stand or bust
        if value <= 16 draw card
        if value > 17 and less than 21 stand and compare cards
        if over 21 player wins
        """
        value = self.dealer.calculate_card_values()
        if value == 21:
            return "win"
        if 17 < value < 21:
            return "stand"
        if value > 21:
            return "bust"
        self.dealer.draw_card()
        return "hit"

    def compare_cards(self):
        """Return winner"""
        player_value = self.player.calculate_card_values()
        dealer_value = self.dealer.calculate_card_values()
        if player_value == dealer_value:
            return "push"
        if player_value > dealer_value:
            return "player"
        if dealer_value > player_value:
            return "dealer"

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
        self.p_action_loop = True

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

    def dealer_cards(self, delay: int, hide_cards: bool = True):
        """
        Displayer for dealer cards
        args:
            delay: time to wait between printing each card
            hide_cards: whether to hide the second dealer card
        """
        # Add more delay on last card?
        cards = self.game.dealer.cards

        print("\nDEALER CARDS")
        print("------------")
        sleep(delay)
        for i, card in enumerate(cards):
            if i == 1 and hide_cards is True:
                print("(********)")
                sleep(delay)
            else:
                print(f"{repr(card)}")
                sleep(delay)
        if hide_cards is True:
            print("value: ???")
        else:
            print(f"value: {self.game.dealer.calculate_card_values()}\n")
        sleep(delay)

    def player_cards(self, delay: int):
        cards = self.game.player.cards

        print("\nPLAYER CARDS")
        print("------------")
        sleep(delay)
        for card in cards:
            print(f"{repr(card)}")
            sleep(delay)
        print(f"value: {self.game.player.calculate_card_values()}\n")
        sleep(delay)

    def player_action(self):
        msg = "action (hit, stand, double, split): "
        self.p_action_loop = True
        while self.p_action_loop:
            selection = input(msg)
            if selection == "hit":
                self.hit()
            elif selection == "stand":
                self.dealer_action()
            elif selection == "double":
                pass
            elif selection == "split":
                pass
            else:
                print("Not a action")

    def hit(self):
        card_value = self.game.player_hit()
        self.player_cards(0.1)
        if card_value > 21:
            self.lose_round()
        elif card_value == 21:
            self.win_round()

    def dealer_action(self):
        """
        show hidden card
        if value <= 16 draw card
        if value > 17 and less than 21 stand and compare cards
        if over 21 player wins
        """
        self.dealer_cards(0.1, False)
        while True:
            action = self.game.dealer_action()

            if action == "win":
                self.lose_round()
                break

            if action == "hit":
                self.dealer_cards(0.1, False)

            if action == "stand":
                winner = self.game.compare_cards()
                if winner == "player":
                    self.win_round()
                    break
                if winner == "push":
                    self.push_round()
                    break
                self.lose_round()
                break

            if action == "bust":
                self.win_round()
                break

    def push_round(self):
        print("Push")
        self.p_action_loop = False

    def win_round(self):
        print("Round Won")
        self.p_action_loop = False

    def lose_round(self):
        print("Round Lost")
        self.p_action_loop = False


def mainloop():
    view = View()
    view.start_game()
    view.player_chips()
    view.ask_player_bet()
    view.round_start()
    view.player_action()


if __name__ == "__main__":
    mainloop()
