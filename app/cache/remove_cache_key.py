import aioredis

from app.core.config import get_settings

async def remove_cache_key(
    prefix: str,
) -> None:
    
    pattern = f"{prefix}:*"
    
    redis_client: aioredis.Redis = aioredis.from_url(get_settings().REDIS_URL)
    async for key in redis_client.scan_iter(pattern):
        await redis_client.delete(key)
    await redis_client.close()