import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime
import calendar

class MoneyControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Money Control")
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year
        self.expenses = {}
        self.incomes = {}
        self.show_month_view()

    def show_month_view(self):
        self.clear_frame()
        month_name = calendar.month_name[self.current_month]
        label = tk.Label(self.root, text=f"{month_name} {self.current_year}", font=("Arial", 16))
        label.grid(row=0, column=0, columnspan=7)

        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        for i, day in enumerate(days):
            tk.Label(self.root, text=day, font=("Arial", 12)).grid(row=1, column=i)

        first_day_of_month = datetime(self.current_year, self.current_month, 1)
        num_days = calendar.monthrange(self.current_year, self.current_month)[1]

        start_day = first_day_of_month.weekday()
        start_day = (start_day + 1) % 7

        for day in range(1, num_days + 1):
            date = datetime(self.current_year, self.current_month, day)
            expense_count = len(self.expenses.get(date.date(), []))
            income_count = len(self.incomes.get(date.date(), []))

            color_expense = "red" if expense_count > 0 else "black"
            color_income = "green" if income_count > 0 else "black"

            button = tk.Button(self.root, text=f"{day}\n{income_count} / {expense_count}",
                               fg=color_income if income_count > 0 else color_expense,
                               command=lambda d=day: self.show_day_view(d))
            button.grid(row=(day + start_day) // 7 + 2, column=(day + start_day) % 7)

        prev_button = tk.Button(self.root, text="<<", command=self.prev_month)
        prev_button.grid(row=num_days // 7 + 3, column=0)

        next_button = tk.Button(self.root, text=">>", command=self.next_month)
        next_button.grid(row=num_days // 7 + 3, column=1)

        add_expense_button = tk.Button(self.root, text="Добавить Расход", command=self.add_expense)
        add_expense_button.grid(row=num_days // 7 + 3, column=2)

        add_income_button = tk.Button(self.root, text="Добавить Доход", command=self.add_income)
        add_income_button.grid(row=num_days // 7 + 3, column=3)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.show_month_view()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.show_month_view()

    def show_day_view(self, day):
        date = datetime(self.current_year, self.current_month, day)
        expense_list = self.expenses.get(date.date(), [])
        income_list = self.incomes.get(date.date(), [])

        self.clear_frame()

        label = tk.Label(self.root, text=f"День: {date.date()}", font=("Arial", 16))
        label.grid(row=0, column=0)

        for expense in expense_list:
            tk.Label(self.root, text=f"Расход: {expense}", fg="red").grid(sticky='w')

        for income in income_list:

            tk.Label(self.root, text=f"Доход: {income}", fg="green").grid(sticky='w')

        back_button = tk.Button(self.root, text="Назад", command=self.show_month_view)
        back_button.grid(row=len(expense_list) + len(income_list) + 1, column=0)

        add_expense_button = tk.Button(self.root, text="Добавить Расход", command=lambda: self.add_expense(date))
        add_expense_button.grid(row=len(expense_list) + len(income_list) + 1, column=1)

        add_income_button = tk.Button(self.root, text="Добавить Доход", command=lambda: self.add_income(date))
        add_income_button.grid(row=len(expense_list) + len(income_list) + 1, column=2)

    def add_expense(self, date=None):
        amount = simpledialog.askfloat("Добавить Расход", "Введите сумму расхода:")
        if amount is not None:
            if date is None:
                date = datetime.now()
            if date.date() not in self.expenses:
                self.expenses[date.date()] = []
            self.expenses[date.date()].append(amount)
            messagebox.showinfo("Расход добавлен", f"Вы добавили расход: {amount}")
            self.show_month_view()  # Обновляем календарь

    def add_income(self, date=None):
        amount = simpledialog.askfloat("Добавить Доход", "Введите сумму дохода:")
        if amount is not None:
            if date is None:
                date = datetime.now()
            if date.date() not in self.incomes:
                self.incomes[date.date()] = []
            self.incomes[date.date()].append(amount)
            messagebox.showinfo("Доход добавлен", f"Вы добавили доход: {amount}")
            self.show_month_view()

if __name__ == "__main__":
    root = tk.Tk()
    app = MoneyControlApp(root)
    root.mainloop()
