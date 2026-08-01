import sqlite3

class DatabaseManager:
    def __init__(self, db_name = "expense_tracker.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
        Create table if not exists expense(
        id Integer Primary Key AUTOINCREMENT,
        amount REAL NOT NULL,
        category Text Not Null,
        description text,
        expense_date text
        )
""")
        self.connection.commit()

    def add_expense(self, amount, category, expense_date, description):
        self.cursor.execute("""
        Insert into expense values(?, ?, ?, ?)
""", (amount, category, description, expense_date))
        self.connection.execute()

    def get_expense(self):
        self.cursor.execute("select * from expense")
        return self.cursor.fetchall()

    def get_expense_by_category(self, category):
        self.cursor.execute("select * from expense where category = ?", (category,))
        return self.cursor.fetchall()

    def update_expense(self, expense_id, amount, category, description, expense_date):
        self.cursor.execute("""
        Update expense set amount = ?, category = ?, description = ?, expense_date = ? where expense_id = ?
""", (amount, category, description, expense_date, expense_id))

        self.connection.commit()

    def delete_expense(self, expense_id):
        self.cursor.execute("delete from expense where id = ?", (expense_id))

        self.connection.commit()