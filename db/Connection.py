import sqlite3 as sq


class Connection:
    conn = sq.connect("my_proj.db", check_same_thread=False)
    cursor = conn.cursor()
    users_table = "users"

    def __init__(self):
        try:
            self.execute(
                f"create table {self.users_table} (fname varchar(30),lname varchar(30),email varchar(30),pwd varchar(30));")
        except:
            print("table already exist")

    def execute(self, query):
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        return row

    def commit(self):
        self.conn.commit()

# depricated---
    def create(self):
        query = f"create table {self.users_table} (uname varchar(30),pwd varchar(30));"
        self.cursor.execute(query)

    def insert(self, query):
        a = self.cursor.execute(query)
        self.conn.commit()
        return a
