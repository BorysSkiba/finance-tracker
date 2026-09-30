import sqlite3

DATABASE_FILE = "transactions.db"


def initialize_database():
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, amount REAL, type TEXT, date TEXT)""")
    connection.commit()
    connection.close()


def insert_transaction(data):
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO transactions (name, amount, type, date) VALUES (?, ?, ?, ?)", data)
    connection.commit()
    connection.close()


def get_transaction_by_id(tid):
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM transactions WHERE id = ?", (tid,))
    transaction = cursor.fetchone()
    connection.close()

    return transaction


def update_transaction(edited_field, edited_value, tid):
    allowed_fields = ["name", "amount", "type"]

    if edited_field not in allowed_fields:
        if edited_field not in allowed_fields:
            raise ValueError("You are not allowed to edit this field")

    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()
    cursor.execute(f"UPDATE transactions SET {edited_field} = ? WHERE id = ?", (edited_value, tid))
    connection.commit()
    connection.close()


def delete_transaction_from_db(tid):
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ?", (tid,))
    connection.commit()
    connection.close()


def get_all_transactions():
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    connection.close()

    return rows


def get_total_amounts(atype):
    validate_transaction_type(atype)

    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()
    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type = ?", (atype,))
    total_amount = cursor.fetchone()
    connection.close()

    return total_amount[0]


def get_transactions_by_type(atype):
    validate_transaction_type(atype)

    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM transactions WHERE type = ?", (atype,))
    rows = cursor.fetchall()
    connection.close()

    return rows


def validate_transaction_type(atype):
    if atype not in ["Income", "Expense"]:
        raise ValueError("Invalid transaction type.")