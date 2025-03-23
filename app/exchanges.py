from abc import ABC, abstractmethod
import aiohttp
from typing import Optional#None
import logging
from .constants import (
    BINANCE, SUPPORTED_COINS,
    BINANCE_ARP_URL, BINANCE_BTC_PRICE_URL
)

class ExchangeBase(ABC):
    def __init__(self):
        self.name = ""
        self.supported_coins = []
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    @abstractmethod
    async def get_arp_rates(self, coin: str) -> Optional[int]:
        pass

class BinanceExchange(ExchangeBase):
    def __init__(self):
        super().__init__()
        self.name = BINANCE
        self.supported_coins = SUPPORTED_COINS
        self.arp_url = BINANCE_ARP_URL
        self.btc_price_url = BINANCE_BTC_PRICE_URL

    async def get_arp_rates(self, coin: str) -> Optional[int]:
        # if coin not in self.supported_coins:
        #     logging.error(f"Unsupported coin {coin} for {self.name}")
        #     return None

        try:
            async with self.session.get(self.arp_url % coin) as response:
                if response.status == 200:
                    data = await response.json()
                    # Extract value from Binance
                    if data.get("data") and len(data["data"]) > 0:
                        return round(float(data['data']['savingFlexibleProduct'][0]['apy']) * 100, 2)
                return None
        except Exception as e:
            logging.error(f"Error fetching ARP rates from {self.name}: {str(e)}")
            return None

    async def get_btc_price(self) -> Optional[int]:
        try:
            async with self.session.get(self.btc_price_url) as response:
                if response.status == 200:
                    data = await response.json()
                    return round(float(data['price']))
                return None
        except Exception as e:
            logging.error(f"Error fetching BTC price from {self.name}: {str(e)}")
            return None 