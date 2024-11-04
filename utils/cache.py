import json, asyncio, pickle, os
from typing import Callable, Any
import redis.asyncio as redis
from functools import wraps
from fastapi import Request

# redis_client = redis.Redis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), db=int(os.getenv("REDIS_DB")), password=os.getenv("REDIS_PASSWORD"))
# prefix = os.getenv("PREFIX")
# all_caches = {}

# def redis_cache(ttl:int, auto_cache:bool=False):
#     global all_caches
#     def decorator(func: Callable):
#         @wraps(func)
#         async def wrapper(request:Request, *args, **kwargs) -> Any:
#             try:
#                 key = f"/{prefix}{request.url._url.split(f'/{prefix}')[1]}"
#             except:
#                 key = request.url._url
            
#             cached_value = await redis_client.get(key)
            
#             if auto_cache:
#                 all_caches[key] = {"func":lambda: func(request, *args, **kwargs), "ttl":ttl}

#             if cached_value is not None:
#                 return pickle.loads(cached_value)

#             result = await func(request, *args, **kwargs)

#             await redis_client.setex(key, ttl, pickle.dumps(result))

#             return result

#         return wrapper
#     return decorator


# async def auto_cache():
#     global all_caches
#     while True:
#         for key, data in all_caches.items():
#             func, ttl = data["func"], data["ttl"]
#             if await redis_client.get(key) is None:
#                 result = await func()
#                 await redis_client.setex(key, ttl, pickle.dumps(result))
#         await asyncio.sleep(3)