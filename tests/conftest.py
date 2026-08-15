import pytest
from app.shopping_cart import ShoppingCart


@pytest.fixture(scope="function")
def empty_cart():
    """Provides a fresh shopping cart before each test function."""
    cart = ShoppingCart()
    yield cart
    # Teardown logic (runs after test execution)
    cart.items.clear()


@pytest.fixture(scope="function")
def populated_cart(empty_cart):
    """Fixture chaining: Pre-populates the empty cart with sample items."""
    empty_cart.add_item("Laptop", 100.0, 1)
    empty_cart.add_item("Mouse", 50.0, 2)
    return empty_cart
