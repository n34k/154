from deck import Deck
from deriveScore import Score
#this class has all the game logic, like turns, checking score, etc
class Game:
    def __init__(self, singleDeck = True):
        self.dealerScore = Score()
        self.playerScore = Score()
        self.dealerCards = []
        self.playerCards = []
        self.deck = Deck()
        self.singleDeck = singleDeck # whether we are playing with a single deck (w or w/o replacement)
        self.result = False

    def startGame(self):
        for _ in range(2):
            self.dealerCards.append(self.deck.dealSingle() if self.singleDeck else self.deck.dealInf())
            self.playerCards.append(self.deck.dealSingle() if self.singleDeck else self.deck.dealInf())

        self.playerScore.calcScore(self.playerCards)

    def dealerHit(self):
        self.dealerCards.append(self.deck.dealSingle() if self.singleDeck else self.deck.dealInf())
        self.dealerScore.calcScore(self.dealerCards)

    def printHands(self):
        print(f"Your hand: {self.playerCards}")
        print(f"Dealer hand: {self.dealerCards}")

    def printHandsOneDealerCard(self):
        print(f"Your hand: {self.playerCards}")
        print(f"Dealer hand: {self.dealerCards[0]}")

    def hit(self):
        self.playerCards.append(self.deck.dealSingle() if self.singleDeck else self.deck.dealInf())
        return self.checkScoreAfterHit()

    def checkScoreAfterHit(self):
        self.playerScore.calcScore(self.playerCards)
        if self.playerScore.score > 21:
            return False
        else: 
            return True
        
    # when we stand, this ends the game, dealer will hit until they bust, 
    # have a better score than the player, or reached 17 (not soft)      
    def stand(self):  
        self.dealerScore.calcScore(self.dealerCards)
        self.playerScore.calcScore(self.playerCards)

        # check ig player has busted for safety (should be done in checkScoreAfterHit)
        if self.playerScore.score > 21:
            self.result = False
            return False

        # dealer hits 16, stands 17, hits soft 17
        while self.dealerScore.score < 17 or (self.dealerScore.soft and self.dealerScore.score == 17):
            self.dealerHit()

        # dealer busted
        if self.dealerScore.score > 21:
            self.result = True
            return True

        # check tie
        if self.dealerScore.score == self.playerScore.score:
            self.result = "Tie"
            return "Tie"

        # dealer has reached 17, check who has higher score
        self.result = self.playerScore.score > self.dealerScore.score
        return self.result


            
