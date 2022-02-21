import os
import sys
import time
import json 

sys.path.append("../AssembleeNationale")
import AssembleeNationale

from flask import abort
from flask import request
from flask import Flask, request, _request_ctx_stack
from flask_cors import CORS, cross_origin




app = Flask(__name__)
cors = CORS(app)

if os.getenv("POSTGRESQL_ADDON_DB") is not None:
    # Clever cloud
    assembleeNationale = AssembleeNationale.AssembleeNationale(
        database=os.getenv("POSTGRESQL_ADDON_DB"),
        userDatabase = os.getenv("POSTGRESQL_ADDON_USER"),
        passwordDatabase = os.getenv("POSTGRESQL_ADDON_PASSWORD"),
        hostDatabase = os.getenv("POSTGRESQL_ADDON_HOST"),
        portDatabase = os.getenv("POSTGRESQL_ADDON_PORT"),
        verbose=2, 
        setup=False)
else:
    # Local
    assembleeNationale = AssembleeNationale.AssembleeNationale(
        database='postgres',
        userDatabase='postgres',
        passwordDatabase='password',
        hostDatabase='localhost',
        portDatabase='5432',
        verbose=2,
        setup=False)


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
        #print(ret)
        return ret

    else:
        # 405 Method Forbidden
        abort(405)

@app.route("/api/lastNews/", methods=['GET'])
def getLastNews():
    if request.method == 'GET':
        ret = assembleeNationale.getLastNews()
        #print(ret)
        return ret

    else:
        # 405 Method Forbidden
        abort(405)

@app.route("/api/documentsDossierLegislatif/<string:uid>", methods=['GET'])
def getDocumentsDossierLegislatif(uid):
    if request.method == 'GET':
        ret = assembleeNationale.getDossierLegislatifdocumentsByUid(uid)
        #print(ret)
        return ret

    else:
        # 405 Method Forbidden
        abort(405)

@app.route("/api/documentById/<string:uid>", methods=['GET'])
def getDocumentById(uid):
    if request.method == 'GET':
        ret = assembleeNationale.getDocumentByUid(uid)
        #print(ret)
        return ret

    else:
        # 405 Method Forbidden
        abort(405)

@app.route("/api/dossierLegislatif/<string:uid>", methods=['GET'])
def getDossierLegislatif(uid):
    if request.method == 'GET':
        ret = assembleeNationale.getDossierLegislatifByUid(uid)
        #print(ret)
        return ret

    else:
        # 405 Method Forbidden
        abort(405)

@app.route("/api/amendements/<string:uid>", methods=['GET'])
def getAmendements(uid):
    if request.method == 'GET':
        lastTime = time.time()
        ret = assembleeNationale.getAmendementsByUid(uid)
        print("duration for getting "+ str(ret["numberOfAmendement"])+" amendements : "+str(time.time()-lastTime))
        return ret

    else:
        # 405 Method Forbidden
        abort(405)

@app.route("/api/amendementsQuery/<string:query>&<string:uid>", methods=['GET'])
def getAmendementsQuery(uid, query):
    if request.method == 'GET':
        ret = assembleeNationale.getAmendementsQuery(uid, query)
        #print(ret)
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
