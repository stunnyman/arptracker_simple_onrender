import asyncio
import requests
from ..config.settings import EXCHANGES, BINANCE, USDT, SLEEP_TIME
from ..database.db import save_arp_value

async def fetch_arp(exchange_key: str, token: str) -> float:
    exchange = EXCHANGES.get(exchange_key)
    if exchange:
        url = exchange['api_url'].format(token)
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None, lambda: requests.get(url)
            )
            response.raise_for_status()
            data = response.json()
            arp_value = round(float(data['data']['savingFlexibleProduct'][0]['apy']) * 100, 2)
            await save_arp_value(exchange_key, token, arp_value)
            return arp_value
        except Exception as ex:
            print(f"Error fetching ARP: {ex}")
            return None
    return None

async def background_monitor():
    while True:
        await fetch_arp(BINANCE, USDT)
        await asyncio.sleep(SLEEP_TIME) 