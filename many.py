import uuid
import time
import boto3

s3 = boto3.resource('s3')

start = time.time()

objs = []
for i in range(100):
    txt_data = b'This is the content of the file uploaded from python boto3 asdfasdf'

    task_id = str(uuid.uuid4())
    task_addr = task_id
    obj = s3.Object('kir-test-bucket-1', task_addr)
    obj.put(Body=txt_data)

    objs.append(obj)

end = time.time()
diff1 = end - start
print(diff1)

start = time.time()

for obj in objs:
    res = obj.get()['Body'].read()
    obj.delete()

end = time.time()
diff2 = end - start
print(diff2)
