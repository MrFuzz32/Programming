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
        
        
board = []
deck = shuffle(populated_deck())
for stack_len in range(1,8):
    stack = []
    for i in range(stack_len):
        card_to_add = deck.pop(0)
        if i == stack_len-1:
            card_to_add.flip()
        stack.append(card_to_add)
    board.append(stack)
    
for column in board:
    for card in column:
        print(card.visible_info())
    print('')