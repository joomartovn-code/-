import sqlite3

class DBManager:
    def __init__(self, db_name="staff.db"):
        self.db = sqlite3.connect(db_name, check_same_thread=False)
        self.cur = self.db.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fio TEXT,
                job TEXT,
                money REAL
            )
        """)
        self.db.commit()

    def get_users(self, search="", sort="fio"):
        val = f"%{search}%"
        self.cur.execute(f"SELECT * FROM users WHERE fio LIKE ? OR job LIKE ? ORDER BY {sort}", (val, val))
        return self.cur.fetchall()

    def add_user(self, fio, job, money):
        self.cur.execute("INSERT INTO users (fio, job, money) VALUES (?, ?, ?)", (fio, job, money))
        self.db.commit()

    def delete_user(self, idx):
        self.cur.execute("DELETE FROM users WHERE id = ?", (idx,))
        self.db.commit()