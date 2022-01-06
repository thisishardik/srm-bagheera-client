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
        return True
    else:
        return False


def abort_if_country_is_incorrect(country):
    if config.is_country_verified(country):
        return False
    else:
        return True


class HelloWorldResource(Resource):
    """Root Resource"""

    def get(self, *args, **kwargs):
        data = {
            "message": "It's working",
            "statusCode": 200,
        }
        response = jsonify(data)

        return response


class TaxonomyResource(Resource):
    """Taxonomy Resource to fetch data from all clients"""

    def get(self, *args, **kwargs):
        # args = taxon_args.parse_args()
        query_params = request.args.to_dict(flat=False)

        taxon_names = query_params.get('names')
        if abort_if_name_is_missing(taxon_names):
            abort(404)

        country = request.args.get('country', default="IN")
        if abort_if_country_is_incorrect(country):
            abort(404)

        limit = request.args.get('limit', default=3)

        eol_api_key = eol.API(key=12345)
        eol_pages = 1

        print(taxon_names, country, limit)

        try:
            eol_client = SRMEOLClient(
                eol_api_key, taxon_names, [], eol_pages, "")
            eol_client_res = eol_client.process_threads_pages()

            gbif_client = SRMGbifClient(taxon_names, [],
                                        country, limit, "")
            gbif_client_res = gbif_client.getOccurrence()

            data = {
                "statusCode": 200,
                "timestamp": str(datetime.datetime.now()),
                "gbif_client_res": gbif_client_res,
                "eol_client_res": eol_client_res,
                "metadata": {
                    "country_code": country,
                    "limit": limit,
                }
            }

            response = jsonify(data)

            return response

        except Exception as e:
            data = {
                "timestamp": str(datetime.datetime.now()),
                "statusCode": 500,
                "message": "Internal Server Error. The server has encountered a situation it does not know how to handle."
            }

            response = jsonify(data)

            return response


api.add_resource(HelloWorldResource, "/" + config.VERSION + "/")
api.add_resource(TaxonomyResource, "/" + config.VERSION + "/search")

if __name__ == '__main__':
    app.run()
