import Stateofplayin
import random
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
def detectwin(thisboardstate, isBot):
    #the boardstate is the state of play, isbot is the toggle to see if the bot is the one being checked
    #the next move can land a win in one of the spots, return the index of that pos or position that would result in a win
    player = 1 if isBot else 2 # Assign the marker based on who is being checked 
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
        
        # If there are two markers of the player and one empty spot 
        if count_player == 2 and count_empty == 1: 
            for i in pos: 
                if thisboardstate[i] == 0: 
                    return i # Return the index of the winning move 
        return -1 # Return -1 if no winning move is found

def setupBoardStateNumbers(boardstate, boolSelfX):
    #if boolSelfX is true, we are x else we are 0
    thisboard = [0,0,0,
                 0,0,0,
                 0,0,0]
    #bot is 1, 2 is player
    if boolSelfX:
        for no in range(1,9):
            match boardstate[no]:
                case "X":
                    thisboard[no] = 1
                case "O":
                    thisboard[no] = 2
                case defualt:
                    #empty, we dont need to do something
                    thisboard[no] = 0
    else:
        match boardstate[no]:
                case "X":
                    thisboard[no] = 2
                case "O":
                    thisboard[no] = 1
                case defualt:
                    #empty, we dont need to do something
                    thisboard[no] = 0
    return thisboard

    #this is to determine whether the turn type is 
doomCounteronlocations = [-1, -1, -1,
                          -1, -1, -1,
                          -1, -1, -1] #this is for the medium bot
turnNoType= 0 #this is a selector for what type of turn this is
difficultyNo = 0 # 0 is easy, 1 is medium, 2 is hard
turnNo= 0 #this checks the BOT's move counter
firstmove = False #this is to check if we(the bot) get the first move

def botMove(boardState):
    global turnNo, turnNoType, difficultyNo, firstmove
    thisBoard = setupBoardStateNumbers(boardState, firstmove)
    empty_positions = [i for i, val in enumerate(thisBoard) if val == 0]
    move = -1
    
    match turnNoType:
        case 0:
            if difficultyNo in [0, 1]:  # Easy and Medium
                move = random.choice([i for i in [1, 3, 5, 7] if i in empty_positions])
            elif difficultyNo == 2:  # Hard
                move = 4 if 4 in empty_positions else random.choice(empty_positions)
        
        case 1:
            player_move = next((i for i, val in enumerate(thisBoard) if val == 2), None)
            adjacent_moves = {
                0: [1, 3], 1: [0, 2, 4], 2: [1, 5],
                3: [0, 4, 6], 4: [], 5: [2, 4, 8],
                6: [3, 7], 7: [6, 8, 4], 8: [5, 7]
            }

            match difficultyNo:
                case 0:  # Easy
                    move = next((m for m in adjacent_moves[player_move] if m in [1, 3, 5, 7] and m in empty_positions), 
                                random.choice([i for i in [1, 3, 5, 7] if i in empty_positions]))
                    if player_move == 4:
                        move = botMove(boardState)
                
                case 1:  # Medium
                    move = next((m for m in adjacent_moves[player_move] if m in [1, 3, 5, 7] and m in empty_positions), 
                                random.choice([i for i in [1, 3, 5, 7] if i in empty_positions]))
                    if player_move == 4:
                        move = botMove(boardState)
                
                case 2:  # Hard
                    move = 4 if 4 in empty_positions else random.choice([i for i in [0, 2, 6, 8] if i in empty_positions])
        
        case 3:
            # Logic for bot's win conditions
            match difficultyNo:
                case 0:  # Easy avoids win condition
                    move = random.choice(empty_positions)
                case 1:  # Medium logic
                    # Implement medium logic
                    pass
                case 2:  # Hard will play win
                    # Implement hard logic
                    pass

        case 4:
            # Logic for player's win condition
            match difficultyNo:
                case 1 | 2:  # Medium and Hard will block win
                    # Implement blocking logic
                    pass
                case 0:  # Easy avoids blocking win unless necessary
                    move = random.choice(empty_positions)
        
        case 2:
            match difficultyNo:
                case 0:  # Easy follows simple priority
                    priorities = [1, 3, 5, 7] + [0, 2, 6, 8] + [4]
                case 1:  # Medium follows random edges, then corners, then center
                    priorities = random.sample([1, 3, 5, 7], 4) + random.sample([0, 2, 6, 8], 4) + [4]
                case 2:  # Hard follows specific strategy
                    priorities = random.sample([0, 2, 6, 8], 4) + random.sample([1, 3, 5, 7], 4) + [4]
            
            for pos in priorities:
                if pos in empty_positions:
                    move = pos
                    break

    return move + 1 if move != -1 else move

def botStartup(difficulty, starting):
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
    player = 1 if isBot else 2 # Assign the marker based on who is being checked 
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
        
        # If there are two markers of the player and one empty spot 
        if count_player == 2 and count_empty == 1: 
            for i in pos: 
                if thisboardstate[i] == 0: 
                    return i # Return the index of the winning move 
        return -1 # Return -1 if no winning move is found