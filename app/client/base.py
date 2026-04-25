from decimal import Decimal
from pydantic import BaseModel

class CryptoBaseInfo(BaseModel):
    market: str
    symbol: str
    name: str | None = None
    price: Decimal


class Client:

    def __init__(self, api_name: str):
        self.__api = api_name

    # the api name of the client
    @property
    def api_name(self):
        return self.__api

    # gets the current price #REQUIRED
    async def get_current_state(self) -> CryptoBaseInfo:
        pass

    # gets the current price from the data given from the response #NOT REQUIRED
    def extract_price(self, data: dict) -> Decimal:
        return None

    # returns the pair (symbol, name) of the cryptocurrency #NOT REQUIRED
    def extract_crypto_info(self, data: dict) -> tuple[str, str]:
        return None


    def __contains__(self, item):
        return item.api_name == self.__api
    
