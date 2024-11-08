from todo_list import TodoList
from utils import get_valid_date, get_valid_priority, display_tasks, filter_tasks
from exports import export_to_csv, export_to_pdf

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

        choice = input("Enter your choice: ").strip()

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
                task_index = int(input("Enter task index to edit: ").strip()) - 1
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
                        # Validate the new due date
                        get_valid_date("Confirm new due date (YYYY-MM-DD): ")
                    except:
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
                task_index = int(input("Enter task index to delete: ").strip()) - 1
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
                export_to_csv(todo_list.tasks, filename)
            elif export_choice == '2':
                filename = input("Enter PDF filename (default 'tasks.pdf'): ").strip() or "tasks.pdf"
                export_to_pdf(todo_list.tasks, filename)
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