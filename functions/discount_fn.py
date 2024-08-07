def calculate_discount_percentage(original_price: float, discounted_price: float) -> float:
    """
    Calculates the percentage discount given the original and discounted prices.

    The discount percentage is computed using the formula:
    ((original_price - discounted_price) / original_price) * 100

    Parameters:
        original_price (float): The original price of the item.
        discounted_price (float): The discounted price of the item.

    Returns:
        float: The discount percentage.

    Raises:
        ValueError: If the original price is zero, as division by zero is not allowed.
    """
    if original_price == 0:
        raise ValueError("Original price must be non-zero")
    
    discount_percentage = ((original_price - discounted_price) / original_price) * 100
    return discount_percentage
