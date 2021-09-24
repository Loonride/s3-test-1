# How to run benchmark

Create Amazon S3 Bucket and EC2 instance with access to it via IAM
Create ElasiCache Redis Instance

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

# Results

![alt text](https://raw.githubusercontent.com/Loonride/s3-test-1/main/figure.png)

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

# Extra Notes

Do tests and make plots for:
2K Bytes, 20K Bytes, 200K Bytes, 2M Bytes

(Whisker plots to see if there are extreme cases)

It's costly to establish HTTPS connection every time,
vs. Redis where you can create a single connection and use it the whole time
