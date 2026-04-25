from app.client.base import CryptoBaseInfo
from app.client.dialect import crypto_to_short_form, crypto_to_full_form
from decimal import Decimal
from typing import NamedTuple


class CalculatingResult(NamedTuple):
    total_margin: Decimal
    percent: float


def get_margins(markets_data: list[list[CryptoBaseInfo]]) -> list[tuple[CryptoBaseInfo, CryptoBaseInfo]]:
    """
        Find the best margins for each crypto currency \n

        markets_data - the list, where each sub list is information about crypto
        currency from one market.

        Returns the list of the best margins as a tuple - (min_price, max_price)
    """
    result = []

    for short_name, full_name in zip(crypto_to_short_form(), crypto_to_full_form()):
        collected_offers = group_offers_by_symbol(markets_data, short_name, full_name)

        if len(collected_offers) <= 0:
            continue

        min_offer = get_min_offer(collected_offers)
        max_offer = get_max_offer(collected_offers)

        result.append((min_offer, max_offer))

    return result

def get_min_offer(data: list[CryptoBaseInfo]) -> CryptoBaseInfo | None:
    if len(data) <= 0:
        return None

    _min: CryptoBaseInfo = data[0]
    for crypto_info in data:
        if crypto_info.price < _min.price:
            _min = crypto_info
    return _min


def get_max_offer(data: list[CryptoBaseInfo]) -> CryptoBaseInfo | None:
    if len(data) <= 0:
        return None

    _max: CryptoBaseInfo = data[0]
    for crypto_info in data:
        if crypto_info.price > _max.price:
            _max = crypto_info
    return _max


# return grouped offers by one symbol from different market data
def group_offers_by_symbol(market_data: list[list[CryptoBaseInfo]], 
                           short_symbol: str,
                           full_symbol: str) -> list[CryptoBaseInfo]:
    
    """
        Group offers by one crypto currency symbol \n
        short_symbol - the short version of the crypto currency symbol (like BTC or ETH) \n
        full_symbol - the long version of the crypto currency symbol (like BTCUSDT) \n

        Returns the list which contains only offers with one crypto symbol
    """
    result = []
    for market_crypto_data in market_data:
        one_symbol = list(filter(lambda info: info.symbol == short_symbol or info.symbol == full_symbol, market_crypto_data))
        if len(one_symbol) <= 0:
            break

        result.append(one_symbol[0])

    return result


def calculate_offer_sum(min_offer: CryptoBaseInfo, max_offer: CryptoBaseInfo) -> CalculatingResult | None:
    """
        Calculate margin between min price and max price \n
        If margin is negative, returns None, otherwise returns margin sum and margin percent
    """

    margin = max_offer.price - min_offer.price

    if margin <= 0.0:
        return None
    
    percent = (margin / min_offer.price) * 100
    return CalculatingResult(margin, percent)