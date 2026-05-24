import sqlite3

class BookRepository:
    def __init__(self, db_path='test.db'):
        self.db_path = db_path
        self.initialize()

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
        conn.cl
