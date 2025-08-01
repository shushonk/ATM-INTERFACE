import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class ATMPhonePeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("💳 ATM & PhonePe Simulator")
        self.geometry("560x500")
        self.configure(bg="#181818")

        self.balance = 100000.0
        self.atm_pin = "2004"
        self.phonepe_pin = "2004"
        self.transactions = []

        self.title_font = ("Segoe UI", 18, "bold")
        self.text_font = ("Segoe UI", 12)

        self.show_login_screen()

    # --- Screens ---
    def show_login_screen(self):
        self.clear()
        self._title("🔐 Login to ATM")
        self.pin_entry = self._entry(show="*")
        self._animated_button("Login", self.login)

    def login(self):
        if self.pin_entry.get() == self.atm_pin:
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Incorrect PIN")

    def show_main_menu(self):
        self.clear()
        self._title("🏦 Main Menu")
        self._animated_button("💰 Check Balance", self.check_balance)
        self._animated_button("📥 Deposit", self.deposit_screen)
        self._animated_button("📤 Withdraw", self.withdraw_screen)
        self._animated_button("📲 PhonePe Transfer", self.phonepe_screen)
        self._animated_button("📄 Transaction History", self.show_transactions)
        self._animated_button("🔐 Logout", self.show_login_screen)

    def check_balance(self):
        messagebox.showinfo("Balance", f"Your current balance is ₹{self.balance:.2f}")

    def deposit_screen(self):
        self.clear()
        self._title("💵 Deposit Amount")
        self.amount_entry = self._entry()
        self._animated_button("Deposit", self.deposit)
        self._animated_button("🔙 Back", self.show_main_menu)

    def deposit(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError
            self.balance += amount
            self.add_transaction("Deposit", amount)
            messagebox.showinfo("Success", f"Deposited ₹{amount:.2f}")
            self.show_main_menu()
        except ValueError:
            messagebox.showerror("Error", "Enter a valid amount")

    def withdraw_screen(self):
        self.clear()
        self._title("💸 Withdraw Amount")
        self.amount_entry = self._entry()
        self._animated_button("Withdraw", self.withdraw)
        self._animated_button("🔙 Back", self.show_main_menu)

    def withdraw(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0 or amount > self.balance:
                messagebox.showerror("Error", "Invalid or insufficient balance")
                return
            self.balance -= amount
            self.add_transaction("Withdraw", amount)
            messagebox.showinfo("Success", f"Withdrew ₹{amount:.2f}")
            self.show_main_menu()
        except ValueError:
            messagebox.showerror("Error", "Enter a valid amount")

    def phonepe_screen(self):
        self.clear()
        self._title("📲 PhonePe Transfer")
        self.recipient_entry = self._entry("Recipient Name")
        self.phonepe_amount_entry = self._entry("Amount")
        self.phonepe_pin_entry = self._entry("PhonePe PIN", show="*")
        self._animated_button("Send", self.phonepe_transfer)
        self._animated_button("🔙 Back", self.show_main_menu)

    def phonepe_transfer(self):
        try:
            name = self.recipient_entry.get()
            amount = float(self.phonepe_amount_entry.get())
            pin = self.phonepe_pin_entry.get()
            if pin != self.phonepe_pin:
                messagebox.showerror("Error", "Incorrect PhonePe PIN")
                return
            if amount <= 0 or amount > self.balance or not name:
                raise ValueError
            self.balance -= amount
            self.add_transaction("PhonePe", amount, name)
            messagebox.showinfo("Success", f"Sent ₹{amount:.2f} to {name}")
            self.show_main_menu()
        except ValueError:
            messagebox.showerror("Error", "Invalid input or insufficient balance")

    def show_transactions(self):
        self.clear()
        self._title("📄 Transaction History")

        if not self.transactions:
            tk.Label(self, text="No transactions yet.", font=self.text_font, fg="gray", bg="#181818").pack(pady=10)
        else:
            frame = tk.Frame(self, bg="#181818")
            frame.pack(padx=20, pady=10)
            for txn in reversed(self.transactions[-15:]):
                label = tk.Label(
                    frame, text=txn,
                    anchor="w", justify="left",
                    font=("Courier New", 10),
                    bg="#262626", fg="white",
                    padx=10, pady=5
                )
                label.pack(fill="x", pady=2)

        self._animated_button("🔙 Back", self.show_main_menu)

    # --- Helper Functions ---
    def add_transaction(self, type, amount, recipient=""):
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"{time} | {type:<10} | ₹{amount:<10.2f} | {'To: ' + recipient if recipient else ''}"
        self.transactions.append(entry)

    def _title(self, text):
        tk.Label(self, text=text, font=self.title_font, bg="#181818", fg="white").pack(pady=20)

    def _entry(self, placeholder="", show=None):
        entry = tk.Entry(self, font=self.text_font, width=32, bg="#2a2a2a", fg="white", insertbackground="white", bd=0, show=show)
        entry.pack(pady=6)
        if placeholder:
            entry.insert(0, placeholder)
        return entry

    def _animated_button(self, text, command):
        btn = tk.Label(self, text=text, font=self.text_font, bg="#2f2f2f", fg="white", padx=10, pady=8, width=25, cursor="hand2")
        btn.pack(pady=6)
        btn.bind("<Enter>", lambda e: btn.config(bg="#404040"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#2f2f2f"))
        btn.bind("<Button-1>", lambda e: self.animate_click(btn, command))

    def animate_click(self, widget, callback):
        original = widget.cget("bg")
        widget.config(bg="#606060")
        self.after(100, lambda: widget.config(bg=original))
        self.after(150, callback)

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = ATMPhonePeApp()
    app.mainloop()
