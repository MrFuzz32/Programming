suits = {1:'♣',2:'♠',3:'♥',4:'♦'} #clubs, spades, hearts, diamonds
special_numbers = {1:'A',11:'J',12:'Q',13:'K'} #ace, jack, queen, king

#a class for an individual playing card
class Card:
    def __init__(self, number, suitNum, faceUp = False):
        self.number = number
        self.suitNum = suitNum
        self.faceUp = faceUp
    
    #change the card's faceUp status, and return the new faceUp status
    def flip(self):
        self.faceUp = not self.faceUp
        return self.faceUp
    
    #return a tidy summary of the properties of the card
    def tidy_summary(self):
        if self.number in special_numbers:
            value = special_numbers[self.number]
        else:
            value = str(self.number)
        
        suit = suits[self.suitNum]
        
        return [value,suit]
    
    #return the information about the card that should be visible to the user, based on it's faeUp status
    def visible_info(self):
        if self.faceUp == True:
            return self.tidy_summary(),self.faceUp
        else:
            return ['-','-'],self.faceUp
    
    #return whether the card is red
    def red(self):
        return (self.suitNum == 3 or self.suitNum == 4)
    
    #return whether the card is black
    def black(self):
        return (self.suitNum == 1 or self.suitNum == 2)