import asyncio
import logging
from app.client import binance_api, kucoin, bybit
from app.client.base import Client
from app.client.expections import ClientAPIError, ClientInternalError, BreakingRequestLimitError, DialectParsingError
from app import price_analyzer, text_color
from app import settings

logging.basicConfig(
    format="%(asctime)s: %(message)s",
    level=logging.INFO,
    datefmt=text_color.blue_text("%d/%m/%y %H:%M:%S")
)

active_api_clients = [kucoin.KucoinClient(), binance_api.BinanceAPIClient(), bybit.BybitAPIClient()]
blocked_api_clients = []


async def main():
    global active_api_clients, blocked_api_clients

    while True:
        if len(active_api_clients) <= 1:
            break

        tasks: list[Client] = []

        for client in active_api_clients:
            if client.api_name not in blocked_api_clients:
                tasks.append(client.get_current_state())
                logging.info(text_color.yellow_text(f"{client.api_name} will be used"))
        try:
            result = await asyncio.gather(*tasks)
            offers = price_analyzer.get_margins(result)
            for min_offer, max_offer in offers:
                calculations = price_analyzer.calculate_offer_sum(min_offer, max_offer)

                if calculations is not None:
                    message = (
                        text_color.green_text(f"{min_offer.market}, {min_offer.symbol} {min_offer.price} -> ") +
                        text_color.red_text(f"{max_offer.market}, {max_offer.symbol} {max_offer.price} => ") +
                        text_color.ligth_green_text(f"{calculations.total_margin} (+{calculations.percent:.2f}%)")
                    )

                    logging.info(message)
        except ClientAPIError as e:
            logging.error(text_color.error_message(f"API error for {e.api_name}: ", e.msg))
        except ClientInternalError as e:
            logging.error(text_color.error_message(f"Internal error for {e.api_name}: ", e.msg))
        except BreakingRequestLimitError as e:
            logging.error(text_color.error_message(f"Critical error for {e.api_name}: ", e.msg))
            logging.info(text_color.yellow_text("This API will be disabled"))
            
            if e.api_name not in blocked_api_clients:
                blocked_api_clients.append(e.api_name)

        except DialectParsingError as e:
            logging.error(text_color.error_message("Critical error: ", e.args[0]))
            break

        await asyncio.sleep(60)


if len(settings.CHECK_CRYPTO) <= 0:
    logging.error(text_color.error_message("Error: ", "The Crypto-Check list is empty"))
else:
    asyncio.run(main())
