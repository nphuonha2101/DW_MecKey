def convert_price(price_str):
    price_str = price_str.replace('₫', '').strip()
    price_str = price_str.replace(',', '')
    return int(price_str)