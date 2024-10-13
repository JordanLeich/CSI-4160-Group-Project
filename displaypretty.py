from flask import Flask, render_template, request, jsonify
from sense_hat import SenseHat
from time import sleep
X_color = [255, 0, 0]    # Red for X player
O_color = [0, 0, 255]    # Blue for O player
empty_color = [0, 0, 0]  # Black
select_color = [0, 255, 0]  # Green
e = empty_color
X = X_color
O = O_color
s = select_color
def get_slot(input_for_slot, end_slot_bool, end_row):
    out_board = []
    outrow = []
    if(end_slot_bool and end_row): #last one in the column, and in the row.
        match(input_for_slot):
            case 'X':   #x has clamed, this spot
                outrow = [X,X]
                out_board.append(outrow)
                outrow = [X,X]
                out_board.append(outrow)
            case "S": #selection cursor is on this spot
                outrow = [s,e]
                out_board.append(outrow)
                outrow = [e,e]
                out_board.append(outrow)
            case "O": #O has clamed this spot
                outrow = [O,O]
                out_board.append(outrow)
                outrow = [O,O]
                out_board.append(outrow)
            case default: #empty slot
                outrow = [e,e]
                out_board.append(outrow)
                outrow = [e,e]
                out_board.append(outrow)
    elif(end_slot_bool and not end_row): #last one in the row, but not in the last column
        match(input_for_slot):
            case 'X':
                outrow = [X,X]
                out_board.append(outrow)
                outrow = [X,X]
                out_board.append(outrow)
                outrow = [X,X]
                out_board.append(outrow)
            case "S":
                outrow = [e,e]
                out_board.append(outrow)
                outrow = [s,e]
                out_board.append(outrow)
                outrow = [e,e]
                out_board.append(outrow)
            case "O":
                outrow = [O,O]
                out_board.append(outrow)
                outrow = [e,e]
                out_board.append(outrow)
                outrow = [O,O]
                out_board.append(outrow)
            case default:
                outrow = [e,e]
                out_board.append(outrow)
                outrow = [e,e]
                out_board.append(outrow)
                outrow = [e,e]
                out_board.append(outrow)
    elif(end_row): #bottom row, not the last one in the row
        match(input_for_slot):
            case 'X':
                outrow = [X,X,X]
                out_board.append(outrow)
                outrow = [X,X,X]
                out_board.append(outrow)
            case "S":
                outrow = [e,s,e]
                out_board.append(outrow)
                outrow = [e,e,e]
                out_board.append(outrow)
            case "O":
                outrow = [O,O,O]
                out_board.append(outrow)
                outrow = [O,O,O]
                out_board.append(outrow)
            case default:
                outrow = [e,e,e]
                out_board.append(outrow)
                outrow = [e,e,e]
                out_board.append(outrow)
    else: #this is not on the end slots
        match(input_for_slot):
            case 'X':
                outrow = [X,e,X]
                out_board.append(outrow)
                outrow = [e,X,e]
                out_board.append(outrow)
                outrow = [X,e,X]
                out_board.append(outrow)
            case "S":
                outrow = [e,e,e]
                out_board.append(outrow)
                outrow = [e,s,e]
                out_board.append(outrow)
                outrow = [e,e,e]
                out_board.append(outrow)
            case "O":
                outrow = [O,O,O]
                out_board.append(outrow)
                outrow = [O,e,O]
                out_board.append(outrow)
                outrow = [O,O,O]
                out_board.append(outrow)
            case default:
                outrow = [e,e,e]
                out_board.append(outrow)
                out_board.append(outrow)
                out_board.append(outrow)
    return out_board
def compile_lines_three(temp1_board, temp2_board, temp3_board, rownum):
    out_line = []
    toloopint = 3
    if(rownum == 2):
        toloopint = 2
    #print("this row:")
    #print(str(temp1_board))
    #print(str(temp2_board))
    #print(str(temp3_board))
    for item in range(toloopint):
        out_line.extend(temp1_board[item])
        out_line.extend(temp2_board[item])
        out_line.extend(temp3_board[item])
    return out_line

def prettydisplay(board):
    out_board = []
    temp1_board = []
    temp2_board = []
    temp3_board = []
    temp2 = 0
    #print("thisboard:")
    #print(str(board))
    for row in board:
        for temp1 in range(3):
            booltemp1 = temp2 == 2
            match(temp1):
                case 0:
                    temp1_board = get_slot(row[temp1],False,booltemp1)
                case 1:
                    temp2_board = get_slot(row[temp1],False,booltemp1)
                case 2:
                    temp3_board = get_slot(row[temp1],True,booltemp1)
                case 3:
                    print("error in display pretty code at prettydisplay, row :" + str(temp2) + ", unexpected temp1")
        out_board.extend(compile_lines_three(temp1_board, temp2_board, temp3_board,temp2))
        temp2 = temp2 + 1
    '''
    if(out_board.__len__() != 64):
        if(out_board.__len__()>64):
            temp4 = out_board.__len__()-64
            for item in range(temp4):
                out_board.pop()
        else:
            temp4 = 64-out_board.__len__()
            for item in range(temp4):
                out_board.append(e)
    '''
    return out_board

