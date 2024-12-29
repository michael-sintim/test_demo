import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import psycopg2
from datetime import datetime

class ExpenseTracker:
    def __init__(self, master):
        self.master = master
        self.master.title("Expense Tracker")
        self.master.geometry("700x500")

        # Database connection
        self.conn = psycopg2.connect(
            dbname="Employee",  # Replace with your database name
            user="postgres",  # Your PostgreSQL user
            password="672345",  # Your PostgreSQL password
            host="localhost",
            port="5432"
        )
        self.cursor = self.conn.cursor()

        # Ensure the expenses table exists
        self.create_expenses_table()

        # Default Categories
        self.categories = [
            "Food", "Transportation", "Housing",
            "Utilities", "Entertainment",
            "Shopping", "Healthcare",
            "Education", "Miscellaneous"
        ]

        # Create UI Components
        self.create_widgets()

        # Load existing expenses
        self.load_expenses()

    def create_expenses_table(self):
        """Create the expenses table if it doesn't exist"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS expenses (
            id SERIAL PRIMARY KEY,
            date DATE NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            category VARCHAR(100) NOT NULL,
            description TEXT
        );
        """
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def create_widgets(self):
        # Expense Input Frame
        input_frame = ttk.LabelFrame(self.master, text="Add New Expense")
        input_frame.pack(padx=10, pady=10, fill="x")

        # Amount Entry
        ttk.Label(input_frame, text="Amount ($):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.amount_entry = ttk.Entry(input_frame, width=20)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        # Category Dropdown
        ttk.Label(input_frame, text="Category:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(
            input_frame,
            textvariable=self.category_var,
            values=self.categories,
            width=20
        )
        self.category_dropdown.grid(row=0, column=3, padx=5, pady=5)

        # Description Entry
        ttk.Label(input_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.description_entry = ttk.Entry(input_frame, width=50)
        self.description_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

        # Add Expense Button
        ttk.Button(input_frame, text="Add Expense", command=self.add_expense).grid(
            row=2, column=0, columnspan=4, padx=5, pady=5
        )

        # Expenses Treeview
        self.tree_frame = ttk.Frame(self.master)
        self.tree_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Scrollbar for Treeview
        tree_scroll = ttk.Scrollbar(self.tree_frame)
        tree_scroll.pack(side="right", fill="y")

        # Treeview
        self.expense_tree = ttk.Treeview(
            self.tree_frame,
            columns=("Date", "Amount", "Category", "Description"),
            show="headings",
            yscrollcommand=tree_scroll.set
        )
        self.expense_tree.heading("Date", text="Date")
        self.expense_tree.heading("Amount", text="Amount")
        self.expense_tree.heading("Category", text="Category")
        self.expense_tree.heading("Description", text="Description")

        self.expense_tree.column("Date", width=100, anchor="center")
        self.expense_tree.column("Amount", width=100, anchor="e")
        self.expense_tree.column("Category", width=150, anchor="center")
        self.expense_tree.column("Description", width=250)
        self.expense_tree.pack(side="left", fill="both", expand=True)
        tree_scroll.config(command=self.expense_tree.yview)

        # Buttons Frame
        button_frame = ttk.Frame(self.master)
        button_frame.pack(padx=10, pady=10, fill="x")

        # Buttons
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_expense).pack(side="left", padx=5)
        ttk.Button(button_frame, text="View Summary", command=self.view_summary).pack(side="left", padx=5)

    def load_expenses(self):
        """Load expenses from the database and display them in the treeview"""
        query = "SELECT date, amount, category, description FROM expenses"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        for row in rows:
            self.expense_tree.insert("", "end", values=row)

    def add_expense(self):
        """Add a new expense to the database"""
        amount = self.amount_entry.get()
        category = self.category_var.get()
        description = self.description_entry.get()

        if not amount or not category:
            messagebox.showwarning("Input Error", "Please enter all required fields.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid amount.")
            return

        date = datetime.now().strftime("%Y-%m-%d")
        new_expense = [date, f"{amount:.2f}", category, description]

        # Insert expense into the database
        insert_query = """
        INSERT INTO expenses (date, amount, category, description)
        VALUES (%s, %s, %s, %s);
        """
        self.cursor.execute(insert_query, (date, amount, category, description))
        self.conn.commit()

        # Update the treeview
        self.expense_tree.insert("", "end", values=new_expense)
        self.amount_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.category_var.set("")

    def delete_expense(self):
        """Delete the selected expense from the database and treeview"""
        selected_item = self.expense_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an expense to delete.")
            return

        for item in selected_item:
            # Get the values of the selected row
            expense = self.expense_tree.item(item)['values']
            date, amount, category, description = expense

            # Delete the expense from the database
            delete_query = """
            DELETE FROM expenses WHERE date = %s AND amount = %s AND category = %s AND description = %s;
            """
            self.cursor.execute(delete_query, (date, amount, category, description))
            self.conn.commit()

            # Delete the expense from the treeview
            self.expense_tree.delete(item)

    def view_summary(self):
        """View a summary of expenses grouped by category"""
        query = "SELECT category, SUM(amount) FROM expenses GROUP BY category"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        summary = "\n".join(f"{category}: ${total:.2f}" for category, total in rows)
        messagebox.showinfo("Expense Summary", summary if summary else "No expenses recorded.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
