import datetime
import json
from json import JSONDecodeError

transactions = {}

def load_transactions():
    global transactions

    try:
        with open("transactions.json", "r") as f:
            transactions = json.load(f)
            print("Successfully loaded transactions.")
    except JSONDecodeError:
        print("No saved transactions found.")
    except FileNotFoundError:
        print("No transactions found. Creating new transactions file.")


def add_transaction():
    transaction = {"Name": input("Enter your transaction name: "), "Amount": 0.0, "Type": "", "Date": ""}

    transaction["Type"] = get_transaction_type()

    transaction["Amount"] = get_transaction_amount()

    transaction["Date"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")

    tid = ""
    for char in transaction["Date"]:
        if char.isdigit():
            tid += char

    transactions["t" + tid] = transaction

    save_transactions(transactions)


def save_transactions(data):
    with open("transactions.json", "w") as f:
        json.dump(data, f, indent=4)


def edit_transaction():
    while True:
        tid = input("Give an id of the transaction to edit ([c] to cancel): ").strip().lower()
        if tid in transactions:
            edited = False

            while not edited:
                transaction = transactions[tid]
                print("Editing: " + tid)
                edit_choice = input("Select the attribute to edit ([n]ame/[t]ype/[a]mount/[c]ancel): ").strip().lower()

                if edit_choice == "n":
                    new_value = input("Enter new value for name: ")
                    transaction["Name"] = new_value
                    edited = True
                elif edit_choice == "t":
                    transaction["Type"] = get_transaction_type()
                    edited = True
                elif edit_choice == "a":
                    transaction["Amount"] = get_transaction_amount()
                    edited = True
                elif edit_choice == "c":
                    print("Editing cancelled.")
                    return
                else:
                    print("Invalid input. Please enter a valid choice.")
            print("Successfully edited: " + tid)
            save_transactions(transactions)
            break
        elif tid == "c":
            print("Editing cancelled.")
            return
        else:
            print("Transaction not found.")


def get_transaction_type():
    while True:
        ttype = input("Select your transaction type ([i]ncome/[e]xpense): ")
        if ttype.strip().lower() == "i":
            return "Income"
        elif ttype.strip().lower() == "e":
            return "Expense"
        else:
            print("Invalid input. Please enter a valid choice.")


def get_transaction_amount():
    while True:
        try:
            amount = float(input("Enter your transaction amount: "))
            if amount > 0.0:
                return amount
            else:
                print("Invalid input. Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def delete_transaction():
    while True:
        tid = input("Give an id of the transaction to delete ([c] to cancel): ").strip().lower()
        if tid in transactions:
            while True:
                confirm = input("Are you sure you want to delete the transaction [y/n]: ").strip().lower()
                if confirm == "y":
                    transactions.pop(tid)
                    save_transactions(transactions)

                    print("Transaction successfully deleted.")

                    return
                elif confirm == "n":
                    return
                else:
                    print("Invalid input. Please enter a valid choice.")
        elif tid == "c":
            return
        else:
            print("Transaction not found.")


def show_transactions():
    if not transactions:
        print("No transactions found.")
        return

    total_balance = 0
    total_income = 0
    total_expense = 0

    for key, value in transactions.items():
        print(f"{key}: Name: {value["Name"]}, {value["Type"]}, {value['Amount']:.2f} PLN, {value['Date'][:17]}")

        if  value["Type"] == "Income":
            total_balance += value['Amount']
            total_income += value['Amount']
        elif value["Type"] == "Expense":
            total_balance -= value['Amount']
            total_expense += value['Amount']

    print(f"\nTotal income: {total_income:.2f} PLN\nTotal expense: {total_expense:.2f} PLN\nTotal balance: {total_balance:.2f} PLN")


def main():
    load_transactions()

    print("Welcome to the Financial Analysis Tool.")

    while True:
        print("1. Add transaction.\n2. Show transactions.\n3. Edit transaction.\n4. Delete transaction\n5. Exit.")

        while True:
            try:
                choice = int(input("Enter your choice: "))

                if choice in [1, 2, 3, 4, 5]:
                    break
                else:
                    print("Invalid input. Choose 1, 2, 3, 4 or 5.")

            except ValueError:
                print("Invalid input. Please enter a number.")

        if choice == 1:
            add_transaction()
        elif choice == 2:
            show_transactions()
        elif choice == 3:
            edit_transaction()
        elif choice == 4:
            delete_transaction()
        elif choice == 5:
            print("Thank you for using this tool.")
            break


if __name__ == '__main__':
    main()