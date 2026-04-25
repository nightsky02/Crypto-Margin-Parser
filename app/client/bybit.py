from app.client.base import Client, CryptoBaseInfo
from app.client.expections import ClientInternalError
from app.client.dialect import crypto_to_full_form
from app import settings
from decimal import Decimal
import httpx
import logging

logger = logging.getLogger(__name__)


class BybitAPIClient(Client):
    def __init__(self):
        super().__init__("BybitAPI")

    async def get_current_state(self) -> list[CryptoBaseInfo]:
        # Since bybit doesn't support multi symbols in one request,
        # use the 'for' loop to send one request for one crypto symbol

        result = []
        async with httpx.AsyncClient() as client:
            logger.info(f"BybitAPIClient starts sending requests to get prices")

            for crypto_name in crypto_to_full_form():
                response = await client.get(
                    url=settings.BYBIT_PRICE_URL,
                    params={
                        "category": "spot",
                        "symbol": crypto_name
                    }
                )

                response_body = self.extract_body_or_raise_error(response.json())
                symbol, _ = self.extract_crypto_info(response_body)

                result.append(CryptoBaseInfo(
                    market="Bybit",
                    symbol=symbol,
                    price=self.extract_price(response_body)
                ))

            logger.info(f"BybitAPIClient successfully finished")

            return result

    def extract_body_or_raise_error(self, response_data: dict):
        # TODO: directly handling IP blocking or warning about it
        if response_data["retCode"] != 0:
            raise ClientInternalError(
                api_name=self.api_name,
                msg=response_data["retMsg"]
            )

        if "list" not in response_data["result"]:
            raise ClientInternalError(
                self.api_name,
                msg="Couldn't get cryptocurrencies from the response"
            )
        
        # The first element of the list property
        return response_data["result"]["list"][0]

    def extract_price(self, data: dict) -> Decimal:
        return Decimal(data["lastPrice"])

    def extract_crypto_info(self, data: dict) -> tuple[str, str]:
        return (data["symbol"], None)
