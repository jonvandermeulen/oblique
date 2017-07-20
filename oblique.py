from flask import Flask
from flask_slack import Slack
from rdoclient import RandomOrgClient as rorgcli
import os

app = Flask(__name__)
slack = Slack(app)
app.add_url_rule('/', view_func=slack.dispatch)

slacktoken = os.getenv('SLACKTOKEN')
randokey = os.getenv('RANDOMORG_KEY')
team = os.getenv('SLACKTEAM')


def random_client():
    rnd = rorgcli(randokey)
    return rnd

rnd = random_client()


def strategy():
    with open('oblique.txt', 'r') as ost:
        strats = ost.readlines()
        length = len(strats)
    idx = rnd.generate_integers(1, 0, length)
    strat = strats[idx[0]].strip()
    return strat


def acute():
    with open('acute.txt', 'r') as ost:
        acutes = ost.readlines()
        length = len(acutes)
    idx = rnd.generate_integers(1, 0, length)
    strat = acutes[idx[0]].strip()
    return strat


@slack.command('oblique',
               token=slacktoken,
               team_id=team,
               methods=['POST'])
def oblique(**kwargs):
    text = kwargs.get('text')
    strat = strategy()
    acu = acute()
    if text == 'dev':
        message = '%s\n' % (acu)
    else:
        message = '%s\n' % (strat)
    return slack.response(message)


# strategy text url - for backward compatibility
@app.route('/strategy')
def strategy_txt():
    strat = strategy() + '\n'
    return strat

# oblique text url
@app.route('/oblique')
def oblique_txt():
    strat = strategy() + '\n'
    return strat

# acute text url
@app.route('/acute')
def acute_txt():
    acu = acute() + '\n'
    return acu


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
