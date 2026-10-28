import sqlite3


class TriangleDatabase:
    """Класс работы с БД (SQLite)."""

    def __init__(self, db_path=":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS triangles (
                a REAL,
                b REAL,
                c REAL,
                triangle_type TEXT,
                error_message TEXT,
                PRIMARY KEY (a, b, c)
            )
        """)
        self.conn.commit()

    def add(self, a, b, c, triangle_type, error_message):
        self.cursor.execute(
            "INSERT OR REPLACE INTO triangles VALUES (?, ?, ?, ?, ?)",
            (a, b, c, triangle_type, error_message),
        )
        self.conn.commit()

    def get(self, a, b, c):
        self.cursor.execute(
            "SELECT triangle_type, error_message FROM triangles WHERE a=? AND b=? AND c=?",
            (a, b, c),
        )
        return self.cursor.fetchone()  # (type, error) или None

    def delete(self, a, b, c):
        self.cursor.execute(
            "DELETE FROM triangles WHERE a=? AND b=? AND c=?", (a, b, c)
        )
        self.conn.commit()

    def close(self):
        self.conn.close()