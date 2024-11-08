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

    def task_summary(self):
        total_tasks = len(self.tasks)
        completed_tasks = len([task for task in self.tasks if task.completed])
        pending_tasks = total_tasks - completed_tasks
        return {
            "Total Tasks": total_tasks,
            "Completed Tasks": completed_tasks,
            "Pending Tasks": pending_tasks
        }

def main():
    todo_list = TodoList()

    while True:
        print("\nTodo List Application")
        print("1. Add Task")
        print("2. Edit Task")
        print("3. Delete Task")
        print("4. View Tasks")
        print("5. Filter Tasks")
        print("6. Set Reminders")
        print("7. Reorder Tasks")
        print("8. Task Summary")
        print("9. Export Tasks")
        print("10. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter title: ")
            description = input("Enter description: ")
            due_date = input("Enter due date (YYYY-MM-DD): ")
            category = input("Enter category: ")
            priority = input("Enter priority (High, Medium, Low): ")
            todo_list.add_task(title, description, due_date, category, priority)
            print("Task added successfully.")

        elif choice == '2':
            try:
                task_index = int(input("Enter task index to edit: "))
                title = input("Enter new title (leave blank to skip): ")
                description = input("Enter new description (leave blank to skip): ")
                due_date = input("Enter new due date (YYYY-MM-DD, leave blank to skip): ")
                category = input("Enter new category (leave blank to skip): ")
                priority = input("Enter new priority (High, Medium, Low, leave blank to skip): ")
                updates = {"title": title, "description": description, "due_date": due_date, "category": category,
                           "priority": priority}
                todo_list.edit_task(task_index, **{k: v for k, v in updates.items() if v})
                print("Task updated successfully.")
            except ValueError:
                print("Invalid input! Please enter a valid index.")


        elif choice == '3':
            task_index = int(input("Enter task index to delete: "))
            todo_list.delete_task(task_index)
            print("Task deleted.")

        elif choice == '4':
            tasks = todo_list.view_tasks()
            display_tasks(tasks)

        elif choice == '5':
            status = input("Filter by status (completed, pending, leave blank for all): ")
            category = input("Filter by category (leave blank for all): ")
            priority = input("Filter by priority (High, Medium, Low, leave blank for all): ")
            tag = input("Filter by tag (leave blank for all): ")

            tasks = todo_list.filter_tasks(status=status, category=category, priority=priority, tag=tag)
            display_tasks(tasks)


        elif choice == '6':
            days = int(input("Enter number of days before due date for reminders: "))
            reminders = todo_list.set_reminders(days)
            print("\nUpcoming Reminders:")
            for task in reminders:
                print(task)

        elif choice == '7':
            todo_list.reorder_tasks()
            print("Tasks reordered by completion status, priority, and due date.")

        elif choice == '8':
            summary = todo_list.task_summary()
            print("\nTask Summary:")
            for key, value in summary.items():
                print(f"{key}: {value}")

        elif choice == '9':
            # Export Tasks
            export_choice = input("Export as (1) CSV or (2) PDF: ")
            if export_choice == '1':
                filename = input("Enter CSV filename (default 'tasks.csv'): ") or "tasks.csv"
                todo_list.export_to_csv(filename)
                print(f"Tasks exported to {filename}")
            elif export_choice == '2':
                filename = input("Enter PDF filename (default 'tasks.pdf'): ") or "tasks.pdf"
                todo_list.export_to_pdf(filename)
                print(f"Tasks exported to {filename}")
            else:
                print("Invalid export option.")

        elif choice == '10':
            print("Exiting application.")
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()