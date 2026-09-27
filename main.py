import datetime
import database


def add_transaction():
    transaction = {"Name": "", "Amount": 0.0, "Type": "", "Date": ""}

    transaction["Name"] = get_transaction_name()

    transaction["Type"] = get_transaction_type()

    transaction["Amount"] = get_transaction_amount()

    transaction["Date"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")

    database.insert_transaction((transaction["Name"], transaction["Amount"], transaction["Type"], transaction["Date"]))


def edit_transaction():
    while True:
        tid = input("Give an id of the transaction to edit ([c] to cancel): ").strip().lower()

        if tid == "c":
            print("Editing cancelled.")
            return

        transaction = database.get_transaction_by_id(tid)

        if transaction:
            edited_field = ""
            edited_value = ""

            while True:
                print("Editing: " + tid)
                edit_choice = input("Select the attribute to edit ([n]ame/[t]ype/[a]mount/[c]ancel): ").strip().lower()

                if edit_choice == "n":
                    edited_value = get_transaction_name()
                    edited_field = "name"
                    break
                elif edit_choice == "t":
                    edited_value = get_transaction_type()
                    edited_field = "type"
                    break
                elif edit_choice == "a":
                    edited_value = get_transaction_amount()
                    edited_field = "amount"
                    break
                elif edit_choice == "c":
                    print("Editing cancelled.")
                    return
                else:
                    print("Invalid input. Please enter a valid choice.")

            database.update_transaction(edited_field, edited_value, tid)

            print("Successfully edited: " + tid)
            break
        else:
            print("Transaction not found.")


def get_transaction_name():
    while True:
        name = input("Enter your transaction name: ").strip()
        if name:
            return name
        else:
            print("The name cannot be empty.")


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

        if tid == "c":
            print("Deleting cancelled.")
            return

        transaction = database.get_transaction_by_id(tid)

        if transaction:
            while True:
                print(f"Selected transaction: ID: {transaction[0]},\n"
                      f"Name: {transaction[1]},\n"
                      f"Type: {transaction[3]},\n"
                      f"Amount: {transaction[2]:.2f} PLN,\n"
                      f"Date: {transaction[4][:17]}")

                confirm = input("Are you sure you want to delete the transaction [y/n]: ").strip().lower()
                if confirm == "y":
                    database.delete_transaction_from_db(tid)

                    print("Transaction successfully deleted.")

                    return
                elif confirm == "n":
                    print("Deleting cancelled.")
                    return
                else:
                    print("Invalid input. Please enter a valid choice.")
        else:
            print("Transaction not found.")


def show_transactions():
    rows = database.get_all_transactions()

    if not rows:
        print("No transactions found.")
        return

    total_balance = 0
    total_income = 0
    total_expense = 0

    for row in rows:
        print(f"{row[0]}: Name: {row[1]}, {row[3]}, {row[2]:.2f} PLN, {row[4][:17]}")

        if  row[3] == "Income":
            total_balance += row[2]
            total_income += row[2]
        elif row[3] == "Expense":
            total_balance -= row[2]
            total_expense += row[2]

    print(f"\nTotal income: {total_income:.2f} PLN\nTotal expense: {total_expense:.2f} PLN\nTotal balance: {total_balance:.2f} PLN")


def main():
    database.initialize_database()

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