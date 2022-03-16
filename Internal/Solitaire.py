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

#return a list containing all 52 playing cards, ordered by suit and value
def populated_deck():
    deck = []
    for suit in range(1,5):
        for num in range(1,14):
            deck.append(Card(num,suit))
    return deck

#take in a list (doesn't have to be, but named to imply: of cards) and return it in a random order 
def shuffle(deck):
    new_deck = []
    while not len(deck) == 0:
        index = random.randint(0,len(deck)-1)
        card = deck.pop(index)
        new_deck.append(card)
    return new_deck
        

board = [] #where the current cards 'in play' and their arrangement is stored
deck = shuffle(populated_deck()) #generate a random deck of 52 cards and store it in an array
#deal out seven stacks of cards in increasing sizes (as is required for the beginning of solitaire)
for stack_len in range(1,8):
    stack = []
    for i in range(stack_len):
        card_to_add = deck.pop(0)
        if i == stack_len-1: #cards are by default face down, so flip the final card in each stack
            card_to_add.flip()
        stack.append(card_to_add)
    board.append(stack)

#debug readout
for column in board:
    for card in column:
        print(card.visible_info())
    print('')