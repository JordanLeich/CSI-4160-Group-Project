import Stateofplayin
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
 h a   b   c d
   1 | 2 | 3 e
  ---+---+---
   4 | 5 | 6 f
  ---+---+---
   7 | 8 | 9 g
a is 147, e is 123,d is 375, h is 159, for example
'''
def detectWinConditions(boolSelf):
    #boolself is true if checking for chances for self to win and false for opponent checking, this should return a tuplet of the possable win locatons, and return it
    winConLocations = []
    return winConLocations

def setupBoardStateNumbers(boardstate, boolSelfX):
    #if boolSelfX is true, we are x else we are 0
    thisboard = [0,0,0,
                 0,0,0,
                 0,0,0,]
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

turnNoType= 0 #this is a selector for what type of turn this is
difficultyNo = 0 # 0 is easy, 1 is medium, 2 is hard
turnNo= 0 #this checks the BOT's move counter
firstmove = False #this is to check if we(the bot) get the first move
def botMove(boardState):
    #see above  comment as string to get what is going on here 
    thisBoard = setupBoardStateNumbers(boardstate=boardState, boolSelfX=firstmove)

    match difficultyNo:
        case 0:
            match turnNoType:
                case 0:

                case default:
        case 1:
            match turnNoType:
                case 0:

                case default:

        case 2:
            match turnNoType:
                case 0:

                case default:

        case default:
            #throw error
            print ("failure to set difficultyNo")
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
    return
def detectwin(thisboardstate, isBot):
    #the boardstate is the state of play, isbot checks to see if the bot is the one being checked