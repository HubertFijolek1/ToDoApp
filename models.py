from datetime import timedelta, datetime

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