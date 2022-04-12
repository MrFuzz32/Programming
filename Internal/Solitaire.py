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

#makes printing compound strings easier
sp = ' '

# the total length of each header
hdrlen = 40

#coloring themes for the game
board_style = Back.GREEN
side_style = Back.LIGHTGREEN_EX
red_card_style = Back.WHITE + Fore.RED
black_card_style = Back.WHITE + Fore.BLACK
facedown_card_style = Back.BLUE + Fore.LIGHTYELLOW_EX
empty_space_style = Back.LIGHTBLACK_EX + Fore.WHITE
draw_pile_card_style = Back.LIGHTBLACK_EX + Fore.WHITE
held_title_style = Back.LIGHTYELLOW_EX + Fore.BLACK + Style.BRIGHT
input_line_style = Back.LIGHTYELLOW_EX + Fore.BLACK
title_style = Back.LIGHTYELLOW_EX + Fore.BLACK + Style.BRIGHT
extra_card_status_style = Back.LIGHTGREEN_EX + Fore.BLACK
error_style = Back.LIGHTRED_EX + Fore.BLACK
reset_format = Style.RESET_ALL

#all possible random background colours, excluding black and white
randoms = [Back.BLUE,Back.CYAN,Back.GREEN,Back.LIGHTBLUE_EX,Back.LIGHTCYAN_EX,Back.LIGHTGREEN_EX,Back.LIGHTMAGENTA_EX,Back.LIGHTRED_EX,Back.LIGHTYELLOW_EX,Back.MAGENTA,Back.RED,Back.YELLOW]


#the width (in spaces) of each card on the board, cannot be less than 5
card_width = 7
if card_width < 5:
    card_width = 5

#how many spaces on either side of the collection area
side_collection_buffer = 3

#how many spaces to put between stacks
stack_spacing = 2

#how many spaces to put between each card in the draw pile
draw_pile_spacing = 0

#calculations of section widths
board_width = 7*card_width+8*stack_spacing
side_width = 2*side_collection_buffer+card_width

#the ammount of ['s used to indicate the size of the remaining draw pile
draw_pile_preview = 10

#how wide the control screen should be
control_screen_width = 70

#the amount of cards to draw each time the draw pile is cycled
drawCount = 3

#stands for colour string
#takes in a plain string and returns the string coloured with the chosen style
def cs(text,style):
    return style+text+reset_format

#one background 'segment' of the board
board_back_seg = cs(sp,board_style)
#one background 'segment' of the side
side_back_seg = cs(sp,side_style)

# taken from https://stackoverflow.com/questions/517970/how-to-clear-the-interpreter-console
# clears the console
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

# takes in a title and total target length of the header, and returns a string with the title surrounded by the correct number of (by default)'-'s
def header(textRaw, length=hdrlen, char='-', style=None):
    if not style == None:
        text = cs(textRaw,style)
    else:
        text = textRaw
    return math.floor((length - len(textRaw)) / 2) * char + text + math.ceil(
        (length - len(textRaw)) / 2) * char

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

#deal out seven stacks of cards in increasing sizes (as is required for the beginning of solitaire) into the deck passed in
def init_board(deck):
    board = []
    for stack_len in range(1,8):
        stack = []
        for i in range(stack_len):
            card_to_add = deck.pop(0)
            if i == stack_len-1: #cards are by default face down, so flip the final card in each stack
                card_to_add.flip()
            stack.append(card_to_add)
        board.append(stack)
    return board

#take in a card object and return the tidy string out, coloured appropriately by default
def card_string(card, colour = True):
    info,faceUp = card.visible_info()
    if faceUp:
        middle = info[0]
        middle += sp*((card_width-3)-len(middle))
        middle +=  info[1]
    else:
        middle = 'x'*(card_width-2)
    output = '[' + middle + ']'
    
    #if colour is true, colour the card string
    if colour:
        if faceUp:
            if card.red():
                formatting = red_card_style
            else:
                formatting = black_card_style
        else:
            formatting = facedown_card_style
        output = cs(output,formatting)
    
    return output

#return a row of blank spaces of the length of a blank row of the board and/or side, coloured appropriately
def blank_row(board=True,side=True):
    output = ''
    if board:
        output += cs(sp*board_width,board_style)
    if side:
        output += cs(sp*side_width,side_style)
    return output

#print out the current state of the board, collection piles, draw pile, and held cards
def printPlayBoard(board,drawPile,held_cards):
    #find the longest stack on the board
    max_stack_len = 0
    for stack in board:
        if len(stack) > max_stack_len:
            max_stack_len = len(stack)
    
    #make sure the board is at least 4 spaces tall to allow for card collection on the right
    if max_stack_len < 4:
        board_height = 4
    else:
        board_height = max_stack_len
    
    print(blank_row())
    # print out each row of the baord's stacks, as well as the collection piles
    for row_index in range(board_height):
        for count,stack in enumerate(board): # loop through each stack, taking the row_index-th card in it (if that index exists)
            if count == 6:
                suffix = board_back_seg*stack_spacing
            else:
                suffix = ''
            if len(stack) > row_index: # if the stack has an item at the specified row
                card = stack[row_index]
                output = card_string(card)
                print(board_back_seg*stack_spacing + output + suffix, end='')
            else: # if the stack doesn't have an item at the specified index
                print(board_back_seg*(card_width+stack_spacing) + suffix, end='')
        buffer = side_back_seg*side_collection_buffer
        #if one of the first 4 rows, add on a collection pile
        if row_index <=3:
            try:
                print(buffer + card_string(collection[row_index][0]) + buffer,end='')
            except:
                print(buffer + cs('[',empty_space_style) + header(suits[row_index+1],card_width-2,cs(sp,empty_space_style),empty_space_style) + cs(']',empty_space_style) + buffer,end='')
        else:
            print(buffer*2+side_back_seg*card_width,end='')
        print() # print a newline for each row
    
    #print the held section title
    print(blank_row(True,False),end='')
    buffer = side_back_seg*side_collection_buffer
    line = buffer + header('Held:',card_width,side_back_seg,held_title_style) + buffer
    print(line)
    
    #print out the draw pile
    if len(deck) >= draw_pile_preview:
        start = '['*draw_pile_preview
        delta = 0
    elif len(deck) == 0:
        start = ''
        delta = draw_pile_preview
    else:
        start = '['*(len(deck)-1)
        delta = draw_pile_preview-len(deck)+1
    try:
        middle = card_string(deck[0])
    except:
        middle = board_back_seg*card_width
    line = board_back_seg*(stack_spacing) + cs(start+middle,facedown_card_style) + board_back_seg*(delta+1)
    for i in range(2,-1,-1): #loop through the top three cards of the deck
        try:
            index = i
            if len(held_cards) == 2 and held_cards[1] == 'd': #if a card from the draw pile is in the held cards
                if i == 0: #don't print the last card
                    raise Exception()
                else:
                    index = i-1
            if i == 0:
                cardstring = card_string(drawPile[index])
            else:
                cardstring = cs(card_string(drawPile[index],False),draw_pile_card_style)
            
            if i == 2:
                spacing = ''
            else:
                spacing = board_back_seg*draw_pile_spacing
            line += spacing + cardstring
        except:
            line += board_back_seg*(card_width+draw_pile_spacing)
    print(line,end='')
    #print out the line
    line_length = stack_spacing + len(start) + card_width +1 + 3*card_width + 2*draw_pile_spacing + delta
    print(board_back_seg*(board_width-line_length),end='')
    
    #print the held cards
    try:
        print(buffer+card_string(held_cards[0][0])+buffer)
    except:
        print(buffer+side_back_seg*card_width+buffer)
    
    if len(held_cards[0]) > 1:
        print(blank_row(True,False),end='')
        line = header('(+'+str(len(held_cards[0])-1)+' more)',card_width+2*side_collection_buffer,side_back_seg,extra_card_status_style)
        print(line)
    else:
        print(blank_row())
    

    
#print out the UI and returns the user input
def interface(board,drawPile,held_cards):
    cls()
    #print the title
    print(header('SOLITAIRE',board_width+side_width,cs(sp,title_style),title_style))
    #print the board
    printPlayBoard(board,drawPile,held_cards)
    #print the user input line
    print(cs('Input your command here:',input_line_style) + sp,end='')
    
    return input()

#make all letters lowercase except the first
def correct(text):
    text = text.lower()
    text = text[0].upper() + text[1:]
    return text

#output the specified error message
def print_error(message):
    print(cs(correct(message),error_style))
    input(cs('Press enter to continue',error_style))

#cut off any non-alphanumeric characters at the ends of the text
def clip(text):
    # find at what index the actual characters start
    start = 0
    end = len(text) - 1
    for n in range(start, end + 1):
        if text[n].isalnum():
            start = n
            break
    # find at what index the actual characters end
    for n in range(end, start - 1, -1):
        if text[n].isalnum():
            end = n
            break
    # clip input to specified start and end values
    tweaked = text[start:end + 1]
    return tweaked

#cycles the draw pile through a specified amount of cards
def cycleDraw(count):
    for i in range(count):
        card = deck.pop(0)
        card.flip()
        drawPile.insert(0,card)

#blindly places the specified cards in the specified destination
def place(cards,destination):
    if destination in ['1','2','3','4','5','6','7']:
        index = int(destination)-1
        for held_index in range(len(cards)):
            board[index].append(cards.pop(0))
    elif destination in ['p1','p2','p3','p4']:
        pileIndex = int(destination[1])-1
        collection[pileIndex].insert(0,cards.pop(0))
    else:
        drawPile.insert(0,cards.pop(0))

#execute the given command on the board if it is valid
def execute(command_string,board):
    command_string = clip(command_string)
    command_string_lower = command_string.lower()
    segments = command_string_lower.split(' ')
    nb_segments = [] #stands for non_blank_segments
    #check each segment to see if it's blank, if it isn't: append it to nb_segments
    for count,segment in enumerate(segments):
        if not len(segment) == 0:
            nb_segments.append(segments[count])
    #if there was no substance to the user's input, return None
    if len(nb_segments) == 0:
        return None,board,False
    first_item = nb_segments[0]
    if first_item == 'grab': #grab a card or cards
        if len(nb_segments) == 2:
            modifier = 1
        elif len(nb_segments) == 3:
            modifier = 0
        else:
            return first_item + ' has been used incorrectly',board,False
                    
        try:
            if modifier == 0:
                quantity = int(nb_segments[1])
        except:
            return first_item + ' has been used incorrectly',board,False
        try:
            location = int(nb_segments[2-modifier])
            if modifier == 1:
                quantity = 0
                for card in board[location-1]:
                    if card.faceUp == True:
                        quantity += 1
            if quantity < 0:
                return first_item + ' has been used incorrectly',board,False
            if quantity < 1:
                return 'You cannot grab no cards',board,False
            # grab from a stack
            if location > 7 or location < 1: #check if the location is a number 1-7 (stack 1-7)
                return first_item + ' has been used incorrectly',board,False
            if not len(held_cards[0]) == 0:
                if len(held_cards[0]) == 1:
                    return 'There is already a card being held',board,False
                else:
                    return 'There are already cards being held',board,False
            stack = board[location-1]
            faceUps = 0
            for card in stack:
                if card.faceUp == True:
                    faceUps += 1
            if faceUps < quantity: #check if there are enough face up cards in the stack to grab the requested ammount
                return 'There are not enough face up cards in stack ' + str(location) + ' to grab ' + str(quantity),board,False
            for index in range(-quantity,0):
                held_cards[0].append(board[location-1].pop(index))
            held_cards.append(nb_segments[2-modifier])
        except:
            if modifier == 1:
                quantity = 1
            if not quantity == 1:
                return first_item + ' has been used incorrectly',board,False
            if nb_segments[2-modifier] in ['d','p1','p2','p3','p4']:
                if nb_segments[2-modifier] == 'd':
                    # grab from draw pile
                    if len(drawPile) == 0:
                        return 'The draw pile is empty',board,False
                    card = drawPile.pop(0)
                else:
                    # grab from a collection pile
                    pileIndex = int(nb_segments[2-modifier][1])-1
                    if len(collection[pileIndex]) == 0:
                        return 'Collection pile ' + str(pileIndex+1) + ' is empty',board,False
                    card = collection[pileIndex].pop(0)
                held_cards[0].append(card)
                held_cards.append(nb_segments[2-modifier])
            else:
                return first_item + ' has been used incorrectly',board,False
    elif first_item == 'place': #place a card or cards
        placed = False
        if len(held_cards[0]) == 0:
            return 'there are no held cards to place',board,False
        if len(nb_segments) < 2:
            return first_item + ' has been used incorrectly',board,False
        if nb_segments[1] == held_cards[1]: #if the requested location is the same as where the cards were grabbed from, place them
            place(held_cards[0],nb_segments[1])
            placed = True
        if not placed:
            try:
                #place on a stack
                location = int(nb_segments[1])
                if location > 7 or location < 1:
                    return first_item + ' has been used incorrectly',board,False
                placeCard = held_cards[0][0]
                if len(board[location-1]) == 0:
                    if placeCard.number == 13:
                        place(held_cards[0],nb_segments[1])
                        placed = True
                    else:
                        if len(held_cards[0]) == 1:
                            return 'The held card cannot be placed there',board,False
                        else:
                            return 'The held cards cannot be placed there',board,False
                else:
                    destCard = board[location-1][-1]
                if not placed:
                    if placeCard.red() == destCard.black() and placeCard.number == destCard.number-1:
                        place(held_cards[0],nb_segments[1])
                        placed = True
                    else:
                        if len(held_cards[0]) == 1:
                            return 'The held card cannot be placed there',board,False
                        else:
                            return 'The held cards cannot be placed there',board,False
            except Exception as e:
                if not nb_segments[1] in ['p1','p2','p3','p4','d']:
                    return first_item + ' has been used incorrectly',board,False
                if nb_segments[1] == 'd': #draw pile
                    return 'Only a card taken from the draw pile can be placed back there',board,False
                else:
                    #collection pile
                    if not len(held_cards[0]) == 1:
                        return 'Only one card can be placed in a collection pile at a time',board,False
                    pileNum = int(nb_segments[1][1])
                    if not pileNum == held_cards[0][0].suitNum:
                        return 'The held card cannot be placed there',board,False
                    if len(collection[pileNum-1]) == 0:
                        if held_cards[0][0].number == 1:
                            place(held_cards[0],nb_segments[1])
                        else:
                            return 'The held card cannot be placed there',board,False
                    else:
                        if held_cards[0][0].number == collection[pileNum-1][0].number + 1:
                            place(held_cards[0],nb_segments[1])
                        else:
                            return 'The held card cannot be placed there',board,False
                    placed = True
        if placed:
            held_cards.pop(1)
    elif first_item == 'drop': #drop cards back to where they came from
        if len(held_cards[0]) == 0:
            return 'there are no cards to drop',board,False
        place(held_cards[0],held_cards[1])
        held_cards.pop(1)
    elif first_item == 'draw': #cycle the draw pile
        if not len(held_cards[0]) == 0:
            if len(held_cards[0]) == 1:
                return 'You must drop or place the held card first',board,False
            else:
                return 'You must drop or place the held cards first',board,False
        if len(deck) == 0 and len(drawPile) == 0:
            return 'There are no cards to draw',board,False
        if len(deck) == 0:
            #no cards in deck
            for i in range(len(drawPile)):
                card = drawPile.pop(-1)
                card.flip()
                deck.append(card)
        if len(deck) >= drawCount:
            rng = drawCount
        else:
            rng = len(deck)
        cycleDraw(rng)
    elif first_item == 'exit': #exit the program
        return None,board,True
    else:
        return first_item + ' is not a recognised command',board,False
    
    return None,board,False #the operation was executed successfully

#flip any cards at the top of a stack that are face down, if no cards are currently held
def flip_cards(board):
    if not len(held_cards[0]) == 0:
        return board
    for stack in board:
        try:
            if stack[-1].faceUp == False:
                stack[-1].flip()
        except:
            pass
    return board

#celebration animation
def celebrate():
    cls()
    #read in the celebration template
    with open('Internal\Game_win.txt') as file:
        template = file.readlines()
        size = (len(template[0])+1,len(template)+2)
    #fill the grid with blank spaces
    grid = []
    for y in range(size[1]):
        row = []
        for x in range(size[0]):
            row.append(cs(' ',Back.WHITE))
        grid.append(row)
    #fill the points list with every possible point on the grid
    points = []
    for x in range(size[0]):
        for y in range(size[1]):
            points.append((x,y))
    #fill the grid with random colours and print it out once every 10 cycles
    while not len(points) == 0:
        for i in range(10):
            index = random.randint(0,len(points)-1)
            point = points.pop(index)
            grid[point[1]][point[0]] = cs(' ',random.choice(randoms))
            if len(points) == 0:
                break
        cls()
        for row in grid:
            for char in row:
                print(char,end='')
            print('')
    #for every part of the template with a B, colour the grid black
    for y,line in enumerate(template):
        for x,char in enumerate(line):
            if char == 'B':
                grid[y+1][x+1] = cs(' ',Back.BLACK)
        time.sleep(0.3)
        cls()
        for row in grid:
            for char in row:
                print(char,end='')
            print('')


board = [] #where the current cards 'in play' and their arrangement are stored
deck = shuffle(populated_deck()) #generate a random deck of 52 cards and store it in an array
collection = [[],[],[],[]] #where the collected cards of each suit are stored (clubs, spades, hearts, diamonds)
drawPile = [] #where the draw cards are stored
held_cards = [[]] #where the current held cards are stored
board = init_board(deck)
end = False #set to true once the user chooses to exit or wins the game
won = False #set to true if the user has won
#main loop
while not end:
    userIn = interface(board,drawPile,held_cards) #print out the UI and collect the user input
    error,board,end = execute(userIn, board) #attempt to execute the user's input
    board = flip_cards(board) #flip cards if applicable
    if not error == None: #if there was an error, print it
        print_error(error)
    #check if the user has satisfied the win condition
    won = True
    for pile in collection:
        if not len(pile) == 13:
            won = False
    #if the user won, print the board a final time
    if won == True:
        cls()
        printPlayBoard(board,drawPile,held_cards)
        time.sleep(1.3)
        end = True
    
#celebrate the user winning
if won == True:
    celebrate()