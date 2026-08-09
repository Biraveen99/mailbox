import os
import tkinter as tk

import requests


API_URL = os.getenv("LOVEBOX_API_URL", "http://127.0.0.1:8000").rstrip("/")
DEVICE_ID = os.getenv("LOVEBOX_DEVICE_ID", "LB-000001")
POLL_INTERVAL_MS = 2000
REQUEST_TIMEOUT_SECONDS = 5


class LoveBoxDisplay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"Love Box Simulator · {DEVICE_ID}")
        self.root.geometry("700x450")
        self.root.configure(bg="#f48fb1")

        self.current_message_id = None

        self.container = tk.Frame(
            self.root,
            bg="#f48fb1",
            padx=35,
            pady=35,
        )
        self.container.pack(fill="both", expand=True)

        self.screen = tk.Frame(
            self.container,
            bg="#1a1118",
            highlightbackground="#5b2a42",
            highlightthickness=8,
        )
        self.screen.pack(fill="both", expand=True)

        self.heart_label = tk.Label(
            self.screen,
            text="💗  💕  💖",
            font=("Arial", 28),
            fg="#ff7eb6",
            bg="#1a1118",
        )
        self.heart_label.pack(pady=(35, 20))

        self.title_label = tk.Label(
            self.screen,
            text="Love Box ❤️",
            font=("Arial", 30, "bold"),
            fg="#ff9fc8",
            bg="#1a1118",
        )
        self.title_label.pack(pady=(10, 20))

        self.body_label = tk.Label(
            self.screen,
            text="Venter på en melding...",
            font=("Arial", 20),
            fg="#fff0f6",
            bg="#1a1118",
            wraplength=520,
            justify="center",
        )
        self.body_label.pack(padx=40, pady=20)

        self.status_label = tk.Label(
            self.screen,
            text="● Connecting...",
            font=("Arial", 12),
            fg="#fff0f6",
            bg="#1a1118",
        )
        self.status_label.pack(side="bottom", pady=20)

    @property
    def messages_url(self):
        return f"{API_URL}/devices/{DEVICE_ID}/messages"

    def show_message(self, message):
        self.current_message_id = message["id"]
        self.title_label.config(text=message["title"])
        self.body_label.config(text=message["body"])

    def poll_messages(self):
        try:
            response = requests.get(
                f"{self.messages_url}/latest",
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()

            message = response.json()
            self.status_label.config(text=f"● Connected · {DEVICE_ID}")

            if message and message["id"] != self.current_message_id:
                self.show_message(message)
        except requests.RequestException as error:
            self.status_label.config(text="● Offline · retrying...")
            print(f"LoveBox API error: {error}")

        self.root.after(POLL_INTERVAL_MS, self.poll_messages)

    def run(self):
        self.root.after(100, self.poll_messages)
        self.root.mainloop()


if __name__ == "__main__":
    LoveBoxDisplay().run()
