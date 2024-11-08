# Todo List Application 📝🚀

> A Python-based command-line Todo List application to help you manage your tasks efficiently.

## Features ✨

- **Add Task**: Create new tasks with details like title, description, due date, category, priority, tags, and recurring days.
- **Edit Task**: Modify existing tasks to update their information.
- **Delete Task**: Remove tasks that are no longer needed.
- **View Tasks**: Display all tasks with their details.
- **Filter Tasks**: View tasks based on status, category, priority, or tags.
- **Set Reminders**: View tasks due within a specified number of days.
- **Reorder Tasks**: Sort tasks based on completion status and priority.
- **Task Summary**: Get an overview of total, completed, and pending tasks.
- **Export Tasks**: Export your task list to CSV or PDF formats.
- **Persistent Storage**: Tasks are saved to a JSON file, ensuring data is retained between sessions.
- **Modular Design**: Organized into separate modules for better maintainability and scalability.

## Project Structure 📁

The application is organized into multiple modules, each handling specific functionalities to promote code modularity and maintainability.

```
todo_app/
│
├── main.py
├── models.py
├── todo_list.py
├── utils.py
├── exports.py
├── requirements.txt
└── tasks.json
```

### Module Descriptions

- **main.py**: Entry point of the application. Handles user interactions, displays menus, and orchestrates calls to other modules based on user input.
- **models.py**: Contains the `Task` class definition, representing individual tasks with attributes like title, description, due date, category, priority, tags, and recurring days.
- **todo_list.py**: Contains the `TodoList` class definition, managing the collection of tasks. Handles operations like adding, editing, deleting, viewing, filtering, reordering, setting reminders, exporting tasks, and managing persistent storage.
- **utils.py**: Includes utility functions for input validation (`get_valid_date`, `get_valid_priority`), displaying tasks (`display_tasks`), and filtering tasks (`filter_tasks`).
- **exports.py**: Handles exporting tasks to CSV and PDF formats. Utilizes the `csv` module and `fpdf` library for generating PDF files.
- **requirements.txt**: Lists all Python dependencies required for the application.
- **tasks.json**: Stores the tasks data persistently. This file is automatically created and managed by the application.

## Installation 🛠️

### Prerequisites

- **Python 3.6 or higher**: Ensure that Python is installed on your system. You can download it from the [official website](https://www.python.org/downloads/).

### Clone the Repository

```bash
git clone https://github.com/HubertFijolek1/todo_app.git
cd todo_app
```

### Create a Virtual Environment (Optional but Recommended)

Creating a virtual environment helps manage project-specific dependencies.

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies

Install the required Python packages using `pip` and the provided `requirements.txt` file.

```bash
pip install -r requirements.txt
```

**Note**: If `fpdf` is not listed in `requirements.txt`, ensure to install it manually:

```bash
pip install fpdf
```

## Usage 💻

### Running the Application

Navigate to the project directory and run the `main.py` script using Python.

```bash
python main.py
```

Ensure you’re in the `todo_app` directory and that your virtual environment is activated if you created one.

### Application Menu

Upon running, you’ll be presented with a menu offering various options:

```
=== Todo List Application ===
1. Add Task
2. Edit Task
3. Delete Task
4. View All Tasks
5. Filter Tasks
6. Set Reminders
7. Reorder Tasks
8. Task Summary
9. Export Tasks
10. Exit
Enter your choice:
```

#### 1. Add Task

- **Description**: Create a new task by providing details such as title, description, due date, category, priority, tags, and recurring days.
- **Example Interaction**:

    ```
    Enter your choice: 1
    Enter title: Do Python Project
    Enter description: Develop a Todo List application
    Enter due date (YYYY-MM-DD): 2024-12-31
    Enter category: Work
    Enter priority (High, Medium, Low): High
    Enter tags (comma-separated, optional): python, project
    Enter recurring days (optional, press Enter to skip):
    Task added successfully.
    ```

#### 2. Edit Task

- **Description**: Modify existing tasks by updating their details.
- **Example Interaction**:

    ```
    Enter your choice: 2
    Enter task index to edit: 1
    Leave a field blank to skip updating it.
    Enter new title: Complete Python Project
    Enter new description:
    Enter new due date (YYYY-MM-DD):
    Enter new category:
    Enter new priority (High, Medium, Low):
    Enter new tags (comma-separated):
    Enter new recurring days:
    Task updated successfully.
    ```

#### 3. Delete Task

- **Description**: Remove a task from the list by specifying its index.
- **Example Interaction**:

    ```
    Enter your choice: 3
    Enter task index to delete: 1
    Are you sure you want to delete task 'Do Python Project'? (y/n): y
    Task deleted.
    ```

#### 4. View All Tasks

- **Description**: Display all tasks with their details.
- **Example Interaction**:

    ```
    Enter your choice: 4

    Task 1:
    Title: Do Python Project
    Description: Develop a Todo List application
    Due Date: 2024-12-31
    Category: Work
    Priority: High
    Status: Pending
    Tags: python, project
    --------------------
    ```

#### 5. Filter Tasks

- **Description**: View tasks based on specific criteria like status, category, priority, or tags.
- **Example Interaction**:

    ```
    Enter your choice: 5

    --- Filter Tasks ---
    Filter by status (completed, pending, leave blank for all): pending
    Filter by category (leave blank for all):
    Filter by priority (High, Medium, Low, leave blank for all): High
    Filter by tag (leave blank for all):

    Task 1:
    Title: Do Python Project
    Description: Develop a Todo List application
    Due Date: 2024-12-31
    Category: Work
    Priority: High
    Status: Pending
    Tags: python, project
    --------------------
    ```

#### 6. Set Reminders

- **Description**: Display tasks that are due within a specified number of days.
- **Example Interaction**:

    ```
    Enter your choice: 6
    Enter number of days before due date for reminders: 7

    --- Upcoming Reminders ---

    Task 1:
    Title: Submit Report
    Description: Submit the quarterly report
    Due Date: 2024-11-15
    Category: Work
    Priority: Medium
    Status: Pending
    Tags: report, quarterly
    --------------------
    ```

#### 7. Reorder Tasks

- **Description**: Sort tasks based on completion status and priority.
- **Example Interaction**:

    ```
    Enter your choice: 7
    Tasks reordered by completion status and priority.
    ```

#### 8. Task Summary

- **Description**: View a summary of total, completed, and pending tasks.
- **Example Interaction**:

    ```
    Enter your choice: 8

    --- Task Summary ---
    Total Tasks: 5
    Completed Tasks: 2
    Pending Tasks: 3
    ```

#### 9. Export Tasks

- **Description**: Export your tasks to CSV or PDF formats.
- **Example Interaction**:

    ```
    Enter your choice: 9

    --- Export Tasks ---
    1. Export as CSV
    2. Export as PDF
    Choose export format (1 or 2): 1
    Enter CSV filename (default 'tasks.csv'): my_tasks.csv
    Tasks successfully exported to 'my_tasks.csv'.
    ```

#### 10. Exit

- **Description**: Close the application.
- **Example Interaction**:

    ```
    Enter your choice: 10
    Exiting application. Goodbye!
    ```

## Exporting Tasks 📤

The application allows you to export your tasks in two formats:

### 1. CSV (Comma-Separated Values)

- **Usage**: Choose the CSV export option from the menu and specify a filename (default is `tasks.csv`).
- **Example**:

    ```
    Choose export format (1 or 2): 1
    Enter CSV filename (default 'tasks.csv'): my_tasks.csv
    Tasks successfully exported to 'my_tasks.csv'.
    ```

### 2. PDF (Portable Document Format)

- **Usage**: Choose the PDF export option from the menu and specify a filename (default is `tasks.pdf`).
- **Example**:

    ```
    Choose export format (1 or 2): 2
    Enter PDF filename (default 'tasks.pdf'): my_tasks.pdf
    Tasks successfully exported to 'my_tasks.pdf'.
    ```

**Ensure that you have the `fpdf` library installed. If not, install it using:**

```bash
pip install fpdf
```

## Dependencies 📦

All dependencies are listed in the `requirements.txt` file. Ensure they are installed before running the application.

### Python Libraries

- **fpdf**: For exporting tasks to PDF format.

### Installation

```bash
pip install -r requirements.txt
```

If you encounter issues with `fpdf`, install it separately:

```bash
pip install fpdf
```



