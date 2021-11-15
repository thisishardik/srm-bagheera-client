import eol_api_wrapper as eol
import os
import json
import jsonify
import urllib
import datetime
from urllib.parse import quote

api = eol.API(key=12345)
print(api.ping())

# res = api.Search(q="Marchantia", page=1)
page = api.Page(id=491995, details=True, images=10,
                synonyms=True, common_names=True)
# obj = api.DataObject()
# hei = api.Hierachy_entries()

# a = []
# a = res.results
js_data = {"data": page.taxon_concepts}

with open('sample.json', 'w') as handle:
    json.dump(js_data, handle)
