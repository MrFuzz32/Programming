from Classes import Card
import random
from colorama import Fore, Back, Style

#7 columns
#52 cards
#2D list for board - 1st dimmension for columns, 2nd dimmension for rows

# [---] [---] [---] [A:D] [2:C]       [3:S]      C - [---]
# [K:S] [---] [J:D]                              S - [---]
#       [4:H]                                    H - [---]
#       [3:C]                                    D - [---]
#
# Draw Pile (12 left): [Q:H]

sp = ' '

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

#print out the UI
def print_screen(board):
    #find the longest stack on the board
    max_stack_len = 0
    for stack in board:
        if len(stack) > max_stack_len:
            max_stack_len = len(stack)
    
    # print out each row of the baord
    for row_index in range(max_stack_len):
        for count,stack in enumerate(board):
            #if the stack is the last on the board, don't put a space after the card
            if count == 6:
                suffix = ''
            else:
                suffix = ' '

            if len(stack) > row_index: # if the stack has an item at the specified row
                card = stack[row_index]
                info,faceUp = card.visible_info()
                middle = info[0]
                middle += sp*(2-len(middle))
                middle +=  info[1]
                output = '[' + middle + ']'
                if faceUp:
                    if card.red():
                        formatting = Back.WHITE + Fore.RED
                    else:
                        formatting = Back.WHITE + Fore.BLACK
                else:
                    formatting = Back.BLUE
                print(formatting + output, end='')
                print(Style.RESET_ALL+suffix, end='')
            else: # if the stack doesn't have an item at the specified index
                print(sp*5 + suffix, end='')
        print() # print a newline for each row
    
        

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

print_screen(board)