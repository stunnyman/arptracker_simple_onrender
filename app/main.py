from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
import asyncio
import logging
from datetime import datetime
from .database import get_db, engine

from .exchanges import BinanceExchange
from .models import Exchange, ARPData, BTCPrice
from .constants import (BINANCE, USDT, USDC, FETCH_INTERVAL_SECONDS, ERROR_RETRY_INTERVAL_SECONDS)
from .models import Base
Base.metadata.create_all(bind=engine)

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def fetch_and_store_data(db: Session):
    try:
        # Get or create Binance exchange record
        exchange = db.query(Exchange).filter(Exchange.name == BINANCE).first()
        if not exchange:
            exchange = Exchange(name=BINANCE)
            db.add(exchange)
            db.commit()

        async with BinanceExchange() as binance:
            # Fetch ARP rates for supported coins
            for coin in [USDT, USDC]:
                arp_value = await binance.get_arp_rates(coin)
                if arp_value is not None:
                    arp_data = ARPData(
                        exchange_id=exchange.id,
                        coin=coin,
                        arp_value=arp_value,
                        timestamp=datetime.utcnow()
                    )
                    db.add(arp_data)

            # Fetch BTC price
            btc_price = await binance.get_btc_price()
            if btc_price is not None:
                price_data = BTCPrice(
                    exchange_id=exchange.id,
                    price=btc_price,
                    timestamp=datetime.utcnow()
                )
                db.add(price_data)

            db.commit()
            logger.info("Data fetched and stored successfully")

    except Exception as e:
        logger.error(f"Error fetching data: {str(e)}")
        db.rollback()
        raise

@app.get("/")
async def get_latest_data(db: Session = Depends(get_db)):
    try:
        latest_timestamp = db.query(
            db.query(ARPData.timestamp.label('timestamp'))
            .union(db.query(BTCPrice.timestamp.label('timestamp')))
            .order_by(desc('timestamp'))
            .limit(1)
            .scalar_subquery()
        ).scalar()

        if not latest_timestamp:
            return {
                "timestamp": None,
                "btc_price": None
            }

        # Get BTC price for this timestamp
        btc_price = (
            db.query(BTCPrice)
            .filter(BTCPrice.timestamp <= latest_timestamp)
            .order_by(desc(BTCPrice.timestamp))
            .first()
        )

        # Get ARP data for each coin
        latest_arp_data = (
                db.query(
                    ARPData.coin,
                    Exchange.name.label('exchange_name'),
                    ARPData.arp_value
                )
                .join(Exchange)
                .filter(ARPData.timestamp <= latest_timestamp)
                .distinct(ARPData.coin, Exchange.name)
                .order_by(
                    ARPData.coin,
                    Exchange.name,
                    desc(ARPData.timestamp)
                )
                .all()
        )

            # Format the ARP data
        arp_values = {}
        seen_pairs = set()
        for arp in latest_arp_data:
            pair_key = f"{arp.coin}_{arp.exchange_name}"
            if pair_key not in seen_pairs:
                arp_values[pair_key] = arp.arp_value
                seen_pairs.add(pair_key)

        return {
            "timestamp": latest_timestamp,
            "btc_price": btc_price.price if btc_price else None,
            **arp_values
        }

    except Exception as e:
        logger.error(f"Error fetching latest data: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Background task for fetching data
@app.on_event("startup")
async def startup_event():
    async def periodic_fetch():
        while True:
            try:
                db = next(get_db())
                await fetch_and_store_data(db)
                await asyncio.sleep(FETCH_INTERVAL_SECONDS)
            except Exception as e:
                logger.error(f"Error in periodic fetch: {str(e)}")
                await asyncio.sleep(ERROR_RETRY_INTERVAL_SECONDS)
            finally:
                if db is not None:
                    db.close()

    asyncio.create_task(periodic_fetch())
