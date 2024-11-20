                                                    
from flask import Flask, request, jsonify
from botfile import botMove  # Import the botMove function from your bot script

app = Flask(__name__)

@app.route('/get_bot_move', methods=['POST'])
def get_bot_move():
    data = request.get_json()
    board_state = data['board_state']
    difficulty = data['difficulty']
    
    # Set the difficulty level in the bot script
    bot.difficultyNo = difficulty

    # Compute the bot's move
    move_index = botMove(board_state) - 1  # Adjust to 0-based index
    return jsonify({"bot_move": move_index})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)





























