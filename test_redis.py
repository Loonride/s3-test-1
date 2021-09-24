import os
import redis

redis_host = os.environ.get('REDIS_HOST')

r = redis.from_url(redis_host, port=6379, db=0)
r.set('foo', 'bar')
r.get('foo')
