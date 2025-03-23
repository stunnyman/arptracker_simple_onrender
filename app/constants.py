USDT = 'USDT'
USDC = 'USDC'

BINANCE = 'Binance'
# GATE = 'Gate'#TODO
# BYBIT = 'Bybit'

BINANCE_ARP_URL = "https://www.binance.com/bapi/earn/v2/friendly/finance-earn/calculator/product/list?asset=%s&type=Flexible"
BINANCE_BTC_PRICE_URL = "https://api.binance.com/api/v3/avgPrice?symbol=BTCUSDT"

SUPPORTED_COINS = [USDT, USDC]

FETCH_INTERVAL_SECONDS = 300
ERROR_RETRY_INTERVAL_SECONDS = 60