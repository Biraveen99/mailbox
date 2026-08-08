import time
import requests

SERVER_URL = "http://127.0.0.1:8000"
POLL_INTERVAL = 2


def get_latest_message():
    response = requests.get(
        f"{SERVER_URL}/messages/latest"
    )

    response.raise_for_status()

    return response.json()


def acknowledge_message(message_id):
    response = requests.post(
        f"{SERVER_URL}/messages/{message_id}/ack"
    )

    response.raise_for_status()

    return response.json()


def display_message(message):
    print()
    print("=" * 50)
    print("💗 LOVE BOX 💗")
    print("=" * 50)
    print()
    print(message["title"])
    print()
    print(message["body"])
    print()
    print("=" * 50)
    print()


def run():
    print("Love Box simulator started ❤️")
    print(f"Backend: {SERVER_URL}")
    print()

    while True:
        try:
            message = get_latest_message()

            if message is not None:
                display_message(message)

                acknowledge_message(
                    message["id"]
                )

                print(
                    f"Message #{message['id']} acknowledged ✅"
                )

        except requests.RequestException as error:
            print(
                f"Could not reach backend: {error}"
            )

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    run()