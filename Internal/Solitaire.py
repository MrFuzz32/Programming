from logging import exception
from msilib.schema import ReserveCost
from Classes import Card,suits
import random
import time
import os
import math
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

#user input:
#row of card to move,how many cards from that row:where to move it ----- or draw pile
#options: [1,2,3,4,5,6,7],num or D

sp = ' '


# the total length of each header
hdrlen = 40

#coloring theme for the game
board_style = Back.GREEN
side_style = Back.LIGHTGREEN_EX
red_card_style = Back.WHITE + Fore.RED
black_card_style = Back.WHITE + Fore.BLACK
facedown_card_style = Back.BLUE + Fore.LIGHTYELLOW_EX
empty_space_style = Back.LIGHTBLACK_EX + Fore.WHITE
reset_format = Style.RESET_ALL

#the width (in spaces) of each card on the board, cannot be less than 5
card_width = 5
if card_width < 5:
    card_width = 5

#how many spaces on either side of the collection area
side_collection_buffer = 2

# taken from https://stackoverflow.com/questions/517970/how-to-clear-the-interpreter-console
# clears the console
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

# takes in a title and total target length of the header, and returns a string with the title surrounded by the correct number of (by default)'-'s
def header(text, length=hdrlen, char='-'):
    return math.floor((length - len(text)) / 2) * char + text + math.ceil(
        (length - len(text)) / 2) * char

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

def init_board(deck):
    board = []
    #deal out seven stacks of cards in increasing sizes (as is required for the beginning of solitaire)
    for stack_len in range(1,8):
        stack = []
        for i in range(stack_len):
            card_to_add = deck.pop(0)
            if i == stack_len-1: #cards are by default face down, so flip the final card in each stack
                card_to_add.flip()
            stack.append(card_to_add)
        board.append(stack)
    return board

def card_string(card, colour = True):
    info,faceUp = card.visible_info()
    if faceUp:
        middle = info[0]
        middle += sp*((card_width-3)-len(middle))
        middle +=  info[1]
    else:
        middle = 'x'*(card_width-2)
    output = '[' + middle + ']'
    
    if colour:
        if faceUp:
            if card.red():
                formatting = red_card_style
            else:
                formatting = black_card_style
        else:
            formatting = facedown_card_style
    
    return cs(output,formatting)

#stands for colour string
def cs(text,style):
    return style+text+reset_format

#print out the UI and returns the user input
def interface(board):
    cls()
    #find the longest stack on the board
    max_stack_len = 0
    for stack in board:
        if len(stack) > max_stack_len:
            max_stack_len = len(stack)
    
    #make sure the board is at least 5 spaces tall to allow for card collection on the right
    if max_stack_len < 5:
        max_stack_len = 5
    
    # print out each row of the baord
    for row_index in range(max_stack_len):
        for count,stack in enumerate(board): # loop through each stack, taking the row_index-th card in it (if that index exists)
            #if the stack is the last on the board, don't put a space after the card
            if count == 6:
                suffix = ''
            else:
                suffix = ' '

            if len(stack) > row_index: # if the stack has an item at the specified row
                card = stack[row_index]
                output = card_string(card)
                print(output, end='')
                print(cs(suffix, board_style), end='')
            else: # if the stack doesn't have an item at the specified index
                print(cs(sp*card_width + suffix, board_style), end='')
        buffer_seg = cs(sp,side_style)
        buffer = buffer_seg*side_collection_buffer
        if row_index <=3:
            try:
                print(buffer + card_string(collection[row_index][-1]) + buffer,end='')
            except:
                print(buffer + cs('[ '+suits[row_index+1]+' ]', empty_space_style) + buffer,end='')
        else:
            print(buffer*2+buffer_seg*card_width,end='')
        print() # print a newline for each row
    return input()

def controls():
    cls()
    print(header('SOLITAIRE CONTROLS'))
    print('Use the keyboard to input actions\n\nPress ENTER to continue')
    input()

#check to see if the input string fits to the input format asked of the user
def check(userIn):
    valid = False
    # find at what index the actual characters start
    start = 0
    end = len(userIn) - 1
    for n in range(start, end + 1):
        if userIn[n].isalnum():
            start = n
            break
    # find at what index the actual characters end
    for n in range(end, start - 1, -1):
        if userIn[n].isalnum():
            end = n
            break
    # clip input to specified start and end values
    tweaked = userIn[start:end + 1]
    return valid,tweaked

#output the specified error message
def error(message):
    print(message)

#execute the given command on the board if it is valid
def execute(command, board):
    valid = False
    return valid,board

board = [] #where the current cards 'in play' and their arrangement is stored
deck = shuffle(populated_deck()) #generate a random deck of 52 cards and store it in an array
collection = [] #where the collected cards of each suit are stored (clubs, spades, hearts, diamonds)
drawPile = [] #where the three draw cards are stored
board = init_board(deck)
controls()

#main loop
end = False #set to true once the user chooses to exit or wins the game
won = False #set to true if the user has won
while not end:
    userIn = interface(board)
    valid,tweaked = check(userIn)
    if not valid:
        error(tweaked + ' is not a valid input')
        time.sleep(1)
    else:
        valid,board = execute(tweaked, board)

if won == True:
    #they won
    pass
else:
    #they gave up
    pass