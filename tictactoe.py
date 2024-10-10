from flask import Flask, render_template, request, jsonify
from sense_hat import SenseHat
from time import sleep

app = Flask(__name__)
sense = SenseHat()

X_color = [255, 0, 0]    # Red for X player
O_color = [0, 0, 255]    # Blue for O player
empty_color = [0, 0, 0]  # Black
select_color = [0, 255, 0]  # Green

board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
current_player = 'X'
cursor = [0, 0]

def display_board():
    pixels = []
    for row in range(3):
        for col in range(3):
            if [row, col] == cursor:
                pixels.append(select_color)
            elif board[row][col] == 'X':
                pixels.append(X_color)
            elif board[row][col] == 'O':
                pixels.append(O_color)
            else:
                pixels.append(empty_color)
        pixels.extend([empty_color] * 5)
    for _ in range(5):
        pixels.extend([empty_color] * 8)
    sense.set_pixels(pixels)

def check_winner():
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != ' ':
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != ' ':
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2]
    if all(board[row][col] != ' ' for row in range(3) for col in range(3)):
        return 'Tie'
    return None

def place_marker():
    global current_player
    row, col = cursor
    if board[row][col] == ' ':
        board[row][col] = current_player
        current_player = 'O' if current_player == 'X' else 'X'

# Web routes
@app.route('/')
def index():
    return render_template('index.html', board=board, current_player=current_player)

@app.route('/move', methods=['POST'])
def move():
    direction = request.json.get('direction')
    if direction:
        move_cursor(direction)
        display_board()
    return jsonify({"status": "success"})

@app.route('/place_marker', methods=['POST'])
def place_marker_route():
    place_marker()
    winner = check_winner()
    display_board()
    if winner:
        if winner != 'Tie':
            message = "{} wins!".format(winner)
        else:
            message = "It's a tie!"
        return jsonify({"status": "game_over", "message": message})
    return jsonify({"status": "success"})

def move_cursor(direction):
    global cursor
    if direction == 'up':
        cursor[0] = (cursor[0] - 1) % 3
    elif direction == 'down':
        cursor[0] = (cursor[0] + 1) % 3
    elif direction == 'left':
        cursor[1] = (cursor[1] - 1) % 3
    elif direction == 'right':
        cursor[1] = (cursor[1] + 1) % 3

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
