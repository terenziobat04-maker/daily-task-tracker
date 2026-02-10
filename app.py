import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import datetime
import json
import os

class TaskTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Task Tracker")
        self.root.geometry("600x700")
        
        self.tasks_file = "tasks.json"
        self.tasks = self.load_tasks()
        
        # Title
        self.title_label = tk.Label(root, text="Daily Task Tracker", font=("Helvetica", 18, "bold"), fg="darkblue")
        self.title_label.pack(pady=10)
        
        # Date Display
        self.date_label = tk.Label(root, text=f"Date: {datetime.now().strftime('%Y-%m-%d')}", font=("Helvetica", 10))
        self.date_label.pack()
        
        # Task Input Frame
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="New Task:").pack(side=tk.LEFT, padx=5)
        self.task_entry = tk.Entry(input_frame, width=40)
        self.task_entry.pack(side=tk.LEFT, padx=5)
        
        # Add Task Button
        self.add_task_button = tk.Button(root, text="Add Task", command=self.add_task, bg="green", fg="white", width=15)
        self.add_task_button.pack(pady=5)
        
        # Tasks Listbox
        tk.Label(root, text="Today's Tasks:", font=("Helvetica", 12, "bold")).pack(anchor=tk.W, padx=10)
        
        self.tasks_listbox = tk.Listbox(root, height=10, width=70)
        self.tasks_listbox.pack(padx=10, pady=5)
        
        # Buttons Frame
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        
        self.mark_complete_button = tk.Button(button_frame, text="Mark Complete", command=self.mark_complete, bg="blue", fg="white")
        self.mark_complete_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_task_button = tk.Button(button_frame, text="Delete Task", command=self.delete_task, bg="red", fg="white")
        self.delete_task_button.pack(side=tk.LEFT, padx=5)
        
        self.generate_report_button = tk.Button(button_frame, text="Daily Report", command=self.generate_report, bg="purple", fg="white")
        self.generate_report_button.pack(side=tk.LEFT, padx=5)
        
        # Refresh the task list
        self.refresh_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.tasks_file):
            try:
                with open(self.tasks_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)
    
    def add_task(self):
        """Add a new task"""
        task_text = self.task_entry.get().strip()
        if task_text:
            task = {
                "id": len(self.tasks) + 1,
                "description": task_text,
                "completed": False,
                "date_added": datetime.now().strftime('%Y-%m-%d'),
                "date_completed": None
            }
            self.tasks.append(task)
            self.save_tasks()
            self.task_entry.delete(0, tk.END)
            self.refresh_tasks()
            messagebox.showinfo("Success", f"Task added: {task_text}")
        else:
            messagebox.showwarning("Warning", "Please enter a task.")
    
    def mark_complete(self):
        """Mark selected task as complete"""
        try:
            selected_index = self.tasks_listbox.curselection()[0]
            self.tasks[selected_index]["completed"] = True
            self.tasks[selected_index]["date_completed"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.save_tasks()
            self.refresh_tasks()
            messagebox.showinfo("Success", "Task marked as complete!")
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task.")
    
    def delete_task(self):
        """Delete selected task"""
        try:
            selected_index = self.tasks_listbox.curselection()[0]
            deleted_task = self.tasks.pop(selected_index)
            self.save_tasks()
            self.refresh_tasks()
            messagebox.showinfo("Success", f"Task deleted: {deleted_task['description']}")
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task.")
    
    def refresh_tasks(self):
        """Refresh the task list display"""
        self.tasks_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✓ DONE" if task["completed"] else "○ TODO"
            self.tasks_listbox.insert(tk.END, f"{status} - {task['description']}")
    
    def generate_report(self):
        """Generate daily report"""
        today = datetime.now().strftime('%Y-%m-%d')
        today_tasks = [t for t in self.tasks if t["date_added"] == today]
        
        completed = [t for t in today_tasks if t["completed"]]
        pending = [t for t in today_tasks if not t["completed"]]
        
        report = f"═══════════════════════════════════\n"
        report += f"DAILY TASK REPORT\n"
        report += f"Date: {today}\n"
        report += f"═══════════════════════════════════\n\n"
        
        report += f"COMPLETED TASKS ({len(completed)}):\n"
        if completed:
            for task in completed:
                report += f"  ✓ {task['description']}\n"
                report += f"    Completed at: {task['date_completed']}\n"
        else:
            report += "  No tasks completed yet.\n"
        
        report += f"\nPENDING TASKS ({len(pending)}):\n"
        if pending:
            for task in pending:
                report += f"  ○ {task['description']}\n"
        else:
            report += "  All tasks completed!\n"
        
        report += f"\n═══════════════════════════════════\n"
        report += f"Total Tasks: {len(today_tasks)}\n"
        report += f"Completion Rate: {len(completed)}/{len(today_tasks)} ({int(len(completed)/len(today_tasks)*100) if today_tasks else 0}%)\n"
        report += f"═══════════════════════════════════\n"
        
        # Display report in a new window
        report_window = tk.Toplevel(self.root)
        report_window.title("Daily Report")
        report_window.geometry("500x400")
        
        report_text = scrolledtext.ScrolledText(report_window, height=20, width=60)
        report_text.pack(padx=10, pady=10)
        report_text.insert(tk.END, report)
        report_text.config(state=tk.DISABLED)

if __name__ == '__main__':
    root = tk.Tk()
    app = TaskTracker(root)
    root.mainloop()