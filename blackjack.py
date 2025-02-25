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
        if len(self.cards) > 2:
            return False
        elif self.cards[0].value == 1 and self.cards[1].value >= 10:
            return True
        elif self.cards[0].value >= 10 and self.cards[1].value == 1:
            return True

    def calculate_card_values(self):
        total_value = 0
        for card in self.cards:
            # so card values are max 10
            if card.value > 10:
                value = 10
            else:
                value = card.value

            total_value += value

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
        if player.blackjack_checker() == True:
            values = 21

        print(f"{player.name} cards:{cards}, value: {values}")


    def check_player_blackjack(self):
        if self.player.blackjack_checker() == True:
            self.win_round()
        else:
            self.lose_round()

    def win_round(self):
        pass

    def lose_round(self):
        pass


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
    game.initial_deal()
    game.display_cards(game.player)
    game.display_cards(game.dealer)


if __name__ == "__main__":
    gameplay()
