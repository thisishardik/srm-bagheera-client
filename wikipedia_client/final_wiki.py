import json
from urllib.request import urlopen
url="http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&titles=Green%20algae&rvsection=0"
json_url = urlopen(url)
data = json.loads(json_url.read())
data=data.json()
with open("sample.json", "w") as outfile:
    json.dump(data, outfile)