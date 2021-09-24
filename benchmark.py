import uuid
import timeit
import secrets
import json
import os
import sys
from statistics import mean
from pathlib import Path
from abc import ABC, abstractmethod
import boto3
import redis


redis_host = os.environ.get('REDIS_HOST')


def generate_bytes(n):
    return secrets.token_bytes(n)


class Benchmark(ABC):
    def __init__(self):
        self.n_tasks = 10
        self.byte_test_sizes = [1000, 10000, 100000, 1000000, 10000000]
        self.task_size_bytes = None
        self.data_filename = 'data.json'
        self.name = 'data'

        file_dir = Path(__file__).parent.resolve()
        self.data_dir = os.path.join(file_dir, 'data')
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)

    def get_data_path(self):
        data_path = os.path.join(self.data_dir, self.data_filename)
        return data_path

    @abstractmethod
    def put_times(self):
        pass

    @abstractmethod
    def get_times(self):
        pass

    @abstractmethod
    def delete_times(self):
        pass

    def time_size(self, task_size_bytes):
        self.task_size_bytes = task_size_bytes
        put_ts = self.put_times()
        get_ts = self.get_times()
        delete_ts = self.delete_times()

        put_mean = mean(put_ts)
        get_mean = mean(get_ts)
        delete_mean = mean(delete_ts)
        print("{:s} {:d} Bytes Means: PUT {:.3f}s, GET {:.3f}s, DELETE {:.3f}s".format(self.name, task_size_bytes, put_mean, get_mean, delete_mean))

        return (put_ts, get_ts, delete_ts)

    def time_sizes(self):
        sizes = self.byte_test_sizes
        put_group = {}
        get_group = {}
        delete_group = {}
        for size in sizes:
            (put_ts, get_ts, delete_ts) = self.time_size(size)
            key = str(size)
            put_group[key] = put_ts
            get_group[key] = get_ts
            delete_group[key] = delete_ts

        final_output = {
            "put": put_group,
            "get": get_group,
            "delete": delete_group
        }
        with open(self.get_data_path(), 'w') as fp:
            json.dump(final_output, fp)


class S3Benchmark(Benchmark):
    def __init__(self):
        super().__init__()
        self.data_filename = 's3_data.json'
        self.name = 'S3'
        self.s3 = boto3.resource('s3')
        self.objs = []

    def put_times(self):
        self.objs = []
        times = []
        for _ in range(self.n_tasks):
            task_id = str(uuid.uuid4())
            obj = self.s3.Object('kir-test-bucket-1', task_id)
            self.objs.append(obj)

            b = generate_bytes(self.task_size_bytes)
            t = timeit.timeit(lambda: obj.put(Body=b), number=1)
            times.append(t)
        return times

    def get_times(self):
        times = []
        for obj in self.objs:
            t = timeit.timeit(lambda: obj.get()['Body'].read(), number=1)
            times.append(t)
        return times

    def delete_times(self):
        times = []
        for obj in self.objs:
            t = timeit.timeit(lambda: obj.delete(), number=1)
            times.append(t)
        return times


class RedisBenchmark(Benchmark):
    def __init__(self):
        super().__init__()
        self.data_filename = 'redis_data.json'
        self.name = 'Redis'
        self.rc = redis.Redis(redis_host, port=6379, db=0)
        self.task_ids = []

    def put_times(self):
        self.task_ids = []
        times = []
        for _ in range(self.n_tasks):
            task_id = str(uuid.uuid4())
            self.task_ids.append(task_id)

            b = generate_bytes(self.task_size_bytes)
            t = timeit.timeit(lambda: self.rc.set(task_id, b), number=1)
            times.append(t)
        return times

    def get_times(self):
        times = []
        for task_id in self.task_ids:
            t = timeit.timeit(lambda: self.rc.get(task_id), number=1)
            times.append(t)
        return times

    def delete_times(self):
        times = []
        for task_id in self.task_ids:
            t = timeit.timeit(lambda: self.rc.delete(task_id), number=1)
            times.append(t)
        return times


if __name__ == '__main__':
    # s3_bench = S3Benchmark()
    # s3_bench.time_sizes()
    redis_bench = RedisBenchmark()
    redis_bench.time_sizes()
