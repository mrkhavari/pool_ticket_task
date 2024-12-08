from functools import wraps
import aioredis
import json
from enum import Enum

from app.core.config import get_settings


class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        return super().default(obj)
    

def cache_response(
    cache_name: str,
    exclude_list: list[str] = ["db"],
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not get_settings().ENABLE_USING_CACHE:
                return await func(*args, **kwargs)
            redis_client: aioredis.Redis = aioredis.from_url(get_settings().REDIS_URL)

            new_kwargs = {
                key: value for key, value in kwargs.items() if key not in exclude_list
            }
            cache_key = "{arg1}:{arg2}".format(arg1=cache_name, arg2=str(new_kwargs))
            cached_response = await redis_client.get(cache_key)

            if cached_response:
                print("Using Cache")
                mapping = json.loads(cached_response.decode("utf-8"))
                return mapping
            
            response = await func(*args, **kwargs)

            await redis_client.set(
                cache_key,
                json.dumps(
                    [res.dict() for res in response]
                    if isinstance(response, list)
                    else response.dict(),
                    cls=EnumEncoder,
                ),
            )

            await redis_client.close()

            return response

        return wrapper

    return decorator
