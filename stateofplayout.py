import json
import logging
from google.cloud import storage
from google.oauth2 import service_account
doomCnt = [-1, -1, -1,
                          -1, -1, -1,
                          -1, -1, -1]
turnType = 2 #because bot never goes first
# Set up logging for debugging
logging.basicConfig(level=logging.INFO)

# Path to your service account key file for Google Cloud Storage
KEY_PATH = "/home/jordan/Downloads/CSI-4160-Group-Project-main/key.json"  # Replace with your actual path

# The name of the Google Cloud Storage bucket
BUCKET_NAME = "my-game-board-state-bucket"  # Replace with your actual bucket name

# File name in the bucket where the game state is stored
GAME_STATE_FILE = "game_state.json"

# Initialize Google Cloud Storage client with credentials
def initialize_storage_client():
    credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
    client = storage.Client(credentials=credentials, project=credentials.project_id)
    return client

# Function to upload the current board state to Google Cloud Storage
def upload_board_state(board_state, turnCounter, bottype):
    global doomCnt, turnType
    client = initialize_storage_client()
    bucket = client.get_bucket(BUCKET_NAME)
    blob = bucket.blob(GAME_STATE_FILE)

    # Prepare the board state data to upload
    board_data = json.dumps({"boardState": board_state,
                             "turnCounter": turnCounter,
                             "difficulty": bottype,
                              "damiclies":doomCnt,
                              "turnstile": turnType})

    # Upload the data to the bucket
    blob.upload_from_string(board_data)
    logging.info("Board state uploaded successfully.")

# Function to download the board state from Google Cloud Storage
def download_board_state():
    global doomCnt, turnType
    client = initialize_storage_client()
    bucket = client.get_bucket(BUCKET_NAME)
    blob = bucket.blob(GAME_STATE_FILE)

    try:
        # Download the data from the bucket
        board_data = blob.download_as_text()
        board_state = json.loads(board_data)["boardState"]
        turnCount = json.loads(board_data)["turnCounter"]
        doomCnt = json.loads(board_data)["damiclies"]
        turnType = json.loads(board_data)["turnstile"]
        logging.info("Board state downloaded successfully.")
        return board_state, turnCount
    except Exception as e:
        logging.error(f"Error downloading board state: {e}")
        return None

# Function to send the updated board state to Google Cloud Storage
def send_updated_board_state(board_state):
    logging.info("Sending updated board state to Google Cloud Storage.")
    upload_board_state(board_state)

# Function to handle the communication process
def handle_game_state(board_state):
    # Save the updated board state to GCS
    send_updated_board_state(board_state)

    # Get the current board state from GCS
    current_board_state = download_board_state()
    if current_board_state is not None:
        logging.info(f"Current board state: {current_board_state}")
    else:
        logging.warning("Failed to retrieve current board state.")
    
    return current_board_state

# Main logic for handling incoming and outgoing game state
if __name__ == "__main__":
    # Example: Assume 'board_state' is coming from your game logic
    # Initialize a board state with some example values
    board_state = ["X", "O", "E", "E", "X", "E", "O", "E", "E"]

    # Handle the game state: save and retrieve from Google Cloud Storage
    handle_game_state(board_state)
