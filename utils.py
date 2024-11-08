from datetime import datetime

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

def display_tasks(tasks):
    if not tasks:
        print("No tasks to display.")
        return
    for idx, task in enumerate(tasks, start=1):
        print(f"\nTask {idx}:")
        print(task)
        print("-" * 40)

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