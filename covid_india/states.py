# imports
import requests, json, os, datetime, itertools
from requests import ConnectionError

# base url for the data
_url = 'https://www.mohfw.gov.in/data/datanew.json'
# path to current file
path = os.path.dirname(os.path.realpath(__file__))

def getdata(state=None) -> dict:

    try:
        req = requests.get(_url).json()
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

    for i in req:
        state, act, cur, dth, tot = i['state_name'], i['new_active'], \
                                    i['new_cured'], i['new_death'], \
                                    (i['new_active'] + i['new_cured'] +
                                     i['new_death'])

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
    _total['Total'] = _total['Total']//2
    _total['Active'] = _total['Active']//2
    _total['Cured'] = _total['Cured']//2
    _total['Death'] = _total['Death']//2
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
