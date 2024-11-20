from google.cloud import pubsub_v1
import json
import logging
from botfile import botMove

# Set GCP Project ID and topic
PROJECT_ID = "class-project-442120"
SUBSCRIPTION_ID = "player-moves"
RESPONSE_TOPIC_ID = "bot-moves"

# Initialize Pub/Sub clients
subscriber = pubsub_v1.SubscriberClient()
publisher = pubsub_v1.PublisherClient()
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
response_topic_path = publisher.topic_path(PROJECT_ID, RESPONSE_TOPIC_ID)

# Initialize logging
logging.basicConfig(level=logging.INFO)

def publish_bot_move(bot_move_index):
    """Publishes the bot's move to a Pub/Sub topic."""
    message_data = {"bot_move": bot_move_index}
    message_json = json.dumps(message_data).encode("utf-8")
    future = publisher.publish(response_topic_path, data=message_json)
    logging.info(f"Published bot move message ID: {future.result()}")

def listen_for_messages():
    """Listens for messages on a Pub/Sub subscription."""
    def callback(message):
        try:
            logging.info(f"Received message: {message.data}")
            data = json.loads(message.data.decode("utf-8"))
            board_state = data["board_state"]
            difficulty = data["difficulty"]

            # Set the difficulty level
            bot.difficultyNo = difficulty

            # Compute the bot's move
            bot_move_index = botMove(board_state) - 1  # Adjust to 0-based index
            publish_bot_move(bot_move_index)

            message.ack()
        except Exception as e:
            logging.error(f"Error handling message: {e}")
            message.nack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    logging.info(f"Listening for messages on {subscription_path}...")

    try:
        streaming_pull_future.result(timeout=60)  # Adjust timeout as necessary
    except TimeoutError:
        streaming_pull_future.cancel()
        logging.error("Listening stopped due to timeout.")

if __name__ == "__main__":
    listen_for_messages()
