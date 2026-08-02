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

    def add_expense(self, amount, category, description, expense_date):
        self.cursor.execute("""
        Insert into expense(amount, category, description, expense_date) values(?, ?, ?, ?)
""", (amount, category, description, expense_date))
        self.connection.commit()

    def get_expense(self):
        self.cursor.execute("select * from expense")
        return self.cursor.fetchall()

    def get_expense_by_category(self, category):
        self.cursor.execute("select * from expense where category = ?", (category,))
        return self.cursor.fetchall()
    
    def update_expense(self, expense_id = None, amount = None, category = None, description = None, expense_date = None):
        self.cursor.execute("""
        Update expense set amount = ?, category = ?, description = ?, expense_date = ? where expense_id = ?
""", (amount, category, description, expense_date, expense_id))

        self.connection.commit()

    def delete_expense(self, expense_id = None, amount = None, category = None, description = None, expense_date = None):
        query = "delete from expense where 1=1"
        params = []

        if expense_id is not None:
            query+=" And id = ?"
            params.append(expense_id)

        if amount is not None:
            query+=" And amount = ?"
            params.append(amount)
        
        if category is not None:
            query+=" And category = ?"
            params.append(category)
        
        if description is not None:
            query+=" And description Like ?"
            params.append(description)
        
        if expense_date is not None:
            query+=" And expense_date = ?"
            params.append(expense_date)

        
        self.cursor.execute(query, params)
        self.connection.commit()

    def close(self):
        self.connection.close()