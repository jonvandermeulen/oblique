from flask import Flask
from flask_slack import Slack
import os
import random

app = Flask(__name__)
slack = Slack(app)
app.add_url_rule('/', view_func=slack.dispatch)

slacktoken = os.getenv('SLACKTOKEN')
randokey = os.getenv('RANDOMORG_KEY')
team = os.getenv('SLACKTEAM')


def obl_strategy():
    with open('oblique.txt', 'r') as ost:
        strats = ost.readlines()
        length = len(strats)
    idx = random.randint(0, length)
    strat = strats[idx].strip()
    return strat


def acu_strategy():
    with open('acute.txt', 'r') as ost:
        acutes = ost.readlines()
        length = len(acutes)
    idx = random.randint(0, length)
    acu = acutes[idx].strip()
    return acu


@slack.command('oblique',
               token=slacktoken,
               team_id=team,
               methods=['POST','GET'])
def oblique(**kwargs):
    text = kwargs.get('text')
    strat = obl_strategy()
    message = '%s\n' % (strat)
    return slack.response(message)


@slack.command('acute',
               token=slacktoken,
               team_id=team,
               methods=['POST', 'GET'])
def acute(**kwargs):
    strat = acu_strategy()
    message = '%s\n' % (strat)
    return slack.response(message)


# oblique text url
@app.route('/oblique', methods=['GET', 'POST'])
def oblique_txt():
    strat = obl_strategy() + '\n'
    return strat


# acute text url
@app.route('/acute', methods=['GET', 'POST'])
def acute_txt():
    acu = acu_strategy() + '\n'
    return acu


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
