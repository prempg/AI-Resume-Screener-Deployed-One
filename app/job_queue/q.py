from redis import Redis
from rq import Queue
from app.config import settings

redis_connection = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
)

q = Queue(connection=redis_connection)