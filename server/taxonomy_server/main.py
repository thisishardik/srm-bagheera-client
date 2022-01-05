from flask import Flask, request, jsonify, Response
from flask_restful import Api, Resource, reqparse, abort
import json

import datetime
from urllib import parse

from pygbif_client.pygbif_client import SRMGbifClient
from eol_client.eol_client import SRMEOLClient
from eol_client import eol_api_wrapper as eol
import config

app = Flask(__name__)
api = Api(app)

taxon_args = reqparse.RequestParser()
taxon_args.add_argument(
    'sci_names', type=list, help='Atleast 1 scientific name is required', required=True)


"""Error handling functions @app.errorhandler"""


def abort_if_name_is_missing(names):
    if names is None or len(names[0]) is 0:
        print("THIS")
        abort(404)


def abort_if_country_is_incorrect(name):
    if name not in config.COUNTRIES:
        print("NOT THIS")
        abort(404)


class TaxonomyResource(Resource):
    """Taxonomy Resource to fetch data from all clients"""

    def get(self, *args, **kwargs):
        # args = taxon_args.parse_args()
        query = request.args.get('names').split(',')
        # abort_if_name_is_missing(query)

        taxon_input_names = [name.replace('%20', " ") for name in query]

        country = request.args.get('country', default="US")
        # abort_if_country_is_incorrect(country)

        limit = request.args.get('limit', default=3)

        eol_api_key = eol.API(key=12345)
        eol_pages = 1

        try:
            print(taxon_input_names, country, limit)
            gbif_client = SRMGbifClient(taxon_input_names, [],
                                        country, limit, "")
            gbif_client_res = gbif_client.getOccurrence()

            eol_client = SRMEOLClient(
                eol_api_key, taxon_input_names, [], eol_pages, "")
            eol_client_res = eol_client.process_threads_pages()

            data = {
                "statusCode": 200,
                "timestamp": str(datetime.datetime.now()),
                "gbif_client_res": gbif_client_res,
                "eol_client_res": eol_client_res,
            }

            response = jsonify(data)

            return response

        except Exception as e:
            return Response(status=500)


api.add_resource(TaxonomyResource, "/taxon")

if __name__ == '__main__':
    app.run(debug=True)
