from datetime import timedelta, datetime
import csv
from fpdf import FPDF


class Task:
    def __init__(self, title, description, due_date, category="General", priority="Medium", tags=None, recurring_days=None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.category = category
        self.priority = priority
        self.completed = False
        self.tags = tags if tags else []
        self.recurring_days = recurring_days

    def mark_completed(self):
        self.completed = True
        if self.recurring_days:
            self.due_date += timedelta(days=self.recurring_days)
            self.completed = False

class TodoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, title, description, due_date, category="General", priority="Medium"):
        task = Task(title, description, due_date, category, priority)
        self.tasks.append(task)

    def edit_task(self, task_index, title=None, description=None, due_date=None, category=None, priority=None):
        if 0 <= task_index < len(self.tasks):
            task = self.tasks[task_index]
            if title:
                task.title = title
            if description:
                task.description = description
            if due_date:
                task.due_date = due_date
            if category:
                task.category = category
            if priority:
                task.priority = priority

    def delete_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            del self.tasks[task_index]

    def view_tasks(self, status=None):
        if status == "completed":
            return [task for task in self.tasks if task.completed]
        elif status == "pending":
            return [task for task in self.tasks if not task.completed]
        else:
            return self.tasks

    def view_tasks_by_category(self, category):
        return [task for task in self.tasks if task.category == category]

    def view_tasks_by_priority(self, priority):
        return [task for task in self.tasks if task.priority == priority]

    def view_tasks_by_tag(self, tag):
        return [task for task in self.tasks if tag in task.tags]

    def reorder_tasks(self):
        priority_map = {"High": 1, "Medium": 2, "Low": 3}
        self.tasks.sort(key=lambda task: (task.completed, priority_map.get(task.priority, 2)))

    def set_reminders(self, days_before_due=1):
        today = datetime.now()
        reminders = []
        for task in self.tasks:
            if not task.completed:
                due_date = datetime.strptime(task.due_date, "%Y-%m-%d")
                if due_date - today <= timedelta(days=days_before_due):
                    reminders.append(task)
        return reminders

    def export_to_csv(self, filename="tasks.csv"):
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Description", "Due Date", "Category", "Priority", "Status", "Tags", "Recurring Days"])
            for task in self.tasks:
                writer.writerow([task.title, task.description, task.due_date, task.category, task.priority, "Completed" if task.completed else "Pending", ", ".join(task.tags), task.recurring_days])

    def export_to_pdf(self, filename="tasks.pdf"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="To-Do List", ln=True, align="C")

        for task in self.tasks:
            pdf.cell(200, 10, txt=f"Title: {task.title}", ln=True)
            pdf.cell(200, 10, txt=f"Description: {task.description}", ln=True)
            pdf.cell(200, 10, txt=f"Due Date: {task.due_date}", ln=True)
            pdf.cell(200, 10, txt=f"Category: {task.category}", ln=True)
            pdf.cell(200, 10, txt=f"Priority: {task.priority}", ln=True)
            pdf.cell(200, 10, txt=f"Tags: {', '.join(task.tags)}", ln=True)
            pdf.cell(200, 10, txt=f"Status: {'Completed' if task.completed else 'Pending'}", ln=True)
            if task.recurring_days:
                pdf.cell(200, 10, txt=f"Recurring Every: {task.recurring_days} Days", ln=True)
            pdf.cell(200, 10, ln=True)
        pdf.output(filename)