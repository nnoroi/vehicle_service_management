from pathlib import Path
from app.database.connection import get_connection

SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def initialise_database():
    """Create the database tables from the schema"""

    connection = get_connection()
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = f.read()

    connection.executescript(schema)
    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialise_database()
    print("Database initialised successfully")
