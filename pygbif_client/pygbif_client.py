from types import TracebackType
import numpy as np
import pandas as pd
from pygbif import registry, species, maps
from pygbif import occurrences as occ
import os
import json
import datetime


class SRMGbifClient():
    def __init__(self, species_list, taxon_keys, country, limit, file_path):
        self.species_list = species_list
        self.taxon_keys = taxon_keys
        self.country = country
        self.limit = limit
        self.file_path = file_path

    def getOccurrence(self):
        print('Finding occurrences...')
        keys = [species.name_backbone(x, self.limit)['usageKey']
                for x in self.species_list]
        occs = [occ.search(taxonKey=key, country=self.country,
                           limit=self.limit) for key in keys]
        print(f"Found {len(occs)} occurrences")

        json_data = {
            "timestamp": f"{datetime.datetime.now()}", "all_occurrences": occs}

        map_out = maps.map(taxonKey=int(self.taxon_keys[0]))
        map_out.response
        map_out.path
        map_out.img
        map_out.plot()


if __name__ == '__main__':
    species_list = ['Cyanocitta stelleri',  'Poa annuus', 'Aix sponsa',
                    'Ursus americanus', 'Pinus conorta']
    country = "US"
    limit = 10
    taxon_keys = []
    file_path = "pygbif\gbif_client_output\output.json"

    client = SRMGbifClient(species_list, taxon_keys,
                           country, limit, file_path)

    try:
        client.getOccurrence()
    except Exception as e:
        print(e)
