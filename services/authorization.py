import hmac

from database.db_manager import DBManager

class AuthService:
    def __init__(self, db_manager):
        self.db = db_manager

    def signup(self, name, email, password):
        self.db.add_customer(name, email, password)

    def login(self, email, password):
        if not isinstance(password, str):
            return None

        customer = self.db.get_customer_by_email(email)
        if customer is None or not isinstance(customer.password, str):
            return None

        if self.db.is_password_hash(customer.password):
            if self.db.verify_password(password, customer.password):
                return customer
            return None

        if hmac.compare_digest(password.encode("utf-8"), customer.password.encode("utf-8")):
            self.db.update_customer_password(customer.customer_id, password)
            return self.db.get_customer_by_email(email)

        return None
