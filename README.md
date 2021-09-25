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

# Extra Notes

Make whisker plots to check extreme cases

It's costly to establish HTTPS connection every time, vs. Redis where you can create a single connection and use it the whole time
