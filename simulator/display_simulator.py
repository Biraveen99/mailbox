import tkinter as tk


class LoveBoxDisplay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Love Box Simulator")
        self.root.geometry("700x450")
        self.root.configure(bg="#f48fb1")

        self.container = tk.Frame(
            self.root,
            bg="#f48fb1",
            padx=35,
            pady=35,
        )
        self.container.pack(
            fill="both",
            expand=True,
        )

        self.screen = tk.Frame(
            self.container,
            bg="#1a1118",
            highlightbackground="#5b2a42",
            highlightthickness=8,
        )
        self.screen.pack(
            fill="both",
            expand=True,
        )

        self.heart_label = tk.Label(
            self.screen,
            text="💗  💕  💖",
            font=("Arial", 28),
            fg="#ff7eb6",
            bg="#1a1118",
        )
        self.heart_label.pack(
            pady=(35, 20)
        )

        self.title_label = tk.Label(
            self.screen,
            text="Love Box ❤️",
            font=("Arial", 30, "bold"),
            fg="#ff9fc8",
            bg="#1a1118",
        )
        self.title_label.pack(
            pady=(10, 20)
        )

        self.body_label = tk.Label(
            self.screen,
            text="Venter på en melding...",
            font=("Arial", 20),
            fg="#fff0f6",
            bg="#1a1118",
            wraplength=520,
            justify="center",
        )
        self.body_label.pack(
            padx=40,
            pady=20,
        )

        self.status_label = tk.Label(
            self.screen,
            text="● Connected",
            font=("Arial", 12),
            fg="#a7f3d0",
            bg="#1a1118",
        )
        self.status_label.pack(
            side="bottom",
            pady=20,
        )

    def show_message(self, title, body):
        self.title_label.config(text=title)
        self.body_label.config(text=body)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    display = LoveBoxDisplay()

    display.show_message(
        "Hei ❤️",
        "Dette er første melding på den virtuelle Love Box-skjermen.",
    )

    display.run()