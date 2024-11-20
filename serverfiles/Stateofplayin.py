import socket
import json

boardstate = ["E"] * 9

def sendBotMove(intToSend):
    global boardstate
    boardstate[intToSend] = "O"
    HOST = "RPI_IP"  # Replace with the Pi's IP address
    PORT = 65432
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(json.dumps({"botMove": intToSend}).encode())
    return boardstate

def returnBoardState():
    global boardstate
    return boardstate

def clearBoard():
    global boardstate
    boardstate = ["E"] * 9

def listenForPlayerMove():
    # Assuming Pi sends JSON containing {"playerMove": index}
    HOST = "0.0.0.0"  # Listen on all available interfaces
    PORT = 65432       # Arbitrary port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Waiting for player move...")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            data = conn.recv(1024)
            if data:
                move = json.loads(data.decode())["playerMove"]
                boardstate[move] = "X"
                return boardstate
