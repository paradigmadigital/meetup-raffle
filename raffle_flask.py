import os
import uuid
from flask import Flask, request, render_template, url_for, redirect
import json
import random

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


app = Flask(__name__)

ASSISTANTS_FILES = {
    'jetbrains': 'jetbrains.xls',
    'bds': 'bds.xls'
}


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/raffle/<name>', methods=['GET'])
def raffle(name):
    return render_template('raffle.html', raffle_name=name, winner=None)


@app.route('/raffle/<name>/<get_winner>', methods=['GET'])
def winner(name, get_winner):
    f = open(ASSISTANTS_FILES.get(name))
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

    return render_template('raffle.html', raffle_name=name, winner=winner)


if __name__ == '__main__':
    app.run(debug=True)
