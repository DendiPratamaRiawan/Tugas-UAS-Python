from database.db import Database
from models.product import Product
from services.transaction_service import TransactionService

class CustomerService:
    def __init__(self, user):
        self.user = user
        self.db = Database()
        self.tx = TransactionService()

    def menu(self):
        while True:
            print("\n=== MENU PELANGGAN ===")
            print("1. Lihat Produk")
            print("2. Cari Produk")
            print("3. Beli Produk")
            print("4. Riwayat Pembelian")
            print("5. Logout")

            p = input("Pilih: ")

            if p == "1":
                self.list_products()
            elif p == "2":
                self.search_product()
            elif p == "3":
                self.buy_product()
            elif p == "4":
                self.view_history()
            elif p == "5":
                break

    def list_products(self):
        rows = self.db.fetch("SELECT * FROM products")
        for r in rows:
            Product(r['id'], r['name'], r['category'], r['price']).display()

    def search_product(self):
        keyword = input("Cari nama: ")
        rows = self.db.fetch("SELECT * FROM products WHERE name LIKE %s",
                             (f"%{keyword}%",))
        for r in rows:
            Product(r['id'], r['name'], r['category'], r['price']).display()

    def buy_product(self):
        pid = int(input("Masukkan ID Produk: "))
        qty = int(input("Jumlah: "))

        product = self.db.fetch("SELECT * FROM products WHERE id=%s", (pid,))
        if not product:
            print("Produk tidak ditemukan!")
            return

        price = product[0]['price']
        total = price * qty

        print(f"Total harga = Rp {total}")
        confirm = input("Konfirmasi beli? (y/n): ")

        if confirm.lower() == 'y':
            self.tx.create_transaction(self.user.id, pid, qty, total)

    def view_history(self):
        rows = self.tx.get_user_history(self.user.id)
        
        print("\n=== RIWAYAT PEMBELIAN ===")
        for r in rows:
            print(f"{r['id']}. {r['name']} x{r['quantity']} = Rp{r['total']} ({r['created_at']})")
