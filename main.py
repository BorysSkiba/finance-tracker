import datetime

transactions = {}


def add_transaction():
    transaction = {"Name": "", "Amount": 0.0, "Type": "", "Date": ""}

    transaction["Name"] = input("Enter your transaction name: ")

    while True:
        ttype = input("Select your transaction type ([i]ncome/[e]xpense): ")
        if ttype.strip().lower() == "i":
            transaction["Type"] = "Income"
            break
        elif ttype.strip().lower() == "e":
            transaction["Type"] = "Expense"
            break
        else:
            print("Invalid input. Please enter a valid choice.")

    while True:
        try:
            amount = float(input("Enter your transaction amount: "))
            if amount > 0.0:
                transaction["Amount"] = amount
                break
            else:
                print("Invalid input. Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    transaction["Date"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")

    tid = ""
    for char in transaction["Date"]:
        if char.isdigit():
            tid += char

    transactions["t" + tid] = transaction


def show_transactions():
    total_balance = 0
    total_income = 0
    total_expense = 0

    for key, value in transactions.items():
        print(f"{key}: {value["Type"]}, {value['Amount']} PLN, {value['Date'][:17]}")

        if  value["Type"] == "Income":
            total_balance += value['Amount']
            total_income += value['Amount']
        elif value["Type"] == "Expense":
            total_balance -= value['Amount']
            total_expense += value['Amount']

    print(f"\nTotal income: {total_income:.2f} PLN\nTotal expense: {total_expense:.2f} PLN\nTotal balance: {total_balance:.2f} PLN")


if __name__ == '__main__':
    print("Welcome to the Financial Analysis Tool.")
    while True:
        print("1. Add transaction.\n2. Show transactions.\n3. Exit.")

        while True:
            try:
                choice = int(input("Enter your choice: "))

                if choice in [1, 2, 3]:
                    break
                else:
                    print("Invalid input. Choose 1, 2 or 3.")

            except ValueError:
                print("Invalid input. Please enter a number.")

        if choice == 1:
            add_transaction()
        elif choice == 2:
            show_transactions()
        elif choice == 3:
            print("Thank you for using this tool.")
            break