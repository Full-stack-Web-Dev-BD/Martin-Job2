
def parse_price(price_str):
    if isinstance(price_str, (int, float)):
        return float(price_str)
    elif isinstance(price_str, str):
        # Remove currency symbols and commas, and then convert to float
        try:
            numeric_value = float(''.join(filter(lambda x: x.isdigit() or x == '.', price_str)))
            return numeric_value
        except ValueError:
            return 0  # Set default value to 0 if cannot convert to float
    else:
        return 0  # Set default value to 0 for None or other non-string types
