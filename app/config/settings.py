import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
TABLE_NAME = 'arp_values'

EXCHANGES = {
    'binance': {
        'api_url': 'https://www.binance.com/bapi/earn/v2/friendly/finance-earn/calculator/product/list?asset={}&type=Flexible'
    }
}

USDT = 'USDT'
BINANCE = 'binance'
SLEEP_TIME = 30 #1\2 min