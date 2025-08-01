import tkinter as tk
from tkinter import font, messagebox, ttk

class ATMApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ATM Machine Simulator with Phone Pay")
        self.configure(bg="black")
        self.attributes('-fullscreen', True)

        # Fonts
        self.title_font = font.Font(family="Segoe UI", size=28, weight="bold")
        self.btn_font = font.Font(family="Segoe UI", size=16, weight="bold")
        self.msg_font = font.Font(family="Segoe UI", size=18)

        # ATM data
        self.user_pin = "1234"
        self.balance = 100000.0
        self.transaction_history = []

        # Internal input states
        self.input_value = ""
        self.passcode_value = ""
        self.phonepay_data = None
        self.current_screen = None

        # Container frame
        self.container = tk.Frame(self, bg="black")
        self.container.pack(expand=True, fill="both")

        # Start with login screen
        self.show_login_screen()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    # --------- LOGIN SCREEN ----------
    def show_login_screen(self):
        self.clear_container()
        self.current_screen = "login"
        frame = tk.Frame(self.container, bg="black")
        frame.pack(expand=True)

        tk.Label(frame, text="Welcome to ATM", fg="cyan", bg="black", font=self.title_font).pack(pady=20)
        tk.Label(frame, text="Enter your 4-digit PIN", fg="white", bg="black", font=self.msg_font).pack(pady=10)

        self.input_value = ""
        self.pin_display = tk.Label(frame, text="", fg="white", bg="#111", font=self.title_font,
                                    width=10, height=2, relief="sunken", bd=4)
        self.pin_display.pack(pady=10)

        keypad = self.build_keypad(frame, self.on_pin_press, self.clear_input, self.login_attempt)
        keypad.pack(pady=10)

        tk.Button(frame, text="Exit", font=self.btn_font, bg="#b22222", fg="white", width=10,
                  command=self.quit).pack(pady=10)

    def on_pin_press(self, num):
        if len(self.input_value) < 4:
            self.input_value += str(num)
            self.pin_display.config(text="• " * len(self.input_value))

    def clear_input(self):
        self.input_value = ""
        if self.current_screen == "login":
            self.pin_display.config(text="")
        elif hasattr(self, "input_display"):
            self.input_display.config(text="")
        if hasattr(self, "amount_display"):
            self.amount_display.config(text="")
        if hasattr(self, "passcode_display"):
            self.passcode_display.config(text="")
        self.passcode_value = ""

    def login_attempt(self):
        if self.input_value == self.user_pin:
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Incorrect PIN. Try again.")
            self.clear_input()

    # --------- MAIN MENU ----------
    def show_main_menu(self):
        self.clear_container()
        self.current_screen = "menu"
        frame = tk.Frame(self.container, bg="black")
        frame.pack(expand=True)

        tk.Label(frame, text="Select Operation", fg="cyan", bg="black", font=self.title_font).pack(pady=20)

        buttons = [
            ("Deposit", self.show_deposit_screen),
            ("Withdraw", self.show_withdraw_screen),
            ("Transfer", self.show_transfer_screen),
            ("Balance", self.show_balance_screen),
            ("Transactions", self.show_transactions_screen),
            ("Phone Pay", self.show_phonepay_screen),
            ("Logout", self.show_login_screen)
        ]

        for (text, cmd) in buttons:
            btn = tk.Button(frame, text=text, font=self.btn_font, fg="white", bg="#222",
                            activebackground="cyan", width=20, height=2, command=cmd)
            btn.pack(pady=10)

    # --------- KEYPAD BUILDER ----------
    def build_keypad(self, parent, num_cmd, clear_cmd, enter_cmd):
        keypad_frame = tk.Frame(parent, bg="black")
        # Buttons 1-9
        for i in range(1, 10):
            btn = tk.Button(keypad_frame, text=str(i), font=self.btn_font, fg="white", bg="#222",
                            activebackground="cyan", width=5, height=2,
                            command=lambda x=i: num_cmd(x))
            btn.grid(row=(i-1)//3, column=(i-1)%3, padx=8, pady=8)
        # Clear, 0, Enter
        btn_clear = tk.Button(keypad_frame, text="Clear", font=self.btn_font, fg="white", bg="#b22222",
                              activebackground="#ff5555", width=5, height=2,
                              command=clear_cmd)
        btn_clear.grid(row=3, column=0, padx=8, pady=8)

        btn_zero = tk.Button(keypad_frame, text="0", font=self.btn_font, fg="white", bg="#222",
                             activebackground="cyan", width=5, height=2,
                             command=lambda: num_cmd(0))
        btn_zero.grid(row=3, column=1, padx=8, pady=8)

        btn_enter = tk.Button(keypad_frame, text="Enter", font=self.btn_font, fg="white", bg="#228b22",
                              activebackground="#55ff55", width=5, height=2,
                              command=enter_cmd)
        btn_enter.grid(row=3, column=2, padx=8, pady=8)
        return keypad_frame

    # --------- DEPOSIT ----------
    def show_deposit_screen(self):
        self.clear_container()
        self.current_screen = "deposit"
        frame = tk.Frame(self.container, bg="black")
        frame.pack(expand=True)

        tk.Label(frame, text="Deposit Amount", fg="cyan", bg="black", font=self.title_font).pack(pady=20)

        self.input_value = ""
        self.input_display = tk.Label(frame, text="", fg="white", bg="#111", font=self.title_font,
                                      width=20, height=2, relief="sunken", bd=4)
        self.input_display.pack(pady=10)

        keypad = self.build_keypad(frame, self.on_input_press, self.clear_input, self.deposit_action)
        keypad.pack(pady=10)

        self.passcode_label = tk.Label(frame, text="Enter Passcode (4 or 6 digits)", fg="white", bg="black",
                                       font=self.msg_font)
        self.passcode_label.pack(pady=5)

        self.passcode_entry = tk.Entry(frame, show="*", font=self.btn_font, width=15)
        self.passcode_entry.pack(pady=5)

        btn_back = tk.Button(frame, text="Back", font=self.btn_font, fg="white", bg="#b22222",
                             activebackground="#ff5555", width=10, command=self.show_main_menu)
        btn_back.pack(pady=10)

    def on_input_press(self, num):
        if len(self.input_value) < 12:
            self.input_value += str(num)
            self.input_display.config(text=self.input_value)

    def deposit_action(self):
        if not self.validate_amount():
            return
        amount = float(self.input_value)
        passcode = self.passcode_entry.get()
        if self.validate_passcode(passcode):
            self.balance += amount
            self.transaction_history.append(("Deposit", f"₹{amount:.2f}", "-", f"₹{self.balance:.2f}"))
            messagebox.showinfo("Success", f"₹{amount:.2f} deposited successfully!")
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Invalid passcode. Transaction canceled.")
            self.clear_input()
            self.passcode_entry.delete(0, tk.END)

    # --------- WITHDRAW ----------
    def show_withdraw_screen(self):
        self.clear_container()
        self.current_screen = "withdraw"
        frame = tk.Frame(self.container, bg="black")
        frame.pack(expand=True)

        tk.Label(frame, text="Withdraw Amount", fg="cyan", bg="black", font=self.title_font).pack(pady=20)

        self.input_value = ""
        self.input_display = tk.Label(frame, text="", fg="white", bg="#111", font=self.title_font,
                                      width=20, height=2, relief="sunken", bd=4)
        self.input_display.pack(pady=10)

        keypad = self.build_keypad(frame, self.on_input_press, self.clear_input, self.withdraw_action)
        keypad.pack(pady=10)

        self.passcode_label = tk.Label(frame, text="Enter Passcode (4 or 6 digits)", fg="white", bg="black",
                                       font=self.msg_font)
        self.passcode_label.pack(pady=5)

        self.passcode_entry = tk.Entry(frame, show="*", font=self.btn_font, width=15)
        self.passcode_entry.pack(pady=5)

        btn_back = tk.Button(frame, text="Back", font=self.btn_font, fg="white", bg="#b22222",
                             activebackground="#ff5555", width=10, command=self.show_main_menu)
        btn_back.pack(pady=10)

    def withdraw_action(self):
        if not self.validate_amount():
            return
        amount = float(self.input_value)
        if amount > self.balance:
            messagebox.showerror("Error", "Insufficient balance.")
            self.clear_input()
            return
        passcode = self.passcode_entry.get()
        if self.validate_passcode(passcode):
            self.balance -= amount
            self.transaction_history.append(("Withdraw", f"₹{amount:.2f}", "-", f"₹{self.balance:.2f}"))
            messagebox.showinfo("Success", f"₹{amount:.2f} withdrawn successfully!")
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Invalid passcode. Transaction canceled.")
            self.clear_input()
            self.passcode_entry.delete(0, tk.END)

    # --------- TRANSFER ----------
    def show_transfer_screen(self):
        self.clear_container()
        self.current_screen = "transfer"
        frame = tk.Frame(self.container, bg="black")
        frame.pack(expand=True)

        tk.Label(frame, text="Transfer Money", fg="cyan", bg="black", font=self.title_font).pack(pady=20)

        tk.Label(frame, text="Recipient Account Number", fg="white", bg="black", font=self.msg_font).pack(pady=5)
        self.recipient_entry = tk.Entry(frame, font=self.btn_font, width=25)
        self.recipient_entry.pack(pady=5)

        tk.Label(frame, text="Amount", fg="white", bg="black", font=self.msg_font).pack(pady=5)
        self.input_value = ""
        self.input_display = tk.Label(frame, text="", fg="white", bg="#111", font=self.title_font,
                                      width=20, height=2, relief="sunken", bd=4)
        self.input_display.pack(pady=5)

        keypad = self.build_keypad(frame, self.on_input_press, self.clear_input, self.transfer_action)
        keypad.pack(pady=10)

        self.passcode_label = tk.Label(frame, text="Enter Passcode (4 or 6 digits)", fg="white", bg="black",
                                       font=self.msg_font)
        self.passcode_label.pack(pady=5)

        self.passcode_entry = tk.Entry(frame, show="*", font=self.btn_font, width=15)
        self.passcode_entry.pack(pady=5)

        btn_back = tk.Button(frame, text="Back", font=self.btn_font, fg="white", bg="#b22222",
                             activebackground="#ff5555", width=10, command=self.show_main_menu)
        btn_back.pack(pady=10)

    def transfer_action(self):
        recipient = self.recipient_entry.get().strip()
        if not recipient.isdigit() or len(recipient) < 6:
            messagebox.showerror("Error", "Enter valid recipient account number (min 6 digits).")
            return
        if not self.validate_amount():
            return
        amount = float(self.input_value)
        if amount > self.balance:
            messagebox.showerror("Error", "Insufficient balance.")
            self.clear_input()
            return
        passcode = self.passcode_entry.get()
        if self.validate_passcode(passcode):
            self.balance -= amount
            self.transaction_history.append(("Transfer", f"₹{amount:.2f}", recipient, f"₹{self.balance:.2f}"))
            messagebox.showinfo("Success", f"₹{amount:.2f} transferred to {recipient} successfully!")
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Invalid passcode. Transaction canceled.")
            self.clear_input()
            self.passcode_entry.delete(0, tk.END)

    # --------- BALANCE ----------
    def show_balance_screen(self):
        self.clear_container()
        self.current_screen = "balance"
        frame = tk.Frame(self.container, bg="black")
        frame.pack(expand=True)

        tk.Label(frame, text="Current Balance", fg="cyan", bg="black", font=self.title_font).pack(pady=20)
        tk.Label(frame, text=f"₹{self.balance:.2f}", fg="white", bg="black", font=self.title_font).pack(pady=20)

        btn_back = tk.Button(frame, text="Back to Menu", font=self.btn_font, fg="white", bg="#222",
                             activebackground="cyan", width=20, command=self.show_main_menu)
        btn_back.pack(pady=20)

    # --------- TRANSACTIONS HISTORY ----------
    def show_transactions_screen(self):
        self.clear_container()
        self.current_screen = "transactions"
        frame = tk.Frame(self.container, bg="black")
        frame.pack(expand=True, fill="both")

        tk.Label(frame, text="Transaction History", fg="cyan", bg="black", font=self.title_font).pack(pady=10)

        columns = ("Type", "Amount", "Recipient/Remarks", "Balance After")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=180, anchor=tk.CENTER)
        for trx in self.transaction_history:
            tree.insert("", tk.END, values=trx)
        tree.pack(expand=True, fill="both", padx=10, pady=10)

        btn_back = tk.Button(frame, text="Back to Menu", font=self.btn_font, fg="white", bg="#222",
                             activebackground="cyan", width=20, command=self.show_main_menu)
        btn_back.pack(pady=10)

    # --------- PHONE PAY ----------
    def show_phonepay_screen(self):
        self.clear_container()
        self.current_screen = "phonepay"
        frame = tk.Frame(self.container, bg="black")
        frame.pack(expand=True)

        tk.Label(frame, text="Phone Pay - Send Money", fg="cyan", bg="black", font=self.title_font).pack(pady=20)

        tk.Label(frame, text="Recipient Phone Number (10 digits)", fg="white", bg="black", font=self.msg_font).pack(pady=5)
        self.phone_entry = tk.Entry(frame, font=self.btn_font, width=25)
        self.phone_entry.pack(pady=5)

        tk.Label(frame, text="Amount (₹)", fg="white", bg="black", font=self.msg_font).pack(pady=5)
        self.input_value = ""
        self.amount_display = tk.Label(frame, text="", fg="white", bg="#111", font=self.title_font,
                                       width=20, height=2, relief="sunken", bd=4)
        self.amount_display.pack(pady=5)

        keypad = self.build_keypad(frame, self.on_amount_press, self.clear_amount, self.phonepay_next_step)
        keypad.pack(pady=10)

        tk.Label(frame, text="Remarks (Optional)", fg="white", bg="black", font=self.msg_font).pack(pady=5)
        self.remarks_entry = tk.Entry(frame, font=self.btn_font, width=25)
        self.remarks_entry.pack(pady=5)

        btn_cancel = tk.Button(frame, text="Cancel", font=self.btn_font, fg="white", bg="#b22222",
                               activebackground="#ff5555", width=15, command=self.show_main_menu)
        btn_cancel.pack(pady=15)

    def on_amount_press(self, num):
        if len(self.input_value) < 12:
            self.input_value += str(num)
            self.amount_display.config(text=self.input_value)

    def clear_amount(self):
        self.input_value = ""
        self.amount_display.config(text="")

    def phonepay_next_step(self):
        phone = self.phone_entry.get().strip()
        if not (phone.isdigit() and len(phone) == 10):
            messagebox.showerror("Error", "Enter a valid 10-digit phone number.")
            return
        if not self.input_value:
            messagebox.showerror("Error", "Enter amount to send.")
            return
        try:
            amount = float(self.input_value)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter a valid positive amount.")
            return

        self.phonepay_data = {
            "phone": phone,
            "amount": amount,
            "remarks": self.remarks_entry.get().strip()
        }
        self.show_phonepay_passcode_screen()

    def show_phonepay_passcode_screen(self):
        self.clear_container()
        self.current_screen = "phonepay_passcode"
        frame = tk.Frame(self.container, bg="black")
        frame.pack(expand=True)

        tk.Label(frame, text="Enter Passcode to Confirm", fg="cyan", bg="black", font=self.title_font).pack(pady=20)

        self.passcode_value = ""
        self.passcode_display = tk.Label(frame, text="", fg="white", bg="#111", font=self.title_font,
                                         width=20, height=2, relief="sunken", bd=4)
        self.passcode_display.pack(pady=10)

        keypad = self.build_keypad(frame, self.on_passcode_press, self.clear_passcode, self.phonepay_confirm)
        keypad.pack(pady=10)

        btn_cancel = tk.Button(frame, text="Cancel", font=self.btn_font, fg="white", bg="#b22222",
                               activebackground="#ff5555", width=15, command=self.show_phonepay_screen)
        btn_cancel.pack(pady=20)

    def on_passcode_press(self, num):
        if len(self.passcode_value) < 6:
            self.passcode_value += str(num)
            self.passcode_display.config(text="• " * len(self.passcode_value))

    def clear_passcode(self):
        self.passcode_value = ""
        self.passcode_display.config(text="")

    def phonepay_confirm(self):
        if len(self.passcode_value) not in (4, 6):
            messagebox.showerror("Error", "Passcode must be 4 or 6 digits.")
            self.clear_passcode()
            return

        amount = self.phonepay_data["amount"]
        if amount > self.balance:
            messagebox.showerror("Error", "Insufficient balance.")
            self.show_main_menu()
            return

        # Deduct balance and log transaction
        self.balance -= amount
        recipient = f"Phone: {self.phonepay_data['phone']}"
        remarks = self.phonepay_data.get("remarks", "")
        if remarks:
            recipient += f" ({remarks})"

        self.transaction_history.append(("Phone Pay", f"₹{amount:.2f}", recipient, f"₹{self.balance:.2f}"))
        messagebox.showinfo("Success", f"₹{amount:.2f} sent to {self.phonepay_data['phone']} successfully!")
        self.show_main_menu()

    # --------- VALIDATORS ----------
    def validate_amount(self):
        if not self.input_value:
            messagebox.showerror("Error", "Enter amount.")
            return False
        try:
            amount = float(self.input_value)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid amount.")
            return False
        return True

    def validate_passcode(self, passcode):
        return passcode.isdigit() and len(passcode) in (4, 6)

if __name__ == "__main__":
    app = ATMApp()
    app.mainloop()
