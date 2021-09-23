import uuid
import time
import boto3

from generate_task import S3Task

s3 = boto3.resource('s3')

n_tasks = 1000

tasks = []
task_data_list = []
for i in range(n_tasks):
    task = S3Task()
    tasks.append(task)
    task_data_list.append(task.serialize())

start = time.time()

objs = []
for task_data in task_data_list:
    task_id = str(uuid.uuid4())
    task_addr = task_id
    obj = s3.Object('kir-test-bucket-1', task_addr)
    obj.put(Body=task_data)

    objs.append(obj)

end = time.time()
diff1 = end - start
print(f"Total put time: {diff1}")
time_per_task = diff1 / n_tasks
print(f"Time per task: {time_per_task}")

start = time.time()

for obj in objs:
    res = obj.get()['Body'].read()
    obj.delete()

end = time.time()
diff2 = end - start
print(f"Total get and delete time: {diff2}")
time_per_task = diff2 / n_tasks
print(f"Time per task: {time_per_task}")
