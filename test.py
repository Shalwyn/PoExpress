import json
import requests
from itertools import chain
from typing import List, Tuple

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    f = open('mod.txt', 'a')
    print(text, file=f)


json_blob = requests.get(url="https://www.pathofexile.com/api/trade/data/stats").json()

jprint(json_blob)

#items = tuple(chain(*[[build_from_json(y) for y in x["entries"]] for x in json_blob["result"]]))
