import os
import uuid
from flask import Flask, request, render_template
import json
import random

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/raffle', methods=['GET'])
def raffle():
    ASSISSTANTS_FILE = 'Microservicios_y_Serverless_en_proyectos_Python.xls'
    f = open(ASSISSTANTS_FILE)
    content = f.read()

    assistants = {}

    for row in content.split('\n')[1:]:
        columns = row.split('\t')
        if len(columns) > 1 and not columns[2]:  # skip empty rows and staff assistants
            assistants[columns[1]] = {'nombre': columns[0], 'url': columns[8]}

    logger.info('Read {} rows'.format(len(assistants)))

    winner_id = random.choice(list(assistants.keys()))
    winner = assistants.get(winner_id)

    logger.info('Randomly get: (user: {}, name: {})'.format(winner_id, winner.get('nombre')))

    return render_template('index.html', winner=winner)

#
# def lambda_handler(event, context):
#     assistant = get_random_assistant()
#     html = '<h1>...and the winner is: ' \
#            '<a href="{}" target="_blank">{}</a></h1>' \
#            '<a href="javascript:window.location.href=window.location.href">try again</a>'\
#         .format(assistant.get('url'), assistant.get('nombre'))
#
#     return {
#         'statusCode': '200',
#         'body': html,
#         'headers': {
#             'Content-Type': 'text/html; charset=utf-8',
#         }
#     }

if __name__ == '__main__':
    app.run(debug=True)
