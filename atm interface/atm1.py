import tkinter as tk
from tkinter import font, messagebox, ttk

class ATMApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ATM Machine Simulator")
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

        # Internal input state
        self.input_value = ""
        self.current_passcode = ""
        self.current_screen = None

        # Container frame
        self.container = tk.Frame(self, bg="black")
        self.container.pack(expand=True, fill="both")

        # Start with login screen
        self.show_login_screen()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_container()
        self.current_screen = "login"
        frame = tk.Frame(self.container, bg="black")
        frame.pack(expand=True)

        tk.Label(frame, text="Welcome to ATM", fg="cyan", bg="black", font=self.title_font).pack(pady=20)
        tk.Label(frame, text="Enter your 4-digit PIN", fg="white", bg="black", font=self.msg_font).pack(pady=10)

        self.input_value = ""
        self.pin_display = tk.Label(frame, text="• " * 0, fg="white", bg="#111", font=self.title_font,
                                    width=10, height=2, relief="sunken", bd=4)
        self.pin_display.pack(pady=10)

        keypad = self.build_keypad(frame, self.on_pin_press, self.clear_input, self.login_attempt)
        keypad.pack(pady=10)

        self.btn_exit = tk.Button(frame, text="Exit", font=self.btn_font, bg="#b22222", fg="white",
                                  command=self.quit, width=10)
        self.btn_exit.pack(pady=10)

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

    def on_pin_press(self, num):
        if len(self.input_value) < 4:
            self.input_value += str(num)
            self.pin_display.config(text="• " * len(self.input_value))

    def clear_input(self):
        self.input_value = ""
        if self.current_screen == "login":
            self.pin_display.config(text="• " * 0)
        else:
            self.input_display.config(text="")

    def login_attempt(self):
        if self.input_value == self.user_pin:
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Incorrect PIN. Try again.")
            self.clear_input()

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
            ("Logout", self.show_login_screen)
        ]

        for (text, cmd) in buttons:
            btn = tk.Button(frame, text=text, font=self.btn_font, fg="white", bg="#222",
                            activebackground="cyan", width=20, height=2, command=cmd)
            btn.pack(pady=10)

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

    def show_transfer_screen(self):
        self.clear_container()
        self.current_screen = "transfer"
        frame = tk.Frame(self.container, bg="black")
        frame.pack(expand=True)

        tk.Label(frame, text="Transfer Amount", fg="cyan", bg="black", font=self.title_font).pack(pady=20)

        self.input_value = ""
        self.input_display = tk.Label(frame, text="", fg="white", bg="#111", font=self.title_font,
                                      width=20, height=2, relief="sunken", bd=4)
        self.input_display.pack(pady=10)

        keypad = self.build_keypad(frame, self.on_input_press, self.clear_input, self.transfer_amount_entered)
        keypad.pack(pady=10)

        tk.Label(frame, text="Recipient Name", fg="white", bg="black", font=self.msg_font).pack(pady=5)
        self.recipient_entry = tk.Entry(frame, font=self.btn_font, width=20)
        self.recipient_entry.pack(pady=5)

        self.passcode_label = tk.Label(frame, text="Enter Passcode (4 or 6 digits)", fg="white", bg="black",
                                      font=self.msg_font)
        self.passcode_label.pack(pady=5)

        self.passcode_entry = tk.Entry(frame, show="*", font=self.btn_font, width=15)
        self.passcode_entry.pack(pady=5)

        btn_back = tk.Button(frame, text="Back", font=self.btn_font, fg="white", bg="#b22222",
                             activebackground="#ff5555", width=10, command=self.show_main_menu)
        btn_back.pack(pady=10)

    def show_balance_screen(self):
        self.clear_container()
        frame = tk.Frame(self.container, bg="black")
        frame.pack(expand=True)
        tk.Label(frame, text="Account Balance", fg="cyan", bg="black", font=self.title_font).pack(pady=20)
        tk.Label(frame, text=f"₹ {self.balance:,.2f}", fg="white", bg="black", font=self.title_font).pack(pady=20)
        btn_back = tk.Button(frame, text="Back", font=self.btn_font, fg="white", bg="#b22222",
                             activebackground="#ff5555", width=15, command=self.show_main_menu)
        btn_back.pack(pady=20)

    def show_transactions_screen(self):
        self.clear_container()
        frame = tk.Frame(self.container, bg="black")
        frame.pack(expand=True, fill="both")

        tk.Label(frame, text="Transaction History", fg="cyan", bg="black", font=self.title_font).pack(pady=20)

        # Table with scroll
        columns = ("Type", "Amount", "Recipient", "Balance")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        tree.pack(pady=10, expand=True, fill="both")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        for txn in self.transaction_history:
            tree.insert("", "end", values=txn)

        btn_back = tk.Button(frame, text="Back", font=self.btn_font, fg="white", bg="#b22222",
                             activebackground="#ff5555", width=15, command=self.show_main_menu)
        btn_back.pack(pady=20)

    def on_input_press(self, num):
        if len(self.input_value) < 12:  # Limit input length
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

    def withdraw_action(self):
        if not self.validate_amount():
            return
        amount = float(self.input_value)
        passcode = self.passcode_entry.get()
        if self.validate_passcode(passcode):
            if amount > self.balance:
                messagebox.showerror("Error", "Insufficient balance.")
                self.clear_input()
                self.passcode_entry.delete(0, tk.END)
                return
            self.balance -= amount
            self.transaction_history.append(("Withdraw", f"₹{amount:.2f}", "-", f"₹{self.balance:.2f}"))
            messagebox.showinfo("Success", f"₹{amount:.2f} withdrawn successfully!")
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Invalid passcode. Transaction canceled.")
            self.clear_input()
            self.passcode_entry.delete(0, tk.END)

    def transfer_amount_entered(self):
        if not self.validate_amount():
            return
        recipient = self.recipient_entry.get().strip()
        if not recipient:
            messagebox.showerror("Error", "Please enter a recipient name.")
            return
        passcode = self.passcode_entry.get()
        if self.validate_passcode(passcode):
            amount = float(self.input_value)
            if amount > self.balance:
                messagebox.showerror("Error", "Insufficient balance.")
                self.clear_input()
                self.passcode_entry.delete(0, tk.END)
                return
            self.balance -= amount
            self.transaction_history.append(("Transfer", f"₹{amount:.2f}", recipient, f"₹{self.balance:.2f}"))
            messagebox.showinfo("Success", f"₹{amount:.2f} transferred to {recipient} successfully!")
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Invalid passcode. Transaction canceled.")
            self.clear_input()
            self.passcode_entry.delete(0, tk.END)

    def validate_amount(self):
        if not self.input_value:
            messagebox.showerror("Error", "Please enter an amount.")
            return False
        try:
            amount = float(self.input_value)
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than zero.")
                return False
            return True
        except ValueError:
            messagebox.showerror("Error", "Invalid amount entered.")
            return False

    def validate_passcode(self, passcode):
        # Dummy validation: passcode must be length 4 or 6 digits, and numeric
        return passcode.isdigit() and (len(passcode) == 4 or len(passcode) == 6)

if __name__ == "__main__":
    app = ATMApp()
    app.mainloop()
