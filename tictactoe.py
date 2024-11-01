from flask import Flask, render_template, jsonify, request
from sense_hat import SenseHat
from displaypretty import prettydisplay
import random

app = Flask(__name__)
sense = SenseHat()

# Define colors
X_color = [255, 0, 0]    # Red for X player
O_color = [0, 0, 255]    # Blue for O player
empty_color = [0, 0, 0]  # Black for empty cells
select_color = [0, 255, 0]  # Green for selected cell

# Initial game state
board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
current_player = 'X'
cursor = [0, 0]

# Game statistics
stats = {
    "X_wins": 0,
    "O_wins": 0,
    "AI_wins": 0,
    "ties": 0,
    "games_played": 0
}

def reset_game():
    global board, current_player, cursor
    board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    current_player = 'X'
    cursor = [0, 0]
    display_board()

@app.route('/reset_game', methods=['POST'])
def reset_game_route():
    reset_game()
    return jsonify({"status": "game_reset", "message": "Board has been reset"})

def display_board():
    temp_board = []
    for row in range(3):
        temp_board2 = []
        for col in range(3):
            if [row, col] == cursor:
                temp_board2.append("S")
            elif board[row][col] == 'X':
                temp_board2.append("X")
            elif board[row][col] == 'O':
                temp_board2.append("O")
            else:
                temp_board2.append("E")
        temp_board.append(temp_board2)
    pixels = prettydisplay(temp_board)
    sense.set_pixels(pixels)

def cpu_move():
    empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] == ' ']
    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = 'O'  
        display_board()

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

@app.route('/move', methods=['POST'])
def move_cursor():
    global cursor
    data = request.get_json()
    direction = data['direction']

    if direction == 'up':
        cursor[0] = (cursor[0] - 1) % 3
    elif direction == 'down':
        cursor[0] = (cursor[0] + 1) % 3
    elif direction == 'left':
        cursor[1] = (cursor[1] - 1) % 3
    elif direction == 'right':
        cursor[1] = (cursor[1] + 1) % 3

    display_board()
    return jsonify({"status": "success"})

@app.route('/place_marker', methods=['POST'])
def place_marker_route():
    global current_player
    row, col = cursor

    if board[row][col] == ' ' and current_player == 'X':
        board[row][col] = current_player
        display_board()

        winner = check_winner()
        if winner:
            if winner == 'X':
                stats['X_wins'] += 1
            elif winner == 'O':
                stats['O_wins'] += 1
            else:
                stats['ties'] += 1

            stats['games_played'] += 1
            return jsonify({"status": "game_over", "message": f"{winner} wins!" if winner != 'Tie' else "It's a tie", "stats": stats})

        current_player = 'O'
        cpu_move()
        display_board()

        winner = check_winner()
        if winner:
            if winner == 'O':
                stats['AI_wins'] += 1
            elif winner == 'X':
                stats['X_wins'] += 1
            else:
                stats['ties'] += 1

            stats['games_played'] += 1
            return jsonify({"status": "game_over", "message": f"{winner} wins!" if winner != 'Tie' else "It's a tie", "stats": stats})

        current_player = 'X'

    return jsonify({"status": "success"})

@app.route('/reset_stats', methods=['POST'])
def reset_stats():
    stats['X_wins'] = 0
    stats['O_wins'] = 0
    stats['ties'] = 0
    stats['games_played'] = 0
    return jsonify({"status": "success", "stats": stats})

@app.route('/')
def index():
    return render_template('index.html', board=board, current_player=current_player, stats=stats)

if __name__ == '__main__':
    reset_game()
    app.run(host='0.0.0.0', port=5000)
