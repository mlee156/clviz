import boto3

s3_client = boto3.client('s3')
bucket = 'clviz-bucket'
prefix = ''

# List all objects within a S3 bucket path
response = s3_client.list_objects(
    Bucket = bucket,
    Prefix = prefix
)

# print('response:')
# print(response)

# Loop through each file
for file in response['Contents']:
    # Get the file name
    name = file['Key'].rsplit('/', 1)[0]

    # name_str = file['Key'].rsplit('/', 1).split("'")[1].split("'",[0])

    print('filename: %s' % name)
    # Download each file that contains a certain string to local disk
    if '.html' in name:
	print('Downloading: %s' % name)
	# (bucket, name on s3, name to download as)
        s3_client.download_file(bucket, name, name)
