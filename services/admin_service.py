from database.db import Database
from models.product import Product
from services.transaction_service import TransactionService
import csv

class AdminService:
    def __init__(self):
        self.db = Database()
        self.tx = TransactionService()

    def menu(self):
        while True:
            print("\n=== MENU ADMIN ===")
            print("1. Lihat Produk")
            print("2. Tambah Produk")
            print("3. Edit Produk")
            print("4. Hapus Produk")
            print("5. Lihat Semua Transaksi")
            print("6. Export Transaksi ke CSV")
            print("7. Logout")

            choice = input("Pilih: ")

            if choice == "1":
                self.list_products()
            elif choice == "2":
                self.add_product()          # ← ADA DI SINI
            elif choice == "3":
                self.update_product()       # ← ADA DI SINI
            elif choice == "4":
                self.delete_product()       # ← ADA DI SINI
            elif choice == "5":
                self.view_transactions()
            elif choice == "6":
                self.export_csv()
            elif choice == "7":
                break
            else:
                print("Pilihan tidak valid!")

    # =========================
    # READ
    # =========================
    def list_products(self):
        rows = self.db.fetch("SELECT * FROM products")
        print("\n=== DAFTAR PRODUK ===")
        for r in rows:
            Product(r['id'], r['name'], r['category'], r['price']).display()

    # =========================
    # CREATE
    # =========================
    def add_product(self):
        print("\n=== TAMBAH PRODUK ===")
        name = input("Nama produk: ")
        category = input("Kategori: ")
        price = int(input("Harga: "))

        self.db.execute(
            "INSERT INTO products (name, category, price) VALUES (%s, %s, %s)",
            (name, category, price)
        )
        print("Produk berhasil ditambahkan!")

    # =========================
    # UPDATE
    # =========================
    def update_product(self):
        print("\n=== EDIT PRODUK ===")
        pid = input("Masukkan ID produk: ")

        row = self.db.fetch("SELECT * FROM products WHERE id=%s", (pid,))
        if not row:
            print("Produk tidak ditemukan!")
            return

        old = row[0]

        print(f"Nama lama     : {old['name']}")
        print(f"Kategori lama : {old['category']}")
        print(f"Harga lama    : {old['price']}")

        name = input("Nama baru (kosong = tidak ubah): ") or old['name']
        category = input("Kategori baru (kosong = tidak ubah): ") or old['category']
        new_price = input("Harga baru (kosong = tidak ubah): ")

        if new_price == "":
            new_price = old['price']
        else:
            new_price = int(new_price)

        self.db.execute(
            "UPDATE products SET name=%s, category=%s, price=%s WHERE id=%s",
            (name, category, new_price, pid)
        )
        print("Produk berhasil diperbarui!")

    # =========================
    # DELETE
    # =========================
    def delete_product(self):
        print("\n=== HAPUS PRODUK ===")
        pid = input("Masukkan ID produk: ")

        self.db.execute("DELETE FROM products WHERE id=%s", (pid,))
        print("Produk berhasil dihapus!")

    # =========================
    # VIEW TRANSACTIONS
    # =========================
    def view_transactions(self):
        print("\n=== SEMUA TRANSAKSI ===")
        rows = self.tx.get_all_history()
        for r in rows:
            print(f"{r['id']}. {r['username']} membeli {r['name']} x{r['quantity']} "
                  f"= Rp{r['total']} ({r['created_at']})")

    # =========================
    # EXPORT CSV
    # =========================
    def export_csv(self):
        rows = self.tx.get_all_history()

        with open("laporan_transaksi.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["ID", "USER", "PRODUK", "JUMLAH", "TOTAL", "TANGGAL"])
            for r in rows:
                w.writerow([
                    r['id'],
                    r['username'],
                    r['name'],
                    r['quantity'],
                    r['total'],
                    r['created_at']
                ])

        print("Laporan berhasil diexport → laporan_transaksi.csv")
