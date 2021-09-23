# How to run benchmark

Create Amazon S3 Bucket and EC2 instance with access to it via IAM

```
pip3 install -r requirements.txt
python3 many.py
```

# Current Stats

```
Total put time: 38.172523975372314
Time per task: 0.03817252397537232
Total get and delete time: 50.64864802360535
Time per task: 0.050648648023605344
```

# Next Step

Do tests and make plots for:
2K Bytes, 20K Bytes, 200K Bytes, 2M Bytes

(Whisker plots to see if there are extreme cases)

It's costly to establish HTTPS connection every time,
vs. Redis where you can create a single connection and use it the whole times
