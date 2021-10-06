# How to run benchmark

- Create Amazon S3 Bucket and EC2 instance with access to it via IAM
- Create ElasiCache Redis Instance

## To Start on Ubuntu 20.04 EC2

```
sudo apt update
sudo apt install python3-pip
git clone https://github.com/Loonride/s3-test-1.git
cd s3-test-1
pip3 install -r requirements.txt
export REDIS_HOST=...

python3 benchmark.py
```

## To Retrieve results then plot

```
./scp_data.sh <EC2 ip>
python plot.py
```

# Results on EC2

- Using Redis cache.t3.medium, EC2 t2.small
- 100 runs each
- Redis/S3 always emptied before each PUT-GET-DELETE sequence
- Single Redis connection used, boto3 makes new API calls for each request
- Uses random bytes of a fixed length

![alt text](https://raw.githubusercontent.com/Loonride/s3-test-1/main/figures/figure1.png)

```
Redis 1000 Bytes Means: PUT 0.001s, GET 0.001s, DELETE 0.001s
Redis 10000 Bytes Means: PUT 0.001s, GET 0.001s, DELETE 0.001s
Redis 100000 Bytes Means: PUT 0.001s, GET 0.001s, DELETE 0.001s
Redis 1000000 Bytes Means: PUT 0.012s, GET 0.009s, DELETE 0.001s
Redis 10000000 Bytes Means: PUT 0.088s, GET 0.092s, DELETE 0.001s
Redis 100000000 Bytes Means: PUT 0.989s, GET 1.057s, DELETE 0.001s
S3 1000 Bytes Means: PUT 0.047s, GET 0.025s, DELETE 0.029s
S3 10000 Bytes Means: PUT 0.038s, GET 0.020s, DELETE 0.022s
S3 100000 Bytes Means: PUT 0.063s, GET 0.026s, DELETE 0.024s
S3 1000000 Bytes Means: PUT 0.096s, GET 0.040s, DELETE 0.023s
S3 10000000 Bytes Means: PUT 0.288s, GET 0.253s, DELETE 0.024s
S3 100000000 Bytes Means: PUT 1.645s, GET 1.810s, DELETE 0.025s
```

# Results on External Endpoint (Kir's Laptop)

**Important: these results are much more susceptible to network latency since the laptop communicating with S3 is outside of the AWS internal network, as any other FuncX endpoint would be**

![alt text](https://raw.githubusercontent.com/Loonride/s3-test-1/main/figures/figure2.png)

```
S3 1000 Bytes Means: PUT 0.115s, GET 0.053s, DELETE 0.057s
S3 10000 Bytes Means: PUT 0.105s, GET 0.055s, DELETE 0.056s
S3 100000 Bytes Means: PUT 0.134s, GET 0.062s, DELETE 0.059s
S3 1000000 Bytes Means: PUT 0.493s, GET 0.105s, DELETE 0.060s
S3 10000000 Bytes Means: PUT 3.655s, GET 0.462s, DELETE 0.056s
S3 100000000 Bytes Means: PUT 36.265s, GET 3.626s, DELETE 0.058s
```

# Cost Structure Analysis

- All prices here are based on AWS us-east-1 region on 10/6/21
- Outbound data transfer costs are $0.09 per GB for both S3 and EC2. However, note that this cost could be removed if results were sent directly to a user-owned S3 instance.
- Integrating S3 alongside Redis could probably allow us to reduce the size of the Redis cache, meaning the low cost of S3 is a small price to pay for savings from Redis.

### S3

S3 charges $0.023 per GB per month, which is a trivial cost compared to Redis rates and the PUT/GET rates of S3.

The PUT rate is $0.005 per 1000 PUTs and GET rate is $0.0004 per 1000 GETs. DELETE is free.

#### Cost for 1 million 1MB (1,000 GB total) tasks

(Assume each task sat in S3 for ~1 week, 1 PUT/GET, with outbound transfer)

```
monthly cost = (S3 storage cost) + (S3 PUT/GET cost) + (outbound transfer)
monthly cost = 0.023 * 1000 * 0.25 + 0.0054 * 1000 + 0.09 * 1000
monthly cost = 5.75 + 5.4 + 90
monthly cost = $101.15
monthly cost w/o outbound transfer = $11.15
```

### Redis

For the current `cache.r5.xlarge` instance we are using, on-demand price per hour is $0.431/hour

#### Cost for 1 million 1MB (1,000 GB total) tasks

```
monthly cost = (redis monthly cost) + (outbound transfer)
monthly cost = 0.431 * 730 + 0.09 * 1000
monthly cost = 314.63 + 90
monthly cost = $404.63
monthly cost w/o outbound transfer = $314.63
```

# Conclusion

Redis has massive costs compared to S3 and is less scalable, so we should only be using Redis for small tasks that require fast PUT/GET operations. The benefit of keeping Redis for fast-cache storage is reducing PUT/GET overhead in performance-critical situations. S3 can add close to 0.1s of overhead for small tasks, while Redis adds <0.002s  of overhead, which is a significant difference for small tasks that can take on average <0.5s to execute using the executor interface.

# Storage/Caching Rules Proposal

- Tasks <1MB should be placed in Redis, and all others should go straight to S3
- Users should be able to indicate in a task submission that they want a task to go directly to S3 (but they cannot request going to Redis)
- A service can be created that is designated to moving tasks that are >1 hour old from Redis to S3 (Is there a way in Redis to trigger an action on expiration?)
- When a the web service or WebSocket service queries a task, it will first check Redis, and if it is a cache miss it will go to S3 (We need to make S3 directly queryable by the user so that we don't have to copy from S3 then send within our services)

# Extra Notes

Make whisker plots to check extreme cases

It's costly to establish HTTPS connection every time, vs. Redis where you can create a single connection and use it the whole time
