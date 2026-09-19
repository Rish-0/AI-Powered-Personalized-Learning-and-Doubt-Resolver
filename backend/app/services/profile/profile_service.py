import json

from app.database.sqlite import get_connection


class ProfileService:

    def __init__(self):

        self.conn = get_connection()

        self.create_tables()

    def create_tables(self):

        cursor = self.conn.cursor()

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS student_profile(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            difficulty TEXT DEFAULT 'medium',

            learning_style TEXT DEFAULT 'visual',

            weak_topics TEXT DEFAULT '',

            strong_topics TEXT DEFAULT '',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

        """)

        self.conn.commit()

    def create_user(self, username):

        cursor = self.conn.cursor()

        cursor.execute("""

        INSERT OR IGNORE INTO student_profile(

            username

        )

        VALUES(?)

        """,(username,))

        self.conn.commit()

    def update_profile(self, username, difficulty=None,
                       learning_style=None, weak_topics=None,
                       strong_topics=None):

        self.create_user(username)

        cursor = self.conn.cursor()

        updates = []
        values = []

        if difficulty is not None:
            updates.append("difficulty = ?")
            values.append(difficulty)

        if learning_style is not None:
            updates.append("learning_style = ?")
            values.append(learning_style)

        if weak_topics is not None:
            updates.append("weak_topics = ?")
            values.append(weak_topics)

        if strong_topics is not None:
            updates.append("strong_topics = ?")
            values.append(strong_topics)

        if updates:
            values.append(username)
            cursor.execute(
                f"UPDATE student_profile SET {', '.join(updates)} WHERE username = ?",
                values
            )
            self.conn.commit()

    def get_profile(self, username):

        self.create_user(username)

        cursor = self.conn.cursor()

        cursor.execute("""

        SELECT *

        FROM student_profile

        WHERE username=?

        """,(username,))

        row = cursor.fetchone()

        return dict(row) if row else None