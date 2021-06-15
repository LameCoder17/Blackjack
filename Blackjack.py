'''
Casino Style Blackjack game
'''

import random
import time

class Card():
    ''' Simulates a single card with its rank, value and suit '''

    def __init__(self, rank, value, suit):
        ''' Initialize card attributes '''
        self.rank = rank
        self.value = value
        self.suit = suit

    def displayCard(self):
        ''' Prints rank and suit of individual card '''
        print(self.rank + " of " + self.suit)


class Deck():
    ''' Simulates deck of 52 playing cards '''
    def __init__(self):
        ''' Initialize deck attributes '''
        self.cards = [] # A list to hold all cards

    def buildDeck(self):
        ''' Builds deck of 52 cards '''
        # Information of all cards
        suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
        ranks = {
            'A' : 11,  # Ace can have value of 1 or 11
            '2' : 2,
            '3' : 3,
            '4' : 4,
            '5' : 5,
            '6' : 6,
            '7' : 7,
            '8' : 8,
            '9' : 9,
            '10' : 10,
            'J' : 10,
            'K' : 10,
            'Q' : 10
        }

        # Builds whole deck by creating 52 cards
        for suit in suits:
            for rank, value in ranks.items():
                card = Card(rank, value, suit)
                self.cards.append(card)

    def shuffleDeck(self):
        ''' Shuffles the deck '''
        random.shuffle(self.cards)

    def dealCard(self):
        ''' Removes a card from deck and deals it '''
        card = self.cards.pop() # Deals the last card in the deck
        return card


class Player():
    ''' A class for the user to play blackjack '''
    def __init__(self):
        ''' Initializes the player '''
        self.hand = [] # A list to hold player's card
        self.handValue = 0 # Total value of player's card
        self.playingHand = True # Tracks if player is playing current hand

    def drawHand(self, deck):
        ''' Deals the player starting hands '''
        for i in range(2):  # Player starts with 2 cards in hand
            card = deck.dealCard()
            self.hand.append(card)

    def displayHand(self):
        ''' Shows player's hand '''
        print("\n Player's hand : ")
        for card in self.hand:
            card.displayCard()

    def hit(self, deck):
        ''' Gives player 1 new card '''
        card = deck.dealCard()
        self.hand.append(card)

    def getHandValue(self):
        ''' Computes value of player's hand '''
        self.handValue = 0

        aceInHand = False # Bool to check if player has Ace

        for card in self.hand:
            self.handValue += card.value
            
            if card.rank == 'A': # Checks for Ace
                aceInHand = True

        if self.handValue > 21 and aceInHand:  # Player went over 21 but have Ace in hand
            self.handValue -= 10  # Ace gets treated as 1 instead of 11

        print("Total value : " + str(self.handValue))
            
    def updateHand(self, deck):
        ''' Updates player hand by giving them an option to hit '''
        if self.handValue < 21:
            choice = input("Would you like to hit (y/n) ? ")  # Option to hit
            if choice == 'y':
                self.hit(deck)
            else:
                self.playingHand = False  # Done playing hand
        else:
            self.playingHand = False  # Can't play anymore as value over 21

    

class Dealer():
    ''' Simulates blackjack dealer and must hit up to 17 '''

    def __init__(self):
        ''' Initializes the dealer '''
        self.hand = [] # A list to hold dealer's card
        self.handValue = 0 # Total value of dealer's card
        self.playingHand = True # Tracks if dealer is playing current hand

    def drawHand(self, deck):
        ''' Deal starting hand of dealer's card'''
        for i in range(2):  # Dealer starts with 2 cards in hand
            card = deck.dealCard()
            self.hand.append(card)

    def displayHand(self):
        ''' Shows player's hand '''
        input("\nPress Enter to reveal dealer's hand")
        for card in self.hand:
            card.displayCard()
            time.sleep(1)  # Builds suspense


    def hit(self, deck):
        ''' Dealer must hit till they reach atleast 17 '''
        self.getHandValue()
        while self.handValue < 17: # Dealer must keep hitting till they reach more than 17
            card = deck.dealCard()
            self.hand.append(card)
            self.getHandValue()

        print("\nDealer has " + str(len(self.hand)) + " cards")

    def getHandValue(self):
        ''' Computes value of dealer's hand '''
        self.handValue = 0

        aceInHand = False # Bool to check if dealer has Ace

        for card in self.hand:
            self.handValue += card.value
            
            if card.rank == 'A': # Checks for Ace
                aceInHand = True

        if self.handValue > 21 and aceInHand:  # Dealer went over 21 but have Ace in hand
            self.handValue -= 10  # Ace gets treated as 1 instead of 11


class Game():
    ''' Holds bets and payouts '''

    def __init__(self, money):
        ''' Initialize attributes'''
        self.money = int(money)  # Total money
        self.bet = 10  # Minimum bet per hand
        self.winner = ""  # As no hand has been played yet
        

    def setBet(self):
        ''' Sets users bet '''
        betting = True
        while betting:
            bet = int(input("How much would you like to bet ? (Minimum is 10) "))  # Gets user's bet

            if bet < 10:  # If bet is too low
                bet = 10
            if bet > self.money:  # If bet is too high
                print("You can't afford that bet")
            else:  # Bet is acceptable
                self.bet = bet
                betting = False

    def scoring(self, playerValue, dealerValue):
        ''' Score a round of blackjack '''

        # Someone got Blackjack
        if playerValue == 21:
            print("\nYou got Blackjack !!! You WON !!!")
            self.winner = 'player'
        elif dealerValue == 21:
            print("\nDealer got Blackjack !!! You lost")
            self.winner = 'dealer' 

        # Someone went over 21
        elif playerValue > 21:
            print("\nYou went over 21. You lose")
            self.winner = 'dealer'
        elif dealerValue > 21:
            print("\nDealer went over 21. You WIN!!!")
            self.winner = 'player'
        
        # Other cases
        else:
            if playerValue > dealerValue:
                print("\nDealer gets " + str(dealerValue) + " . You WIN !!!")
                self.winner = 'player'
            elif dealerValue < playerValue:
                print("\nDealer gets " + str(dealerValue) + " . You lose")
                self.winner = 'dealer'
            else:
                print("\nDealer gets " + str(dealerValue) + " . It's a tie")
                self.winner = 'tie'

    def payout(self): 
        ''' Updates money based on who won '''
        if self.winner == 'player':  # User won and thus earned money
            self.money += self.bet
        elif self.winner == 'dealer':  # User lost and thus lost money
            self.money -= self.bet

    def displayMoney(self):
        ''' Prints current money for the game '''
        print("\nCurrent Money : " + str(self.money))

    def displayMoneyAndBet(self):
        ''' Displays current money and bet for the game '''
        print("\nCurrent Money : " + str(self.money) + "\t Current Bet : " + str(self.bet))

# Main code
print("Welcome to Casino Blackjack")
print("Minimum bet is $10")

# Create game object
money = int(input("\nHow much money are you willing to gamble with ? "))
game = Game(money)

# Main game loop
playing = True 
while playing:
    # Creates a deck
    deck = Deck() 
    deck.buildDeck()
    deck.shuffleDeck()

    # Create player and dealer
    player = Player()
    dealer = Dealer()

    # Shows how much money player has and gets current bet
    game.displayMoney()
    game.setBet()

    # Draw player and dealer's hands
    player.drawHand(deck)
    dealer.drawHand(deck)

    # Simulates one round of blackjack
    game.displayMoneyAndBet()
    print("The dealer is showing a " + dealer.hand[0].rank + " of " + dealer.hand[0].suit)

    # While player is playing, show hand and calculate value of current hand, allowing player to hit/stay
    while player.playingHand:
        player.displayHand()
        player.getHandValue()
        player.updateHand(deck)

    # Simulate one round of blackjack for the dealer
    dealer.hit(deck)
    dealer.displayHand()

    # Determine winner and payout
    game.scoring(player.handValue, dealer.handValue)
    game.payout()

    # If user ran out of money
    if game.money < 10:
        playing = False
        print("\nRan out of Money !!!")



