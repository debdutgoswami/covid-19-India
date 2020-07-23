# imports
import requests, json, os, datetime, itertools, pandas as pd
from requests import ConnectionError

# base url for the data
_url = 'https://www.mohfw.gov.in/'
# path to current file
path = os.path.dirname(os.path.realpath(__file__))

def getdata(state=None) -> dict:

    try:
        req = requests.get(_url).text
        update_json(req)
        return is_offline(state)
    except ConnectionError:
        return is_offline(state, offline=True)

def update_json(req):

    _timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    _update = dict()
    _total = {
        'Total' : 0,
        'Active': 0,
        'Cured' : 0,
        'Death' : 0
    }
    df = pd.read_html(req)

    _, s, a, c, d, t = df[0]

    for i in range(36):
        try:
            state, act, cur, dth, tot = df[0][s][i].rstrip('# '), df[0][a][i].rstrip('# '), df[0][c][i].rstrip('# '), df[0][d][i].rstrip('# '), df[0][t][i].rstrip('# ')
        except AttributeError:
            continue

        _update.update({
            state: {
                "Total" : int(tot),
                "Active": int(act),
                "Cured" : int(cur),
                "Death" : int(dth)
            }
        })

        _total['Total'] += _update[state]['Total']
        _total['Active'] += _update[state]['Active']
        _total['Cured'] += _update[state]['Cured']
        _total['Death'] += _update[state]['Death']

    _update.update({
        'Total': _total
    })

    _update.update({
        "lastupdated": _timestamp
    })

    with open(os.path.join(path,'stats.json'), 'w') as f:
        json.dump(_update, f)


def is_offline(state, offline=False):

    with open(os.path.join(path,'stats.json'), 'r') as f:
        _json = json.load(f)

    if not state:
        val = dict(itertools.islice(_json.items(), len(_json)-2))
    else:
        try:
            val = _json[state]
        except KeyError:
            val = {}
    if offline:
        val.update({
            "lastupdated": _json['lastupdated']
        })

    return val