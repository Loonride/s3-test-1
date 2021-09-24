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

# Stats

```
Total put time: 38.172523975372314
Time per task: 0.03817252397537232
Total get and delete time: 50.64864802360535
Time per task: 0.050648648023605344
```

# Extra Notes

Do tests and make plots for:
2K Bytes, 20K Bytes, 200K Bytes, 2M Bytes

(Whisker plots to see if there are extreme cases)

It's costly to establish HTTPS connection every time,
vs. Redis where you can create a single connection and use it the whole time
