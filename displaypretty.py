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
                outrow = [e,e,e]
                out_board.append(outrow)
    return out_board
def compile_lines_three(temp1_board, temp2_board, temp3_board):
    out_line = []
    int_temp1 = 0
    for item in temp1_board:
        out_line.extend(item)
        out_line.extend(temp2_board[int_temp1])
        out_line.extend(temp3_board[int_temp1])
        int_temp1 = int_temp1 + 1
    return out_line

def prettydisplay(board):
    out_board = []
    temp1_board = []
    temp2_board = []
    temp3_board = []
    temp1 = 0
    temp2 = 0
    for row in board:
        for col in row:
            booltemp1 = temp2 == 2
            match(temp1):
                case 0:
                    temp1_board = get_slot(col,False,booltemp1)
                case 1:
                    temp1_board = get_slot(col,False,booltemp1)
                case 2:
                    temp1_board = get_slot(col,True,booltemp1)
                case 3:
                    print("error in display pretty code at prettydisplay, row :" + temp2 + ", unexpected temp1 value."  )
            temp1 = temp1 + 1
        out_board.extend(compile_lines_three(temp1_board, temp2_board, temp3_board))
        temp2 = temp2 + 1
    return out_board
