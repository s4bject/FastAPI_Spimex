import redis.asyncio as asyncio_redis
import asyncio

redis_client = None


async def init_redis():
    global redis_client
    try:
        redis_client = await asyncio_redis.from_url("redis://redis:6379", decode_responses=True)  # redis://localhost:6379 если сервер не в контейнере
        print("Redis успешно инициализирован.")
    except Exception as e:
        print(f"Ошибка инициализации Redis: {e}")
        redis_client = None


async def close_redis():
    global redis_client
    if redis_client:
        await redis_client.close()
        print("Подключение к Redis закрыто.")
    else:
        print("Нет активного соединения с Redis.")


def get_redis_client():
    if redis_client is None:
        raise RuntimeError("Redis не инициализирован. Убедитесь, что init_redis был вызван.")
    return redis_client
