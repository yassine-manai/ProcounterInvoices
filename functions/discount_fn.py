def calculate_discount_percentage(original_price, discounted_price):
    if original_price == 0:
        raise ValueError("Original price must be non-zero")
    
    discount_percentage = ((original_price - discounted_price) / original_price) * 100
    return discount_percentage






