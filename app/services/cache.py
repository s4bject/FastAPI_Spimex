import json
from datetime import date

from database.redis_client import get_redis_client
from fastapi import Request, Response
from functools import wraps
from typing import Callable
import logging

logger = logging.getLogger(__name__)


def date_handler(obj):
    if isinstance(obj, date):
        return obj.isoformat()


def cache_response():
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            redis = get_redis_client()

            request: Request = kwargs.get("request")
            if not request:
                raise ValueError("Request объект должен быть передан через Depends")

            cache_key = f"cache:{request.url.path}:{request.url.query}"

            cached_data = await redis.get(cache_key)
            if cached_data:
                logger.info(f"Кэш найден для ключа {cache_key}. Возвращаем кэшированные данные.")
                return Response(content=cached_data, media_type="application/json")

            logger.info(f"Кэш для ключа {cache_key} не найден. Выполняем запрос.")
            response = await func(*args, **kwargs)
            if isinstance(response, list) or isinstance(response, dict):
                response_json = json.dumps(
                    [
                        item.dict() if hasattr(item, 'dict') else item
                        for item in response
                    ],
                    ensure_ascii=False, default=date_handler
                )
                await redis.set(cache_key, response_json)
                logger.info(f"Данные успешно сохранены в кэш для ключа: {cache_key}")
            return response

        return wrapper

    return decorator
