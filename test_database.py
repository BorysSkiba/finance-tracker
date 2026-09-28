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