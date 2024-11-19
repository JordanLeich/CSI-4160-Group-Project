"""
this should be the handler on the clouds's end of communications for bot, and possably database for milestone 4
we need to get the state of play and bot turn input, and get what the player moves are for each turn, as well as send the info to the pi regarding bot moves
bot output from file will be sent according to the following grid:
 1 | 2 | 3
---+---+---
 4 | 5 | 6
---+---+---
 7 | 8 | 9
board cell # holds X, O or E (empty)
boardstate =    [1, 2, 3, 
                 4, 5, 6, 
                 7, 8, 9]
"""
boardstate = ["E", "E", "E",
              "E", "E", "E", 
              "E", "E", "E"]
def sendBotMove(intToSend):
    #this should send the int that the bot is selecting on it's turn
    #the return should let us know the boardstate after that 
    return boardstate
def returnBoardState():
    #returns the state of the board. as of current
    return boardstate
def clearBoard():
    #clears the board
    boardstate = ["E", "E", "E", 
                  "E", "E", "E", 
                  "E", "E", "E"]
    return
