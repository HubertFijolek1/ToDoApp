from datetime import timedelta, datetime
import csv
import json
from fpdf import FPDF

class Task:
    def __init__(self, title, description, due_date, category="General", priority="Medium", tags=None, recurring_days=None):
        self.title = title
        self.description = description
        self.due_date = due_date  # Stored as string in 'YYYY-MM-DD' format
        self.category = category
        self.priority = priority
        self.completed = False
        self.tags = tags if tags else []
        self.recurring_days = recurring_days

    def mark_completed(self):
        self.completed = True
        if self.recurring_days:
            try:
                due_date_obj = datetime.strptime(self.due_date, "%Y-%m-%d")
                due_date_obj += timedelta(days=self.recurring_days)
                self.due_date = due_date_obj.strftime("%Y-%m-%d")
                self.completed = False  # Reset completion for recurring tasks
            except ValueError:
                print(f"Error updating due date for task '{self.title}'. Invalid date format.")

    def __str__(self):
        base_str = (f"Title: {self.title}\n"
                    f"Description: {self.description}\n"
                    f"Due Date: {self.due_date}\n"
                    f"Category: {self.category}\n"
                    f"Priority: {self.priority}\n"
                    f"Status: {'Completed' if self.completed else 'Pending'}\n"
                    f"Tags: {', '.join(self.tags)}\n")
        if self.recurring_days:
            base_str += f"Recurring Every: {self.recurring_days} Days"
        return base_str

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

    def export_to_csv(self, filename="tasks.csv"):
        try:
            with open(filename, mode="w", newline="", encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Title", "Description", "Due Date", "Category", "Priority", "Status", "Tags", "Recurring Days"])
                for task in self.tasks:
                    writer.writerow([
                        task.title,
                        task.description,
                        task.due_date,
                        task.category,
                        task.priority,
                        "Completed" if task.completed else "Pending",
                        ", ".join(task.tags),
                        task.recurring_days if task.recurring_days else ""
                    ])
            print(f"Tasks successfully exported to '{filename}'.")
        except Exception as e:
            print(f"Error exporting to CSV: {e}")

    def export_to_pdf(self, filename="tasks.pdf"):
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="To-Do List", ln=True, align="C")
            pdf.ln(10)  # Add a line break

            pdf.set_font("Arial", size=12)
            for idx, task in enumerate(self.tasks, start=1):
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, txt=f"Task {idx}: {task.title}", ln=True)
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, txt=f"Description: {task.description}")
                pdf.cell(0, 10, txt=f"Due Date: {task.due_date}", ln=True)
                pdf.cell(0, 10, txt=f"Category: {task.category}", ln=True)
                pdf.cell(0, 10, txt=f"Priority: {task.priority}", ln=True)
                pdf.cell(0, 10, txt=f"Tags: {', '.join(task.tags)}", ln=True)
                pdf.cell(0, 10, txt=f"Status: {'Completed' if task.completed else 'Pending'}", ln=True)
                if task.recurring_days:
                    pdf.cell(0, 10, txt=f"Recurring Every: {task.recurring_days} Days", ln=True)
                pdf.ln(5)  # Add space between tasks
            pdf.output(filename)
            print(f"Tasks successfully exported to '{filename}'.")
        except Exception as e:
            print(f"Error exporting to PDF: {e}")

    def task_summary(self):
        total_tasks = len(self.tasks)
        completed_tasks = len([task for task in self.tasks if task.completed])
        pending_tasks = total_tasks - completed_tasks
        return {
            "Total Tasks": total_tasks,
            "Completed Tasks": completed_tasks,
            "Pending Tasks": pending_tasks
        }

def display_tasks(tasks):
    if not tasks:
        print("No tasks to display.")
        return
    for idx, task in enumerate(tasks, start=1):
        print(f"\nTask {idx}:")
        print(task)
        print("-" * 40)

def get_valid_date(prompt):
    while True:
        date_str = input(prompt)
        try:
            # Validate the date format
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str  # Return as string to maintain consistency
        except ValueError:
            print("Invalid date format! Please enter in YYYY-MM-DD format.")

def get_valid_priority(prompt):
    priorities = ["High", "Medium", "Low"]
    while True:
        priority = input(prompt).capitalize()
        if priority in priorities:
            return priority
        else:
            print(f"Invalid priority! Choose from {', '.join(priorities)}.")

def filter_tasks(todo_list, status=None, category=None, priority=None, tag=None):
    filtered = todo_list.tasks
    if status:
        if status.lower() == "completed":
            filtered = [task for task in filtered if task.completed]
        elif status.lower() == "pending":
            filtered = [task for task in filtered if not task.completed]
    if category:
        filtered = [task for task in filtered if task.category.lower() == category.lower()]
    if priority:
        filtered = [task for task in filtered if task.priority.lower() == priority.lower()]
    if tag:
        filtered = [task for task in filtered if tag.lower() in [t.lower() for t in task.tags]]
    return filtered

def main():
    todo_list = TodoList()

    while True:
        print("\n=== Todo List Application ===")
        print("1. Add Task")
        print("2. Edit Task")
        print("3. Delete Task")
        print("4. View All Tasks")
        print("5. Filter Tasks")
        print("6. Set Reminders")
        print("7. Reorder Tasks")
        print("8. Task Summary")
        print("9. Export Tasks")
        print("10. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            # Add Task
            title = input("Enter title: ").strip()
            description = input("Enter description: ").strip()
            due_date = get_valid_date("Enter due date (YYYY-MM-DD): ")
            category = input("Enter category: ").strip() or "General"
            priority = get_valid_priority("Enter priority (High, Medium, Low): ")
            tags_input = input("Enter tags (comma-separated, optional): ").strip()
            tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
            recurring_input = input("Enter recurring days (optional, press Enter to skip): ").strip()
            recurring_days = int(recurring_input) if recurring_input.isdigit() else None
            todo_list.add_task(title, description, due_date, category, priority)
            # Add tags and recurring_days if provided
            if tags:
                todo_list.tasks[-1].tags = tags
            if recurring_days:
                todo_list.tasks[-1].recurring_days = recurring_days
            todo_list.save_tasks()
            print("Task added successfully.")

        elif choice == '2':
            # Edit Task
            try:
                task_index = int(input("Enter task index to edit: ")) - 1
                if not (0 <= task_index < len(todo_list.tasks)):
                    print("Invalid task index!")
                    continue
                print("Leave a field blank to skip updating it.")
                title = input("Enter new title: ").strip()
                description = input("Enter new description: ").strip()
                due_date_input = input("Enter new due date (YYYY-MM-DD): ").strip()
                due_date = due_date_input if due_date_input else None
                if due_date:
                    try:
                        datetime.strptime(due_date, "%Y-%m-%d")
                    except ValueError:
                        print("Invalid date format! Skipping due date update.")
                        due_date = None
                category = input("Enter new category: ").strip() or None
                priority_input = input("Enter new priority (High, Medium, Low): ").strip()
                priority = priority_input.capitalize() if priority_input else None
                if priority and priority not in ["High", "Medium", "Low"]:
                    print("Invalid priority! Skipping priority update.")
                    priority = None
                tags_input = input("Enter new tags (comma-separated): ").strip()
                tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else None
                recurring_input = input("Enter new recurring days: ").strip()
                recurring_days = int(recurring_input) if recurring_input.isdigit() else None

                updates = {
                    "title": title if title else None,
                    "description": description if description else None,
                    "due_date": due_date,
                    "category": category,
                    "priority": priority,
                }
                # Remove None or empty updates
                updates = {k: v for k, v in updates.items() if v is not None}

                todo_list.edit_task(task_index, **updates)

                # Update tags and recurring_days separately
                if tags is not None:
                    todo_list.tasks[task_index].tags = tags
                if recurring_days is not None:
                    todo_list.tasks[task_index].recurring_days = recurring_days

                todo_list.save_tasks()
                print("Task updated successfully.")
            except ValueError:
                print("Invalid input! Please enter a valid index.")

        elif choice == '3':
            # Delete Task
            try:
                task_index = int(input("Enter task index to delete: ")) - 1
                if not (0 <= task_index < len(todo_list.tasks)):
                    print("Invalid task index!")
                    continue
                confirm = input(f"Are you sure you want to delete task '{todo_list.tasks[task_index].title}'? (y/n): ").strip().lower()
                if confirm == 'y':
                    todo_list.delete_task(task_index)
                    print("Task deleted.")
                else:
                    print("Deletion cancelled.")
            except ValueError:
                print("Invalid input! Please enter a valid index.")

        elif choice == '4':
            # View All Tasks
            tasks = todo_list.view_tasks()
            display_tasks(tasks)

        elif choice == '5':
            # Filter Tasks
            print("\n--- Filter Tasks ---")
            status = input("Filter by status (completed, pending, leave blank for all): ").strip().lower()
            category = input("Filter by category (leave blank for all): ").strip()
            priority = input("Filter by priority (High, Medium, Low, leave blank for all): ").strip().capitalize()
            tag = input("Filter by tag (leave blank for all): ").strip()

            tasks = filter_tasks(
                todo_list,
                status=status if status in ["completed", "pending"] else None,
                category=category if category else None,
                priority=priority if priority in ["High", "Medium", "Low"] else None,
                tag=tag if tag else None
            )
            display_tasks(tasks)

        elif choice == '6':
            # Set Reminders
            try:
                days = int(input("Enter number of days before due date for reminders: ").strip())
                reminders = todo_list.set_reminders(days_before_due=days)
                print("\n--- Upcoming Reminders ---")
                display_tasks(reminders)
            except ValueError:
                print("Please enter a valid number of days.")

        elif choice == '7':
            # Reorder Tasks
            todo_list.reorder_tasks()
            print("Tasks reordered by completion status and priority.")

        elif choice == '8':
            # Task Summary
            summary = todo_list.task_summary()
            print("\n--- Task Summary ---")
            for key, value in summary.items():
                print(f"{key}: {value}")

        elif choice == '9':
            # Export Tasks
            print("\n--- Export Tasks ---")
            print("1. Export as CSV")
            print("2. Export as PDF")
            export_choice = input("Choose export format (1 or 2): ").strip()
            if export_choice == '1':
                filename = input("Enter CSV filename (default 'tasks.csv'): ").strip() or "tasks.csv"
                todo_list.export_to_csv(filename)
            elif export_choice == '2':
                filename = input("Enter PDF filename (default 'tasks.pdf'): ").strip() or "tasks.pdf"
                todo_list.export_to_pdf(filename)
            else:
                print("Invalid export option.")

        elif choice == '10':
            # Exit
            print("Exiting application. Goodbye!")
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()