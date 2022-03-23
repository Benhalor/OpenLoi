import os
import io
import time
import json

import sys
import fileinput
import shutil
import zipfile
import traceback
import datetime
import psycopg2
import requests
from psycopg2 import sql


class Senat:

    """Constructor
            Creation of the object with default values
            @params verbose : integer specifying the amount of text written in the console by this lib.
                    0 : nothing
                    1 : important informations
                    2 : everything

    """

    def __init__(self, database='', userDatabase='', passwordDatabase='', hostDatabase='', portDatabase='', verbose=0):

        self.__verbose = verbose

        self.__amendementDbUrl = "https://data.senat.fr/data/ameli/ameli.zip"

        self.__database = database
        self.__userDatabase = userDatabase
        self.__passwordDatabase = passwordDatabase
        self.__hostDatabase = hostDatabase
        self.__portDatabase = portDatabase

        self.__amendementTableDefinition = {
            "tableName": "amd",
            "source": "SENAT",
            "schema": {
                "uid": {"path": "id", "htmlEscape": False, "type": "VARCHAR ( 40 ) PRIMARY KEY", "search": True},
                "texteLegislatifRef": {"path": "txtid", "htmlEscape": True, "type": "VARCHAR ( 200 )", "search": True},
                "signataires": {"path": "", "htmlEscape": True, "type": "VARCHAR ( 20000 )", "search": True},
                "dispositif": {"path": "dis", "htmlEscape": True, "type": "VARCHAR ( 1000000 )", "search": True},
                "exposeSommaire": {"path": "obj", "htmlEscape": True, "type": "VARCHAR ( 50000 )", "search": True},
                "documentURI": {"path": "", "htmlEscape": True, "type": "VARCHAR ( 200 )", "search": True},
                "dateDepot": {"path": "datdep", "htmlEscape": False, "type": "DATE", "search": False},
                "etat": {"path": "etaid", "htmlEscape": True, "type": "VARCHAR ( 200 )", "search": True},
                "sousEtat": {"path": "", "htmlEscape": True, "type": "VARCHAR ( 201 )", "search": True},
                "dateSort": {"path": "datenvemairrasoc", "htmlEscape": False, "type": "TIMESTAMP WITH TIME ZONE", "search": False},
                "sort": {"path": "sorid", "htmlEscape": True, "type": "VARCHAR ( 202 )", "search": False},
                "article": {"path": "ord", "htmlEscape": True, "type": "VARCHAR ( 203 )", "search": False},
                "urlDivisionTexteVise": {"path": "", "htmlEscape": True, "type": "VARCHAR ( 600 )", "search": False},
                "alinea": {"path": "alinea", "htmlEscape": True, "type": "VARCHAR ( 404 )", "search": False},
            }
        }

        self.__statusOfTextTable = {
            1: "",
            2: "",
            3: "",
            4: "",
            5: "",
            6: "",
            7: "",
            8: "",
            9: "",
            10: "Le Sénat a adopté",
            11: "Le Sénat a adopté définitivement",
            12: "Le Sénat n'a pas adopté",
            0: "",
            20: "Le texte est adopté par la commission",
            25: "Le texte n'est pas adopté par la commission",
        }

        self.__sortOfTextTable = {
            "A": "Adopté",
            "R": "Retiré",
            "J": "Rejeté",
            "K": "Rejeté - vote unique",
            "N": "Non soutenu",
            "S": "Tombé",
            "B": "Adopté - vote unique",
            "1": "Adopté",
            "2": "Adopté avec modification",
            "3": "Rejeté",
            "4": "Retiré",
            "5": "Satisfait ou sans objet",
            "6": "NE",
        }

    """reloadDatabase
			Download and upload the database
			@params  :

	"""

    def reloadDatabase(self, dataDirectory, replace=False):

        sourceDirectory = dataDirectory + "Amendements/"
        path = sourceDirectory+"Amendements.zip"

        # Remove older extracted zip
        try:
            if replace:
                self.__debugPrint("Remove old directory: " +
                                  sourceDirectory+"...", end="", level=1)
                shutil.rmtree(sourceDirectory)
                self.__debugPrint("Finished", level=1)
        except:
            traceback.print_exc()
            pass

        # Create directory if not exists
        if not os.path.exists(sourceDirectory):
            os.makedirs(sourceDirectory)

        # Download
        if replace:
            self.__debugPrint("Download amendements database...", end="")
            sourceFile = requests.get(
                self.__amendementDbUrl, allow_redirects=True)
            f = open(path, 'wb')
            f.write(sourceFile.content)
            f.close()
            self.__debugPrint("Finished")

        # Extract zip
        if (not os.path.exists(sourceDirectory)) or replace:
            self.__debugPrint("Start unzipping "+path+"...", end="", level=1)
            with zipfile.ZipFile(path, 'r') as zipRef:
                zipRef.extractall(sourceDirectory)
                self.__debugPrint("Finished", level=1)
        else:
            print("not unzipping"+path)

        # Import to DB
        connection = psycopg2.connect(database=self.__database, user=self.__userDatabase,
                                      password=self.__passwordDatabase, host=self.__hostDatabase, port=self.__portDatabase)
        connection.autocommit = True
        cursor = connection.cursor()

        self.__debugPrint("Start importing db "+path+"...", end="", level=1)

        # Execute sql, with special handling for copy from stdin command
        with open(sourceDirectory+"var/opt/opendata/ameli.sql", "rb") as file:
            dbExport = file.read().decode('latin-1').split("\n")
            copyMode = False
            copyBuffer = ""
            commandBuffer = ""
            copyCommand = ""
            i = 0
            for line in dbExport:
                # Some column are too small. This piece of code update sizes.
                line = line.replace("\"int\" character varying(80)", "\"int\" character varying(150)")
                line = line.replace("inl character varying(720)", "inl character varying(1500)")
                

                i += 1
                if line[0:4] == "COPY":
                    copyMode = True
                    copyCommand = line
                elif copyMode and line[0:2] == "\.":
                    copyMode = False
                    # print(copyCommand)
                    try:
                        cursor.copy_expert(
                            copyCommand, io.StringIO(copyBuffer))
                    except:
                        traceback.print_exc()
                        pass  # traceback.print_exc()
                    copyBuffer = ""
                    copyCommand = ""
                elif copyMode:
                    copyBuffer += line+"\n"
                elif len(line) != 0 and line[0:2] != "--":
                    commandBuffer += line+"\n"
                    if line[-1] == ";":
                        # send command
                        try:
                            cursor.execute(commandBuffer)
                        except:
                            pass
                            #print(str(i)+" : "+line)
                            # traceback.print_exc()
                        commandBuffer = ""

        # Connect on the database and upload db
        """cursor.execute("SELECT * FROM txt_ameli")

        for element in cursor.fetchall():
            print(element)"""

        connection.close()

        self.__debugPrint("Finished", level=1)

    """getAmendementsByUid
				return a all amendements of a document by its uid
				@params uid : uid of dossier
				@return :

	"""

    def getAmendementsByUid(self, id, projectId,  maxNumberOfAmendement=10):
        connection = psycopg2.connect(database=self.__database, user=self.__userDatabase,
                                      password=self.__passwordDatabase, host=self.__hostDatabase, port=self.__portDatabase)
        connection.autocommit = True
        cursor = connection.cursor()

        # First find amendement ID... because it is not referenced in the assemble nationale JSON, we have to to magic...
        query = "SELECT id, num, doslegsignet FROM txt_ameli WHERE (num::INTEGER)=%s AND doslegsignet=%s "
        try:
            cursor.execute(query, (id, projectId, ))
            uid = cursor.fetchall()[0][0]

        except:
            traceback.print_exc()
            pass

        ret = {}
        tableDef = self.__amendementTableDefinition
        ret["amendements"] = []
        query = "SELECT "
        for key in tableDef["schema"].keys():
            if tableDef["schema"][key]["path"] != "":
                query += tableDef["schema"][key]["path"] + ","
        query = query[:-1]
        query += ", irrsaisiepar FROM " + \
            tableDef["tableName"] + " WHERE txtid=%s ORDER BY datdep DESC;"
        try:
            cursor.execute(query, (uid,))
            for entry in cursor.fetchall():
                entryData = {}
                i = 0
                for key in tableDef["schema"].keys():
                    if tableDef["schema"][key]["path"] != "":
                        if type(entry[i]) == datetime.datetime:
                            entryData[key] = str(entry[i])
                        else:
                            entryData[key] = entry[i]
                        i += 1
                    else:
                        entryData[key] = ""
                recevabilite = entry[i]
                ret["amendements"].append(entryData)
        except:
            traceback.print_exc()
            pass
        ret["numberOfAmendement"] = len(ret["amendements"])
        ret["amendements"] = ret["amendements"][:maxNumberOfAmendement]

        # post processing
        for amendement in ret["amendements"]:
            if amendement["etat"] is not None:
                amendement["etat"] = self.__statusOfTextTable[amendement["etat"]]
            else:
                amendement["etat"] = ""
            if amendement["sort"] is not None:
                amendement["sort"] = self.__sortOfTextTable[amendement["sort"]]
            else:
                amendement["sort"] = ""
            for senateur in self.getSenateursOfAmendement(amendement["uid"]):
                amendement["signataires"] += senateur["qua"] + " " + \
                    senateur["prenomuse"] + " " + senateur["nomuse"]

        connection.close()
        return ret

    """__debugPrint
			Private method that print debug informations only if verbose mode is activated
			@params string : string to be printed
			@params level (optionnal): level of verbose
	"""

    def __debugPrint(self, string, end="\n", level=1):
        if self.__verbose >= level:
            print(string, end=end, flush=True)

    """getSenateursOfAmendement(self, amendementUid):
			Private method that get the list of senateurs of an amendement
			@params amendementUid : id of the amendement
			@returns : list of dictionnary of senateurs
	"""

    def getSenateursOfAmendement(self, amendementUid):
        connection = psycopg2.connect(database=self.__database, user=self.__userDatabase,
                                      password=self.__passwordDatabase, host=self.__hostDatabase, port=self.__portDatabase)
        connection.autocommit = True
        cursor = connection.cursor()
        listOfColumns = ["amdid", "senid", "rng", "qua", "nomuse", "prenomuse"]
        query = "SELECT "
        for column in listOfColumns:
            query += column + ","
        query = query[:-1]
        query += "  FROM amdsen WHERE amdid=%s ORDER BY rng ASC;"

        listOfSenateurs = []
        try:
            cursor.execute(query, (amendementUid,))
            for entry in cursor.fetchall():
                entryData = {}
                i = 0
                for column in listOfColumns:
                    entryData[column] = entry[i]
                    i += 1
                listOfSenateurs.append(entryData)
        except:
            traceback.print_exc()
            pass
        return listOfSenateurs
