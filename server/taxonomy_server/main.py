from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
import json

app = Flask(__name__)
api = Api(app)

user_args = reqparse.RequestParser()
user_args.add_argument(
    'name', type=str, help='Name of the person is required.', required=True)


class HelloWorld(Resource):
    def get(self, name):
        args = user_args.parse_args()
        res = {"data": "Hello World!", 'args': args}
        return res


api.add_resource(HelloWorld, "/hello/<string:name>")

if __name__ == '__main__':
    app.run(debug=True)
