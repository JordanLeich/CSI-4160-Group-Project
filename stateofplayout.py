import socket
import json
import Stateofplayin

HOST = "0.0.0.0"  # Listen on all available interfaces
PORT = 65432      # Port to listen on

def handle_bot_communication():
    """
    Handles incoming requests from the bot, updates the board state, and responds to player moves.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server listening on {HOST}:{PORT}...")
        while True:
            conn, addr = server_socket.accept()
            print(f"Connection established with {addr}")
            with conn:
                try:
                    data = conn.recv(1024) # Receive the incoming JSON data
                    if not data:
                        break
                    message = json.loads(data.decode())
                    print(f"Received message: {message}")
                    # Process the message based on its type
                    if "playerMove" in message:
                        player_move = message["playerMove"]
                        Stateofplayin.listenForPlayerMove()  # Update the board state
                        print(f"Player moved at index: {player_move}")
                        # Respond with the updated board state
                        board_state = Stateofplayin.returnBoardState()
                        response = {"boardState": board_state}
                        conn.sendall(json.dumps(response).encode())
                    elif "botMove" in message:
                        bot_move = message["botMove"]
                        Stateofplayin.sendBotMove(bot_move)  # Update the board state
                        print(f"Bot moved at index: {bot_move}")
                        response = {"status": "Bot move processed"}
                        conn.sendall(json.dumps(response).encode())
                    elif "clearBoard" in message:
                        Stateofplayin.clearBoard()
                        print("Board cleared.")
                        response = {"status": "Board cleared"}
                        conn.sendall(json.dumps(response).encode())
                    else:
                        print("Unknown command received.")
                        response = {"error": "Unknown command"}
                        conn.sendall(json.dumps(response).encode())
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    conn.sendall(json.dumps({"error": "Invalid JSON format"}).encode())
                except Exception as e:
                    print(f"Error: {e}")
                    conn.sendall(json.dumps({"error": str(e)}).encode())

if __name__ == "__main__":
    handle_bot_communication()
