import eol_api_wrapper as eol
import os
import json
import jsonify
import urllib
import datetime
from urllib.parse import quote


class SRMEOLClient():
    def __init__(self, api, species_list, taxon_keys, page, file_path):
        self.api = api
        self.species_list = species_list
        self.taxon_keys = taxon_keys
        self.page = page
        self.file_path = file_path

    def fetchTaxonKeys(self):
        print('Searching occurrences...')
        search_results = []

        self.species_list = [quote(spec) for spec in self.species_list]

        search_results = [self.api.Search(
            q=x, page=self.page) for x in self.species_list]

        # keys = [result['results'][i]['id']
        #         for result in search_results[0] for i in range(len(result['results']))]

        for occurence in search_results:
            for k in range(len(occurence.results)):
                self.taxon_keys.append(occurence.results[k]['id'])

        print(f"Found {len(self.taxon_keys)} taxonomy identifiers.")
        print(self.api.ping())

        return self.taxon_keys

    def fetchEolPages(self):
        self.taxon_keys = self.fetchTaxonKeys()

        eol_pages = [self.api.Page(id=id, details=True, images=10,
                                   synonyms=True, common_names=True) for id in self.taxon_keys]

        json_data = {
            "timestamp": f"{datetime.datetime.now()}", "all_pages": eol_pages}

        file_name = "eol_pages.json"
        self.writeDataToFile(file_name, json_data)

    def fetchEolDataObjects(self):
        self.taxon_keys = self.fetchTaxonKeys()

        data_objects = [self.api.DataObject(
            id=id) for id in self.taxon_keys]

        json_data = {
            "timestamp": f"{datetime.datetime.now()}", "all_data_objects": data_objects}

        file_name = "eol_data_objects.json"

        self.writeDataToFile(file_name, json_data)

    def fetchEolHierarchyEntries(self):
        self.taxon_keys = self.fetchTaxonKeys()

        heirarchy_entries = [self.api.Hierachy_entries(
            id=id, common_names=True, synonyms=True) for id in self.taxon_keys]

        json_data = {
            "timestamp": f"{datetime.datetime.now()}", "all_heirarchy_entries": heirarchy_entries}

        file_name = "eol_heirarchy_entries.json"

        self.writeDataToFile(file_name, json_data)

    def writeDataToFile(self, file_name, json_data):
        print(f"Writing data on {file_name}")
        if not os.path.exists(os.path.dirname(self.file_path)):
            try:
                os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            except OSError as exc:
                print(exc)

        out_file_path = os.path.join(self.file_path, file_name)

        with open(out_file_path, 'w') as handle:
            json.dump(json_data, handle)


if __name__ == '__main__':
    species_list = ['Marchantia']
    api = eol.API(key=12345)
    taxon_keys = []
    page = 1
    file_path = "eol_client/eol_client_output/"

    client = SRMEOLClient(api, species_list, taxon_keys, page,
                          file_path)

    client.fetchEolPages()

    # try:
    #     client.fetchTaxonKeys()
    # except Exception as e:
    #     print(e)
