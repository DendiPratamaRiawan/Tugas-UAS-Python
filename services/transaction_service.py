from database.db import Database

class TransactionService:
    def __init__(self):
        self.db = Database()

    def create_transaction(self, user_id, product_id, qty, total):
        self.db.execute(
            "INSERT INTO transactions (user_id, product_id, quantity, total) VALUES (%s,%s,%s,%s)",
            (user_id, product_id, qty, total)
        )
        print("Transaksi berhasil disimpan!")

    def get_user_history(self, user_id):
        return self.db.fetch("""
            SELECT t.id, p.name, t.quantity, t.total, t.created_at
            FROM transactions t
            JOIN products p ON t.product_id = p.id
            WHERE t.user_id=%s
            ORDER BY t.created_at DESC
        """, (user_id,))

    def get_all_history(self):
        return self.db.fetch("""
            SELECT t.id, u.username, p.name, t.quantity, t.total, t.created_at
            FROM transactions t
            JOIN users u ON t.user_id = u.id
            JOIN products p ON t.product_id = p.id
            ORDER BY t.created_at DESC
        """)
