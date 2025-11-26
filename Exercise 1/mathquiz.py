import tkinter as tk
from tkinter import messagebox
import random

class MathsQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Maths Quiz")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
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
        
        # Create main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        self.displayMenu()
    
    def displayMenu(self):
        """Display the difficulty level menu at the beginning"""
        self.clearFrame()
        
        title_label = tk.Label(self.main_frame, text="MATHS QUIZ", 
                              font=('Arial', 18, 'bold'))
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(self.main_frame, text="DIFFICULTY LEVEL",
                                 font=('Arial', 14, 'bold'))
        subtitle_label.pack(pady=10)
        
        # Difficulty buttons
        easy_btn = tk.Button(self.main_frame, text="1. Easy (Single-digit numbers)", 
                            font=('Arial', 12), width=25, height=2,
                            command=lambda: self.startQuiz("easy"))
        easy_btn.pack(pady=5)
        
        moderate_btn = tk.Button(self.main_frame, text="2. Moderate (Double-digit numbers)", 
                                font=('Arial', 12), width=25, height=2,
                                command=lambda: self.startQuiz("moderate"))
        moderate_btn.pack(pady=5)
        
        advanced_btn = tk.Button(self.main_frame, text="3. Advanced (4-digit numbers)", 
                                font=('Arial', 12), width=25, height=2,
                                command=lambda: self.startQuiz("advanced"))
        advanced_btn.pack(pady=5)
    
    def randomInt(self, difficulty):
        """Generate random numbers based on difficulty level"""
        if difficulty == "easy":
            return random.randint(0, 9)
        elif difficulty == "moderate":
            return random.randint(10, 99)
        else:  # advanced
            return random.randint(1000, 9999)
    
    def decideOperation(self):
        """Randomly decide whether it's addition or subtraction"""
        return random.choice(['+', '-'])
    
    def generateQuestion(self):
        """Generate a new question"""
        self.num1 = self.randomInt(self.difficulty)
        self.num2 = self.randomInt(self.difficulty)
        self.operation = self.decideOperation()
        
        # Calculate correct answer
        if self.operation == '+':
            self.correct_answer = self.num1 + self.num2
        else:  # subtraction
            self.correct_answer = self.num1 - self.num2
        
        self.current_attempt = 1
    
    def displayProblem(self):
        """Display the current problem and accept answer"""
        self.clearFrame()
        
        # Progress indicator
        progress_label = tk.Label(self.main_frame, 
                                 text=f"Question {self.current_question + 1} of {self.total_questions}",
                                 font=('Arial', 12))
        progress_label.pack(pady=5)
        
        # Score display
        score_label = tk.Label(self.main_frame, 
                              text=f"Current Score: {self.score}",
                              font=('Arial', 12))
        score_label.pack(pady=5)
        
        # Question display
        question_text = f"{self.num1} {self.operation} {self.num2} = ?"
        question_label = tk.Label(self.main_frame, text=question_text,
                                 font=('Arial', 16, 'bold'))
        question_label.pack(pady=20)
        
        # Answer entry
        self.answer_var = tk.StringVar()
        answer_entry = tk.Entry(self.main_frame, textvariable=self.answer_var,
                               font=('Arial', 14), width=10, justify='center')
        answer_entry.pack(pady=10)
        answer_entry.focus()
        
        # Submit button
        submit_btn = tk.Button(self.main_frame, text="Submit Answer",
                              font=('Arial', 12), command=self.checkAnswer)
        submit_btn.pack(pady=10)
        
        # Bind Enter key to submit
        self.root.bind('<Return>', lambda event: self.checkAnswer())
    
    def isCorrect(self, user_answer):
        """Check if the user's answer is correct"""
        try:
            return int(user_answer) == self.correct_answer
        except ValueError:
            return False
    
    def checkAnswer(self):
        """Check the user's answer and provide feedback"""
        user_answer = self.answer_var.get().strip()
        
        if not user_answer:
            messagebox.showwarning("Input Error", "Please enter an answer!")
            return
        
        if self.isCorrect(user_answer):
            # Award points based on attempt
            points = 10 if self.current_attempt == 1 else 5
            self.score += points
            
            messagebox.showinfo("Correct!", 
                              f"Excellent! You earned {points} points!")
            self.nextQuestion()
        else:
            self.current_attempt += 1
            if self.current_attempt <= 2:
                messagebox.showerror("Incorrect", 
                                   f"Wrong answer! Try again. Attempt {self.current_attempt}/2")
                self.answer_var.set("")  # Clear the entry for retry
            else:
                messagebox.showerror("Incorrect", 
                                   f"Wrong answer! The correct answer was {self.correct_answer}")
                self.nextQuestion()
    
    def nextQuestion(self):
        """Move to the next question or end quiz"""
        self.current_question += 1
        if self.current_question < self.total_questions:
            self.generateQuestion()
            self.displayProblem()
        else:
            self.displayResults()
    
    def displayResults(self):
        """Display final results and ask to play again"""
        self.clearFrame()
        
        # Calculate percentage and grade
        percentage = (self.score / 100) * 100
        
        if percentage >= 90:
            grade = "A+"
            message = "Outstanding! 🎉"
        elif percentage >= 80:
            grade = "A"
            message = "Excellent! 👍"
        elif percentage >= 70:
            grade = "B"
            message = "Good job! 😊"
        elif percentage >= 60:
            grade = "C"
            message = "Well done! 🙂"
        elif percentage >= 50:
            grade = "D"
            message = "You passed! 👏"
        else:
            grade = "F"
            message = "Keep practicing! 💪"
        
        # Results display
        title_label = tk.Label(self.main_frame, text="QUIZ COMPLETE!", 
                              font=('Arial', 18, 'bold'))
        title_label.pack(pady=20)
        
        score_label = tk.Label(self.main_frame, 
                              text=f"Final Score: {self.score}/100",
                              font=('Arial', 16))
        score_label.pack(pady=10)
        
        grade_label = tk.Label(self.main_frame, 
                              text=f"Grade: {grade}",
                              font=('Arial', 16, 'bold'))
        grade_label.pack(pady=10)
        
        message_label = tk.Label(self.main_frame, 
                                text=message,
                                font=('Arial', 14))
        message_label.pack(pady=10)
        
        # Play again buttons
        play_again_btn = tk.Button(self.main_frame, text="Play Again", 
                                  font=('Arial', 12), width=15,
                                  command=self.restartQuiz)
        play_again_btn.pack(pady=10)
        
        quit_btn = tk.Button(self.main_frame, text="Quit", 
                            font=('Arial', 12), width=15,
                            command=self.root.quit)
        quit_btn.pack(pady=5)
    
    def startQuiz(self, difficulty):
        """Start the quiz with selected difficulty"""
        self.difficulty = difficulty
        self.score = 0
        self.current_question = 0
        self.generateQuestion()
        self.displayProblem()
    
    def restartQuiz(self):
        """Restart the quiz by showing the menu again"""
        self.difficulty = None
        self.score = 0
        self.current_question = 0
        self.displayMenu()
    
    def clearFrame(self):
        """Clear all widgets from the main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    app = MathsQuiz(root)
    root.mainloop()

if __name__ == "__main__":
    main()