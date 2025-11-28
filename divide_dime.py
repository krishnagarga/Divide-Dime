import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class DivideDime:
    def __init__(self, root):
        self.root = root
        self.root.title("Divide Dime - Expense Splitter")
        self.root.geometry("600x700")
        self.root.configure(bg="#f5f5f5")
        self.people = []
        self.expenses = []
        self.show_welcome_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_welcome_screen(self):
        self.clear_window()
        welcome_frame = tk.Frame(self.root, bg="#3d2316")
        welcome_frame.pack(fill="both", expand=True)

        try:
            logo_img = Image.open("image.jpeg").resize((300, 300), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            tk.Label(welcome_frame, image=self.logo_photo, bg="#3d2316").pack(pady=40)
        except:
            tk.Label(welcome_frame, text="DIVIDE DIME", font=("Arial", 36, "bold"), fg="white", bg="#3d2316").pack(pady=80)

        tk.Label(welcome_frame, text="Split expenses fairly among friends!", font=("Arial", 16), fg="white", bg="#3d2316").pack(pady=20)
        tk.Button(welcome_frame, text="Get Started", font=("Arial", 14, "bold"), bg="#32b8c6", fg="white", padx=40, pady=15, relief="flat", cursor="hand2", command=self.show_main_screen).pack(pady=30)

    def show_main_screen(self):
        self.clear_window()
        tk.Label(self.root, text="Divide Dime", font=("Arial", 24, "bold"), fg="white", bg="#3d2316").pack(fill="x", pady=20)

        main_frame = tk.Frame(self.root, bg="#f5f5f5")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # People section
        people_section = tk.LabelFrame(main_frame, text="Step 1: Add People", font=("Arial", 12, "bold"), bg="#f5f5f5", fg="#3d2316", padx=10, pady=10)
        people_section.pack(fill="x", pady=10)

        name_frame = tk.Frame(people_section, bg="#f5f5f5")
        name_frame.pack(fill="x", pady=5)
        tk.Label(name_frame, text="Name:", font=("Arial", 10), bg="#f5f5f5").pack(side="left", padx=5)
        self.name_entry = tk.Entry(name_frame, font=("Arial", 10), width=30)
        self.name_entry.pack(side="left", padx=5)
        tk.Button(name_frame, text="Add Person", bg="#32b8c6", fg="white", font=("Arial", 10, "bold"), relief="flat", cursor="hand2", command=self.add_person).pack(side="left", padx=5)

        self.people_listbox = tk.Listbox(people_section, height=4, font=("Arial", 10))
        self.people_listbox.pack(fill="x", pady=5)

        # Expense section
        expense_section = tk.LabelFrame(main_frame, text="Step 2: Add Expenses", font=("Arial", 12, "bold"), bg="#f5f5f5", fg="#3d2316", padx=10, pady=10)
        expense_section.pack(fill="x", pady=10)

        desc_frame = tk.Frame(expense_section, bg="#f5f5f5")
        desc_frame.pack(fill="x", pady=5)
        tk.Label(desc_frame, text="Description:", font=("Arial", 10), bg="#f5f5f5").pack(side="left", padx=5)
        self.desc_entry = tk.Entry(desc_frame, font=("Arial", 10), width=25)
        self.desc_entry.pack(side="left", padx=5)
        tk.Label(desc_frame, text="Amount (₹):", font=("Arial", 10), bg="#f5f5f5").pack(side="left", padx=5)
        self.amount_entry = tk.Entry(desc_frame, font=("Arial", 10), width=10)
        self.amount_entry.pack(side="left", padx=5)

        paid_frame = tk.Frame(expense_section, bg="#f5f5f5")
        paid_frame.pack(fill="x", pady=5)
        tk.Label(paid_frame, text="Paid by:", font=("Arial", 10), bg="#f5f5f5").pack(side="left", padx=5)
        self.paid_by_var = tk.StringVar()
        self.paid_by_combo = ttk.Combobox(paid_frame, textvariable=self.paid_by_var, font=("Arial", 10), state="readonly", width=20)
        self.paid_by_combo.pack(side="left", padx=5)
        tk.Button(paid_frame, text="Add Expense", bg="#32b8c6", fg="white", font=("Arial", 10, "bold"), relief="flat", cursor="hand2", command=self.add_expense).pack(side="left", padx=5)

        self.expenses_listbox = tk.Listbox(expense_section, height=5, font=("Arial", 10))
        self.expenses_listbox.pack(fill="x", pady=5)

        # Calculate button
        tk.Button(main_frame, text="Calculate Split", bg="#3d2316", fg="white", font=("Arial", 14, "bold"), padx=30, pady=10, relief="flat", cursor="hand2", command=self.calculate_split).pack(pady=20)

    def add_person(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Please enter a name!")
            return
        if name in self.people:
            messagebox.showwarning("Warning", "Person already added!")
            return
        self.people.append(name)
        self.people_listbox.insert(tk.END, name)
        self.paid_by_combo['values'] = self.people
        self.name_entry.delete(0, tk.END)

    def add_expense(self):
        description = self.desc_entry.get().strip()
        amount_str = self.amount_entry.get().strip()
        paid_by = self.paid_by_var.get()

        if not description or not amount_str or not paid_by:
            messagebox.showwarning("Warning", "Please fill all fields!")
            return

        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid amount!")
            return

        self.expenses.append({'description': description, 'amount': amount, 'paid_by': paid_by})
        self.expenses_listbox.insert(tk.END, f"{description} - ₹{amount:.2f} (paid by {paid_by})")
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

    def calculate_split(self):
        if not self.people or not self.expenses:
            messagebox.showwarning("Warning", "Add people and expenses first!")
            return

        total = sum(exp['amount'] for exp in self.expenses)
        per_person = total / len(self.people)
        balances = {person: -per_person for person in self.people}
        for exp in self.expenses:
            balances[exp['paid_by']] += exp['amount']

        self.show_results(total, per_person, balances)

    def calculate_settlements(self, balances):
        settlements = []
        debtors = sorted([(p, abs(b)) for p, b in balances.items() if b < -0.01], key=lambda x: x[1], reverse=True)
        creditors = sorted([(p, b) for p, b in balances.items() if b > 0.01], key=lambda x: x[1], reverse=True)

        i = j = 0
        while i < len(debtors) and j < len(creditors):
            debtor, debt = debtors[i]
            creditor, credit = creditors[j]
            amount = min(debt, credit)
            settlements.append({'from': debtor, 'to': creditor, 'amount': amount})
            debtors[i] = (debtor, debt - amount)
            creditors[j] = (creditor, credit - amount)
            if debtors[i][1] < 0.01:
                i += 1
            if creditors[j][1] < 0.01:
                j += 1

        return settlements

    def show_results(self, total, per_person, balances):
        result_window = tk.Toplevel(self.root)
        result_window.title("Split Results")
        result_window.geometry("500x600")
        result_window.configure(bg="#f5f5f5")

        tk.Label(result_window, text="Divide Dime Results", font=("Arial", 20, "bold"), bg="#3d2316", fg="white", pady=20).pack(fill="x")

        summary_frame = tk.Frame(result_window, bg="#f5f5f5")
        summary_frame.pack(fill="x", padx=20, pady=20)
        tk.Label(summary_frame, text=f"Total Expenses: ₹{total:.2f}", font=("Arial", 14, "bold"), bg="#f5f5f5", fg="#3d2316").pack(pady=5)
        tk.Label(summary_frame, text=f"Per Person Share: ₹{per_person:.2f}", font=("Arial", 14, "bold"), bg="#f5f5f5", fg="#3d2316").pack(pady=5)

        ttk.Separator(result_window, orient="horizontal").pack(fill="x", padx=20, pady=10)

        balance_frame = tk.Frame(result_window, bg="#f5f5f5")
        balance_frame.pack(fill="both", expand=True, padx=20, pady=10)
        tk.Label(balance_frame, text="Individual Balances:", font=("Arial", 12, "bold"), bg="#f5f5f5", fg="#3d2316").pack(pady=5)

        for person, balance in balances.items():
            if balance > 0.01:
                text, color = f"{person} should receive ₹{balance:.2f}", "#21803c"
            elif balance < -0.01:
                text, color = f"{person} owes ₹{abs(balance):.2f}", "#c0152f"
            else:
                text, color = f"{person} is settled up", "#626c71"
            tk.Label(balance_frame, text=text, font=("Arial", 11), bg="#f5f5f5", fg=color).pack(pady=3)

        ttk.Separator(result_window, orient="horizontal").pack(fill="x", padx=20, pady=10)

        settlement_frame = tk.Frame(result_window, bg="#f5f5f5")
        settlement_frame.pack(fill="both", expand=True, padx=20, pady=10)
        tk.Label(settlement_frame, text="Settlement Suggestions:", font=("Arial", 12, "bold"), bg="#f5f5f5", fg="#3d2316").pack(pady=5)

        for settlement in self.calculate_settlements(balances):
            text = f"💸 {settlement['from']} pays ₹{settlement['amount']:.2f} to {settlement['to']}"
            tk.Label(settlement_frame, text=text, font=("Arial", 10), bg="#f5f5f5", fg="#134252").pack(pady=3)

        tk.Button(result_window, text="Close", bg="#32b8c6", fg="white", font=("Arial", 12, "bold"), padx=30, pady=10, relief="flat", cursor="hand2", command=result_window.destroy).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = DivideDime(root)
    root.mainloop()
