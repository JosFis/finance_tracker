import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os
from datetime import datetime
import pandas as pd

# File to store transactions
DATA_FILE = "finance_log.csv"

# Ensure the data file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Type", "Amount", "Description"])

# Function to add a new entry
def add_entry():
    date = date_entry.get()
    category = category_entry.get()
    entry_type = type_var.get()
    amount = amount_entry.get()
    description = description_entry.get()

    if not date or not category or not entry_type or not amount:
        messagebox.showerror("Input Error", "Please fill in all required fields.")
        return

    try:
        float(amount)
    except ValueError:
        messagebox.showerror("Input Error", "Amount must be a number.")
        return

    with open(DATA_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, entry_type, amount, description])

    status_label.config(text="Entry added successfully.")
    clear_fields()
    load_data()

# Function to clear input fields
def clear_fields():
    date_entry.delete(0, tk.END)
    date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
    category_entry.delete(0, tk.END)
    type_var.set("Expense")
    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)

# Function to load data into the table
def load_data():
    for row in tree.get_children():
        tree.delete(row)

    with open(DATA_FILE, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            tree.insert("", tk.END, values=row)

# Function to show summary
def show_summary():
    df = pd.read_csv(DATA_FILE)
    income = df[df["Type"] == "Income"]["Amount"].astype(float).sum()
    expense = df[df["Type"] == "Expense"]["Amount"].astype(float).sum()
    balance = income - expense
    summary_label.config(text=f"Income: ${income:.2f} | Expense: ${expense:.2f} | Balance: ${balance:.2f}")

# Function to export data
def export_data():
    export_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if export_path:
        with open(DATA_FILE, "r") as src, open(export_path, "w", newline="") as dst:
            dst.write(src.read())
        messagebox.showinfo("Export", f"Data exported to {export_path}")

# GUI setup
root = tk.Tk()
root.title("Personal Finance Tracker")

# Input fields
tk.Label(root, text="Date (YYYY-MM-DD)").grid(row=0, column=0)
date_entry = tk.Entry(root)
date_entry.grid(row=0, column=1)
date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))

tk.Label(root, text="Category").grid(row=1, column=0)
category_entry = tk.Entry(root)
category_entry.grid(row=1, column=1)

tk.Label(root, text="Type").grid(row=2, column=0)
type_var = tk.StringVar(value="Expense")
ttk.Combobox(root, textvariable=type_var, values=["Income", "Expense"]).grid(row=2, column=1)

tk.Label(root, text="Amount").grid(row=3, column=0)
amount_entry = tk.Entry(root)
amount_entry.grid(row=3, column=1)

tk.Label(root, text="Description").grid(row=4, column=0)
description_entry = tk.Entry(root)
description_entry.grid(row=4, column=1)

# Buttons
tk.Button(root, text="Add Entry", command=add_entry).grid(row=5, column=0, columnspan=2)
tk.Button(root, text="Show Summary", command=show_summary).grid(row=6, column=0, columnspan=2)
tk.Button(root, text="Export to CSV", command=export_data).grid(row=7, column=0, columnspan=2)

# Status and Summary
status_label = tk.Label(root, text="", fg="green")
status_label.grid(row=8, column=0, columnspan=2)

summary_label = tk.Label(root, text="", font=("Arial", 10, "bold"))
summary_label.grid(row=9, column=0, columnspan=2)

# Table to display transactions
tree = ttk.Treeview(root, columns=("Date", "Category", "Type", "Amount", "Description"), show="headings")
for col in ("Date", "Category", "Type", "Amount", "Description"):
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.grid(row=10, column=0, columnspan=2)

load_data()
root.mainloop()
