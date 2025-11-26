import tkinter as tk
from tkinter import messagebox
import random
import os

FILENAME = "randomJokes.txt"

#Load Jokes
def load_jokes():
    if not os.path.exists(FILENAME):
        messagebox.showerror("Error", f"{FILENAME} not found!")
        return []

    jokes = []
    with open(FILENAME, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if "?" in line:
                setup, punchline = line.split("?", 1)
                jokes.append((setup + "?", punchline.strip()))
    return jokes

#GUI App
class JokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa Joke Assistant")
        self.root.geometry("600x350")

        self.jokes = load_jokes()
        self.current_joke = None

        # Title Label
        self.title_label = tk.Label(
            root, text="Alexa Joke Assistant", font=("Helvetica", 20, "bold")
        )
        self.title_label.pack(pady=15)

        # Setup Label
        self.setup_label = tk.Label(
            root, text="", font=("Arial", 14), wraplength=500
        )
        self.setup_label.pack(pady=10)

        # Punchline Label
        self.punchline_label = tk.Label(
            root, text="", font=("Arial", 14, "italic"), fg="navy blue", wraplength=500
        )
        self.punchline_label.pack(pady=10)

        # Buttons Frame
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=20)

        # Buttons
        tk.Button(btn_frame, text="Alexa tell me a Joke", width=20, command=self.show_joke)\
            .grid(row=0, column=0, padx=10)

        tk.Button(btn_frame, text="Show Punchline", width=20, command=self.show_punchline)\
            .grid(row=0, column=1, padx=10)

        tk.Button(btn_frame, text="Next Joke", width=20, command=self.show_joke)\
            .grid(row=1, column=0, pady=10)

        tk.Button(btn_frame, text="Quit", width=20, command=root.quit)\
            .grid(row=1, column=1, pady=10)

    #Logic
    def show_joke(self):
        if not self.jokes:
            self.setup_label.config(text="No jokes found!")
            return

        self.current_joke = random.choice(self.jokes)
        setup, _ = self.current_joke
        self.setup_label.config(text=setup)
        self.punchline_label.config(text="")   # hide punchline

    def show_punchline(self):
        if self.current_joke:
            _, punchline = self.current_joke
            self.punchline_label.config(text=punchline)
        else:
            messagebox.showinfo("No joke", "Click 'Alexa tell me a Joke' first!")

#Run Program
if __name__ == "__main__":
    root = tk.Tk()
    app = JokeApp(root)
    root.mainloop()
