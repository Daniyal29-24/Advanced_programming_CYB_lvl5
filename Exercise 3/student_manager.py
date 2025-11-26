import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

#Student Class
class Student:
    def __init__(self, code, name, cw1, cw2, cw3, exam):
        self.code = int(code)
        self.name = name.strip()
        self.cw = [int(cw1), int(cw2), int(cw3)]
        self.exam = int(exam)

    def total_cw(self):
        return sum(self.cw)

    def total_score(self):
        return self.total_cw() + self.exam

    def percentage(self):
        return (self.total_score() / 160) * 100

    def grade(self):
        p = self.percentage()
        if p >= 70: return 'A'
        elif p >= 60: return 'B'
        elif p >= 50: return 'C'
        elif p >= 40: return 'D'
        else: return 'F'


#File Handling
FILENAME = "studentMarks.txt"

def load_students():
    if not os.path.exists(FILENAME):
        messagebox.showerror("File Error", f"{FILENAME} not found!")
        return []

    with open(FILENAME, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    if not lines:
        return []

    students = []
    try:
        n = int(lines[0])
        for line in lines[1:1+n]:
            parts = line.split(',')
            if len(parts) == 6:
                code, name, c1, c2, c3, exam = parts
                students.append(Student(code, name, c1, c2, c3, exam))
    except Exception as e:
        messagebox.showerror("Load Error", f"Error reading file:\n{e}")

    return students


def save_students(students):
    try:
        with open(FILENAME, 'w', encoding='utf-8') as f:
            f.write(f"{len(students)}\n")
            for s in students:
                f.write(f"{s.code},{s.name},{s.cw[0]},{s.cw[1]},{s.cw[2]},{s.exam}\n")
    except Exception as e:
        messagebox.showerror("Save Error", f"Could not save:\n{e}")


#Main App
class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager Pro")
        self.root.geometry("1200x800")

        self.students = load_students()

        self.setup_styles()
        self.create_layout()
        self.update_status(f"Loaded {len(self.students)} students")

    # UI Theme
    def setup_styles(self):
        style = tb.Style()

        # Primary colors
        self.primary = "#007bff"
        self.success = "#28a745"
        self.warning = "#ffc107"
        self.danger = "#dc3545"
        self.dark = "#212529"

        # Button style
        style.configure("Card.TButton", font=("Segoe UI", 11, "bold"), padding=10)

        # Treeview
        style.configure("Modern.Treeview", font=("Segoe UI", 10), rowheight=36)
        style.configure("Modern.Treeview.Heading", font=("Segoe UI", 11, "bold"))

        # Header text
        style.configure("Title.TLabel", font=("Segoe UI", 28, "bold"), foreground=self.primary)
        style.configure("Subtitle.TLabel", font=("Segoe UI", 12), foreground="#555")

        # Status
        style.configure("Status.TLabel", font=("Segoe UI", 10), background="#e9f2ff")

    # Layout
    def create_layout(self):
        # Header
        header = tb.Frame(self.root, padding=20)
        header.pack(fill=tk.X)

        tb.Label(header, text="Student Manager Pro", style="Title.TLabel").pack()
        tb.Label(header, text="Modern • Clean • Professional", style="Subtitle.TLabel").pack()

        # Main container
        main = tb.Frame(self.root, padding=10)
        main.pack(fill=tk.BOTH, expand=True)

        # Left panel
        left = tb.Frame(main, bootstyle="light", padding=10)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))

        tb.Label(left, text="Actions", font=("Segoe UI", 15, "bold")).pack(pady=10)

        actions = [
            ("All Students", self.view_all),
            ("Search Student", self.view_individual),
            ("Top Performer", self.show_highest),
            ("Lowest Score", self.show_lowest),
            ("Sort Records", self.sort_records),
            ("Add New Student", self.add_student),
            ("Delete Student", self.delete_student),
            ("Update Record", self.update_student),
        ]

        for text, cmd in actions:
            tb.Button(left, text=text, bootstyle="primary", command=cmd).pack(fill=tk.X, pady=6)

        # Right panel
        right = tb.Frame(main, bootstyle="light", padding=10)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        columns = ("Name", "Student ID", "CW Total /60", "Exam /100",
                   "Total /160", "Percentage", "Grade")

        # Use ttk.Treeview for reliability
        self.tree = ttk.Treeview(right, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=130)
        self.tree.column("Name", width=200, anchor=tk.W)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.status_var = tk.StringVar()
        status = tb.Label(self.root, textvariable=self.status_var, style="Status.TLabel", anchor=tk.W, padding=5)
        status.pack(fill=tk.X)

    # Utility functions
    def update_status(self, msg):
        self.status_var.set(f"Status: {msg}")

    def clear_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

    def display_students(self, stu_list):
        self.clear_tree()
        if not stu_list:
            self.update_status("No students found")
            return

        total_perc = sum(s.percentage() for s in stu_list)
        avg = total_perc / len(stu_list)

        colors = {
            'A': "#28a745",
            'B': "#007bff",
            'C': "#ffc107",
            'D': "#fd7e14",
            'F': "#dc3545"
        }

        for s in stu_list:
            grade = s.grade()
            color = colors.get(grade, "black")
            tag = f"grade_{grade}"
            self.tree.tag_configure(tag, foreground=color)

            self.tree.insert("", tk.END, values=(
                s.name, s.code, s.total_cw(), s.exam,
                s.total_score(), f"{s.percentage():.1f}%", grade
            ), tags=(tag,))

        self.update_status(f"Showing {len(stu_list)} students • Class Avg: {avg:.1f}%")

    # Actions
    def view_all(self):
        self.display_students(self.students)

    def find_student(self):
        q = simpledialog.askstring("Search", "Enter Student ID or Name:")
        if not q: return None

        q = q.strip()
        if q.isdigit():
            code = int(q)
            return next((s for s in self.students if s.code == code), None)
        else:
            return next((s for s in self.students if s.name.lower() == q.lower()), None)

    def view_individual(self):
        s = self.find_student()
        if not s:
            messagebox.showinfo("Not Found", "No matching student.")
            return
        self.display_students([s])
        self.update_status(f"Showing: {s.name}")

    def show_highest(self):
        if not self.students:
            return messagebox.showinfo("Empty", "No records.")
        best = max(self.students, key=lambda s: s.percentage())
        self.display_students([best])
        self.update_status(f"Top: {best.name}")

    def show_lowest(self):
        if not self.students:
            return messagebox.showinfo("Empty", "No records.")
        worst = min(self.students, key=lambda s: s.percentage())
        self.display_students([worst])
        self.update_status(f"Lowest: {worst.name}")

    def sort_records(self):
        if not self.students: return
        choice = simpledialog.askstring("Sort", "1=Name\n2=ID\n3=Percentage")
        if not choice: return
        reverse = messagebox.askyesno("Order", "Sort descending?")

        keys = {
            "1": lambda s: s.name.lower(),
            "2": lambda s: s.code,
            "3": lambda s: s.percentage()
        }

        if choice not in keys:
            messagebox.showerror("Invalid", "Choose 1, 2, or 3")
            return

        sorted_list = sorted(self.students, key=keys[choice], reverse=reverse)
        self.display_students(sorted_list)

    def add_student(self):
        code = simpledialog.askinteger("Add", "Student ID (1000-9999):", minvalue=1000, maxvalue=9999)
        if not code or any(s.code == code for s in self.students):
            return messagebox.showerror("Error", "Invalid or duplicate ID")

        name = simpledialog.askstring("Add", "Full name:")
        if not name: return

        def ask(prompt, mx):
            return simpledialog.askinteger("Input", prompt, minvalue=0, maxvalue=mx)

        cw = [ask(f"Coursework {i+1} (0-20):", 20) for i in range(3)]
        if None in cw: return
        exam = ask("Exam (0-100):", 100)
        if exam is None: return

        self.students.append(Student(code, name, *cw, exam))
        save_students(self.students)
        self.update_status("Student added")
        messagebox.showinfo("Success", "Student added successfully.")

    def delete_student(self):
        s = self.find_student()
        if not s: return
        if messagebox.askyesno("Confirm", f"Delete {s.name}?"):
            self.students.remove(s)
            save_students(self.students)
            self.update_status("Record deleted")
            messagebox.showinfo("Deleted", "Student removed.")

    def update_student(self):
        s = self.find_student()
        if not s: return

        choice = simpledialog.askstring(
            "Update",
            "Choose field:\n1 - Name\n2 - Coursework 1\n3 - Coursework 2\n4 - Coursework 3\n5 - Exam"
        )
        if not choice: return

        if choice == "1":
            new = simpledialog.askstring("Name", "New name:", initialvalue=s.name)
            if new: s.name = new.strip()

        elif choice in ["2", "3", "4"]:
            idx = int(choice) - 2
            new = simpledialog.askinteger("CW", "New mark (0-20):", minvalue=0, maxvalue=20)
            if new is not None: s.cw[idx] = new

        elif choice == "5":
            new = simpledialog.askinteger("Exam", "New exam mark (0-100):", minvalue=0, maxvalue=100)
            if new is not None: s.exam = new

        save_students(self.students)
        self.update_status("Record updated")
        messagebox.showinfo("Updated", "Student data updated.")


#Launch App
if __name__ == "__main__":
    root = tb.Window(themename="cosmo")  # modern light theme
    app = StudentManagerApp(root)
    root.mainloop()
