from app.database.sqlite import get_connection


class MemoryService:

    def __init__(self):

        self.conn = get_connection()

        self.create_tables()

    def create_tables(self):

        cursor = self.conn.cursor()

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS conversations(

            id INTEGER PRIMARY KEY,

            question TEXT,

            answer TEXT,

            route TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

        """)

        self.conn.commit()

    def save(self, question, answer, route):

        cursor = self.conn.cursor()

        cursor.execute(

            """

            INSERT INTO conversations(

                question,

                answer,

                route

            )

            VALUES(?,?,?)

            """,

            (

                question,

                answer,

                route

            )

        )

        self.conn.commit()

    def history(self, limit=5):

        cursor = self.conn.cursor()

        cursor.execute(

            """

            SELECT *

            FROM conversations

            ORDER BY id DESC

            LIMIT ?

            """,

            (limit,)

        )

        return cursor.fetchall()