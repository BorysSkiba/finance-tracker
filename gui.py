import sys

from PySide6.QtGui import QFont

import database
import datetime

from PySide6.QtCore import Qt, QDate

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
    QDateEdit, QGroupBox, QGridLayout,
)


def display_transaction_rows(rows):
    transaction_table.setRowCount(len(rows))

    for row_index, row in enumerate(rows):
        for column_index, value in enumerate(row):
            if column_index == 2:
                item = QTableWidgetItem(f"{value:.2f} PLN")
            else:
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

    database.insert_transaction((name, amount, ttype, datetime.datetime.now().isoformat(sep=" ", timespec="seconds"), category))

    refresh_view()

    QMessageBox.information(window, "Info", "Transaction added successfully.")

    name_input.clear()
    amount_input.clear()
    type_input.setCurrentIndex(0)
    category_input.setCurrentIndex(0)


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
    edit_type_input.addItems(database.TYPES)
    edit_type_input.setCurrentText(database_row[3])
    dialog_layout.addWidget(edit_type_input)

    edit_category_input = QComboBox()
    edit_category_input.addItems(database.CATEGORIES)
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


def update_summary(rows):
    total_income = 0
    total_expense = 0

    for row in rows:
        if row[3] == "Income":
            total_income += row[2]
        elif row[3] == "Expense":
            total_expense += row[2]

    total_balance = total_income - total_expense

    income_label.setText(f"{total_income:.2f} PLN")
    expense_label.setText(f"{total_expense:.2f} PLN")
    balance_label.setText(f"{total_balance:.2f} PLN")


def delete_selected_transaction():
    row = transaction_table.currentRow()

    if row == -1:
        QMessageBox.warning(window, "Warning", "No transaction selected.")
        return

    answer = QMessageBox.question(window, "Delete transaction", f"Are you sure you want to delete\n{transaction_table.item(row, 1).text()} - {transaction_table.item(row, 2).text()}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

    if answer == QMessageBox.StandardButton.No:
        return

    tid = int(transaction_table.item(row, 0).text())
    database.delete_transaction_from_db(tid)
    QMessageBox.information(window, "Info", "Transaction deleted successfully.")
    refresh_view()


def filter_transactions(_=None):
    filter_transaction_type = None
    filter_transaction_category = None
    filter_transaction_start_date = None
    filter_transaction_end_date = None

    if filter_input_type.currentText() != "All":
        filter_transaction_type = filter_input_type.currentText()
    if filter_input_category.currentText() != "All Categories":
        filter_transaction_category = filter_input_category.currentText()
    if start_date_input.date() != QDate(2000, 1, 1):
        filter_transaction_start_date = start_date_input.date().toString("yyyy-MM-dd") + " 00:00:00"
    if end_date_input.date() != QDate(2000, 1, 1):
        filter_transaction_end_date = end_date_input.date().toString("yyyy-MM-dd") + " 23:59:59"

    rows = database.get_filtered_transactions(transaction_type=filter_transaction_type, transaction_category=filter_transaction_category, start_date=filter_transaction_start_date, end_date=filter_transaction_end_date)

    display_transaction_rows(rows)

    return rows


def refresh_view():
    rows = filter_transactions()
    update_summary(rows)


database.initialize_database()

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Finance Tracker")
window.resize(1000, 700)

layout = QVBoxLayout()

title = QLabel("Finance Tracker")
layout.addWidget(title)

add_transaction_group = QGroupBox("Add Transaction")
add_transaction_layout = QGridLayout()
add_transaction_group.setLayout(add_transaction_layout)
add_transaction_layout.setHorizontalSpacing(10)
add_transaction_layout.setVerticalSpacing(6)
layout.addWidget(add_transaction_group)

add_transaction_layout.addWidget(QLabel("Name"), 0, 0)
add_transaction_layout.addWidget(QLabel("Amount"), 0, 1)
add_transaction_layout.addWidget(QLabel("Type"), 0, 2)
add_transaction_layout.addWidget(QLabel("Category"), 0, 3)

name_input = QLineEdit()
name_input.setPlaceholderText("Transaction Name")
add_transaction_layout.addWidget(name_input, 1, 0)

amount_input = QLineEdit()
amount_input.setPlaceholderText("Transaction Amount")
add_transaction_layout.addWidget(amount_input, 1, 1)

type_input = QComboBox()
type_input.addItems(database.TYPES)
add_transaction_layout.addWidget(type_input, 1, 2)

category_input = QComboBox()
category_input.addItems(database.CATEGORIES)
add_transaction_layout.addWidget(category_input, 1, 3)

add_button = QPushButton("Add transaction")
add_button.clicked.connect(add_transaction)
add_transaction_layout.addWidget(add_button, 2, 0, 1, 4)

filter_group = QGroupBox("Filter")
filter_layout = QGridLayout()
filter_group.setLayout(filter_layout)
filter_layout.setHorizontalSpacing(10)
filter_layout.setVerticalSpacing(6)
layout.addWidget(filter_group)

filter_layout.addWidget(QLabel("Type"), 0, 0)
filter_layout.addWidget(QLabel("Category"), 0, 1)
filter_layout.addWidget(QLabel("Start Date"), 0, 2)
filter_layout.addWidget(QLabel("End Date"), 0, 3)

filter_input_type = QComboBox()
filter_input_type_items = database.TYPES.copy()
filter_input_type_items.insert(0, "All")
filter_input_type.addItems(filter_input_type_items)
filter_input_type.currentTextChanged.connect(refresh_view)
filter_layout.addWidget(filter_input_type, 1, 0)

filter_input_category = QComboBox()
filter_input_category_items = database.CATEGORIES.copy()
filter_input_category_items.insert(0, "All Categories")
filter_input_category.addItems(filter_input_category_items)
filter_input_category.currentTextChanged.connect(refresh_view)
filter_layout.addWidget(filter_input_category, 1, 1)

start_date_input = QDateEdit()
start_date_input.setCalendarPopup(True)
start_date_input.dateChanged.connect(refresh_view)
filter_layout.addWidget(start_date_input, 1, 2)

end_date_input = QDateEdit()
end_date_input.setCalendarPopup(True)
end_date_input.dateChanged.connect(refresh_view)
filter_layout.addWidget(end_date_input, 1, 3)

transaction_table = QTableWidget()
transaction_table.setColumnCount(6)

transaction_table.verticalHeader().setVisible(False)
transaction_table.setColumnHidden(0, True)

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

summary_group = QGroupBox("Summary")
summary_layout = QGridLayout()
summary_group.setLayout(summary_layout)
layout.addWidget(summary_group)

summary_layout.addWidget(QLabel("Income"), 0, 0)
summary_layout.addWidget(QLabel("Expense"), 0, 1)
summary_layout.addWidget(QLabel("Balance"), 0, 2)

income_label = QLabel()
expense_label = QLabel()
balance_label = QLabel()
summary_layout.addWidget(income_label, 1, 0)
summary_layout.addWidget(expense_label, 1, 1)
summary_layout.addWidget(balance_label, 1, 2)

refresh_view()

bottom_buttons_layout = QHBoxLayout()
layout.addLayout(bottom_buttons_layout)

edit_button = QPushButton("Edit selected")
edit_button.clicked.connect(edit_selected_transaction)
bottom_buttons_layout.addWidget(edit_button)

delete_button = QPushButton("Delete selected")
delete_button.clicked.connect(delete_selected_transaction)
bottom_buttons_layout.addWidget(delete_button)

# Styling
add_button.setObjectName("primaryButton")

edit_button.setObjectName("editButton")
delete_button.setObjectName("deleteButton")

income_label.setObjectName("incomeLabel")
expense_label.setObjectName("expenseLabel")
balance_label.setObjectName("balanceLabel")

app.setFont(QFont("Segoe UI", 10))

app.setStyleSheet("""
    QWidget {
        background-color: #1e1e1e;
        color: #f0f0f0;
        font-size: 10pt;
    }

    QGroupBox {
        border: 1px solid #4a4a4a;
        border-radius: 6px;
        margin-top: 10px;
        padding-top: 10px;
        font-weight: bold;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px;
    }

    QLineEdit,
    QComboBox,
    QDateEdit {
        background-color: #2b2b2b;
        border: 1px solid #4a4a4a;
        border-radius: 5px;
        padding: 6px;
        color: #f0f0f0;
    }

    QLineEdit:focus,
    QComboBox:focus,
    QDateEdit:focus {
        border: 1px solid #3daee9;
    }

    QPushButton {
        background-color: #333333;
        border: 1px solid #4a4a4a;
        border-radius: 5px;
        padding: 7px 12px;
        color: #f0f0f0;
    }

    QPushButton:hover {
        background-color: #404040;
    }

    QPushButton:pressed {
        background-color: #2a2a2a;
    }

    QPushButton#primaryButton {
        background-color: #287fa8;
        border: none;
        font-weight: bold;
    }

    QPushButton#primaryButton:hover {
        background-color: #3296c4;
    }

    QPushButton#editButton {
        background-color: #3c4d58;
    }

    QPushButton#deleteButton {
        background-color: #7a3434;
    }

    QPushButton#deleteButton:hover {
        background-color: #934040;
    }
    
    QComboBox::drop-down,
    QDateEdit::drop-down {
        border: none;
        border-left: 1px solid #4a4a4a;
        width: 28px;
    }
    
    QComboBox::down-arrow,
    QDateEdit::down-arrow {
        image: url("assets/icons/chevron_down.svg");
    }
    
    QComboBox,
    QDateEdit {
        padding-right: 30px;
    }
    
    QScrollBar:vertical {
        background: #1e1e1e;
        width: 12px;
        margin: 2px;
        border: none;
        border-radius: 6px;
    }

    QScrollBar::handle:vertical {
        background: #4a4a4a;
        min-height: 30px;
        border-radius: 6px;
    }

    QScrollBar::handle:vertical:hover {
        background: #5a5a5a;
    }

    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {
        height: 0px;
        background: none;
    }

    QScrollBar::add-page:vertical,
    QScrollBar::sub-page:vertical {
        background: none;
    }

    QScrollBar:horizontal {
        background: #1e1e1e;
        height: 12px;
        margin: 2px;
        border: none;
        border-radius: 6px;
    }

    QScrollBar::handle:horizontal {
        background: #4a4a4a;
        min-width: 30px;
        border-radius: 6px;
    }

    QScrollBar::handle:horizontal:hover {
        background: #5a5a5a;
    }

    QScrollBar::add-line:horizontal,
    QScrollBar::sub-line:horizontal {
        width: 0px;
        background: none;
    }

    QScrollBar::add-page:horizontal,
    QScrollBar::sub-page:horizontal {
        background: none;
    }
""")

window.setLayout(layout)

window.show()

app.exec()