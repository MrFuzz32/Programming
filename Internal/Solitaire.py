from Classes import Card
import random

#7 columns
#52 cards
#2D list for board - 1st dimmension for columns, 2nd dimmension for rows

# [---] [---] [---] [A:D] [2:C]       [3:S]      C - [---]
# [K:S] [---] [J:D]                              S - [---]
#       [4:H]                                    H - [---]
#       [3:C]                                    D - [---]
#
# Draw Pile (12 left): [Q:H]

def populated_deck():
    deck = []
    for suit in range(1,5):
        for num in range(1,14):
            deck.append(Card(num,suit))
    return deck
    
def shuffle(deck):
    new_deck = []
    while not len(deck) == 0:
        index = random.randint(0,len(deck)-1)
        card = deck.pop(index)
        new_deck.append(card)
    return new_deck
        
deck = populated_deck()
board = []

for i in range(5):
    print(deck[i].tidy_summary())
    
for i in range(1,6):
    print(deck[-i].tidy_summary())
    
deck = shuffle(deck)
print('\nnow shuffled\n')

for i in range(5):
    print(deck[i].tidy_summary())
    
for i in range(1,6):
    print(deck[-i].tidy_summary())

    