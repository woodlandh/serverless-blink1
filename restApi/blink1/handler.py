from __future__ import print_function

import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../"))

from lib import dynamoRead, dynamoUpdate, dynamoCreate, dynamoDelete

import json
import logging
import string

log = logging.getLogger()
log.setLevel(logging.DEBUG)

def handler(event, context):
    log.debug("Received event {}".format(json.dumps(event)))
    method = event['httpMethod']
    if method == 'GET':
        endpoint = event['endpoint']
        return dynamoRead(endpoint)
    elif method == 'PUT':
        endpoint = event['endpoint']
        rgb = event['rgb']
        return dynamoUpdate(endpoint, rgb)
    elif method == 'POST':
        endpoint = event['endpoint']
        return dynamoCreate(endpoint)
    elif method == 'DELETE':
        endpoint = event['endpoint']
        return dynamoDelete(endpoint)
    else:
        return "UNSUPPORTED"

