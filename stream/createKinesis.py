# Author: Hyeong Joon Suh
# Filename: createKinesis.py
# Description: use boto3 library to create AWS Kinesis Stream

import boto3

client = boto3.client("kinesis")
client.create_stream(StreamName="twitter", ShardCount=1)
