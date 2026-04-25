from app import settings
from app.client.base import Client, CryptoBaseInfo
from app.client.expections import ClientAPIError, ClientInternalError
from app.client.dialect import crypto_to_short_form
from decimal import Decimal
import httpx

class KucoinClient(Client):
    SUCCESS_CODE = 200000

    def __init__(self):
        super().__init__("KucoinAPI")


    # get the current price
    async def get_current_state(self) -> list[CryptoBaseInfo]:
        async with httpx.AsyncClient() as session:
            response = await session.get(
                url=settings.KUCOIN_PRICE_URL,
                params={"currencies" : ",".join(crypto_to_short_form())}
            )

            if response.status_code != 200:
                raise ClientAPIError(
                    api_name=self.api_name,
                    msg="Some error occured during making request"
                )
        
            data = response.json()
            self._validate_response_body(data)

            result = []
            for symbol, price in data["data"].items():
                result.append(
                    CryptoBaseInfo(
                        market="Kucoin",
                        symbol=symbol,
                        name=None,
                        price=Decimal(price)
                    )
                )

            return result
    

    def _validate_response_body(self, response_json: dict):
        """Get the response json and check its body. If some body structure is invalid, raise error"""

        if "data" not in response_json:
            raise ClientInternalError(
                api_name=self.api_name,
                msg="No data about cryptocurrency"
            )
        
        if len(response_json["data"]) <= 0:
            raise ClientAPIError(
                api_name=self.api_name,
                msg="No cryptocurrenies got"
            )
