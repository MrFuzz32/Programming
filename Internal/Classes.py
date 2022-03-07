suits = {1:'Clubs',2:'Spades',3:'Hearts',4:'Diamonds'}

class Card:
    def __init__(self, number, suitNum):
        self.number = number
        self.suitNum = suitNum
        self.suit = suits[suitNum]
    
    def summary(self):
        return [self.number,self.suitNum,self.suit]