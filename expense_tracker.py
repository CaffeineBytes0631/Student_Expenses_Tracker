import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime

FILE_NAME = "expenses.csv"


# Create CSV file if it does not exist
def create_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Description"])


# Add expense
def add_expense():
    category = category_var.get()
    amount = amount_entry.get()
    description = description_entry.get()

    if category == "Select Category":
        messagebox.showwarning("Warning", "Please select a category.")
        return

    if not amount or not description:
        messagebox.showwarning("Warning", "Please fill all fields.")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number.")
        return

    date = datetime.now().strftime("%d-%m-%Y")

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, description])

    messagebox.showinfo("Success", "Expense added successfully!")

    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)

    load_expenses()
    calculate_total()


# Load expenses into table
def load_expenses():
    for item in table.get_children():
        table.delete(item)

    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            table.insert(
                "",
                tk.END,
                values=(
                    row["Date"],
                    row["Category"],
                    row["Amount"],
                    row["Description"]
                )
            )


# Calculate total
def calculate_total():
    total = 0

    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            total += float(row["Amount"])

    total_label.config(text=f"Total Expenses: ₹{total:.2f}")


# Delete selected expense
def delete_expense():
    selected = table.selection()

    if not selected:
        messagebox.showwarning("Warning", "Please select an expense.")
        return

    selected_item = table.item(selected[0])
    selected_values = selected_item["values"]

    rows = []

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        header = next(reader)

        for row in reader:
            if row != [str(x) for x in selected_values]:
                rows.append(row)

    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)

    load_expenses()
    calculate_total()

    messagebox.showinfo("Success", "Expense deleted successfully!")


# Search expense
def search_expense():
    search_text = search_entry.get().lower()

    for item in table.get_children():
        table.delete(item)

    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if (
                search_text in row["Category"].lower()
                or search_text in row["Description"].lower()
            ):
                table.insert(
                    "",
                    tk.END,
                    values=(
                        row["Date"],
                        row["Category"],
                        row["Amount"],
                        row["Description"]
                    )
                )


# Category summary
def category_summary():
    summary = {}

    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            category = row["Category"]
            amount = float(row["Amount"])

            summary[category] = summary.get(category, 0) + amount

    result = "CATEGORY-WISE EXPENSES\n\n"

    for category, amount in summary.items():
        result += f"{category}: ₹{amount:.2f}\n"

    if not summary:
        result += "No expenses available."

    messagebox.showinfo("Category Summary", result)


# Create file
create_file()


# Main window
root = tk.Tk()
root.title("Student Expense Tracker")
root.geometry("850x650")
root.resizable(False, False)


# Title
title_label = tk.Label(
    root,
    text="STUDENT EXPENSE TRACKER",
    font=("Arial", 22, "bold")
)
title_label.pack(pady=15)


# Input frame
input_frame = tk.Frame(root)
input_frame.pack(pady=10)


# Category
tk.Label(
    input_frame,
    text="Category:",
    font=("Arial", 11)
).grid(row=0, column=0, padx=5, pady=5)

category_var = tk.StringVar()
category_var.set("Select Category")

category_box = ttk.Combobox(
    input_frame,
    textvariable=category_var,
    values=[
        "Food",
        "Transport",
        "Education",
        "Shopping",
        "Entertainment",
        "Other"
    ],
    state="readonly",
    width=18
)
category_box.grid(row=0, column=1, padx=5)


# Amount
tk.Label(
    input_frame,
    text="Amount:",
    font=("Arial", 11)
).grid(row=0, column=2, padx=5)

amount_entry = tk.Entry(input_frame, width=20)
amount_entry.grid(row=0, column=3, padx=5)


# Description
tk.Label(
    input_frame,
    text="Description:",
    font=("Arial", 11)
).grid(row=1, column=0, padx=5, pady=10)

description_entry = tk.Entry(input_frame, width=50)
description_entry.grid(row=1, column=1, columnspan=3, padx=5)


# Add button
add_button = tk.Button(
    root,
    text="ADD EXPENSE",
    command=add_expense,
    width=20
)
add_button.pack(pady=10)


# Table
columns = ("Date", "Category", "Amount", "Description")

table = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=12
)

for column in columns:
    table.heading(column, text=column)
    table.column(column, width=180)

table.pack(pady=10)


# Search
search_frame = tk.Frame(root)
search_frame.pack(pady=5)

search_entry = tk.Entry(search_frame, width=30)
search_entry.pack(side=tk.LEFT, padx=5)

search_button = tk.Button(
    search_frame,
    text="SEARCH",
    command=search_expense
)
search_button.pack(side=tk.LEFT)


# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

delete_button = tk.Button(
    button_frame,
    text="DELETE SELECTED",
    command=delete_expense,
    width=18
)
delete_button.grid(row=0, column=0, padx=5)

summary_button = tk.Button(
    button_frame,
    text="CATEGORY SUMMARY",
    command=category_summary,
    width=18
)
summary_button.grid(row=0, column=1, padx=5)

show_button = tk.Button(
    button_frame,
    text="SHOW ALL",
    command=load_expenses,
    width=18
)
show_button.grid(row=0, column=2, padx=5)


# Total
total_label = tk.Label(
    root,
    text="Total Expenses: ₹0.00",
    font=("Arial", 16, "bold")
)
total_label.pack(pady=10)


# Load existing data
load_expenses()
calculate_total()


# Start application
root.mainloop()