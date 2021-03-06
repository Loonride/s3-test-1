import os
import redis

redis_host = os.environ.get('REDIS_HOST')
print(f"Using redis host: {redis_host}")

r = redis.Redis(redis_host, port=6379, db=0)

r.set('foo', b'bar')
print(r.get('foo'))

r.delete('foo')
