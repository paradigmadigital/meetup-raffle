import os
import boto3
import json
import random

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

logger.info('Loading function')


def get_random_assistant():
    bucket = os.environ.get('ASSISTANTS_BUCKET')
    key = os.environ.get('ASSISTANTS_KEY')
    logger.info('Reading data from (bucket: {}, key: {})'.format(bucket, key))

    obj = s3.get_object(Bucket=bucket, Key=key)
    content = obj['Body'].read().decode('utf-8')

    assistants = {}

    for row in content.split('\n')[1:]:
        columns = row.split('\t')
        if len(columns) > 1 and not columns[2]:  # skip empty rows and staff assistants
            assistants[columns[1]] = {'nombre': columns[0], 'url': columns[8]}

    logger.info('Read {} rows'.format(len(assistants)))

    random_assistant_id = random.choice(list(assistants.keys()))
    assistant = assistants.get(random_assistant_id)

    logger.info('Randomly get: (user: {}, name: {})'.format(random_assistant_id, assistant.get('nombre')))

    return assistant


def lambda_handler(event, context):
    assistant = get_random_assistant()
    html = '<h1>...and the winner is: ' \
           '<a href="{}" target="_blank">{}</a></h1>' \
           '<a href="javascript:window.location.href=window.location.href">try again</a>'\
        .format(assistant.get('url'), assistant.get('nombre'))

    return {
        'statusCode': '200',
        'body': html,
        'headers': {
            'Content-Type': 'text/html; charset=utf-8',
        }
    }
