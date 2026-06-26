import pytest

from app.tools import DISCOUNT_CODES, redeem_discount_code


@pytest.fixture(autouse=True)
def reset_discount_codes():
    """Resets the in-memory discount code database state before each test."""
    for code in DISCOUNT_CODES:
        DISCOUNT_CODES[code]["redeemed"] = False
        DISCOUNT_CODES[code]["user_id"] = None


def test_successful_redemption():
    """Verifies that a registered user can successfully redeem a valid code."""
    result = redeem_discount_code("user123", "WELCOME50")
    assert result["status"] == "success"
    assert "successfully redeemed" in result["message"]
    assert DISCOUNT_CODES["WELCOME50"]["redeemed"] is True
    assert DISCOUNT_CODES["WELCOME50"]["user_id"] == "user123"


def test_double_redemption_fails():
    """Ensures that single-use codes cannot be redeemed more than once."""
    # First redemption
    redeem_discount_code("user123", "WELCOME50")
    # Second redemption attempt
    result = redeem_discount_code("user_abhishek", "WELCOME50")
    assert result["status"] == "error"
    assert "already been redeemed" in result["message"]


def test_unregistered_user_fails():
    """Verifies that non-registered users are blocked from code redemption."""
    result = redeem_discount_code("fake_user", "WELCOME50")
    assert result["status"] == "error"
    assert "not registered" in result["message"]


def test_invalid_code_fails():
    """Checks that invalid/unknown codes are rejected."""
    result = redeem_discount_code("user123", "INVALIDCODE")
    assert result["status"] == "error"
    assert "invalid" in result["message"]


def test_whitespace_and_case_normalization():
    """Ensures code input is normalized (whitespace stripped, case ignored)."""
    result = redeem_discount_code("user123", "  summer20  ")
    assert result["status"] == "success"
    assert "successfully redeemed" in result["message"]
    assert DISCOUNT_CODES["SUMMER20"]["redeemed"] is True
    assert DISCOUNT_CODES["SUMMER20"]["user_id"] == "user123"
