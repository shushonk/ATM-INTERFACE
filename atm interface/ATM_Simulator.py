import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class ATMPhonePeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ATM & PhonePe Simulator")
        self.geometry("520x420")
        self.configure(bg="#121212")

        # State
        self.balance = 100000.0  # Starting balance
        self.atm_pin = "2004"
        self.phonepe_pin = "2004"
        self.transactions = []  # In-memory transaction log

        # Fonts
        self.title_font = ("Helvetica", 20, "bold")
        self.text_font = ("Helvetica", 13)

        self.show_login_screen()

    def show_login_screen(self):
        self.clear()
        tk.Label(self, text="🔐 Enter ATM PIN", font=self.title_font, bg="#121212", fg="white").pack(pady=20)
        self.pin_entry = tk.Entry(self, show="*", font=self.text_font, width=20)
        self.pin_entry.pack(pady=10)
        tk.Button(self, text="Login", font=self.text_font, bg="#1f1f1f", fg="white", command=self.login).pack(pady=5)

    def login(self):
        if self.pin_entry.get() == self.atm_pin:
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Incorrect PIN")

    def show_main_menu(self):
        self.clear()
        tk.Label(self, text="🏦 Main Menu", font=self.title_font, bg="#121212", fg="white").pack(pady=20)
        self.create_button("💰 Check Balance", self.check_balance)
        self.create_button("📤 Withdraw", self.withdraw_screen)
        self.create_button("📥 Deposit", self.deposit_screen)
        self.create_button("📲 PhonePe Transfer", self.phonepe_screen)
        self.create_button("📄 Transaction History", self.show_transactions)
        self.create_button("🔐 Logout", self.show_login_screen)

    def create_button(self, text, command):
        tk.Button(self, text=text, font=self.text_font, width=25, bg="#2c2c2c", fg="white", command=command).pack(pady=5)

    def check_balance(self):
        messagebox.showinfo("Balance", f"Your current balance is ₹{self.balance:.2f}")

    def withdraw_screen(self):
        self.clear()
        tk.Label(self, text="💸 Withdraw Money", font=self.title_font, bg="#121212", fg="white").pack(pady=20)
        self.amount_entry = tk.Entry(self, font=self.text_font)
        self.amount_entry.pack(pady=10)
        tk.Button(self, text="Withdraw", font=self.text_font, bg="#2c2c2c", fg="white", command=self.withdraw).pack(pady=5)
        self.create_button("🔙 Back", self.show_main_menu)

    def withdraw(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError
            if amount > self.balance:
                messagebox.showerror("Error", "Insufficient balance")
            else:
                self.balance -= amount
                self.log_transaction("Withdraw", amount)
                messagebox.showinfo("Success", f"Withdrew ₹{amount:.2f}")
                self.show_main_menu()
        except ValueError:
            messagebox.showerror("Error", "Enter a valid amount")

    def deposit_screen(self):
        self.clear()
        tk.Label(self, text="💵 Deposit Money", font=self.title_font, bg="#121212", fg="white").pack(pady=20)
        self.amount_entry = tk.Entry(self, font=self.text_font)
        self.amount_entry.pack(pady=10)
        tk.Button(self, text="Deposit", font=self.text_font, bg="#2c2c2c", fg="white", command=self.deposit).pack(pady=5)
        self.create_button("🔙 Back", self.show_main_menu)

    def deposit(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError
            self.balance += amount
            self.log_transaction("Deposit", amount)
            messagebox.showinfo("Success", f"Deposited ₹{amount:.2f}")
            self.show_main_menu()
        except ValueError:
            messagebox.showerror("Error", "Enter a valid amount")

    def phonepe_screen(self):
        self.clear()
        tk.Label(self, text="📲 PhonePe Transfer", font=self.title_font, bg="#121212", fg="white").pack(pady=10)
        self.recipient_entry = tk.Entry(self, font=self.text_font)
        self.recipient_entry.insert(0, "Recipient Name")
        self.recipient_entry.pack(pady=5)

        self.phonepe_amount_entry = tk.Entry(self, font=self.text_font)
        self.phonepe_amount_entry.insert(0, "Amount")
        self.phonepe_amount_entry.pack(pady=5)

        self.phonepe_pin_entry = tk.Entry(self, show="*", font=self.text_font)
        self.phonepe_pin_entry.pack(pady=5)

        tk.Button(self, text="Send", font=self.text_font, bg="#2c2c2c", fg="white", command=self.phonepe_transfer).pack(pady=5)
        self.create_button("🔙 Back", self.show_main_menu)

    def phonepe_transfer(self):
        try:
            name = self.recipient_entry.get()
            amount = float(self.phonepe_amount_entry.get())
            entered_pin = self.phonepe_pin_entry.get()
            if amount <= 0 or not name:
                raise ValueError
            if entered_pin != self.phonepe_pin:
                messagebox.showerror("Error", "Incorrect PhonePe PIN")
            elif amount > self.balance:
                messagebox.showerror("Error", "Insufficient balance")
            else:
                self.balance -= amount
                self.log_transaction("PhonePe", amount, name)
                messagebox.showinfo("Success", f"Sent ₹{amount:.2f} to {name}")
                self.show_main_menu()
        except ValueError:
            messagebox.showerror("Error", "Invalid details")

    def show_transactions(self):
        self.clear()
        tk.Label(self, text="📄 Transaction History", font=self.title_font, bg="#121212", fg="white").pack(pady=10)
        text_box = tk.Text(self, height=15, width=60, bg="#1e1e1e", fg="white", font=("Courier", 10))
        text_box.pack()

        if not self.transactions:
            text_box.insert(tk.END, "No transactions yet.")
        else:
            for entry in self.transactions:
                text_box.insert(tk.END, entry + "\n")

        self.create_button("🔙 Back", self.show_main_menu)

    def log_transaction(self, type, amount, recipient=""):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if recipient:
            entry = f"{timestamp} | {type:<10} | ₹{amount:<10.2f} | To: {recipient}"
        else:
            entry = f"{timestamp} | {type:<10} | ₹{amount:<10.2f}"
        self.transactions.append(entry)

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = ATMPhonePeApp()
    app.mainloop()
