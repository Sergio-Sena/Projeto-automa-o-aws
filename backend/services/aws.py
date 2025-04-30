import boto3
import os

def get_lambda_functions(access_key, secret_key, region="us-east-1"):
    client = boto3.client(
        "lambda",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )
    response = client.list_functions()
    return [func["FunctionName"] for func in response["Functions"]]