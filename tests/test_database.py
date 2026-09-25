import sqlite3

from app.database.connection import init_db


def test_init_db_creates_tables(tmp_path, monkeypatch):
    database_path = tmp_path / "test_database.db"

    monkeypatch.setattr(
        "app.database.connection.DATABASE_PATH",
        database_path
    )

    init_db()

    connection = sqlite3.connect(database_path)

    tables = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
        """
    ).fetchall()

    connection.close()

    table_names = [table[0] for table in tables]

    assert "vehicles" in table_names
    assert "service_records" in table_names
