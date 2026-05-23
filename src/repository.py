import sqlite3

class BookRepository:
    def __init__(self, db_path='test.db'):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def initialize(self):
        conn = self._connect()
        conn.execute('''CREATE TABLE IF NOT EXISTS book_info
            (ID VARCHAR PRIMARY KEY NOT NULL,
            TITLE VARTEXT NOT NULL,
            AUTHOR VARTEXT NOT NULL,
            GENRE VARTEXT NOT NULL,
            COPIES VARINT NOT NULL,
            LOCATION VARCHAR NOT NULL)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS book_issued
            (BOOK_ID VARCHAR NOT NULL,
            STUDENT_ID VARCHAR NOT NULL,
            ISSUE_DATE DATE NOT NULL,
            RETURN_DATE DATE NOT NULL,
            PRIMARY KEY (BOOK_ID, STUDENT_ID))''')
        conn.commit()
        conn.close()

    def add_book(self, book_id, title, author, genre, copies, location):
        conn = self._connect()
        conn.execute(
            "INSERT INTO book_info VALUES (?,?,?,?,?,?)",
            (book_id, title, author, genre, copies, location)
        )
        conn.commit()
        conn.close()

    def get_book(self, book_id):
        conn = self._connect()
        cursor = conn.execute(
            "SELECT * FROM book_info WHERE ID=?", (book_id,)
        )
        result = cursor.fetchone()
        conn.close()
        return result

    def get_all_books(self):
        conn = self._connect()
        cursor = conn.execute("SELECT * FROM book_info")
        result = cursor.fetchall()
        conn.close()
        return result

    def search_books(self, term):
        conn = self._connect()
        cursor = conn.execute(
            "SELECT * FROM book_info WHERE ID=? OR TITLE=? OR AUTHOR=? OR GENRE=?",
            (term, term, term, term)
        )
        result = cursor.fetchall()
        conn.close()
        return result

    def delete_book(self, book_id):
        conn = self._connect()
        conn.execute("DELETE FROM book_info WHERE ID=?", (book_id,))
        conn.commit()
        conn.close()

    def update_copies(self, book_id, amount):
        conn = self._connect()
        conn.execute(
            "UPDATE book_info SET COPIES=COPIES+? WHERE ID=?",
            (amount, book_id)
        )
        conn.commit()
        conn.close()

    def is_book_issued(self, book_id):
        conn = self._connect()
        cursor = conn.execute(
            "SELECT * FROM book_issued WHERE BOOK_ID=?", (book_id,)
        )
        result = cursor.fetchall()
        conn.close()
        return len(result) > 0

    def issue_book(self, book_id, student_id):
        conn = self._connect()
        conn.execute(
            "INSERT INTO book_issued VALUES (?,?,date('now'),date('now','+7 day'))",
            (book_id, student_id)
        )
        conn.execute(
            "UPDATE book_info SET COPIES=COPIES-1 WHERE ID=?", (book_id,)
        )
        conn.commit()
        conn.close()

    def return_book(self, book_id, student_id):
        conn = self._connect()
        conn.execute(
            "DELETE FROM book_issued WHERE BOOK_ID=? AND STUDENT_ID=?",
            (book_id, student_id)
        )
        conn.execute(
            "UPDATE book_info SET COPIES=COPIES+1 WHERE ID=?", (book_id,)
        )
        conn.commit()
        conn.close()

    def get_issued_by(self, term):
        conn = self._connect()
        cursor = conn.execute(
            "SELECT * FROM book_issued WHERE BOOK_ID=? OR STUDENT_ID=?",
            (term, term)
        )
        result = cursor.fetchall()
        conn.close()
        return result

    def get_all_issued(self):
        conn = self._connect()
        cursor = conn.execute("SELECT * FROM book_issued")
        result = cursor.fetchall()
        conn.close()
        return result
