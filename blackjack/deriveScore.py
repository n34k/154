class Score:
    def __init__(self):
        self.score = 0
        self.soft = False
    
    def calcScore(self, hand: list[str | int]) -> tuple[str, int]: # [S | H for soft or hard hand, then score]
        currScore = 0
        aceCount = 0
        for card in hand:
            if card == 'J' or card == 'Q' or card == 'K':
                currScore += 10
            elif card == 'A':
                aceCount += 1
                currScore += 11
            else:
                currScore += card
        while currScore > 21 and aceCount > 0:
            currScore -= 10
            aceCount -= 1
        self.soft = aceCount > 0
        self.score = currScore
        return ('S' if self.soft else 'H', self.score)

