from app.client.base import Client, CryptoBaseInfo
from app.client.expections import ClientInternalError, BreakingRequestLimitError, ClientAPIError
from app.client.dialect import crypto_to_full_form
from decimal import Decimal
from app import settings
import json
import httpx
from enum import Enum


class BinanceAPIStatusCodes(Enum):
    BREAKING_LIMIT = 429
    IP_BANNED = 418


class BinanceAPIClient(Client):
    def __init__(self):
        super().__init__("Binance API")


    # gets the current price
    async def get_current_state(self) -> CryptoBaseInfo:
        async with httpx.AsyncClient() as session:
            response = await session.get(
                url=settings.BINANCE_PRICE_URL,
                params={"symbols": self._parse_crypto_to_query()}
            )

            self._check_response(response) # Временно перекидываю весь обьект чтобы посмотреть на его состояния при ошибки
            crypto_data = []    
            for crypto in response.json():
                try:
                    price = self.extract_price(crypto)
                    symbol, _ = self.extract_crypto_info(crypto)
                except KeyError:
                    raise ClientInternalError(self.api_name, "Cannot extract price or crypto info")
                
                crypto_data.append(
                    CryptoBaseInfo(
                        market="Binance",
                        price=price,
                        symbol=symbol
                    )
                )

            return crypto_data


    def extract_price(self, data: dict) -> Decimal:
        return Decimal(data["price"])


    def extract_crypto_info(self, data: dict) -> tuple[str, str]:
        return (data["symbol"], None)  # binance api doesnt return full name of crypto


    def _parse_crypto_to_query(self) -> str:
        return json.dumps(crypto_to_full_form(), separators=(",", ":"))


    def _check_response(self, response):
        response_status = response.status_code
        if response_status == BinanceAPIStatusCodes.BREAKING_LIMIT:
            print(response)
            raise BreakingRequestLimitError(self.api_name, "The limit of using Binance API is broken. If continue send requests, IP can be banned by Binance IP")
            # на будующее, почитать сколько составляет лимит и попытаться обойти его (через timestamp + ban_timeout)

        if response_status == BinanceAPIStatusCodes.IP_BANNED:
            raise BreakingRequestLimitError(self.api_name, "The IP Adress is banned")
        
        body = response.json()

        if "code" in body:
            raise ClientAPIError(
                api_name=self.api_name,
                msg=body["msg"]
            )