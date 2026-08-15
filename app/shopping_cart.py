# app/shopping_cart.py
import requests


class InsufficientBalanceError(Exception):
    pass


class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, item: str, price: float, quantity: int = 1):
        if price < 0 or quantity <= 0:
            raise ValueError("Price must be non-negative and quantity must be positive.")

        if item in self.items:
            self.items[item]["quantity"] += quantity
        else:
            self.items[item] = {"price": price, "quantity": quantity}

    def remove_item(self, item: str):
        if item in self.items:
            del self.items[item]

    def get_total_price(self, discount_percent: float = 0.0) -> float:
        if not 0.0 <= discount_percent <= 100.0:
            raise ValueError("Discount must be between 0 and 100.")

        raw_total = sum(data["price"] * data["quantity"] for data in self.items.values())
        discount_amount = (raw_total * discount_percent) / 100.0
        return round(raw_total - discount_amount, 2)

    def checkout(self, payment_api_url: str, card_token: str) -> bool:
        total = self.get_total_price()
        if total == 0:
            raise ValueError("Cannot checkout an empty cart.")

        payload = {"token": card_token, "amount": total}
        response = requests.post(payment_api_url, json=payload, timeout=5)

        if response.status_code == 200 and response.json().get("status") == "SUCCESS":
            self.items.clear()
            return True
        elif response.status_code == 402:
            raise InsufficientBalanceError("Payment failed: Insufficient funds.")
        return False
