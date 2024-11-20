from google.cloud import pubsub_v1
import json
import serverfiles.Stateofplayin

# Set GCP Project ID and topic
PROJECT_ID = "class-project-442120"
TOPIC_ID = "tic-tac-toe"
SUBSCRIPTION_ID = "pi-subscriber"

def publish_message(topic_id, message):
    """Publishes a message to a Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, topic_id)

    # Convert message to JSON
    message_data = json.dumps(message).encode("utf-8")
    future = publisher.publish(topic_path, message_data)
    print(f"Published message ID: {future.result()}")

def listen_for_messages():
    """Listens for messages on a Pub/Sub subscription."""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

    def callback(message):
        try:
            print(f"Received message: {message.data}")
            data = json.loads(message.data.decode("utf-8"))
            
            if "playerMove" in data:
                player_move = data["playerMove"]
                Stateofplayin.listenForPlayerMove()
                print(f"Player moved at index: {player_move}")
                board_state = Stateofplayin.returnBoardState()
                publish_message(TOPIC_ID, {"boardState": board_state})
            elif "botMove" in data:
                bot_move = data["botMove"]
                Stateofplayin.sendBotMove(bot_move)
                print(f"Bot moved at index: {bot_move}")
                publish_message(TOPIC_ID, {"status": "Bot move processed"})
            elif "clearBoard" in data:
                Stateofplayin.clearBoard()
                print("Board cleared.")
                publish_message(TOPIC_ID, {"status": "Board cleared"})
            else:
                print("Unknown command received.")
                publish_message(TOPIC_ID, {"error": "Unknown command"})
            message.ack()
        except Exception as e:
            print(f"Error handling message: {e}")
            message.nack()
            
    subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {SUBSCRIPTION_ID}...")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Stopped listening for messages.")

if __name__ == "__main__":
    listen_for_messages()
