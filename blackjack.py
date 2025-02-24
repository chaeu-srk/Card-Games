from cards import Card, Deck


class BlackJackDeck(Deck):
    """
    creates a 6 deck shoe for blackjack gameplay.
    """

    def __init__(self) -> None:
        super().__init__()
        for _ in range(6):
            self.add_64_cards()


class Player:
    """
    Default behaviour for players
    """

    def __init__(self, deck: BlackJackDeck, cards: list[Card] = []) -> None:
        self.cards = cards
        self.deck = deck
        self.chips = 500

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
        if len(self.cards) > 2:
            return False
        elif self.cards[0].value == 1 and self.cards[1].value >= 10:
            return True
        elif self.cards[0].value >= 10 and self.cards[1].value == 1:
            return True

    def calculate_card_values(self):
        total_value = 0
        for card in self.cards:
            if card.value > 10:
                value = 10

            else:
                value = card.value

            total_value += value

        return total_value


class Game:
    def start_game(self):
        self.deck = BlackJackDeck()
        self.player = Player(self.deck)
        self.dealer = Player(self.deck)

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

    def display_cards(self):
        print(f"player cards:{self.player.cards}")


# gameplay loop
# player bets
# initial_deal
# if blackjack then payout
# player action
# hit: if bust lose round
# stand: dealer action
# if dealer bust payout
# if dealer cards > 17 and <21 then compare with player
# higher value wins
# if == push (player keeps bet amount)
def gameplay():
    game = Game()
    game.start_game()
    game.player_bets()


if __name__ == "__main__":
    gameplay()
