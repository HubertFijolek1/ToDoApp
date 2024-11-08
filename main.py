class Task:
    def __init__(self, title, description, due_date, category="General", priority="Medium"):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.category = category
        self.priority = priority