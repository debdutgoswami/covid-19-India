# imports
import requests, json, os, datetime, itertools
from requests import ConnectionError
# beautifulsoup4
from bs4 import BeautifulSoup

# base url for the data
_url = 'https://www.mohfw.gov.in/'
# path to current file
path = os.path.dirname(os.path.realpath(__file__))

def getdata(state=None) -> dict:

    try:
        req = requests.get(_url).content
        update_json(req)
        return is_offline(state)
    except ConnectionError:
        return is_offline(state, offline=True)


def update_json(req):

    _timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    _update = dict()
    _total = {
        'Total': 0,
        'Cured': 0,
        'Death': 0
    }

    soup = BeautifulSoup(req, 'html.parser')
    rows = soup.find_all('tr')

    for row in rows[1:len(rows)-1]:
        col = row.find_all('td')

        if len(col)!=5:
            continue

        state = col[1].text
        # for graph
        try:
            In, cur, dth = int(col[2].text.rstrip('# ')), int(col[3].text.rstrip('# ')), int(col[4].text.rstrip('# '))
        except ValueError:
            continue

        # current data from the website
        _update.update({
            state: {
                "Total": In,
                "Cured": cur,
                "Death": dth
            }
        })

        _total['Total'] += In
        _total['Cured'] += cur
        _total['Death'] += dth

    _update.update({
        "total": {
            'In': _total['Total'],
            'Cur': _total['Cured'],
            'Dth': _total['Death']
        },
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
