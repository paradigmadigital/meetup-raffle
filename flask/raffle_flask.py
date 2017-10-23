from __future__ import unicode_literals
import codecs

import uuid
from flask import Flask, request, render_template, url_for, redirect
import random
import boto3

import logging

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

app = Flask(__name__)

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')
bucket = s3.Bucket('meetup-raffle')


@app.route('/health', methods=['GET'])
def health():
    return 'ok'


@app.route('/', methods=['GET'])
def index():
    logger.info('Called func "index"')
    raffles = [b.key for b in bucket.objects.all()]
    logger.info('Get raffles files from S3: %s', raffles)
    return render_template('index.html', raffles=raffles)


@app.route('/raffle/<raffle_name>', methods=['GET'])
def raffle(raffle_name):
    logger.info('Called func "raffle"')
    return render_template('raffle.html', raffle_name=raffle_name, winner=None)


@app.route('/raffle/<raffle_name>/winner', methods=['GET'])
def winner(raffle_name):
    logger.info('Called func "winner"')
    tmp_file = '/tmp/{}'.format(uuid.uuid4())
    s3_client.download_file('meetup-raffle', raffle_name, tmp_file)

    f = codecs.open(tmp_file, encoding='utf-8')
    content = f.read()

    assistants = {}

    NAME_COLUMN = 0
    URL_COLUMN = 8
    TITLE_COLUMN = 2

    for row in content.split('\n')[1:]:
        columns = row.split('\t')
        if len(columns) > 1 and not columns[TITLE_COLUMN]:  # skip empty rows and staff assistants
            assistants[columns[1]] = {'name': columns[NAME_COLUMN], 'url': columns[URL_COLUMN], 'winner': False}

    logger.info('Read {} rows'.format(len(assistants)))

    winner_id = random.choice(list(assistants.keys()))
    assistants[winner_id]['winner'] = True

    logger.info('Randomly get: (user: {}, name: {})'.format(winner_id, assistants[winner_id]['name']))

    return render_template('raffle.html', raffle_name=raffle_name, assistants=assistants.values())


if __name__ == '__main__':
    app.run(debug=True)
