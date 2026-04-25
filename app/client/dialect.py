from app import settings
from app.client.expections import DialectParsingError

"""
This module provides two special functions
for parsing cryptocurrenies from settings into two dialiects:
Fullform (Symbol + Type, example: BTCUSDT, ETHUSDT) and OnlySymbol (BTC, ETH).
By default, it strictly uses the convievence that fullform are seperated by /. 
"""

# Convert crypto name to form like "BTC" or "ETH"
def crypto_to_short_form() -> list:
    result = []

    for crypto_name in settings.CHECK_CRYPTO:
        pos = crypto_name.find("/")

        if pos == -1:
            raise DialectParsingError(f"Invalid crypto name {crypto_name}")
        
        result.append(crypto_name[:pos])
    
    return result

# Convert crypto name to form like "BTCUSDT"
def crypto_to_full_form() -> list:
    result = []

    for crypto_name in settings.CHECK_CRYPTO:
        if crypto_name.find("/") == -1:
            raise DialectParsingError(f"Invalid crypto name {crypto_name}")
        
        result.append(crypto_name.replace("/", "", 1))

    return result