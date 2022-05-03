from flask_cors import CORS, cross_origin
from flask import Flask, request, _request_ctx_stack
from flask import request
from flask import abort
import os
import sys

sys.path.append("AssembleeNationale")
sys.path.append('Senat')

import Senat
import AssembleeNationale


app = Flask(__name__)
cors = CORS(app)

if os.getenv("POSTGRESQL_ADDON_DB") is not None:
    # Clever cloud
    assembleeNationale = AssembleeNationale.AssembleeNationale(
        database=os.getenv("POSTGRESQL_ADDON_DB"),
        userDatabase=os.getenv("POSTGRESQL_ADDON_USER"),
        passwordDatabase=os.getenv("POSTGRESQL_ADDON_PASSWORD"),
        hostDatabase=os.getenv("POSTGRESQL_ADDON_HOST"),
        portDatabase=os.getenv("POSTGRESQL_ADDON_PORT"),
        verbose=2,
        setup=False)
    senat = Senat.Senat(
        database=os.getenv("POSTGRESQL_ADDON_DB"),
        userDatabase=os.getenv("POSTGRESQL_ADDON_USER"),
        passwordDatabase=os.getenv("POSTGRESQL_ADDON_PASSWORD"),
        hostDatabase=os.getenv("POSTGRESQL_ADDON_HOST"),
        portDatabase=os.getenv("POSTGRESQL_ADDON_PORT"),
        verbose=2)
else:
    # Local
    assembleeNationale = AssembleeNationale.AssembleeNationale(
        database='postgres',
        userDatabase='postgres',
        passwordDatabase='password',
        hostDatabase='172.30.0.4',
        portDatabase='5432',
        verbose=2,
        setup=False)
    senat = Senat.Senat(
        database='postgres',
        userDatabase='postgres',
        passwordDatabase='172.30.0.4',
        hostDatabase='localhost',
        portDatabase='5432',
        verbose=2)


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
        return ret

    else:
        # 405 Method Forbidden
        abort(405)


@app.route("/api/lastNews/", methods=['GET'])
def getLastNews():
    if request.method == 'GET':
        ret = assembleeNationale.getLastNews()
        return ret

    else:
        # 405 Method Forbidden
        abort(405)


@app.route("/api/documentsDossierLegislatif/<string:uid>", methods=['GET'])
def getDocumentsDossierLegislatif(uid):
    if request.method == 'GET':
        ret = assembleeNationale.getDossierLegislatifdocumentsByUid(uid)
        return ret

    else:
        # 405 Method Forbidden
        abort(405)


@app.route("/api/documentById/<string:uid>", methods=['GET'])
def getDocumentById(uid):
    if request.method == 'GET':
        ret = assembleeNationale.getDocumentByUid(uid)
        # print(ret)
        return ret

    else:
        # 405 Method Forbidden
        abort(405)


@app.route("/api/questionEcrite/<string:uid>", methods=['GET'])
def getQuestionEcrite(uid):
    if request.method == 'GET':
        ret = assembleeNationale.getQuestionEcriteByUid(uid)
        return ret

    else:
        # 405 Method Forbidden
        abort(405)


@app.route("/api/questionOraleSansDebat/<string:uid>", methods=['GET'])
def getQuestionOraleSansDebat(uid):
    if request.method == 'GET':
        ret = assembleeNationale.getQuestionOraleSansDebatByUid(uid)
        # print(ret)
        return ret

    else:
        # 405 Method Forbidden
        abort(405)


@app.route("/api/questionAuGouvernement/<string:uid>", methods=['GET'])
def getQuestionAuGouvernement(uid):
    if request.method == 'GET':
        ret = assembleeNationale.getQuestionAuGouvernementByUid(uid)
        return ret

    else:
        # 405 Method Forbidden
        abort(405)


@app.route("/api/dossierLegislatif/<string:uid>", methods=['GET'])
def getDossierLegislatif(uid):
    if request.method == 'GET':
        ret = assembleeNationale.getDossierLegislatifByUid(uid)
        # print(ret)
        return ret

    else:
        # 405 Method Forbidden
        abort(405)


@app.route("/api/amendementsAN/uid=<string:uid>", methods=['GET'])
def getAmendementsAN(uid):
    if request.method == 'GET':
        ret = assembleeNationale.getAmendementsByUid(uid)
        return ret

    else:
        # 405 Method Forbidden
        abort(405)

@app.route("/api/amendementsSenat/id=<string:id>&projectId=<string:projectId>", methods=['GET'])
def getAmendementsSenat(id, projectId):
    if request.method == 'GET':
        ret = senat.getAmendementsByUid(id, projectId)
        return ret

    else:
        # 405 Method Forbidden
        abort(405)

@app.route("/api/amendementsQuery/<string:query>&<string:uid>", methods=['GET'])
def getAmendementsQuery(uid, query):
    if request.method == 'GET':
        ret = assembleeNationale.getAmendementsQuery(uid, query)
        return ret

    else:
        # 405 Method Forbidden
        abort(405)

@app.route("/api/discussionAN/uid=<string:uid>", methods=['GET'])
def getDiscussionAN(uid):
    if request.method == 'GET':
        ret = assembleeNationale.getDiscussionANByUid(uid)
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
