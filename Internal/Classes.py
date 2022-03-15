suits = {1:'Clubs',2:'Spades',3:'Hearts',4:'Diamonds'}

class Card:
    def __init__(self, number, suitNum, faceUp = True):
        self.number = number
        self.suitNum = suitNum
        self.faceUp = faceUp
        
    def flip(self):
        self.faceUp = not self.faceUp
        return self.faceUp
    
    def red(self):
        return (self.suitNum == 3 or self.suitNum == 4)
    
    def black(self):
        return (self.suitNum == 1 or self.suitNum == 2)