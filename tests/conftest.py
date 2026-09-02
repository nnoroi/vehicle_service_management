import sqlite3
import pytest
from pathlib import Path


@pytest.fixture
def test_database(tmp_path):
    # creates temporart database file in the tmp_path directory
    database_path = tmp_path / "test_database.db"

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    schema_path = (
        Path(__file__).resolve().parent.parent
        / "app"
        / "database"
        / "schema.sql"
    )

    with open(schema_path, "r", encoding="utf-8") as schema_file:
        schema = schema_file.read()

    connection.executescript(schema)
    connection.commit()
    connection.close()

    def get_test_connection():
        connection = sqlite3.connect(database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    return get_test_connection
