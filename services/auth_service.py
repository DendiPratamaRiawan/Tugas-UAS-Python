from database.db import Database
from models.user import User
from utils.hasher import hash_password, verify_password

class AuthService:
    def __init__(self):
        self.db = Database()

    def _convert_default_passwords(self):
        users = self.db.fetch("SELECT * FROM users")
        for u in users:
            if len(u['password']) < 20:  
                hashed = hash_password(u['password'])
                self.db.execute("UPDATE users SET password=%s WHERE id=%s",
                                (hashed, u['id']))

    def login(self):
        self._convert_default_passwords()

        print("\n=== LOGIN SISTEM ===")
        username = input("Username : ")
        password = input("Password : ")

        user = self.db.fetch("SELECT * FROM users WHERE username=%s", (username,))

        if not user:
            print("Username tidak ditemukan!")
            return None

        row = user[0]
        if not verify_password(password, row['password']):
            print("Password salah!")
            return None

        return User(row['id'], row['username'], row['role'])
