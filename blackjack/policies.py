from game import Game

class Play:
    def __init__(self, singleDeck = True):
        self.game = Game(singleDeck)
    
    def playManual(self):
        self.game.startGame()
        gameOn = True
        result = False
        while gameOn:
            move = input("Hit or stand? (Type 'H' or 'S'): ")
            if move == 'H':
                gameOn = self.game.hit()
            elif move == 'S':
                result = self.game.stand()
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