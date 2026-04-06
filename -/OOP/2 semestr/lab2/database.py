import sqlite3

class Database:
    def __init__(self, db_name="group_students.db"):
        self.db_name = db_name
        self._create_table()

    def _get_connection(self):
        return sqlite3.connect(self.db_name)

    def _create_table(self):
        with self._get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS classmates (
                    user_id INTEGER PRIMARY KEY,
                    fio TEXT, age TEXT, group_code TEXT,
                    phone TEXT, email TEXT, github TEXT,
                    lang TEXT, experience TEXT, hobby TEXT, city TEXT
                )
            ''')

    def add_student(self, data):
        with self._get_connection() as conn:
            
            values = (
                data['user_id'], data['fio'], data['age'], data['group_code'],
                data['phone'], data['email'], data['github'],
                data['lang'], data['experience'], data['hobby'], data['city']
            )
            query = 'INSERT OR REPLACE INTO classmates VALUES (?,?,?,?,?,?,?,?,?,?,?)'
            conn.execute(query, values)