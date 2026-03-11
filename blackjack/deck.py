import random
from typing import Union


class Deck:
    def __init__(self):
        self.cards = ['A','A','A','A',2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8,9,9,9,9,10,10,10,10,'J','J','J','J','Q','Q','Q','Q','K','K','K','K']
        self.cardsLeft = 52
        
    def dealInf(self) -> Union[str, int]: #w/o replacement
        randCard = random.randint(0, 51)
        return self.cards[randCard]

    def dealSingle(self) -> Union[str, int]: #w replacement
        randCard = random.randint(0, self.cardsLeft-1) # -1 for 0 indexed arrays
        card = self.cards[randCard]
        self.cardsLeft -= 1
        self.cards.remove(card)
        return card

