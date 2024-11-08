class Task:
    def __init__(self, title, description, due_date, category="General", priority="Medium"):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.category = category
        self.priority = priority
        self.completed = False

    def mark_completed(self):
        self.completed = True

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

    def reorder_tasks(self):
        priority_map = {"High": 1, "Medium": 2, "Low": 3}
        self.tasks.sort(key=lambda task: (task.completed, priority_map.get(task.priority, 2)))