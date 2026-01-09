DEFAULT_CURRENCY = "USD"
TAX_RATE = 0.21
COUPONS = {"SAVE10", "SAVE20", "VIP"}

def parse_request(request: dict):
    user_id = request.get("user_id")
    items = request.get("items")
    coupon = request.get("coupon")
    currency = request.get("currency")
    return user_id, items, coupon, currency

def validate_request(user_id, items, currency):
    if user_id is None:
        raise ValueError("user_id is required")
    if items is None:
        raise ValueError("items is required")
    if currency is None:
        currency = DEFAULT_CURRENCY
    if not isinstance(items, list):
        raise ValueError("items must be a list")
    if len(items) == 0:
        raise ValueError("items must not be empty")
    for it in items:
        if "price" not in it or "qty" not in it:
            raise ValueError("item must have price and qty")
        if it["price"] <= 0:
            raise ValueError("price must be positive")
        if it["qty"] <= 0:
            raise ValueError("qty must be positive")
    return currency

def calculate_subtotal(items):
    return sum(it["price"] * it["qty"] for it in items)

def calculate_discount(subtotal, coupon):
    if not coupon:
        return 0
    if coupon == "SAVE10":
        return int(subtotal * 0.10)
    elif coupon == "SAVE20":
        return int(subtotal * 0.20 if subtotal >= 200 else subtotal * 0.05)
    elif coupon == "VIP":
        return 50 if subtotal >= 100 else 10
    else:
        raise ValueError("unknown coupon")

def calculate_tax(total_after_discount):
    return int(total_after_discount * TAX_RATE)

def generate_order_id(user_id, items_count):
    return f"{user_id}-{items_count}-X"

def process_checkout(request: dict) -> dict:
    user_id, items, coupon, currency = parse_request(request)
    currency = validate_request(user_id, items, currency)
    
    subtotal = calculate_subtotal(items)
    discount = calculate_discount(subtotal, coupon)
    total_after_discount = max(subtotal - discount, 0)
    tax = calculate_tax(total_after_discount)
    total = total_after_discount + tax

    order_id = generate_order_id(user_id, len(items))
    
    return {
        "order_id": order_id,
        "user_id": user_id,
        "currency": currency,
        "subtotal": subtotal,
        "discount": discount,
        "tax": tax,
        "total": total,
        "items_count": len(items),
    }