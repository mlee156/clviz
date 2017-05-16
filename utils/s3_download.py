import boto3

s3_client = boto3.client('s3')
bucket = 'clviz-bucket'
prefix = 'root/jon'

# List all objects within a S3 bucket path
response = s3_client.list_objects(
    Bucket = bucket,
    Prefix = prefix
)

# Loop through each file
for file in response['Contents']:
    # Get the file name
    name = file['Key'].rsplit('/', 1)

    # Download each file that contains a certain string to local disk
    if '.html' in name:
        s3_client.download_file(bucket, file['Key'], prefix + '/' + name[1])