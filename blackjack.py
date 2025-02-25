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

    def draw_card(self):
        self.cards.append(self.deck.draw_one_card())

    def bet(self, amount: int) -> bool:
        if amount > self.chips:
            return False

        self.bet_amount = amount
        return True

    def win_hand(self):
        self.chips += self.bet_amount

    def blackjack_checker(self):
        if len(self.cards) > 2 and self.calculate_card_values() == 21:
            return True

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

    def player_bets(self):
        while True:
            amount = input("Bet amount: ")
            if self.player.bet(int(amount)):
                break
            else:
                print("Not enough chips!")

    def display_cards(self, player: Person):
        cards = player.get_player_cards()
        values = player.calculate_card_values()
        # if player.blackjack_checker() == True:
        #     values = 21

        print(f"{player.name} cards:{cards}, value: {values}")

    def check_player_blackjack(self):
        if self.player.blackjack_checker() == True:
            self.win_round()
        else:
            self.lose_round()

    def player_action(self):
        pass

    def player_hit(self):
        self.player.draw_card()
        self.display_cards(self.player)
        if self.player.calculate_card_values() > 21:
            self.lose_round()
        elif self.player.calculate_card_values() == 21:
            self.win_round()

    def player_double(self):
        pass

    def player_split(self):
        pass

    def dealer_action(self):
        while True:
            self.dealer.draw_card()
            self.display_cards(self.dealer)
            if self.dealer.calculate_card_values() > 21:
                self.win_round()
                break
            # Dealer blackjack
            elif self.dealer.calculate_card_values() == 21:
                self.lose_round()
                break
            elif self.dealer.calculate_card_values() > 17:
                print("compare with player cards")
                break

    def win_round(self):
        print("round won")

    def lose_round(self):
        print("round lost")


def gameplay():
    game = Game()
    game.player_bets()
    game.initial_deal()
    game.display_cards(game.player)
    game.player_hit()
    game.dealer_action()


if __name__ == "__main__":
    gameplay()
