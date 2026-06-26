# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# In-memory store for registered users
REGISTERED_USERS = {"user123", "user_abhishek", "customer_prime", "retail_buyer"}

# In-memory store for discount codes and their redemption status
DISCOUNT_CODES = {
    "WELCOME50": {"redeemed": False, "user_id": None},
    "SUMMER20": {"redeemed": False, "user_id": None},
}


def redeem_discount_code(
    user_id: str,
    code: str,
) -> dict:
    """Redeems a single-use discount code for a registered user.

    Args:
        user_id: The registered user ID of the customer.
        code: The discount code to redeem (e.g., WELCOME50, SUMMER20).

    Returns:
        dict: A dictionary containing the 'status' (success/error) and a descriptive 'message'.
    """
    code_upper = code.strip().upper()

    if user_id not in REGISTERED_USERS:
        return {
            "status": "error",
            "message": f"User ID '{user_id}' is not registered. Only registered users can redeem discount codes.",
        }

    if code_upper not in DISCOUNT_CODES:
        return {
            "status": "error",
            "message": f"Discount code '{code}' is invalid.",
        }

    code_data = DISCOUNT_CODES[code_upper]
    if code_data["redeemed"]:
        return {
            "status": "error",
            "message": f"Discount code '{code_upper}' has already been redeemed by user '{code_data['user_id']}' and cannot be used again.",
        }

    code_data["redeemed"] = True
    code_data["user_id"] = user_id

    return {
        "status": "success",
        "message": f"Success! Discount code '{code_upper}' has been successfully redeemed for user '{user_id}'.",
    }
