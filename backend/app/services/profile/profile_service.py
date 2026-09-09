import json

from app.database.sqlite import get_connection


class ProfileService:

    def __init__(self):

        self.conn = get_connection()

    def create_user(self, username):

        cursor = self.conn.cursor()

        cursor.execute("""

        INSERT OR IGNORE INTO student_profile(

            username

        )

        VALUES(?)

        """,(username,))

        self.conn.commit()

    def get_profile(self, username):

        cursor = self.conn.cursor()

        cursor.execute("""

        SELECT *

        FROM student_profile

        WHERE username=?

        """,(username,))

        row = cursor.fetchone()

        return dict(row) if row else None