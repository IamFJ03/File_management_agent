from database import DatabaseManager

db = DatabaseManager()

db.add_expense(450, "Shoes", "Shopping", "2026-07-31")
db.add_expense(350, "Movie", "Entertainment", "2026-07-31")

expenses = db.get_expense()
for expense in expenses:
    print(expense)

db.close()