import sys
import database
import datetime

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QLineEdit,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QHBoxLayout,
    QHeaderView,
    QAbstractItemView,
    QDialog,
    QStyledItemDelegate,
    QStyle
)


def retrieve_all_transactions():
    rows = database.get_all_transactions()
    display_transaction_rows(rows)
    update_summary()


def display_transaction_rows(rows):
    transaction_table.setRowCount(len(rows))

    for row_index, row in enumerate(rows):
        for column_index, value in enumerate(row):
            item = QTableWidgetItem(str(value))

            item.setFlags(
                item.flags() & ~Qt.ItemFlag.ItemIsEditable
            )

            transaction_table.setItem(row_index, column_index, item)


def add_transaction():
    name = name_input.text().strip()

    if not name:
        QMessageBox.warning(window, "Warning", "Please enter a name.")
        return

    ttype = type_input.currentText()

    try:
        amount = float(amount_input.text())
    except ValueError:
        QMessageBox.warning(window, "Warning", "Please enter a valid amount.")
        return

    if amount <= 0:
        QMessageBox.warning(window, "Warning", "Invalid input, please enter a positive amount.")
        return

    category = category_input.currentText()

    database.insert_transaction((name, amount, ttype, datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f"), category))

    refresh_view()

    QMessageBox.information(window, "Info", "Transaction added successfully.")

    name_input.clear()
    amount_input.clear()
    type_input.setCurrentIndex(0)


def edit_selected_transaction():
    row = transaction_table.currentRow()

    if row == -1:
        QMessageBox.warning(window, "Warning", "No transaction selected.")
        return

    tid = int(transaction_table.item(row, 0).text())

    database_row = database.get_transaction_by_id(tid)

    dialog = QDialog(window)
    dialog.setWindowTitle("Edit transaction")
    dialog_layout = QVBoxLayout()
    dialog.setLayout(dialog_layout)

    edit_name_input = QLineEdit(database_row[1])
    dialog_layout.addWidget(edit_name_input)

    edit_amount_input = QLineEdit(str(database_row[2]))
    dialog_layout.addWidget(edit_amount_input)

    edit_type_input = QComboBox()
    edit_type_input.addItems(["Income", "Expense"])
    edit_type_input.setCurrentText(database_row[3])
    dialog_layout.addWidget(edit_type_input)

    edit_category_input = QComboBox()
    edit_category_input.addItems(["Food", "Transport", "Bills", "Entertainment", "Shopping", "Salary", "Other"])
    edit_category_input.setCurrentText(database_row[5])
    dialog_layout.addWidget(edit_category_input)

    save_changes_button = QPushButton("Save changes")
    dialog_layout.addWidget(save_changes_button)

    def save_changes():
        new_name = edit_name_input.text().strip()

        if not new_name:
            QMessageBox.warning(dialog, "Warning", "Please enter a name.")
            return

        new_type = edit_type_input.currentText()

        try:
            new_amount = float(edit_amount_input.text())
        except ValueError:
            QMessageBox.warning(dialog, "Warning", "Please enter a valid amount.")
            return

        if new_amount <= 0:
            QMessageBox.warning(dialog, "Warning", "Invalid input, please enter a positive amount.")
            return

        new_category = edit_category_input.currentText()

        if new_name != database_row[1]:
            database.update_transaction("name", new_name, tid)
        if  new_amount != database_row[2]:
            database.update_transaction("amount", new_amount, tid)
        if new_type != database_row[3]:
            database.update_transaction("type", new_type, tid)
        if new_category != database_row[5]:
            database.update_transaction("category", new_category, tid)

        refresh_view()
        dialog.close()

    save_changes_button.clicked.connect(save_changes)

    dialog.exec()


def update_summary():
    total_income = database.get_total_amounts("Income")
    total_expense = database.get_total_amounts("Expense")
    total_balance = total_income - total_expense

    income_label.setText(f"Income: {total_income:.2f}")
    expense_label.setText(f"Expense: {total_expense:.2f}")
    balance_label.setText(f"Total Balance: {total_balance:.2f}")


def delete_selected_transaction():
    row = transaction_table.currentRow()

    if row == -1:
        QMessageBox.warning(window, "Warning", "No transaction selected.")
        return

    answer = QMessageBox.question(window, "Info", f"Are you sure you want to delete\n{transaction_table.item(row, 1).text()} - {transaction_table.item(row, 2).text()}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

    if answer == QMessageBox.StandardButton.No:
        return

    tid = int(transaction_table.item(row, 0).text())
    database.delete_transaction_from_db(tid)
    QMessageBox.information(window, "Info", "Transaction deleted successfully.")
    refresh_view()


def filter_transactions(_=None):
    filter_transaction_type = None
    filter_transaction_category = None
    if filter_input_type.currentText() != "All":
        filter_transaction_type = filter_input_type.currentText()
    if filter_input_category.currentText() != "All Categories":
        filter_transaction_category = filter_input_category.currentText()

    display_transaction_rows(database.get_filtered_transactions(filter_transaction_type, filter_transaction_category))


def refresh_view():
    filter_transactions()
    update_summary()


class NoFocusDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        option.state &= ~QStyle.StateFlag.State_HasFocus
        super().paint(painter, option, index)


database.initialize_database()

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Finance Tracker")
window.resize(1000, 700)

layout = QVBoxLayout()

title = QLabel("Finance Tracker")
layout.addWidget(title)

form_layout = QHBoxLayout()
layout.addLayout(form_layout)

name_input = QLineEdit()
name_input.setPlaceholderText("Transaction Name")
form_layout.addWidget(name_input)

amount_input = QLineEdit()
amount_input.setPlaceholderText("Transaction Amount")
form_layout.addWidget(amount_input)

type_input = QComboBox()
type_input.addItems(["Income", "Expense"])
form_layout.addWidget(type_input)

category_input = QComboBox()
category_input.addItems(["Food", "Transport", "Bills", "Entertainment", "Shopping", "Salary", "Other"])
form_layout.addWidget(category_input)

add_button = QPushButton("Add transaction")
add_button.clicked.connect(add_transaction)
layout.addWidget(add_button)

filter_input_type = QComboBox()
filter_input_type.addItems(["All", "Income", "Expense"])
filter_input_type.currentTextChanged.connect(filter_transactions)
layout.addWidget(filter_input_type)

filter_input_category = QComboBox()
filter_input_category.addItems(["All Categories", "Food", "Transport", "Bills", "Entertainment", "Shopping", "Salary", "Other"])
filter_input_category.currentTextChanged.connect(filter_transactions)
layout.addWidget(filter_input_category)

transaction_table = QTableWidget()
transaction_table.setColumnCount(6)

transaction_table.setItemDelegate(
    NoFocusDelegate(transaction_table)
)

transaction_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
transaction_table.setSelectionBehavior(
    QAbstractItemView.SelectionBehavior.SelectRows
)
transaction_table.setSelectionMode(
    QAbstractItemView.SelectionMode.SingleSelection
)
transaction_table.setEditTriggers(
    QAbstractItemView.EditTrigger.NoEditTriggers
)

transaction_table.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
transaction_table.setHorizontalHeaderItem(1, QTableWidgetItem("Name"))
transaction_table.setHorizontalHeaderItem(2, QTableWidgetItem("Amount"))
transaction_table.setHorizontalHeaderItem(3, QTableWidgetItem("Type"))
transaction_table.setHorizontalHeaderItem(4, QTableWidgetItem("Date"))
transaction_table.setHorizontalHeaderItem(5, QTableWidgetItem("Category"))

layout.addWidget(transaction_table)

income_label = QLabel()
expense_label = QLabel()
balance_label = QLabel()
layout.addWidget(income_label)
layout.addWidget(expense_label)
layout.addWidget(balance_label)

retrieve_all_transactions()

edit_button = QPushButton("Edit selected")
edit_button.clicked.connect(edit_selected_transaction)
layout.addWidget(edit_button)

delete_button = QPushButton("Delete selected")
delete_button.clicked.connect(delete_selected_transaction)
layout.addWidget(delete_button)

window.setLayout(layout)

window.show()

app.exec()