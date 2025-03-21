import asyncpg
from datetime import datetime
from app.config.settings import DATABASE_URL, TABLE_NAME

_pool = None

async def get_pool():
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(dsn=DATABASE_URL)
    return _pool

async def setup_database():
    if not DATABASE_URL:
        raise RuntimeError("Database URL not configured")

    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(f'''
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id SERIAL PRIMARY KEY,
                exchange_name VARCHAR(50),
                token VARCHAR(50),
                arp_value DECIMAL,
                timestamp TIMESTAMP
            )
        ''')

async def save_arp_value(exchange_name: str, token: str, arp_value: float):
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            f'INSERT INTO {TABLE_NAME} (exchange_name, token, arp_value, timestamp) VALUES ($1, $2, $3, $4)',
            exchange_name, token, arp_value, datetime.now()
        )

async def get_latest_arp_values(limit: int = 1000):
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.fetch(
            f"SELECT timestamp, arp_value FROM {TABLE_NAME} ORDER BY timestamp DESC LIMIT {limit}"
        )

async def close_pool():
    global _pool
    if _pool:
        await _pool.close()
        _pool = None 