# Blackjack Simulator
import random
from matplotlib import pyplot as plt

LOSS = "Loss"
PUSH = "Push"
WIN = "Win"
BLACKJACK = "Blackjack"
VERBOSE = 0 

class Card():
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        if value == 11 or value == 12 or value == 13:
            self.true_value = 10
        elif value == 14:
            self.true_value = 11
        else:
            self.true_value = value

    def __str__(self):
        return self.suit + ":" + str(self.value)


def sum_cards(card_list):
    card_sum = 0
    for card in card_list:
        card_sum += card.true_value
    return card_sum


def get_singular_outcomes(deck, drawn_cards, target):
    card_sum = sum_cards(drawn_cards)
    # print("sum", card_sum)
    if card_sum == target:
        return [True]
    elif card_sum > target:
        return [False]
    else:
        all_outcomes = []
        for i in range(len(deck)):
            temp_remove_card = deck.pop(i)
            drawn_cards.append(temp_remove_card)
            outcome = get_singular_outcomes(deck, drawn_cards, target)
            all_outcomes.extend(outcome)
            deck.insert(i, temp_remove_card)
            drawn_cards.pop()
            # print(len(all_outcomes))
        return all_outcomes

    




def create_deck(num_decks=1):
    deck = []
    for i in range(num_decks):
        for suit in ["Clubs", "Diamonds", "Hearts", "Spades"]:
            for value in range(2, 15):  # 11=Jack, 12=Queen, 13=King, 14=Ace
                new_card = Card(value, suit)
                deck.append(new_card)
    random.shuffle(deck)
    return deck


class Player():
    def __init__(self):
        self.cards = []
        self.total_value = 0

    def hit(self, deck):
        new_card = deck.pop()
        self.cards.append(new_card)
        self.total_value += new_card.true_value
        return new_card


class Human(Player):
    def __init__(self, total_money=1000.0):
        Player.__init__(self)
        self.strategy_table = []
        self.fill_strategy_table()  # Dealer's card, player's card
        self.doubled = False
        self.total_money = total_money
        self.current_bet = 0.0

    def get_initial_cards(self, deck):
        self.probability_outcomes = []
        self.probability_outcomes_dealer = []
        self.total_value = 0
        self.cards.clear()
        human_card_1 = self.hit(deck)
        human_card_2 = self.hit(deck)
        if VERBOSE:
            print("Humans cards:", human_card_1, human_card_2)

    def hit_or_stand(self, dealers_up_card):
        return self.strategy_table[self.total_value][dealers_up_card.value]

    def play_hand(self, deck, dealers_up_card):
        while True:
            action = self.hit_or_stand(dealers_up_card)
            if VERBOSE:
                print("Human decides to", action)
            if action == "D":
                # Make sure you only double on first hit.
                if len(self.cards) == 2:
                    self.current_bet *= 2
                    new_card = self.hit(deck)
                    if VERBOSE:
                        print("Human draws", new_card)
                    break
                else:
                    action = "H"
            if action == "H":
                new_card = self.hit(deck)
                if VERBOSE:
                    print("Human draws", new_card)
                if self.total_value > 21:
                    break
            
            elif action == "S":
                break

        return action

    
    def bet(self, current_bet=50.0):
        self.current_bet = current_bet
        if VERBOSE:
            print("Human bets $" + str(current_bet))


    def fill_strategy_table(self):
        self.strategy_table.append([None, None, None, None, None, None, None, None, None, None, None, None, None, None, None])
        self.strategy_table.append([None, None, None, None, None, None, None, None, None, None, None, None, None, None, None])
        self.strategy_table.append([None, None, None, None, None, None, None, None, None, None, None, None, None, None, None])
        self.strategy_table.append([None, None, None, None, None, None, None, None, None, None, None, None, None, None, None])
        self.strategy_table.append([None, None, "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H"])
        self.strategy_table.append([None, None, "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H"])
        self.strategy_table.append([None, None, "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H"])
        self.strategy_table.append([None, None, "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H"])
        self.strategy_table.append([None, None, "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H"])
        self.strategy_table.append([None, None, "H", "D", "D", "D", "D", "H", "H", "H", "H", "H", "H", "H", "H"])
        self.strategy_table.append([None, None, "D", "D", "D", "D", "D", "D", "D", "D", "H", "H", "H", "H", "H"])
        self.strategy_table.append([None, None, "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "H", "H", "H"])
        self.strategy_table.append([None, None, "H", "H", "S", "S", "S", "H", "H", "H", "H", "H", "H", "H", "H"])
        self.strategy_table.append([None, None, "S", "S", "S", "S", "S", "H", "H", "H", "H", "H", "H", "H", "H"])
        self.strategy_table.append([None, None, "S", "S", "S", "S", "S", "H", "H", "H", "H", "H", "H", "H", "H"])
        self.strategy_table.append([None, None, "S", "S", "S", "S", "S", "H", "H", "H", "H", "H", "H", "H", "H"])
        self.strategy_table.append([None, None, "S", "S", "S", "S", "S", "H", "H", "H", "H", "H", "H", "H", "H"])
        self.strategy_table.append([None, None, "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S"])
        self.strategy_table.append([None, None, "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S"])
        self.strategy_table.append([None, None, "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S"])
        self.strategy_table.append([None, None, "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S"])
        self.strategy_table.append([None, None, "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S"])
        self.strategy_table.append([None, None, "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S"])
        self.strategy_table.append([None, None, "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S"])
        self.strategy_table.append([None, None, "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S"])
        self.strategy_table.append([None, None, "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S"])
        self.strategy_table.append([None, None, "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S"])
        self.strategy_table.append([None, None, "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S"])
        self.strategy_table.append([None, None, "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S"])
        self.strategy_table.append([None, None, "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S"])
        self.strategy_table.append([None, None, "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S"])
        self.strategy_table.append([None, None, "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S"])

        
class Dealer_AI(Player):
    def __init__(self):
        Player.__init__(self)

    def hit_or_stand(self):
        if self.total_value < 17:
            return "H"
        else:
            return "S"

    def get_initial_cards(self, deck):
        self.cards.clear()
        self.total_value = 0

        dealers_up_card = self.hit(deck)
        if VERBOSE:
            print("Dealers card:", dealers_up_card)
        return dealers_up_card

    def play_hand(self, deck):
        while True:
            action = self.hit_or_stand()
            if VERBOSE:
                print("Dealer decides to", action)
            if action == "H":
                new_card = self.hit(deck)
                if VERBOSE:
                    print("Dealer draws", new_card)
                if self.total_value > 21:
                    break
            elif action == "S":
                break


def process_bet(human, dealer_AI):
    if VERBOSE:
        print("Human:", human.total_value, "|", "Dealer:", dealer_AI.total_value)
    if human.total_value > 21:
        human.total_money -= human.current_bet
        if VERBOSE:
            print("LOSE - BUST: Player loses $" + str(human.current_bet) + " Total money=$" + str(human.total_money))
        return LOSS
    elif human.total_value == 21 and dealer_AI.total_value != 21:
        human.total_money += 1.5 * human.current_bet
        if VERBOSE:
            print("WIN - BLACKJACK: Player earns $" + str(human.current_bet) + " Total money=$" + str(human.total_money))
        return BLACKJACK
    elif human.total_value > dealer_AI.total_value:
        human.total_money += human.current_bet
        if VERBOSE:
            print("WIN: Player earns $" + str(human.current_bet) + " Total money=$" + str(human.total_money))
        return WIN
    elif human.total_value < dealer_AI.total_value and dealer_AI.total_value > 21:
        human.total_money += human.current_bet
        if VERBOSE:
            print("WIN: Player earns $" + str(human.current_bet) + " Total money=$" + str(human.total_money))
        return WIN
    elif human.total_value < dealer_AI.total_value:
        human.total_money -= human.current_bet
        if VERBOSE:
            print("LOSE: Player loses $" + str(human.current_bet) + " Total money=$" + str(human.total_money))
        return LOSS
    else:
        if VERBOSE:
            print("PUSH")
        return PUSH


def incrementCounts(human_action, 
                    result,
                    num_losses,
                    num_wins,
                    num_pushes,
                    num_blackjacks,
                    num_doubles_lost,
                    num_doubles_won,
                    num_doubles_pushed,
                    num_doubles_blackjacked):
    if result == LOSS:
        if human_action == "D":
            num_doubles_lost += 1
        else:
            num_losses += 1
    elif result == WIN:
        if human_action == "D":
            num_doubles_won += 1
        else:
            num_wins += 1
    elif result == PUSH:
        if human_action == "D":
            num_doubles_pushed += 1
        else:
            num_pushes += 1
    elif result == BLACKJACK:
        if human_action == "D":
            num_doubles_blackjacked += 1
        else:
            num_blackjacks += 1
    return num_losses, num_wins, num_pushes, num_blackjacks, num_doubles_lost, num_doubles_won, num_doubles_pushed, num_doubles_blackjacked


def main():
    num_games_list = []
    money_list = []

    for num_games in range(1, 10000):

        # Init players and deck
        human = Human(total_money=200)
        dealer_AI = Dealer_AI()
        deck = create_deck(1)
        num_losses = 0
        num_wins = 0
        num_pushes = 0
        num_blackjacks = 0
        num_doubles_won = 0
        num_doubles_lost = 0
        num_doubles_pushed = 0
        num_doubles_blackjacked = 0

        num_bankrupts = 0

        for num_trials in range(num_games):
            human.get_initial_cards(deck)
            dealers_up_card = dealer_AI.get_initial_cards(deck)

            human.bet(2)
            human_action = human.play_hand(deck, dealers_up_card)

            dealer_AI.play_hand(deck)

            result = process_bet(human, dealer_AI)

            num_losses, num_wins, num_pushes, num_blackjacks, num_doubles_lost, num_doubles_won, num_doubles_pushed, num_doubles_blackjacked = incrementCounts(human_action, 
                                                                                                                                                               result,
                                                                                                                                                               num_losses,
                                                                                                                                                               num_wins,
                                                                                                                                                               num_pushes,
                                                                                                                                                               num_blackjacks,
                                                                                                                                                               num_doubles_lost,
                                                                                                                                                               num_doubles_won,
                                                                                                                                                               num_doubles_pushed,
                                                                                                                                                               num_doubles_blackjacked)

            if human.total_money < 0:
                # human.total_money = 200
                num_bankrupts += 1
                # break

            # Reset deck if running low
            if len(deck) < 13:
                deck = create_deck(1)

        # print(human.total_money)
        # print(num_losses, num_wins, num_pushes, num_blackjacks)
        payback = (num_wins + 1.5*num_blackjacks + 2*num_doubles_won + 2*1.5*num_doubles_blackjacked) / (num_losses + num_doubles_lost + 1)
        # print(str(starting_money) + "," + str(human.total_money))
        print(num_games, payback*100)
        money_list.append(payback*100)
        num_games_list.append(num_games)
    
    plt.plot(num_games_list, money_list)
    plt.xlabel('Number of Hands Played')
    plt.ylabel('Payback Percentage')
    plt.title('The Effect of the Number of Hands Played on the Payback Percentage, \$2 Bets, \$200 Starting Amount')
    plt.show()
    

if __name__ == "__main__":
    main()