import csv
from fpdf import FPDF

def export_to_csv(tasks, filename="tasks.csv"):
    try:
        with open(filename, mode="w", newline="", encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Description", "Due Date", "Category", "Priority", "Status", "Tags", "Recurring Days"])
            for task in tasks:
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

def export_to_pdf(tasks, filename="tasks.pdf"):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="To-Do List", ln=True, align="C")
        pdf.ln(10)  # Add a line break

        pdf.set_font("Arial", size=12)
        for idx, task in enumerate(tasks, start=1):
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