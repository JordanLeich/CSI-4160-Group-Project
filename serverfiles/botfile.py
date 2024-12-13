import socket 
import json 
import random
import Stateofplayin 
import logging 
from Stateofplayin import *

logging.basicConfig(level=logging.INFO)
'''
first we need to get the user's preferred bot level, easy medium, or hard,
easy will try to lose, taking the worst possable move at every oppertunity,
hard will do the opposite, taking optimal placement of your blunders
we can use numbers to represent board points:
 1 | 2 | 3
---+---+---
 4 | 5 | 6
---+---+---
 7 | 8 | 9
for their first play
    if bot is going first (turntype = 0):
            easy and medium will go on a random tile from (2,4,6,8)
            hard will go 5
    if they go second(turntype = 1): 
        easy will go to a (2,4,6,8) that is nearest to the players opening move and will avoid cutting off a possable win condition, if position 5 was selected by the player on first turn, it will run the first turn's routine, then this
        medium will go  to a (2,4,6,8) that is furthest from the players opening move ,if position 5 was selected by the player on first turn, it will run the first turn's routine, then this,
        hard will go to 5 if unclamed, and the corners(1,3,7,9) randomly otherwise
if they get to a possable win condition:
    if it is for the bots win(turntype = 3):
        easy will avoid this at all costs,
        medium will play it if you had a turn to try to stop it(meaning if there are 2 possable wins, it will choose to avoid them until 2 of the player turns have passed)
        hard will play this on it's next available turn
    if it is for the player's win(turntype = 4):
        easy will avoid it unless there are no other moves available,
        medium and hard will play it on it's next turn 
if nither player will win in the subsequent turns(turntype = 2):
    easy will play 2,4,6,8 closest to it's first turn algorithms, when exausted, it will play the corners(1,3,7,9), then 5, following simaler rules above
    med will play 2,4,6,8 randomly to it's first turn algorithms, when exausted, it will play the corners(1,3,7,9), then 5, following simaler rules above
    hard will play 1,3,7,9 after the first turn's algrorithms, but for it's second turn after playing a corner(1,3,7,9), if it has center, it will play right next to the corner(1,3,7, or 9) it already played. otherwise will play randomly corners(1,3,7,9) then edges(2,4,6,8) unless the above conditions are met

sidenote: we may be able to reuse the win condition checker to evaluate potential win conditions.
checking for win conditions:
 g  d   e   f  h
    1 | 2 | 3  a
   ---+---+---
    4 | 5 | 6  b
   ---+---+---
    7 | 8 | 9  c
a is 123, e is 258,h is 375, g is 159, for example
'''


def setupBoardStateNumbers(boardstate, boolSelfX):
    thisBoard = [0] * 9  # Initialize a 0-filled board
    for index, cell in enumerate(boardstate):
        if cell == "X":
            thisBoard[index] = 2
            if boolSelfX:
                thisBoard[index] = 1  
        elif cell == "O":
            thisBoard[index] = 1
            if boolSelfX:
                thisBoard[index] = 2
    return thisBoard

    #this is to determine whether the turn type is 
doomCounteronlocations = [-1, -1, -1,
                          -1, -1, -1,
                          -1, -1, -1] #this is for the medium bot
turnNoType= 0 #this is a selector for what type of turn this is
difficultyNo = 0 # 0 is easy, 1 is medium, 2 is hard
turnNo= 0 #this checks the BOT's move counter
firstmove = False #this is to check if we(the bot) get the first move
thisBoard = [0,0,0,
             0,0,0,
             0,0,0]
def botMove(boardState):
    global turnNo, turnNoType, difficultyNo, firstmove, thisBoard
    logging.info(f"Board state: {boardState}")
    logging.info(f"Turn number: {turnNo}")
    thisBoard = setupBoardStateNumbers(boardState, firstmove)
    empty_positions = [i for i, val in enumerate(thisBoard) if val == 0]
    move = -1

    if turnNoType == 2:
        if difficultyNo == 0:  # Easy bot
            move = random.choice(empty_positions)
        elif difficultyNo == 1:  # Medium bot
            # Medium bot prefers edges first, then corners
            preferred_positions = [1, 3, 5, 7]  # Edges (0-indexed: 2, 4, 6, 8)
            valid_moves = [pos for pos in preferred_positions if pos in empty_positions]
            move = valid_moves[0] if valid_moves else random.choice(empty_positions)
        elif difficultyNo == 2:  # Hard bot
            # Hard bot goes for optimal moves: center, corners, then edges
            if 4 in empty_positions:  # Center (index 4)
                move = 4
            else:
                preferred_positions = [0, 2, 6, 8]  # Corners (0-indexed)
                valid_moves = [pos for pos in preferred_positions if pos in empty_positions]
                move = valid_moves[0] if valid_moves else random.choice(empty_positions)
    #print(f"bot move initial plan = {move+1}")
    
    tempmove = detectwin(thisBoard, False)
    if (tempmove != -1) and (thisBoard[tempmove] == 0 ):
        turnNoType = 4
        #print(f"bot sees possable L")
    
    # Check for player win condition (blocking)
    if turnNoType == 4 and difficultyNo != 0:
        priorchoice = move
        move = detectwin(thisBoard, False)
        if move == -1:
            move = random.choice(empty_positions)
        if (thisBoard[move] != 0):
            move = priorchoice
    #print(f"bot move after checking for playerwin plan = {move+1}")
    tempmove = detectwin(thisBoard, True)
    
    if (tempmove != -1) and (thisBoard[tempmove] == 0 ):
        turnNoType = 3
        #print(f"bot sees possable win")
    
    # Check for bot win condition
    if turnNoType == 3  and difficultyNo != 0:
        priorchoice = move
        move = detectwin(thisBoard, True)
        if move == -1:
            
            move = random.choice(empty_positions)
        priorchoice = move
        if (thisBoard[move] != 0):
            move = priorchoice
    #print(f"bot move after checking for self win plan = {move+1}")

    # First move case
    if turnNo <= 2:
        if difficultyNo == 0:  # Easy bot
            priorchoice = move
            move = random.choice([1, 3, 5, 7])  # Random edge
            if (thisBoard[move-1] != 0):
                move = priorchoice
        elif difficultyNo == 1:  # Medium bot
            if (thisBoard[4] == 0):
                move = 4  # Medium bot prefers center
        elif difficultyNo == 2:  # Hard bot
            if (thisBoard[4] == 0):
                move = 4  # Hard bot always starts with center if available
    #print(f"bot move first move check for self win plan = {move+1}")
    # Increment turn number and return move
    turnNo += 1
    #change back turn no type to 2
    turnNoType = 2
    return move + 1 if move != -1 else move

def botStartup(difficulty, starting):
    global turnNoType, difficultyNo, turnNo, doomCounteronlocations
    #difficulty is one selected, turn order is firstmove and should be 1 or 2, depending on if bot is first or second:
    if (starting == 1):
        firstmove = True
    else:
        firstmove = False
    turnNoType = 0
    difficultyNo = difficulty
    turnNo = 1
    if firstmove:
        #we move first
        botMove(Stateofplayin.returnBoardState)
    else:
        #player goes first, must wait for player move
        dummy = 0
    doomCounteronlocations = [-1, -1, -1,
                              -1, -1, -1,
                              -1, -1, -1] #this is for the medium bot
    return

def detectwin(thisboardstate, isBot):

    #the boardstate is the state of play, isbot is the toggle to see if the bot is the one being checked
    #the next move can land a win in one of the spots, return the index of that pos or position that would result in a win
    player = 2 
    if isBot:
        player = 1 # Assign the marker based on who is being checked 
    #print(f"checking for {player} wins 2142")
    a = (0, 1, 2)
    b = (3, 4, 5)
    c = (6, 7, 8)
    d = (0, 3, 6)
    e = (1, 4, 7)
    f = (2, 5, 8)
    g = (0, 4, 8)
    h = (2, 4, 6)
    win_positions = [ a, b, c, # Rows 
                     d, e, f, # Columns 
                        g, h # Diagonals 
                    ]
    # Check each winning position 
    for pos in win_positions: 
        count_player = sum(thisboardstate[i] == player for i in pos) 
        count_empty = sum(thisboardstate[i] == 0 for i in pos) 
        #print(f"count for "+ str(pos)+ " countplayer: "+ str(count_player) + " empty: "+ str(count_empty) +" 2243")
        # If there are two markers of the player and one empty spot 
        if count_player == 2 and count_empty == 1: 
            for i in pos: 
                print(str(i))
                if thisboardstate[i] == 0: 
                    #print(f"found a position for victory or defeat at position {str(i+1)}")
                    return i # Return the index of the winning move 
    return -1 # Return -1 if no winning move is found
def main(): 
    global boardState, turnNo, difficultyNo, doomCounteronlocations, turnNoType
    clearBoard() 
    bot_first = False # Toggle whether the bot goes first 
    game_over = False 
    while not game_over:
        
        if bot_first: 
            boardState = returnBoardState() 
            botMoveIndex = botMove(boardState) 
            boardState = sendBotMove(botMoveIndex-1,boardState, turnNo, difficultyNo, doomCounteronlocations, turnNoType) 
            print(f"Bot moved to position: {botMoveIndex}") 
            bot_first = False 
        else: 
            boardState, turnNo, difficultyNo, doomCounteronlocations, turnNoType = listenForPlayerMove() 
            print(f"Player moved. Current board state: {boardState}") 
            bot_first = True 
            # Add logic to check for game over conditions (win/draw) 
            # # If the game is over, set game_over = True 
        print(str(boardState)) 

if __name__ == "__main__": 
    main()