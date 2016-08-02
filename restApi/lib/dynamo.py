#!/usr/bin/env python2.7

import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

import os
import logging
log = logging.getLogger()

sls_stage = os.environ['SERVERLESS_STAGE']
sls_proj = os.environ['SERVERLESS_PROJECT']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('{}-{}-table'.format(sls_stage, sls_proj))

def dynamoRead(endpoint):
    try:
        response = table.get_item(
            Key={
                'endpoint': endpoint
            },
            AttributesToGet=[
                'rgb',
            ]
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        if 'Item' in response:
            return "{}".format(response['Item']['rgb'])
        else:
            return "ERROR: no endpoint in database"

def dynamoCreate(endpoint):
    try:
        response = table.put_item(
           Item={
                'endpoint': endpoint,
                'rgb': "#000000"
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return "{}".format(e.response['Error']['Message'])
    else:
        if response is not None:
            return "{}".format(endpoint)
        else:
            return "ERROR: unknown, no return value from dynamo put_item"

def dynamoUpdate(endpoint, rgb):
    try:
        response = table.update_item(
            Key={
                'endpoint': '{}'.format(endpoint)
            },
            UpdateExpression='SET rgb = :val1',
            ExpressionAttributeValues={
                ':val1': '{}'.format(rgb)
            },
            ReturnValues='ALL_NEW'
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return "{}".format(e.response['Error']['Message'])
    else:
        if 'Attributes' in response:
            return "{}".format(response['Attributes']['rgb'])
        else:
            return "ERROR: unknown, no return value from dynamo update_item"

def dynamoDelete(endpoint):
    try:
        response = table.delete_item(
            Key={
                'endpoint': endpoint,
            },
            ReturnValues='ALL_OLD'
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return "{}".format(e.response['Error']['Message'])
    else:
        if 'Attributes' in response:
            return "{}".format(endpoint)
        else:
            return "ERROR: no data, endpoint did not exist"
