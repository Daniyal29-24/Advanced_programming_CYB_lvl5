import tkinter as tk
from tkinter import messagebox
import random

class MathsQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Maths Quiz")
        self.root.geometry("550x450")
        self.root.resizable(False, False)

        # THEME COLORS
        self.bg_color = "#f4f7fb"
        self.fg_color = "#1c1c1c"
        self.accent_color = "#4a90e2"
        self.button_color = "#e1e9f5"
        self.button_hover = "#d0d9e8"

        self.root.configure(bg=self.bg_color)

        # Quiz variables
        self.difficulty = None
        self.score = 0
        self.current_question = 0
        self.total_questions = 10
        self.current_attempt = 1
        self.num1 = 0
        self.num2 = 0
        self.operation = ''
        self.correct_answer = 0

        # Main frame
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        self.displayMenu()

    def styled_button(self, parent, text, command):
        """Theme button with hover effect."""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=('Segoe UI', 12, 'bold'),
            bg=self.button_color,
            fg=self.fg_color,
            activeforeground=self.fg_color,
            relief="flat",
            width=25,
            height=2
        )
        # Hover events
        btn.bind("<Enter>", lambda e: btn.config(bg=self.button_hover))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.button_color))
        return btn

    def displayMenu(self):
        self.clearFrame()

        title_label = tk.Label(
            self.main_frame,
            text="MATHS QUIZ",
            font=('Segoe UI', 22, 'bold'),
            bg=self.bg_color,
            fg=self.accent_color
        )
        title_label.pack(pady=20)

        subtitle_label = tk.Label(
            self.main_frame,
            text="Select Difficulty Level",
            font=('Segoe UI', 14, 'bold'),
            bg=self.bg_color,
            fg=self.fg_color
        )
        subtitle_label.pack(pady=10)

        self.styled_button(self.main_frame,
            "1. Easy (Single-digit numbers)",
            lambda: self.startQuiz("easy")
        ).pack(pady=8)

        self.styled_button(self.main_frame,
            "2. Moderate (Double-digit numbers)",
            lambda: self.startQuiz("moderate")
        ).pack(pady=8)

        self.styled_button(self.main_frame,
            "3. Advanced (4-digit numbers)",
            lambda: self.startQuiz("advanced")
        ).pack(pady=8)

    def randomInt(self, difficulty):
        if difficulty == "easy":
            return random.randint(0, 9)
        elif difficulty == "moderate":
            return random.randint(10, 99)
        else:
            return random.randint(1000, 9999)

    def decideOperation(self):
        return random.choice(['+', '-'])

    def generateQuestion(self):
        self.num1 = self.randomInt(self.difficulty)
        self.num2 = self.randomInt(self.difficulty)
        self.operation = self.decideOperation()

        if self.operation == '+':
            self.correct_answer = self.num1 + self.num2
        else:
            self.correct_answer = self.num1 - self.num2

        self.current_attempt = 1

    def displayProblem(self):
        self.clearFrame()

        progress_label = tk.Label(
            self.main_frame,
            text=f"Question {self.current_question + 1} of {self.total_questions}",
            font=('Segoe UI', 12, 'bold'),
            bg=self.bg_color,
            fg=self.fg_color
        )
        progress_label.pack(pady=5)

        score_label = tk.Label(
            self.main_frame,
            text=f"Current Score: {self.score}",
            font=('Segoe UI', 12),
            bg=self.bg_color,
            fg=self.fg_color
        )
        score_label.pack(pady=5)

        question = f"{self.num1} {self.operation} {self.num2} = ?"
        question_label = tk.Label(
            self.main_frame,
            text=question,
            font=('Segoe UI', 20, 'bold'),
            bg=self.bg_color,
            fg=self.accent_color
        )
        question_label.pack(pady=20)

        self.answer_var = tk.StringVar()
        answer_entry = tk.Entry(
            self.main_frame,
            textvariable=self.answer_var,
            font=('Segoe UI', 16),
            width=10,
            justify='center',
            relief="solid",
            bd=1
        )
        answer_entry.pack(pady=10)
        answer_entry.focus()

        submit_btn = self.styled_button(
            self.main_frame,
            "Submit Answer",
            self.checkAnswer
        )
        submit_btn.pack(pady=10)

        # prevent multiple bindings
        self.root.unbind("<Return>")
        self.root.bind("<Return>", lambda event: self.checkAnswer())

    def isCorrect(self, user_answer):
        try:
            return int(user_answer) == self.correct_answer
        except ValueError:
            return False

    def checkAnswer(self):
        user_answer = self.answer_var.get().strip()

        if not user_answer:
            messagebox.showwarning("Input Error", "Please enter an answer!")
            return

        if self.isCorrect(user_answer):
            points = 10 if self.current_attempt == 1 else 5
            self.score += points
            messagebox.showinfo("Correct!", f"Excellent! You earned {points} points!")
            self.nextQuestion()
        else:
            self.current_attempt += 1
            if self.current_attempt <= 2:
                messagebox.showerror("Incorrect",
                                     f"Wrong answer! Try again. Attempt {self.current_attempt}/2")
                self.answer_var.set("")
            else:
                messagebox.showerror("Incorrect",
                                     f"Wrong answer! The correct answer was {self.correct_answer}")
                self.nextQuestion()

    def nextQuestion(self):
        self.current_question += 1
        if self.current_question < self.total_questions:
            self.generateQuestion()
            self.displayProblem()
        else:
            self.displayResults()

    def displayResults(self):
        self.clearFrame()

        percentage = (self.score / 100) * 100

        if percentage >= 90:
            grade, message = "A+", "Outstanding! 🎉"
        elif percentage >= 80:
            grade, message = "A", "Excellent! 👍"
        elif percentage >= 70:
            grade, message = "B", "Good job! 😊"
        elif percentage >= 60:
            grade, message = "C", "Well done! 🙂"
        elif percentage >= 50:
            grade, message = "D", "You passed! 👏"
        else:
            grade, message = "F", "Keep practicing! 💪"

        title_label = tk.Label(
            self.main_frame,
            text="QUIZ COMPLETE!",
            font=('Segoe UI', 22, 'bold'),
            bg=self.bg_color,
            fg=self.accent_color
        )
        title_label.pack(pady=20)

        score_label = tk.Label(
            self.main_frame,
            text=f"Final Score: {self.score}/100",
            font=('Segoe UI', 16),
            bg=self.bg_color,
            fg=self.fg_color
        )
        score_label.pack(pady=10)

        grade_label = tk.Label(
            self.main_frame,
            text=f"Grade: {grade}",
            font=('Segoe UI', 16, 'bold'),
            bg=self.bg_color,
            fg=self.fg_color
        )
        grade_label.pack(pady=10)

        message_label = tk.Label(
            self.main_frame,
            text=message,
            font=('Segoe UI', 14),
            bg=self.bg_color,
            fg=self.fg_color
        )
        message_label.pack(pady=10)

        self.styled_button(self.main_frame, "Play Again", self.restartQuiz).pack(pady=10)
        self.styled_button(self.main_frame, "Quit", self.root.quit).pack(pady=5)

    def startQuiz(self, difficulty):
        self.difficulty = difficulty
        self.score = 0
        self.current_question = 0
        self.generateQuestion()
        self.displayProblem()

    def restartQuiz(self):
        self.difficulty = None
        self.score = 0
        self.current_question = 0
        self.displayMenu()

    def clearFrame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()


def main():
    root = tk.Tk()
    app = MathsQuiz(root)
    root.mainloop()

if __name__ == "__main__":
    main()
