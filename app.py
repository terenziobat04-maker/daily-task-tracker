import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class TaskTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Task Tracker")
        self.tasks = []

        self.label = tk.Label(root, text="Task Tracker", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.task_entry = tk.Entry(root, width=50)
        self.task_entry.pack(pady=10)

        self.add_task_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_task_button.pack(pady=5)

        self.view_tasks_button = tk.Button(root, text="View Tasks", command=self.view_tasks)
        self.view_tasks_button.pack(pady=5)

        self.generate_report_button = tk.Button(root, text="Generate Report", command=self.generate_report)
        self.generate_report_button.pack(pady=5)

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append(task)
            self.task_entry.delete(0, tk.END)
            messagebox.showinfo("Success", f"Task added: {task}")
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def view_tasks(self):
        task_list = "\n".join(self.tasks) if self.tasks else "No tasks added."
        messagebox.showinfo("Tasks", task_list)

    def generate_report(self):
        report = f"Daily Task Report - {datetime.now().strftime('%Y-%m-%d')}\n\n" + "\n".join(self.tasks) if self.tasks else "No tasks completed for today."
        messagebox.showinfo("Daily Report", report)

if __name__ == '__main__':
    root = tk.Tk()
    app = TaskTracker(root)
    root.mainloop()