import json
from models import Task
from datetime import datetime, timedelta

class TodoList:
    def __init__(self, storage_file="tasks.json"):
        self.tasks = []
        self.storage_file = storage_file
        self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.storage_file, "r") as file:
                tasks_data = json.load(file)
                for task_data in tasks_data:
                    task = Task(
                        title=task_data["title"],
                        description=task_data["description"],
                        due_date=task_data["due_date"],
                        category=task_data["category"],
                        priority=task_data["priority"],
                        tags=task_data.get("tags", []),
                        recurring_days=task_data.get("recurring_days")
                    )
                    task.completed = task_data["completed"]
                    self.tasks.append(task)
        except FileNotFoundError:
            # No existing tasks to load
            pass
        except json.JSONDecodeError:
            print("Error: Corrupted tasks.json file. Starting with an empty task list.")
            self.tasks = []

    def save_tasks(self):
        try:
            with open(self.storage_file, "w") as file:
                tasks_data = [{
                    "title": task.title,
                    "description": task.description,
                    "due_date": task.due_date,
                    "category": task.category,
                    "priority": task.priority,
                    "completed": task.completed,
                    "tags": task.tags,
                    "recurring_days": task.recurring_days
                } for task in self.tasks]
                json.dump(tasks_data, file, indent=4)
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def add_task(self, title, description, due_date, category="General", priority="Medium"):
        task = Task(title, description, due_date, category, priority)
        self.tasks.append(task)
        self.save_tasks()

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
            self.save_tasks()
        else:
            print("Error: Task index out of range.")

    def delete_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            del self.tasks[task_index]
            self.save_tasks()
        else:
            print("Error: Task index out of range.")

    def view_tasks(self, status=None):
        if status == "completed":
            return [task for task in self.tasks if task.completed]
        elif status == "pending":
            return [task for task in self.tasks if not task.completed]
        else:
            return self.tasks

    def view_tasks_by_category(self, category):
        return [task for task in self.tasks if task.category.lower() == category.lower()]

    def view_tasks_by_priority(self, priority):
        return [task for task in self.tasks if task.priority.lower() == priority.lower()]

    def view_tasks_by_tag(self, tag):
        return [task for task in self.tasks if tag.lower() in [t.lower() for t in task.tags]]

    def reorder_tasks(self):
        priority_map = {"High": 1, "Medium": 2, "Low": 3}
        self.tasks.sort(key=lambda task: (task.completed, priority_map.get(task.priority, 2)))

    def set_reminders(self, days_before_due=1):
        today = datetime.now()
        reminders = []
        for task in self.tasks:
            if not task.completed:
                try:
                    due_date = datetime.strptime(task.due_date, "%Y-%m-%d")
                    if due_date - today <= timedelta(days=days_before_due):
                        reminders.append(task)
                except ValueError:
                    print(f"Invalid due date format for task '{task.title}'. Skipping reminder.")
        return reminders

    def task_summary(self):
        total_tasks = len(self.tasks)
        completed_tasks = len([task for task in self.tasks if task.completed])
        pending_tasks = total_tasks - completed_tasks
        return {
            "Total Tasks": total_tasks,
            "Completed Tasks": completed_tasks,
            "Pending Tasks": pending_tasks
        }