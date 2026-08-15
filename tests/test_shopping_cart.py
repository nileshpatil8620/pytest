# tests/test_shopping_cart.py
from unittest.mock import Mock, patch
import pytest
from app.shopping_cart import InsufficientBalanceError

# -------------------------------------------------------------
# 1. Basic Assertions & Fixture Usage
# -------------------------------------------------------------
def test_add_item_to_empty_cart(empty_cart):
    empty_cart.add_item("Book", 20.0, 2)
    assert "Book" in empty_cart.items
    assert empty_cart.items["Book"]["quantity"] == 2
    assert empty_cart.get_total_price() == 40.0


def test_remove_item(populated_cart):
    assert "Mouse" in populated_cart.items
    populated_cart.remove_item("Mouse")
    assert "Mouse" not in populated_cart.items


# -------------------------------------------------------------
# 2. Testing Expected Exceptions
# -------------------------------------------------------------
def test_invalid_item_values_raises_error(empty_cart):
    with pytest.raises(ValueError, match="Price must be non-negative"):
        empty_cart.add_item("InvalidItem", price=-5.0, quantity=1)

    with pytest.raises(ValueError, match="quantity must be positive"):
        empty_cart.add_item("InvalidItem", price=10.0, quantity=0)


def test_empty_cart_checkout_raises_error(empty_cart):
    with pytest.raises(ValueError, match="Cannot checkout an empty cart"):
        empty_cart.checkout("https://api.payment.com/pay", "token_123")


# -------------------------------------------------------------
# 3. Parameterized Testing
# -------------------------------------------------------------
# @pytest.mark.parametrize(
#     "discount, expected_total",
#     [
#         (0.0, 1100.0),    # No discount
#         (10.0, 990.0),    # 10% off
#         (50.0, 550.0),    # 50% off
#         (100.0, 0.0),     # 100% off (Free)
#     ]
# )
# def test_discounts_on_populated_cart(populated_cart, discount, expected_total):
#     # Base: 1000 + (50 * 2) = 1100
#     assert populated_cart.get_total_price(discount_percent=discount) == expected_total


# -------------------------------------------------------------
# 4. Custom Markers & Skipping
# -------------------------------------------------------------
@pytest.mark.smoke
def test_quick_cart_summary(populated_cart):
    assert len(populated_cart.items) == 2


@pytest.mark.skip(reason="Payment v2 endpoint is under maintenance")
def test_legacy_checkout():
    pass


@pytest.mark.xfail(reason="Expected failure: Discount > 100 not yet supported via UI")
def test_over_discount_xfail(populated_cart):
    populated_cart.get_total_price(150.0)


# -------------------------------------------------------------
# 5. Mocking External API Calls (requests.post)
# -------------------------------------------------------------
@patch("app.shopping_cart.requests.post")
def test_successful_checkout(mock_post, populated_cart):
    # Setup mock response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "SUCCESS", "transaction_id": "tx_999"}
    mock_post.return_value = mock_response

    result = populated_cart.checkout("https://api.payment.com/pay", "valid_token")

    assert result is True
    assert len(populated_cart.items) == 0  # Cart cleared on success
    mock_post.assert_called_once()


@patch("app.shopping_cart.requests.post")
def test_checkout_insufficient_balance(mock_post, populated_cart):
    mock_response = Mock()
    mock_response.status_code = 402
    mock_post.return_value = mock_response

    with pytest.raises(InsufficientBalanceError):
        populated_cart.checkout("https://api.payment.com/pay", "low_balance_token")
