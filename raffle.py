
import boto3
import json
import random

s3 = boto3.client('s3')

print('Loading function')

def get_random_assistant():
    obj = s3.get_object(Bucket="python-madrid", Key="Microservicios_y_Serverless_en_proyectos_Python.xls")
    content = obj['Body'].read().decode('utf-8') 

    assistants = {}

    for row in content.split('\n')[1:]:
        columns = row.split('\t')
        if len(columns) > 1 and not columns[2]: # skip empty rows and staff assistants
            assistants[columns[1]] = {'nombre': columns[0], 'url': columns[8]}
    
    random_assistant_id = random.choice(list(assistants.keys()))
    return assistants.get(random_assistant_id)


def lambda_handler(event, context):
    assistant = get_random_assistant()
    
    return {
        'statusCode': '200',
        'body': json.dumps(assistant),
        'headers': {
            'Content-Type': 'application/json',
        }
    }
