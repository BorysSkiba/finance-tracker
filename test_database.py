import database
import pytest


@pytest.fixture
def test_database(tmp_path):
    database.DATABASE_FILE = tmp_path / "test_transactions.db"
    database.initialize_database()


def test_initialize_database(test_database):
    rows = database.get_all_transactions()

    assert rows == []


def test_insert_transaction(test_database):
    database.insert_transaction(("Test transaction", 100, "Income", "28/09/2026"))

    rows = database.get_all_transactions()

    assert len(rows) == 1
    assert rows[0][1] == "Test transaction"
    assert rows[0][2] == 100
    assert rows[0][3] == "Income"
    assert rows[0][4] == "28/09/2026"


def test_update_transaction(test_database):
    database.insert_transaction(("Test transaction", 100, "Income", "28/09/2026"))

    database.update_transaction("amount", 200, 1)

    result = database.get_transaction_by_id(1)

    assert result[2] == 200


def test_delete_transaction_from_db(test_database):
    database.insert_transaction(("Test transaction", 100, "Income", "28/09/2026"))

    database.delete_transaction_from_db(1)

    assert database.get_transaction_by_id(1) is None


def test_update_disallowed_field(test_database):
    database.insert_transaction(("Test transaction", 100, "Income", "28/09/2026"))

    with pytest.raises(ValueError):
        database.update_transaction("date", 200, 1)


def test_get_total_amounts(test_database):
    database.insert_transaction(("Test transaction", 1000, "Income", "28/09/2026"))
    database.insert_transaction(("Test transaction 2", 500, "Income", "28/09/2026"))
    database.insert_transaction(("Test transaction 3", 200, "Expense", "28/09/2026"))
    database.insert_transaction(("Test transaction 4", 150, "Expense", "28/09/2026"))

    income = database.get_total_amounts("Income")
    expense = database.get_total_amounts("Expense")

    assert income == 1500
    assert expense == 350


def test_get_invalid_type_total_amounts(test_database):
    with pytest.raises(ValueError):
        database.get_total_amounts("outcome")


def test_get_total_amounts_with_no_transactions(test_database):
    income = database.get_total_amounts("Income")

    assert income == 0


def test_get_transactions_by_type(test_database):
    database.insert_transaction(("Test transaction", 1000, "Income", "28/09/2026"))
    database.insert_transaction(("Test transaction 2", 500, "Income", "28/09/2026"))
    database.insert_transaction(("Test transaction 3", 200, "Expense", "28/09/2026"))
    database.insert_transaction(("Test transaction 4", 150, "Expense", "28/09/2026"))

    income_rows = database.get_transactions_by_type("Income")
    expense_rows = database.get_transactions_by_type("Expense")

    assert income_rows == [(1, "Test transaction", 1000.0, "Income", "28/09/2026"), (2, "Test transaction 2", 500.0, "Income", "28/09/2026")]
    assert expense_rows == [(3, "Test transaction 3", 200.0, "Expense", "28/09/2026"), (4, "Test transaction 4", 150.0, "Expense", "28/09/2026")]


def test_get_transactions_by_type_invalid_type(test_database):
    with pytest.raises(ValueError):
        database.get_transactions_by_type("outcome")


def test_get_transactions_by_type_no_transactions(test_database):
    income_rows = database.get_transactions_by_type("Income")

    assert income_rows == []