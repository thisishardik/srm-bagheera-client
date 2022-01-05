from . import eol_api_wrapper as eol
# import eol_api_wrapper as eol
from urllib.parse import quote
import os
import json
import jsonify
import urllib
import datetime
from random import random
import threading
import time
from pprint import pprint

# ______ Global variables_______
eol_pages = []


class SRMEOLClient():
    def __init__(self, api, species_list, taxon_keys, page, file_path):
        self.api = api
        self.species_list = species_list
        self.taxon_keys = taxon_keys
        self.page = page
        self.file_path = file_path

    def fetch_taxon_keys(self):
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

        return self.taxon_keys

    def fetch_eol_pages(self):
        self.taxon_keys = self.fetch_taxon_keys()
        global eol_pages
        eol_pages = [self.api.Page(id=id, details=True, images=10,
                                   synonyms=True, common_names=True) for id in self.taxon_keys]

    def process_threads_pages(self):
        thread = threading.Thread(target=self.fetch_eol_pages)
        thread.start()
        print("Thread started")
        json_data = {}

        thread.join()

        print(self.api.ping())
        page_obj = {}
        eol_pages_list = []

        # print(dir(eol_pages[0]))

        for page in eol_pages:
            identifier = page.id
            scientific_name = page.scientific_name
            richness_score = page.richness_score
            synonyms = page.synonyms                 # list
            vernacularNames = page.common_names       # list
            references = page.references
            taxon_concepts = page.taxon_concepts     # list

            page_obj = {
                "identifier": f"{identifier}",
                "scientific_name": f"{scientific_name}",
                "richness_score": f"{richness_score}",
                "synonyms": synonyms,
                "vernacularNames": vernacularNames,
                "references": f"{references}",
                "taxon_concepts": taxon_concepts
            }
            eol_pages_list.append(page_obj)

        json_data = {
            # "timestamp": f"{datetime.datetime.now()}",
            "all_pages": eol_pages_list,
        }

        # file_name = "eol_client_output.json"
        # self.writeDataToFile(file_name, json_data)

        return json_data

    def fetch_eol_data_objects(self):
        self.taxon_keys = self.fetch_taxon_keys()

        eol_data_objects = [self.api.DataObject(
            id=id) for id in self.taxon_keys]

        print(dir(eol_data_objects[0]))

        json_data = {
            "timestamp": f"{datetime.datetime.now()}", "all_data_objects": eol_data_objects}

        file_name = "eol_data_objects.json"

        self.writeDataToFile(file_name, json_data)

    def fetchEolHierarchyEntries(self):
        self.taxon_keys = self.fetch_taxon_keys()

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
    species_list = ['Cyanocitta stelleri',  'Poa annuus', 'Aix sponsa',
                    'Ursus americanus', 'Pinus conorta']
    api = eol.API(key=12345)
    taxon_keys = []
    page = 1
    file_path = "eol_client/eol_client_output/"

    client = SRMEOLClient(api, species_list, taxon_keys, page,
                          file_path)

    client.process_threads_pages()
    # client.fetch_eol_data_objects()

    # try:
    #     client.fetchTaxonKeys()
    # except Exception as e:
    #     print(e)
