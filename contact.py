import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb   # install with: pip install ttkbootstrap

# ---------------- Database Setup ---------------- #
# Connect to database (it will create contacts.db if not exists)
conn = sqlite3.connect("contacts.db")
cursor = conn.cursor()

# Create table if it does not exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT,
    address TEXT
)
""")
conn.commit()

# ---------------- Functions ---------------- #
# Function to add a new contact
def add_contact():
    name = name_var.get()
    phone = phone_var.get()
    email = email_var.get()
    address = address_var.get()

    if name == "" or phone == "":
        messagebox.showwarning("Input Error", "Name and Phone are required!")
        return

    cursor.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
                   (name, phone, email, address))
    conn.commit()
    fetch_contacts()
    clear_form()

# Function to display all contacts
def fetch_contacts():
    # Clear old data from table
    for row in contact_table.get_children():
        contact_table.delete(row)

    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()

    # Insert all rows into table
    for row in rows:
        contact_table.insert("", "end", values=row)

# Function to search by name or phone
def search_contact():
    query = search_var.get()

    for row in contact_table.get_children():
        contact_table.delete(row)

    cursor.execute("SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ?",
                   ('%'+query+'%', '%'+query+'%'))
    rows = cursor.fetchall()

    for row in rows:
        contact_table.insert("", "end", values=row)

# Function to delete selected contact
def delete_contact():
    selected = contact_table.focus()
    if not selected:
        messagebox.showwarning("Selection Error", "Select a contact to delete")
        return

    values = contact_table.item(selected, "values")
    contact_id = values[0]

    cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
    conn.commit()
    fetch_contacts()

# Function to update selected contact
def update_contact():
    selected = contact_table.focus()
    if not selected:
        messagebox.showwarning("Selection Error", "Select a contact to update")
        return

    values = contact_table.item(selected, "values")
    contact_id = values[0]

    cursor.execute("UPDATE contacts SET name=?, phone=?, email=?, address=? WHERE id=?",
                   (name_var.get(), phone_var.get(), email_var.get(), address_var.get(), contact_id))
    conn.commit()
    fetch_contacts()
    clear_form()

# Function to clear input fields
def clear_form():
    name_var.set("")
    phone_var.set("")
    email_var.set("")
    address_var.set("")

# Function to fill form when user clicks a row in table
def fill_form(event):
    selected = contact_table.focus()
    if not selected:
        return
    values = contact_table.item(selected, "values")
    name_var.set(values[1])
    phone_var.set(values[2])
    email_var.set(values[3])
    address_var.set(values[4])

# ---------------- UI Setup ---------------- #
root = tb.Window(themename="cosmo")  # You can try "darkly", "flatly", etc.
root.title("Contact Management System")
root.geometry("850x550")

# Form Variables
name_var = tk.StringVar()
phone_var = tk.StringVar()
email_var = tk.StringVar()
address_var = tk.StringVar()
search_var = tk.StringVar()

# Title
title_label = tb.Label(root, text="Contact Management System", font=("Helvetica", 18, "bold"))
title_label.pack(pady=10)

# -------- Form Frame -------- #
form_frame = tb.Frame(root)
form_frame.pack(side="top", fill="x", padx=20, pady=10)

# Name
tb.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
tb.Entry(form_frame, textvariable=name_var, width=25).grid(row=0, column=1, padx=5, pady=5)

# Phone
tb.Label(form_frame, text="Phone:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
tb.Entry(form_frame, textvariable=phone_var, width=25).grid(row=0, column=3, padx=5, pady=5)

# Email
tb.Label(form_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
tb.Entry(form_frame, textvariable=email_var, width=25).grid(row=1, column=1, padx=5, pady=5)

# Address
tb.Label(form_frame, text="Address:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
tb.Entry(form_frame, textvariable=address_var, width=25).grid(row=1, column=3, padx=5, pady=5)

# -------- Buttons Frame -------- #
btn_frame = tb.Frame(root)
btn_frame.pack(side="top", fill="x", padx=20, pady=10)

tb.Button(btn_frame, text="Add", bootstyle="success", command=add_contact).pack(side="left", padx=5)
tb.Button(btn_frame, text="Update", bootstyle="info", command=update_contact).pack(side="left", padx=5)
tb.Button(btn_frame, text="Delete", bootstyle="danger", command=delete_contact).pack(side="left", padx=5)
tb.Button(btn_frame, text="Clear", bootstyle="secondary", command=clear_form).pack(side="left", padx=5)
tb.Button(btn_frame, text="View All", bootstyle="warning", command=fetch_contacts).pack(side="left", padx=5)
# Search Bar
tb.Entry(btn_frame, textvariable=search_var, width=25).pack(side="right", padx=5)
tb.Button(btn_frame, text="Search", bootstyle="primary", command=search_contact).pack(side="right", padx=5)

# -------- Table Frame -------- #
table_frame = tb.Frame(root)
table_frame.pack(fill="both", expand=True, padx=20, pady=10)

columns = ("ID", "Name", "Phone", "Email", "Address")
contact_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

for col in columns:
    contact_table.heading(col, text=col)
    contact_table.column(col, width=150, anchor="center")

# Add scrollbar
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=contact_table.yview)
contact_table.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

contact_table.pack(fill="both", expand=True)

# Bind row click event
contact_table.bind("<ButtonRelease-1>", fill_form)

# Load initial data
fetch_contacts()

# Run the application
root.mainloop()
