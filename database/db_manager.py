import hashlib
import hmac
import secrets
import sqlite3
from models.customers import Customer
from models.menu import MenuItem


class DBManager:
    # Password hashes include their algorithm, work factor, salt, and derived key.
    _PASSWORD_ALGORITHM = "pbkdf2_sha256"
    _PASSWORD_ITERATIONS = 600_000
    _MAX_PASSWORD_ITERATIONS = 2_000_000
    _PASSWORD_SALT_BYTES = 16
    _PASSWORD_KEY_BYTES = 32

    def __init__(self, db_path='dominos.db'):
        # Open the SQLite database and ensure the application tables exist.
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    @classmethod
    def hash_password(cls, password):
        # Generate a unique salt and derive a one-way password hash.
        salt = secrets.token_bytes(cls._PASSWORD_SALT_BYTES)
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            cls._PASSWORD_ITERATIONS,
            dklen=cls._PASSWORD_KEY_BYTES,
        )
        return (
            f"{cls._PASSWORD_ALGORITHM}${cls._PASSWORD_ITERATIONS}"
            f"${salt.hex()}${digest.hex()}"
        )

    @classmethod
    def is_password_hash(cls, encoded):
        # Identify this application's encoded password format.
        return isinstance(encoded, str) and encoded.startswith(
            f"{cls._PASSWORD_ALGORITHM}$"
        )

    @classmethod
    def verify_password(cls, password, encoded):
        # Reject malformed or unsupported hashes before performing the comparison.
        if not isinstance(password, str) or not isinstance(encoded, str):
            return False

        try:
            algorithm, iterations_text, salt_hex, digest_hex = encoded.split("$")
            iterations = int(iterations_text)
            salt = bytes.fromhex(salt_hex)
            expected_digest = bytes.fromhex(digest_hex)
        except ValueError:
            return False

        if (
            algorithm != cls._PASSWORD_ALGORITHM
            or not 1 <= iterations <= cls._MAX_PASSWORD_ITERATIONS
            or len(salt) != cls._PASSWORD_SALT_BYTES
            or len(expected_digest) != cls._PASSWORD_KEY_BYTES
        ):
            return False

        actual_digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            iterations,
            dklen=cls._PASSWORD_KEY_BYTES,
        )
        # Compare derived keys in constant time to reduce timing leakage.
        return hmac.compare_digest(actual_digest, expected_digest)

    def create_tables(self):
        # Create customer and menu tables when they are not already present.
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT, email TEXT UNIQUE, password TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS menu_items (
                            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT, price REAL, description TEXT)''')
        self.conn.commit()

    def add_customer(self, name, email, password):
        # Store only the password hash alongside the new customer record.
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO customers (name, email, password) VALUES (?, ?, ?)",
            (name, email, self.hash_password(password)),
        )
        self.conn.commit()

    def update_customer_password(self, customer_id, password):
        # Replace a customer's password with a freshly salted hash.
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE customers SET password=? WHERE customer_id=?",
            (self.hash_password(password), customer_id),
        )
        self.conn.commit()

    def get_customer_by_email(self, email):
        # Load the matching customer for login and account-related operations.
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE email=?", (email,))
        row = cursor.fetchone()
        if row:
            return Customer(*row)
        return None

    def add_menu_item(self, name, price, description):
        # Add a menu item to the database.
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO menu_items (name, price, description) VALUES (?, ?, ?)", (name, price, description))
        self.conn.commit()

    def get_all_menu_items(self):
        # Return all menu rows as MenuItem model objects.
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM menu_items")
        rows = cursor.fetchall()
        return [MenuItem(*row) for row in rows]
