from game import Game
from deriveScore import Score

class Policies:
    def __init__(self, singleDeck = True):
        self.game = Game(singleDeck)
    
    def playManual(self):
        self.game.startGame()
        self.game.printHandsOneDealerCard()
        gameOn = True
        result = False
        while gameOn:
            move = input("Hit or stand? (Type 'H' or 'S'): ")
            if move == 'H':
                gameOn = self.game.hit()
                self.game.printHandsOneDealerCard()
            elif move == 'S':
                result = self.game.stand()
                self.game.printHands()
                break
            else:
                print("Invalid move, try again")
                continue

        if result == "Tie":
            print("Tie")
        elif result:
            print("You win")
        else:
            print("You lose")

        return result
    
    def playStandGE17(self): # stand once we reach 17 soft or hard
        self.game.startGame()

        while self.game.playerScore.score < 17:
            stillPlaying = self.game.hit()
            if not stillPlaying:
                self.game.result = False
                return False

        self.game.result = self.game.stand()
        return self.game.result
        
    def playStandGE17AndHard(self): # stand on hard 17, hit on soft 17
        self.game.startGame()

        while self.game.playerScore.score < 17 or (self.game.playerScore.score == 17 and self.game.playerScore.soft):
            stillPlaying = self.game.hit()
            if not stillPlaying:
                self.game.result = False
                return False

        self.game.result = self.game.stand()
        return self.game.result
    
    def playAlwaysStand(self):
        self.game.startGame()
        self.game.result = self.game.stand()
        return self.game.result
    
    def stand16DealerUnder10(self): #always stand on 16, unless dealer has a 10 or higher, then we hit until 17
        self.game.startGame()

        dealerScore = Score()
        _, dealerScoreFirstCard = dealerScore.calcScore([self.game.dealerCards[0]])

        while self.game.playerScore.score < 16: #hit until 16
            stillPlaying = self.game.hit()
            if not stillPlaying:
                self.game.result = False
                return False
        
        if dealerScoreFirstCard >= 10 and self.game.playerScore.score == 16:
            stillPlaying = self.game.hit()
            if not stillPlaying:
                self.game.result = False
                return False
        
        self.game.result = self.game.stand()
        return self.game.result

    def stand17DealerUnder9(self): #always stand on 17, unless dealer has a 9 or higher, then we hit until 18
        self.game.startGame()

        dealerScore = Score()
        _, dealerScoreFirstCard = dealerScore.calcScore([self.game.dealerCards[0]])

        while self.game.playerScore.score < 17: #hit until 17
            stillPlaying = self.game.hit()
            if not stillPlaying:
                self.game.result = False
                return False

        if dealerScoreFirstCard >= 9 and self.game.playerScore.score == 17:
            stillPlaying = self.game.hit()
            if not stillPlaying:
                self.game.result = False
                return False

        self.game.result = self.game.stand()
        return self.game.result

    def playBasicStrategy(self): # classic basic strategy (hit/stand only, no split/double)
        self.game.startGame()

        dealerScore = Score()
        _, dealerUpcard = dealerScore.calcScore([self.game.dealerCards[0]])

        while True:
            score = self.game.playerScore.score
            soft = self.game.playerScore.soft

            if soft:
                # soft 19+: always stand
                if score >= 19:
                    break
                # soft 18: stand vs dealer 2-8, hit vs 9,10,11(A)
                elif score == 18:
                    if dealerUpcard >= 9:
                        pass # hit below
                    else:
                        break
                # soft 13-17: always hit
            else:
                # hard 17+: always stand
                if score >= 17:
                    break
                # hard 13-16: stand vs dealer 2-6, hit vs 7+
                elif score >= 13:
                    if dealerUpcard <= 6:
                        break
                # hard 12: stand vs dealer 4-6, hit otherwise
                elif score == 12:
                    if 4 <= dealerUpcard <= 6:
                        break
                # hard 11 and below: always hit

            stillPlaying = self.game.hit()
            if not stillPlaying:
                self.game.result = False
                return False

        self.game.result = self.game.stand()
        return self.game.result
    