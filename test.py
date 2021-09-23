import boto3

s3 = boto3.resource('s3')

txt_data = b'This is the content of the file uploaded from python boto3 asdfasdf'

obj = s3.Object('kir-test-bucket-1', 'file_name.txt')

result = obj.put() # obj.delete() # .get()['Body'].read() #.put(Body=txt_data)

print(result)
