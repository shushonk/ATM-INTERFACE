import tkinter as tk
from tkinter import messagebox

class ATMApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ATM Interface")
        self.state('zoomed')  # Fullscreen window (maximized)
        self.configure(bg="black")

        self.user_authenticated = False
        self.balance = 100000.00
        self.transaction_history = []

        self.container = tk.Frame(self, bg="black")
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (LoginScreen, MenuScreen, DepositScreen, WithdrawScreen, BalanceScreen):
            frame = F(parent=self.container, controller=self)
            self.frames[F.__name__] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_screen("LoginScreen")

    def show_screen(self, screen_name):
        frame = self.frames[screen_name]
        frame.tkraise()

    def logout(self):
        self.user_authenticated = False
        self.show_screen("LoginScreen")


class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="black")
        self.controller = controller

        self.label_title = tk.Label(self, text="Welcome to ATM", font=("Consolas", 48, "bold"), fg="white", bg="black")
        self.label_title.pack(pady=40)

        self.user_label = tk.Label(self, text="User ID:", font=("Consolas", 24), fg="white", bg="black")
        self.user_label.pack(pady=(20,5))
        self.user_entry = tk.Entry(self, font=("Consolas", 24), justify="center")
        self.user_entry.pack(ipady=8, padx=200)

        self.pin_label = tk.Label(self, text="PIN:", font=("Consolas", 24), fg="white", bg="black")
        self.pin_label.pack(pady=(20,5))
        self.pin_entry = tk.Entry(self, font=("Consolas", 24), justify="center", show="*")
        self.pin_entry.pack(ipady=8, padx=200)

        self.login_btn = tk.Button(self, text="Login", font=("Consolas", 28), bg="dim gray", fg="white",
                                   command=self.check_login)
        self.login_btn.pack(pady=40, ipadx=20, ipady=10)

    def check_login(self):
        user_id = self.user_entry.get()
        pin = self.pin_entry.get()

        if user_id == "123456" and pin == "654321":
            self.controller.user_authenticated = True
            messagebox.showinfo("Login Success", "Welcome!")
            self.controller.show_screen("MenuScreen")
            # Clear inputs after login
            self.user_entry.delete(0, tk.END)
            self.pin_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Login Failed", "Invalid User ID or PIN. Please try again.")


class MenuScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="black")
        self.controller = controller

        title = tk.Label(self, text="Main Menu", font=("Consolas", 48, "bold"), fg="white", bg="black")
        title.pack(pady=40)

        btn_cfg = {"font": ("Consolas", 30), "width": 20, "height": 2, "fg": "white", "relief": "raised"}

        deposit_btn = tk.Button(self, text="Deposit", command=lambda: controller.show_screen("DepositScreen"), bg="dim gray", **btn_cfg)
        deposit_btn.pack(pady=15)

        withdraw_btn = tk.Button(self, text="Withdraw", command=lambda: controller.show_screen("WithdrawScreen"), bg="dim gray", **btn_cfg)
        withdraw_btn.pack(pady=15)

        balance_btn = tk.Button(self, text="Balance", command=lambda: controller.show_screen("BalanceScreen"), bg="dim gray", **btn_cfg)
        balance_btn.pack(pady=15)

        logout_btn = tk.Button(self, text="Logout", command=controller.logout, bg="firebrick", **btn_cfg)
        logout_btn.pack(pady=15)


class DepositScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="black")
        self.controller = controller

        title = tk.Label(self, text="Deposit Money", font=("Consolas", 48, "bold"), fg="white", bg="black")
        title.pack(pady=40)

        self.amount_label = tk.Label(self, text="Enter amount to deposit:", font=("Consolas", 24), fg="white", bg="black")
        self.amount_label.pack(pady=20)

        self.amount_entry = tk.Entry(self, font=("Consolas", 24), justify="center")
        self.amount_entry.pack(ipady=8, padx=200)

        btn_cfg = {"font": ("Consolas", 28), "width": 15, "height": 2, "fg": "white"}

        deposit_btn = tk.Button(self, text="Deposit", bg="green", command=self.deposit_money, **btn_cfg)
        deposit_btn.pack(pady=20)

        back_btn = tk.Button(self, text="Back to Menu", bg="dim gray", command=lambda: controller.show_screen("MenuScreen"), **btn_cfg)
        back_btn.pack()

    def deposit_money(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError
            self.controller.balance += amount
            self.controller.transaction_history.append(f"Deposited ${amount:.2f}")
            messagebox.showinfo("Deposit Successful", f"${amount:.2f} deposited successfully!")
            self.amount_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive number.")


class WithdrawScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="black")
        self.controller = controller

        title = tk.Label(self, text="Withdraw Money", font=("Consolas", 48, "bold"), fg="white", bg="black")
        title.pack(pady=40)

        self.amount_label = tk.Label(self, text="Enter amount to withdraw:", font=("Consolas", 24), fg="white", bg="black")
        self.amount_label.pack(pady=20)

        self.amount_entry = tk.Entry(self, font=("Consolas", 24), justify="center")
        self.amount_entry.pack(ipady=8, padx=200)

        btn_cfg = {"font": ("Consolas", 28), "width": 15, "height": 2, "fg": "white"}

        withdraw_btn = tk.Button(self, text="Withdraw", bg="orange red", command=self.withdraw_money, **btn_cfg)
        withdraw_btn.pack(pady=20)

        back_btn = tk.Button(self, text="Back to Menu", bg="dim gray", command=lambda: controller.show_screen("MenuScreen"), **btn_cfg)
        back_btn.pack()

    def withdraw_money(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError
            if amount > self.controller.balance:
                messagebox.showerror("Insufficient Funds", "You do not have enough balance.")
            else:
                self.controller.balance -= amount
                self.controller.transaction_history.append(f"Withdrawn ${amount:.2f}")
                messagebox.showinfo("Withdrawal Successful", f"${amount:.2f} withdrawn successfully!")
                self.amount_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive number.")


class BalanceScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="black")
        self.controller = controller

        title = tk.Label(self, text="Account Balance", font=("Consolas", 48, "bold"), fg="white", bg="black")
        title.pack(pady=40)

        self.balance_label = tk.Label(self, text="", font=("Consolas", 36), fg="white", bg="black")
        self.balance_label.pack(pady=50)

        btn_cfg = {"font": ("Consolas", 28), "width": 15, "height": 2, "fg": "white"}

        refresh_btn = tk.Button(self, text="Refresh Balance", bg="royal blue", command=self.show_balance, **btn_cfg)
        refresh_btn.pack(pady=20)

        back_btn = tk.Button(self, text="Back to Menu", bg="dim gray", command=lambda: controller.show_screen("MenuScreen"), **btn_cfg)
        back_btn.pack()

        self.show_balance()

    def show_balance(self):
        bal = self.controller.balance
        self.balance_label.config(text=f"${bal:.2f}")


if __name__ == "__main__":
    app = ATMApp()
    app.mainloop()
