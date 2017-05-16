import boto3
import boto3.s3.connection
access_key = 'put your access key here!'
secret_key = 'put your secret key here!'

def get_buckets(access_key, secret_key):
    conn = boto3.connect_s3(
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
        host = 'objects.dreamhost.com',
        #is_secure=False,               # uncomment if you are not using ssl
        calling_format = boto3.s3.connection.OrdinaryCallingFormat(),
        )
    for bucket in conn.get_all_buckets():
        print "{name}\t{created}".format(
                name = bucket.name,
                created = bucket.creation_date,
        )

def get_contents(bucket_name):
    conn = boto3.connect_s3(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        host='objects.dreamhost.com',
        # is_secure=False,               # uncomment if you are not using ssl
        calling_format=boto3.s3.connection.OrdinaryCallingFormat(),
    )
    bucket = conn.lookup('clviz-bucket')

    # downloading all the files with a certain string in their name
    for key in bucket.list():
        if '.html' in key.name:
            key = bucket.get_key(key.name)
            key.get_contents_to_filename(key.name)


# def get_buckets(access_key, secret_key):
#     conn = boto.connect_s3(
#         aws_access_key_id = access_key,
#         aws_secret_access_key = secret_key,
#         host = 'objects.dreamhost.com',
#         #is_secure=False,               # uncomment if you are not using ssl
#         calling_format = boto.s3.connection.OrdinaryCallingFormat(),
#         )
#     for bucket in conn.get_all_buckets():
#         print "{name}\t{created}".format(
#                 name = bucket.name,
#                 created = bucket.creation_date,
#         )
#
# def get_contents(bucket_name):
#     s3 = boto3.resource('s3')
#     bucket = s3.Bucket('test-bucket')
#     # Iterates through all the objects, doing the pagination for you. Each obj
#     # is an ObjectSummary, so it doesn't contain the body. You'll need to call
#     # get to get the whole body.
#     for obj in bucket.objects.all():
#         key = obj.key
#         body = obj.get()['Body'].read()


