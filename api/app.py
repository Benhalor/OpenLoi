import sys
import json 

sys.path.append("../AssembleeNationale")
import AssembleeNationale

from flask import abort
from flask import request
from flask import Flask, request, _request_ctx_stack
from flask_cors import CORS, cross_origin




app = Flask(__name__)
cors = CORS(app)

assembleeNationale = AssembleeNationale.AssembleeNationale(verbose=2)


@app.route("/api/test")
def helloWord():
    """
    Displays a text proving that the API is accessible.
    """
    return "<p>It works !</p>"


@app.route("/api/search/<string:query>", methods=['GET'])
def getSearchResults(query):
    if request.method == 'GET':
        ret = assembleeNationale.search(query)
        print(ret)
        return ret

    else:
        # 405 Method Forbidden
        abort(405)


"""

connection = psycopg2.connect(
		   database="postgres", user='postgres', password='password', host='localhost', port= '5432'
		)
		connection.autocommit = True
		cursor = connection.cursor()"""
