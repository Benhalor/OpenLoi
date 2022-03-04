import os
import sys
import time
import json
import shutil
import zipfile
import traceback
import datetime
import psycopg2
import requests
from psycopg2 import sql


class AssembleeNationale:

    """Constructor
                    Creation of the object with default values
                    @params verbose : integer specifying the amount of text written in the console by this lib.
                            0 : nothing
                            1 : important informations
                            2 : everything

    """

    def __init__(self, database='', userDatabase='', passwordDatabase='', hostDatabase='', portDatabase='', verbose=0, setup=False):

        self.__verbose = verbose
        self.__sourceList = {
            "DOSSIERS_LEGISLATIFS": {"link": "https://data.assemblee-nationale.fr/static/openData/repository/15/loi/dossiers_legislatifs/Dossiers_Legislatifs_XV.json.zip", "pollingFrequency": 6000},
            "AGENDA": {"link": "http://data.assemblee-nationale.fr/static/openData/repository/15/vp/seances/seances_publique_excel.csv", "pollingFrequency": 6000},
            "DEBATS_EN_SEANCE_PUBLIQUE": {"link": "https://data.assemblee-nationale.fr/static/openData/repository/15/vp/syceronbrut/syseron.xml.zip", "pollingFrequency": 6000},
            "VOTES": {"link": "https://data.assemblee-nationale.fr/static/openData/repository/15/loi/scrutins/Scrutins_XV.json.zip", "pollingFrequency": 6000},
            "QUESTIONS_AU_GOUVERNEMENT": {"link": "https://data.assemblee-nationale.fr/static/openData/repository/15/questions/questions_gouvernement/Questions_gouvernement_XV.json.zip", "pollingFrequency": 6000},
            "QUESTIONS_ORALES_SANS_DEBAT": {"link": "https://data.assemblee-nationale.fr/static/openData/repository/15/questions/questions_orales_sans_debat/Questions_orales_sans_debat_XV.json.zip", "pollingFrequency": 6000},
            "QUESTIONS_ECRITES": {"link": "https://data.assemblee-nationale.fr/static/openData/repository/15/questions/questions_ecrites/Questions_ecrites_XV.json.zip", "pollingFrequency": 6000},
            "REUNIONS": {"link": "https://data.assemblee-nationale.fr/static/openData/repository/15/vp/reunions/Agenda_XV.json.zip", "pollingFrequency": 6000},
            "AMENDEMENTS": {"link": "https://data.assemblee-nationale.fr/static/openData/repository/15/loi/amendements_legis/Amendements_XV.json.zip", "pollingFrequency": 6000},

        }

        self.__dossierLegislatifDocumentTableDefinition = {
            "tableName": "DOSSIERS_LEGISLATIFS_DOCUMENT",
            "source": "AN",
            "schema": {
                "uid": {"path": "document:uid", "htmlEscape": False, "type": "VARCHAR ( 40 ) PRIMARY KEY", "search": True},
                "dateCreation": {"path": "document:cycleDeVie:chrono:dateCreation", "htmlEscape": False, "type": "TIMESTAMP WITH TIME ZONE", "search": False},
                "dateDepot": {"path": "document:cycleDeVie:chrono:dateDepot", "htmlEscape": False, "type": "TIMESTAMP WITH TIME ZONE", "search": False},
                "datePublication": {"path": "document:cycleDeVie:chrono:datePublication", "htmlEscape": False, "type": "TIMESTAMP WITH TIME ZONE", "search": False},
                "datePublicationWeb": {"path": "document:cycleDeVie:chrono:datePublicationWeb", "htmlEscape": False, "type": "TIMESTAMP WITH TIME ZONE", "search": False},
                "denominationStructurelle": {"path": "document:denominationStructurelle", "htmlEscape": True, "type": "VARCHAR ( 200 )", "search": True},
                "titrePrincipal": {"path": "document:titres:titrePrincipal", "htmlEscape": True, "type": "VARCHAR ( 2000 )", "search": True},
                "titrePrincipalCourt": {"path": "document:titres:titrePrincipalCourt", "htmlEscape": True, "type": "VARCHAR ( 2000 )", "search": True},
                "dossierRef": {"path": "document:dossierRef", "htmlEscape": True, "type": "VARCHAR ( 200 )", "search": False},
                "notice": {"path": "document:notice:formule", "htmlEscape": True, "type": "VARCHAR ( 2000 )", "search": True}
            }
        }

        self.__dossierLegislatifDossierParlementaireTableDefinition = {
            "tableName": "DOSSIERS_LEGISLATIFS_DOSSIER_PARLEMENTAIRE",
            "source": "AN",
            "schema": {
                "uid": {"path": "dossierParlementaire:uid", "htmlEscape": False, "type": "VARCHAR ( 40 ) PRIMARY KEY", "search": True},
                "titre": {"path": "dossierParlementaire:titreDossier:titre", "htmlEscape": True, "type": "VARCHAR ( 2000 )", "search": True},
                "senatChemin": {"path": "dossierParlementaire:titreDossier:senatChemin", "htmlEscape": False, "type": "VARCHAR ( 2000 )", "search": False},
                "anChemin": {"path": "dossierParlementaire:titreDossier:titreChemin", "htmlEscape": False, "type": "VARCHAR ( 2000 )", "search": False},
                "actesLegislatifs": {"path": "dossierParlementaire:actesLegislatifs", "htmlEscape": True, "type": "VARCHAR ( 200000 )", "search": False},
                "lastUpdate": {"path": "specialHandling...", "htmlEscape": True, "type": "TIMESTAMP WITH TIME ZONE", "search": False},

            }
        }

        self.__amendementTableDefinition = {
            "tableName": "AMENDEMENT",
            "source": "AN",
            "schema": {
                "uid": {"path": "amendement:uid", "htmlEscape": False, "type": "VARCHAR ( 40 ) PRIMARY KEY", "search": True},
                "texteLegislatifRef": {"path": "amendement:texteLegislatifRef", "htmlEscape": True, "type": "VARCHAR ( 200 )", "search": True},
                "signataires": {"path": "amendement:signataires:libelle", "htmlEscape": True, "type": "VARCHAR ( 20000 )", "search": True},
                "dispositif": {"path": "amendement:corps:contenuAuteur:dispositif", "htmlEscape": True, "type": "VARCHAR ( 1000000 )", "search": True},
                "exposeSommaire": {"path": "amendement:corps:contenuAuteur:exposeSommaire", "htmlEscape": True, "type": "VARCHAR ( 50000 )", "search": True},
                "documentURI": {"path": "amendement:representations:representation:contenu:documentURI", "htmlEscape": True, "type": "VARCHAR ( 200 )", "search": True},
                "dateDepot": {"path": "amendement:cycleDeVie:dateDepot", "htmlEscape": False, "type": "DATE", "search": False},
                "etat": {"path": "amendement:cycleDeVie:etatDesTraitements:etat:libelle", "htmlEscape": True, "type": "VARCHAR ( 200 )", "search": True},
                "sousEtat": {"path": "amendement:cycleDeVie:etatDesTraitements:sousEtat:libelle", "htmlEscape": True, "type": "VARCHAR ( 201 )", "search": True},
                "dateSort": {"path": "amendement:cycleDeVie:dateSort", "htmlEscape": False, "type": "TIMESTAMP WITH TIME ZONE", "search": False},
                "sort": {"path": "amendement:cycleDeVie:sort", "htmlEscape": True, "type": "VARCHAR ( 202 )", "search": False},
                "article": {"path": "amendement:pointeurFragmentTexte:division:articleDesignationCourte", "htmlEscape": True, "type": "VARCHAR ( 203 )", "search": False},
                "urlDivisionTexteVise": {"path": "amendement:pointeurFragmentTexte:division:urlDivisionTexteVise", "htmlEscape": True, "type": "VARCHAR ( 600 )", "search": False},
                "alinea": {"path": "amendement:pointeurFragmentTexte:amendementStandard:alinea:alineaDesignation", "htmlEscape": True, "type": "VARCHAR ( 404 )", "search": False},
            }
        }

        self.__questionEcriteTableDefinition = {
            "tableName": "QUESTIONS_ECRITES",
            "source": "AN",
            "schema": {
                "uid": {"path": "question:uid", "htmlEscape": False, "type": "VARCHAR ( 40 ) PRIMARY KEY", "search": True},
                "rubrique": {"path": "question:indexationAN:rubrique", "htmlEscape": True, "type": "VARCHAR ( 500 )", "search": True},
                "resume": {"path": "question:indexationAN:ANALYSE:ANA", "htmlEscape": True, "type": "VARCHAR ( 2000 )", "search": True},
                "auteur": {"path": "question:auteur:identite:acteurRef", "htmlEscape": True, "type": "VARCHAR ( 200 )", "search": False},
                "auteurGroupe": {"path": "question:auteur:groupe:developpe", "htmlEscape": True, "type": "VARCHAR ( 200 )", "search": False},
                "ministere": {"path": "question:minInt:developpe", "htmlEscape": True, "type": "VARCHAR ( 1000 )", "search": True},
                "question": {"path": "question:textesQuestion", "htmlEscape": True, "type": "VARCHAR ( 200000 )", "search": True},
                "reponse": {"path": "question:textesReponse", "htmlEscape": True, "type": "VARCHAR ( 200000 )", "search": True},
                "dateQuestion": {"path": "specialHandling...", "htmlEscape": False, "type": "DATE", "search": False},
                "dateReponse": {"path": "specialHandling...", "htmlEscape": False, "type": "DATE", "search": False}
            }
        }

        self.__questionOraleSansDebatTableDefinition = {
            "tableName": "QUESTIONS_ORALES_SANS_DEBAT",
            "source": "AN",
            "schema": {
                "uid": {"path": "question:uid", "htmlEscape": False, "type": "VARCHAR ( 40 ) PRIMARY KEY", "search": True},
                "rubrique": {"path": "question:indexationAN:rubrique", "htmlEscape": True, "type": "VARCHAR ( 500 )", "search": True},
                "resume": {"path": "question:indexationAN:ANALYSE:ANA", "htmlEscape": True, "type": "VARCHAR ( 2000 )", "search": True},
                "auteur": {"path": "question:auteur:identite:acteurRef", "htmlEscape": True, "type": "VARCHAR ( 200 )", "search": False},
                "auteurGroupe": {"path": "question:auteur:groupe:developpe", "htmlEscape": True, "type": "VARCHAR ( 200 )", "search": False},
                "ministere": {"path": "question:minInt:developpe", "htmlEscape": True, "type": "VARCHAR ( 1000 )", "search": True},
                "question": {"path": "question:textesQuestion", "htmlEscape": True, "type": "VARCHAR ( 200000 )", "search": True},
                "reponse": {"path": "question:textesReponse", "htmlEscape": True, "type": "VARCHAR ( 200000 )", "search": True},
                "dateQuestion": {"path": "specialHandling...", "htmlEscape": False, "type": "DATE", "search": False},
                "dateReponse": {"path": "specialHandling...", "htmlEscape": False, "type": "DATE", "search": False}
            }
        }

        self.__questionAuGouvernementTableDefinition = {
            "tableName": "QUESTIONS_AU_GOUVERNEMENT",
            "source": "AN",
            "schema": {
                "uid": {"path": "question:uid", "htmlEscape": False, "type": "VARCHAR ( 40 ) PRIMARY KEY", "search": True},
                "rubrique": {"path": "question:indexationAN:rubrique", "htmlEscape": True, "type": "VARCHAR ( 500 )", "search": True},
                "resume": {"path": "question:indexationAN:ANALYSE:ANA", "htmlEscape": True, "type": "VARCHAR ( 2000 )", "search": True},
                "auteur": {"path": "question:auteur:identite:acteurRef", "htmlEscape": True, "type": "VARCHAR ( 200 )", "search": False},
                "auteurGroupe": {"path": "question:auteur:groupe:developpe", "htmlEscape": True, "type": "VARCHAR ( 200 )", "search": False},
                "ministere": {"path": "question:minInt:developpe", "htmlEscape": True, "type": "VARCHAR ( 1000 )", "search": True},
                "question": {"path": "question:textesQuestion", "htmlEscape": True, "type": "VARCHAR ( 200000 )", "search": True},
                "reponse": {"path": "question:textesReponse", "htmlEscape": True, "type": "VARCHAR ( 200000 )", "search": True},
                "dateQuestion": {"path": "specialHandling...", "htmlEscape": False, "type": "DATE", "search": False},
                "dateReponse": {"path": "specialHandling...", "htmlEscape": False, "type": "DATE", "search": False}
            }
        }

        self.__tableList = {
            "QUESTIONS_AU_GOUVERNEMENT": self.__questionAuGouvernementTableDefinition,
            "QUESTIONS_ORALES_SANS_DEBAT": self.__questionOraleSansDebatTableDefinition,
            "DOSSIERS_LEGISLATIFS_DOCUMENT": self.__dossierLegislatifDocumentTableDefinition,
            "DOSSIERS_LEGISLATIFS_DOSSIER_PARLEMENTAIRE": self.__dossierLegislatifDossierParlementaireTableDefinition,
            "AMENDEMENT": self.__amendementTableDefinition,
            "QUESTIONS_ECRITES": self.__questionEcriteTableDefinition,
        }

        self.__database = database
        self.__userDatabase = userDatabase
        self.__passwordDatabase = passwordDatabase
        self.__hostDatabase = hostDatabase
        self.__portDatabase = portDatabase

        if setup:
            # Setup database for the first time if requiered by user
            self.setupDatabase()

        self.__jsonReadOK = 0
        self.__jsonReadNOK = 0
        self.__count = 0

    """setupDatabase
			Setup the postgredatabase with the schema
			@params  :

	"""

    def setupDatabase(self):
        # Connect on the new database
        connection = psycopg2.connect(database=self.__database, user=self.__userDatabase,
                                      password=self.__passwordDatabase, host=self.__hostDatabase, port=self.__portDatabase)
        connection.autocommit = True
        cursor = connection.cursor()

        for key, tableDef in self.__tableList.items():
            # Drop existing tables todo remove
            try:
                query = "DROP TABLE "+tableDef["tableName"]
                cursor.execute(query)
                print("Table "+tableDef["tableName"]+" drop successfully...")
            except:
                traceback.print_exc()
                pass

            # Create table
            try:
                query = "CREATE TABLE "+tableDef["tableName"]+"("
                columnString = ""
                for columnName, columnDef in tableDef["schema"].items():
                    columnString += columnName + " "+columnDef["type"]+","
                query += columnString[:-1]+");"
                print(query)
                cursor.execute(query)
                print("Table "+tableDef["tableName"] +
                      " created successfully...")
            except psycopg2.errors.DuplicateTable:
                print("Table "+tableDef["tableName"]+" already exists")
            except:
                traceback.print_exc()

            # Create searching index
            try:
                query = "ALTER TABLE " + \
                    tableDef["tableName"] + \
                        " ADD COLUMN ts tsvector GENERATED ALWAYS AS (to_tsvector('french',"
                columnString = ""
                for columnName, columnDef in tableDef["schema"].items():
                    if (columnDef["search"]):
                        columnString += "coalesce("+columnName+",'') ||"
                columnString = columnString[:-2]
                query += columnString
                query += ")) STORED;"
                cursor.execute(query)
            except:
                traceback.print_exc()

            # For performance only
            """try:
                query = "CREATE INDEX ts_idx ON " + \
                    tableDef["tableName"] + " USING GIN (ts);"
                cursor.execute(query)
            except:
                traceback.print_exc()"""

        connection.close()

    """downloadSources
			Download files from a source list and store them in a specified directory
			@params sourceList : a dict with all source lists. sourceList = {"name1": {"link":"link1", "pollingFrequency1":pollingFrequency1},...}
			@params dataDirectory : directory to store datas
			@params pollingFrequency : Download only if last version of the local file is older than pollingFrequency. In s
			@return : a dict {"duration":downloadDuration, "updatedSources":updatedSources}

	"""

    def downloadSources(self, dataDirectory, sourceList=None):

        if sourceList is None:
            sourceList = self.__sourceList

        startDownloadTime = time.time()

        # Updated sources : list of sources that have been updated this time
        updatedSources = []

        for sourceName, source in sourceList.items():
            sourceLink = source["link"]
            pollingFrequency = source["pollingFrequency"]

            sourceDirectory = dataDirectory+sourceName
            dataName = sourceDirectory+"/"+sourceLink.split("/")[-1]

            # Create directory if not exists
            if not os.path.exists(sourceDirectory):
                os.makedirs(sourceDirectory)

            # Download file only if it is older than POLLING_FREQUENCY_S, (or not exists).
            if not(os.path.exists(dataName)) or time.time() - os.path.getmtime(dataName) > pollingFrequency:
                self.__debugPrint("Start downloading " +
                                  dataName+"...", end="", level=1)
                sourceFile = requests.get(sourceLink, allow_redirects=True)
                f = open(dataName, 'wb')
                f.write(sourceFile.content)
                f.close()
                updatedSources.append(dataName)
                self.__debugPrint("Finished")
            else:
                updatedSources.append(dataName)
                self.__debugPrint(
                    "Download of "+dataName+" is skipped, because file is not older than "+str(pollingFrequency)+"s.")

        downloadDuration = time.time()-startDownloadTime
        self.__debugPrint("Download was made in "+str(downloadDuration)+"s")

        return {"duration": downloadDuration, "updatedSources": updatedSources}

    """__debugPrint
			Private method that print debug informations only if verbose mode is activated
			@params string : string to be printed
			@params level (optionnal): level of verbose
	"""

    def __debugPrint(self, string, end="\n", level=1):
        if self.__verbose >= level:
            print(string, end=end, flush=True)

    """processSources
			Download files from a source list and store them in a specified directory
			@params dataDirectory : directory to store datas
			@params sourceList : a list of path of file to process
			@return :

	"""

    def processSources(self, dataDirectory, sourceList, replace=False):

        for path in sourceList:
            if path[-9:] == "excel.csv":
                pass  # self.__processExcelCsv(path)
            if path[-3:] == "zip":
                self.__processZip(path, replace=replace)

    """__processExcelCsv
			Process files that have a csv format
			@params path : path of the excel csv file to process
			@return :

	"""

    def __processExcelCsv(self, path):
        file = open(path)
        for line in file:
            print(line)
        file.close()

    """__processZip
			Process files that are json compressed in zip
			@params path : path of the json zip file to process
			@params replace : wether to replace if an existing unzipped directory is there.
			@return :

	"""

    def __processZip(self, path, replace=False):
        directoryToExtract = path.split(".")[0]

        # Remove older extracted zip
        try:
            if replace:
                self.__debugPrint("Remove old directory: " +
                                  directoryToExtract+"...", end="", level=1)
                shutil.rmtree(directoryToExtract)
                self.__debugPrint("Finished", level=1)
        except:
            traceback.print_exc()
            pass

        # Extract zip
        if (not os.path.exists(directoryToExtract)) or replace:
            self.__debugPrint("Start unzipping "+path+"...", end="", level=1)
            with zipfile.ZipFile(path, 'r') as zipRef:
                zipRef.extractall(directoryToExtract)
                self.__debugPrint("Finished", level=1)
        else:
            print("not unzipping"+path)

        sourceName = directoryToExtract.split("/")[-2]
        if sourceName == "DOSSIERS_LEGISLATIFS":
            self.__uploadToDb(
                directoryToExtract+"/json/document", table="DOSSIERS_LEGISLATIFS_DOCUMENT")
            self.__uploadToDb(
                directoryToExtract+"/json/dossierParlementaire", table="DOSSIERS_LEGISLATIFS_DOSSIER_PARLEMENTAIRE")
            print("json DOSSIERS_LEGISLATIFS OK:"+str(self.__jsonReadOK))
            print("json DOSSIERS_LEGISLATIFS NOK:"+str(self.__jsonReadNOK))
        elif sourceName == "AGENDA":
            pass
        elif sourceName == "AMENDEMENTS":
            lastTime = time.time()
            self.__jsonReadOK = 0
            self.__jsonReadNOK = 0
            self.__uploadToDb(
                directoryToExtract+"/json", table="AMENDEMENT")
            print("json AMENDEMENTS OK:"+str(self.__jsonReadOK))
            print("json AMENDEMENTS NOK:"+str(self.__jsonReadNOK))
            print("Upload amendements in "+str(time.time()-lastTime))
        elif sourceName == "DEBATS_EN_SEANCE_PUBLIQUE":
            pass
        elif sourceName == "VOTES":
            pass
        elif sourceName == "QUESTIONS_AU_GOUVERNEMENT":
            lastTime = time.time()
            self.__jsonReadOK = 0
            self.__jsonReadNOK = 0
            self.__uploadToDb(
                directoryToExtract+"/json", table="QUESTIONS_AU_GOUVERNEMENT")
            print("json QUESTIONS_AU_GOUVERNEMENT OK:"+str(self.__jsonReadOK))
            print("json QUESTIONS_AU_GOUVERNEMENT NOK:"+str(self.__jsonReadNOK))
            print("Upload QUESTIONS_AU_GOUVERNEMENT in " +
                  str(time.time()-lastTime))
        elif sourceName == "QUESTIONS_ORALES_SANS_DEBAT":
            lastTime = time.time()
            self.__jsonReadOK = 0
            self.__jsonReadNOK = 0
            self.__uploadToDb(
                directoryToExtract+"/json", table="QUESTIONS_ORALES_SANS_DEBAT")
            print("json QUESTIONS_ORALES_SANS_DEBAT OK:"+str(self.__jsonReadOK))
            print("json QUESTIONS_ORALES_SANS_DEBAT NOK:"+str(self.__jsonReadNOK))
            print("Upload QUESTIONS_ORALES_SANS_DEBAT in " +
                  str(time.time()-lastTime))
        elif sourceName == "QUESTIONS_ECRITES":
            lastTime = time.time()
            self.__jsonReadOK = 0
            self.__jsonReadNOK = 0
            self.__uploadToDb(
                directoryToExtract+"/json", table="QUESTIONS_ECRITES")
            print("json QUESTIONS_ECRITES OK:"+str(self.__jsonReadOK))
            print("json QUESTIONS_ECRITES NOK:"+str(self.__jsonReadNOK))
            print("Upload QUESTIONS_ECRITES in "+str(time.time()-lastTime))
        elif sourceName == "REUNIONS":
            pass

    """__getUidList
				Get list of uid of a table.
                @params table : table name
				@return : list of uid on the table

	"""

    def __getUidList(self, table):
        connection = psycopg2.connect(database=self.__database, user=self.__userDatabase,
                                      password=self.__passwordDatabase, host=self.__hostDatabase, port=self.__portDatabase)
        connection.autocommit = True
        cursor = connection.cursor()
        uidList = []
        query = "SELECT uid FROM "+table + ";"
        cursor.execute(query)
        for entry in cursor.fetchall():
            uidList.append(entry[0])
        return uidList

    """__uploadToDb
				Recursively explore the foler dossierLegislatif and upload to db
				@params directory : path of the directory
                @params table : table name
				@return :

	"""

    def __uploadToDb(self, directory, table="DOSSIERS_LEGISLATIFS_DOCUMENT"):
        connection = psycopg2.connect(database=self.__database, user=self.__userDatabase,
                                      password=self.__passwordDatabase, host=self.__hostDatabase, port=self.__portDatabase)
        connection.autocommit = False
        cursor = connection.cursor()

        uidList = self.__getUidList(table)

        if table in self.__tableList:
            tableDefinition = self.__tableList[table]
            count = 0
            lastTime = time.time()
            for root, subdirs, files in os.walk(directory):
                for fileName in files:
                    count += 1
                    if count % 10000 == 0:
                        print(str(count) + ":  "+str(time.time()-lastTime))
                        lastTime = time.time()
                        print(fileName)
                        connection.commit()
                    path = os.path.join(root, fileName)
                    with open(path, 'r') as sourceFile:
                        text = sourceFile.read()
                        try:
                            doc = json.loads(text)
                            try:
                                query, uid = self.__buildQueryFromDef(
                                    doc, tableDefinition)
                                if uid not in uidList:
                                    cursor.execute(query)
                                    self.__jsonReadOK += 1
                            except psycopg2.errors.UniqueViolation:
                                pass
                            except KeyboardInterrupt:
                                sys.exit(0)
                            except:
                                pass
                                # traceback.print_exc()
                        except KeyboardInterrupt:
                            sys.exit(0)
                        except:
                            traceback.print_exc()
                            self.__jsonReadNOK += 1
            print(count)
        connection.commit()
        connection.close()

    """__buildQueryFromDef
				Build a query to insert an element from a dict defining the table
				@params doc : json doc (data)
				@params tableDef : dict defining the table
				@return :

	"""

    def __buildQueryFromDef(self, doc, tableDef):
        uid = None
        query = ""
        query += "INSERT INTO "+tableDef["tableName"]+"("
        columnString = ""
        valuesString = ""
        for columnName, columnDef in tableDef["schema"].items():
            if tableDef["tableName"] == "DOSSIERS_LEGISLATIFS_DOSSIER_PARLEMENTAIRE" and columnName == "lastUpdate":
                lastUpdate = self.__extractLastDateDossierParlementaire(doc)[
                    "value"]
                columnString += columnName+","
                valuesString += "\'"+lastUpdate+"\',"
            elif "QUESTION" in tableDef["tableName"] and columnName == "dateReponse":
                # Sometimes there is not yet a response. Sometimes there are multiple response in a list. In this case, take the last date. Moreover, date format is not standard
                if doc["question"]["textesReponse"] is not None:
                    if type(doc["question"]["textesReponse"]["texteReponse"]) is list:
                        date = doc["question"]["textesReponse"]["texteReponse"][-1]["infoJO"]["dateJO"]
                    else:
                        date = doc["question"]["textesReponse"]["texteReponse"]["infoJO"]["dateJO"]
                    columnString += columnName+","
                    valuesString += "TO_DATE(\'"+date+"\' , \'DD/MM/YYYY\'),"
            elif "QUESTION" in tableDef["tableName"] and columnName == "dateQuestion":
                # Sometimes, there is no question. Sometimes there are multiple question in a list. In this case, take the last date. Moreover, date format is not standard
                if "textesQuestion" in doc["question"].keys():
                    if type(doc["question"]["textesQuestion"]["texteQuestion"]) is list:
                        date = doc["question"]["textesQuestion"]["texteQuestion"][-1]["infoJO"]["dateJO"]
                    else:
                        date = doc["question"]["textesQuestion"]["texteQuestion"]["infoJO"]["dateJO"]
                    columnString += columnName+","
                    valuesString += "TO_DATE(\'"+date+"\' , \'DD/MM/YYYY\'),"
            else:
                try:
                    docPath = doc
                    for pathIter in columnDef["path"].split(":"):
                        try:
                            docPath = docPath[pathIter]
                        except TypeError:
                            docPath = None
                        except KeyboardInterrupt:
                            sys.exit(0)
                        except:
                            docPath = None
                            # case value is null in json

                    if docPath is not None:
                        if type(docPath) == dict:
                            docPath = json.dumps(docPath)

                        if columnDef["type"] == "DATE":
                            try:
                                datetime.datetime.strptime(docPath, "%Y-%m-%d")
                                valuesString += "\'"+docPath+"\',"
                                columnString += columnName+","
                            except ValueError:
                                #traceback.print_exc()
                                pass
                            except KeyboardInterrupt:
                                sys.exit(0)
                        elif columnDef["type"] == "TIMESTAMP WITH TIME ZONE":
                            timestampOK = False
                            # Check that format of timestamp is OL
                            try:
                                datetime.datetime.strptime(
                                    docPath, "%Y-%m-%dT%H:%M:%S%z")
                                timestampOK = True
                            except ValueError:
                                pass
                            except KeyboardInterrupt:
                                sys.exit(0)
                            try:
                                datetime.datetime.strptime(
                                    docPath, "%Y-%m-%dT%H:%M:%S.%f%z")
                                timestampOK = True
                            except ValueError:
                                pass
                            except KeyboardInterrupt:
                                sys.exit(0)

                            # If OK, add to fields.
                            if timestampOK:
                                valuesString += "\'"+docPath+"\',"
                                columnString += columnName+","

                        elif columnDef["htmlEscape"]:
                            valuesString += "\'" + \
                                self.__htmlEscape(docPath)+"\',"
                            columnString += columnName+","
                        else:
                            if columnName == "uid":
                                uid = docPath
                            valuesString += "\'"+docPath+"\',"
                            columnString += columnName+","
                except KeyboardInterrupt:
                    sys.exit(0)
                except:
                    print(doc)
                    traceback.print_exc()
        query += columnString[:-1] + ") VALUES (" + valuesString[:-1]+");"
        if uid is None:
            print("PROBLEM WITH UID")
        return query, uid

    """search
				search a term in tables
				@params term : term to search
                @params maxNumberOfResults : max number of results to return
				@return :

	"""

    def search(self, term, maxNumberOfResults=10, numberOfMonthsOld=6):
        connection = psycopg2.connect(database=self.__database, user=self.__userDatabase,
                                      password=self.__passwordDatabase, host=self.__hostDatabase, port=self.__portDatabase)
        connection.autocommit = True
        cursor = connection.cursor()

        print("Search "+term)
        processedQuery = term.replace("'", "\\'").replace("--", "")

        ret = {}
        ret["listOfDossiersLegislatifs"] = []
        ret["listOfQuestionsEcrites"] = []
        ret["listOfQuestionsOralesSansDebat"] = []
        ret["listOfQuestionsAuGouvernement"] = []
        ret["listOfResults"] = []
        ret["count"] = 0

        # First get the radicals (use for highlight in react)
        try:
            cursor.execute("SELECT to_tsvector('french', %s);",
                           (processedQuery,))
            ret["query"] = " ".join(cursor.fetchone()[0].split("'")[1::2])
        except:
            traceback.print_exc()

        processedQueryLogic = processedQuery.replace(" ", "<1>")

        # ------------------------------------------------------
        # Then get the results for document legislatifs
        count, listOfdossierLegislatif = self.__documentLegislatifSearch(
            cursor, processedQueryLogic, numberOfMonthsOld, maxNumberOfResults, "DOSSIERS_LEGISLATIFS_DOCUMENT")

        ret["count"] += count
        ret["listOfDossiersLegislatifs"].extend(listOfdossierLegislatif)

        # ------------------------------------------------------
        # Then get the results for questions écrites
        count, listOfQuestionsEcrites = self.__listOfQuestionsSearch(
            cursor, processedQueryLogic, numberOfMonthsOld, maxNumberOfResults, "QUESTIONS_ECRITES")
        ret["count"] += count
        ret["listOfQuestionsEcrites"].extend(listOfQuestionsEcrites)

        # ------------------------------------------------------
        # Then get the results for questions orales sans debat
        count, listOfQuestionsOralesSansDebat = self.__listOfQuestionsSearch(
            cursor, processedQueryLogic, numberOfMonthsOld, maxNumberOfResults, "QUESTIONS_ORALES_SANS_DEBAT")
        ret["count"] += count
        ret["listOfQuestionsOralesSansDebat"].extend(
            listOfQuestionsOralesSansDebat)

        # ------------------------------------------------------
        # Then get the results for questions au gouvernement (avec debat)
        count, listOfQuestionsAuGouvernement = self.__listOfQuestionsSearch(
            cursor, processedQueryLogic, numberOfMonthsOld, maxNumberOfResults, "QUESTIONS_AU_GOUVERNEMENT")
        ret["count"] += count
        ret["listOfQuestionsAuGouvernement"].extend(
            listOfQuestionsAuGouvernement)

        tempResult = []
        # Gather all results and give them a type key.
        for questionEcrite in listOfQuestionsEcrites:
            tempResult.append(
                {"type": "questionEcrite", "uid": questionEcrite["uid"], "score": questionEcrite["score"]})
        for questionOraleSansDebat in listOfQuestionsOralesSansDebat:
            tempResult.append(
                {"type": "questionOraleSansDebat", "uid": questionOraleSansDebat["uid"], "score": questionOraleSansDebat["score"]})
        for dossierLegislatif in listOfdossierLegislatif:
            tempResult.append(
                {"type": "dossierLegislatif", "uid": dossierLegislatif["uid"], "score": dossierLegislatif["score"]})
        for questionAuGouvernement in listOfQuestionsAuGouvernement:
            tempResult.append(
                {"type": "questionAuGouvernement", "uid": questionAuGouvernement["uid"], "score": questionAuGouvernement["score"]})

        # Sort by score and extend list of results
        tempResult = sorted(
            tempResult, key=lambda d: d['score'], reverse=True)
        ret["listOfResults"].extend(tempResult)

        if ret["count"] < maxNumberOfResults:
            processedQueryLogic = processedQuery.replace(" ", "|")

            # ------------------------------------------------------
            # Then get the results for document legislatifs
            count, listOfdossierLegislatif = self.__documentLegislatifSearch(
                cursor, processedQueryLogic, numberOfMonthsOld, maxNumberOfResults, "DOSSIERS_LEGISLATIFS_DOCUMENT", initialList=ret["listOfResults"])

            ret["count"] += count
            ret["listOfDossiersLegislatifs"].extend(listOfdossierLegislatif)

            # ------------------------------------------------------
            # Then get the results for questions écrites
            count, listOfQuestionsEcrites = self.__listOfQuestionsSearch(
                cursor, processedQueryLogic, numberOfMonthsOld, maxNumberOfResults, "QUESTIONS_ECRITES", initialList=ret["listOfResults"])
            ret["count"] += count
            ret["listOfQuestionsEcrites"].extend(listOfQuestionsEcrites)

            # ------------------------------------------------------
            # Then get the results for questions orales sans debat
            count, listOfQuestionsOralesSansDebat = self.__listOfQuestionsSearch(
                cursor, processedQueryLogic, numberOfMonthsOld, maxNumberOfResults, "QUESTIONS_ORALES_SANS_DEBAT", initialList=ret["listOfResults"])
            ret["count"] += count
            ret["listOfQuestionsOralesSansDebat"].extend(
                listOfQuestionsOralesSansDebat)

            # ------------------------------------------------------
            # Then get the results for questions au gouvernement (avec debat)
            count, listOfQuestionsAuGouvernement = self.__listOfQuestionsSearch(
                cursor, processedQueryLogic, numberOfMonthsOld, maxNumberOfResults, "QUESTIONS_AU_GOUVERNEMENT", initialList=ret["listOfResults"])
            ret["count"] += count
            ret["listOfQuestionsAuGouvernement"].extend(
                listOfQuestionsAuGouvernement)

            tempResult = []
            # Gather all results and give them a type key.
            for questionEcrite in listOfQuestionsEcrites:
                tempResult.append(
                    {"type": "questionEcrite", "uid": questionEcrite["uid"], "score": questionEcrite["score"]})
            for questionOraleSansDebat in listOfQuestionsOralesSansDebat:
                tempResult.append(
                    {"type": "questionOraleSansDebat", "uid": questionOraleSansDebat["uid"], "score": questionOraleSansDebat["score"]})
            for dossierLegislatif in listOfdossierLegislatif:
                tempResult.append(
                    {"type": "dossierLegislatif", "uid": dossierLegislatif["uid"], "score": dossierLegislatif["score"]})
            for questionAuGouvernement in listOfQuestionsAuGouvernement:
                tempResult.append(
                    {"type": "questionAuGouvernement", "uid": questionAuGouvernement["uid"], "score": questionAuGouvernement["score"]})

            # Sort by score and extend list of results
            tempResult = sorted(
                tempResult, key=lambda d: d['score'], reverse=True)
            ret["listOfResults"].extend(tempResult)

        connection.close()
        return json.dumps(ret)

    """__documentLegislatifSearch
				Generate a list of question containing a given query

	"""

    def __documentLegislatifSearch(self, cursor, processedQueryLogic, numberOfMonthsOld, maxNumberOfResults, tableName, initialList=[]):

        query = "SELECT dossierRef,ts_rank_cd(ts, to_tsquery('french',%s),2) AS score,dateCreation " \
            "FROM " + tableName + " "\
            "WHERE ( ts @@ to_tsquery('french',%s))" \
            "ORDER by score  DESC LIMIT %s;"

        count = 0

        listOfdossierLegislatif = []
        try:
            cursor.execute(query, (processedQueryLogic,
                           processedQueryLogic,  maxNumberOfResults,))
            for entry in cursor.fetchall():
                entryData = {}
                entryData["dossierRef"] = entry[0]
                entryData["score"] = entry[1]
                d = {"uid": entryData["dossierRef"],
                     "score": entryData["score"]}
                if not any(di['uid'] == entryData["dossierRef"] for di in listOfdossierLegislatif+initialList):
                    listOfdossierLegislatif.append(d)
                    count += 1

        except:
            traceback.print_exc()
        return count, listOfdossierLegislatif

    """__listOfQuestionsSearch
				Generate a list of question containing a given query

	"""

    def __listOfQuestionsSearch(self, cursor, processedQueryLogic, numberOfMonthsOld, maxNumberOfResults, tableName, initialList=[]):

        listOfQuestions = []
        count = 0

        query = "SELECT uid ,ts_rank_cd(ts, to_tsquery('french',%s),2) AS score, dateQuestion, dateReponse " \
            "FROM " + tableName + " "\
            "WHERE ( ts @@ to_tsquery('french',%s)" \
            "AND ( (dateQuestion >  CURRENT_DATE - INTERVAL '%s months') OR (dateReponse >  CURRENT_DATE - INTERVAL '%s months') ))" \
            "ORDER by score DESC LIMIT %s;"

        try:
            cursor.execute(query, (processedQueryLogic,
                                   processedQueryLogic, numberOfMonthsOld, numberOfMonthsOld,  maxNumberOfResults,))
            for entry in cursor.fetchall():
                entryData = {}
                entryData["uid"] = entry[0]
                entryData["score"] = entry[1]
                if not any(di['uid'] == entryData["uid"] for di in listOfQuestions+initialList):
                    listOfQuestions.append(
                        {"uid": entryData["uid"], "score": entryData["score"]}
                    )
                    count += 1
        except:
            traceback.print_exc()
        return count, listOfQuestions

    """__listOfMostRecentQuestions
				Generate a list of most recetn questions

	"""

    def __listOfMostRecentQuestions(self, cursor, maxNumberOfResults, tableName, initialList=[]):

        listOfQuestions = []
        count = 0

        query = "SELECT uid, dateQuestion, dateReponse " \
            "FROM " + tableName + " "\
            "ORDER BY GREATEST (COALESCE(dateReponse,'(1970/01/01)'), COALESCE(dateQuestion,'(1970/01/01)')) DESC  LIMIT %s;"

        try:
            cursor.execute(query, (maxNumberOfResults,))
            for entry in cursor.fetchall():
                entryData = {}
                entryData["uid"] = entry[0]
                entryData["score"] = 0
                if not any(di['uid'] == entryData["uid"] for di in listOfQuestions+initialList):
                    listOfQuestions.append(
                        {"uid": entryData["uid"], "score": entryData["score"]}
                    )
                    count += 1
        except:
            traceback.print_exc()
        return count, listOfQuestions

    """getLastNews
				returns last news
                @params maxNumberOfResults : max number of results to return
				@return :

	"""

    def getLastNews(self, maxNumberOfResults=5):
        connection = psycopg2.connect(database=self.__database, user=self.__userDatabase,
                                      password=self.__passwordDatabase, host=self.__hostDatabase, port=self.__portDatabase)
        connection.autocommit = True
        cursor = connection.cursor()

        ret = {}
        ret["listOfDossiersLegislatifs"] = []
        ret["listOfQuestionsEcrites"] = []
        ret["listOfQuestionsOralesSansDebat"] = []
        ret["listOfQuestionsAuGouvernement"] = []
        ret["listOfResults"] = []
        ret["count"] = 0
        ret["query"] = ""

        # Get the results
        tableDef = self.__dossierLegislatifDossierParlementaireTableDefinition

        count = 0
        # Get the list of documents legislatifs refs
        ret["listOfDossiersLegislatifs"] = []
        query = "SELECT DISTINCT(DOSSIERS_LEGISLATIFS_DOCUMENT.dossierRef) dateDepot FROM AMENDEMENT \
            JOIN DOSSIERS_LEGISLATIFS_DOCUMENT ON AMENDEMENT.texteLegislatifRef=DOSSIERS_LEGISLATIFS_DOCUMENT.uid\
            ORDER BY dateDepot DESC LIMIT %s;"
        ret["listOfDossiersLegislatifs"] = []
        try:
            cursor.execute(query, (maxNumberOfResults,))
            for entry in cursor.fetchall():
                count += 1
                ret["listOfDossiersLegislatifs"].append(entry[0])
        except:
            traceback.print_exc()

        ret["count"] += count
        listOfdossierLegislatif = ret["listOfDossiersLegislatifs"]

        # ------------------------------------------------------
        # Then get the results for questions écrites
        count, listOfQuestionsEcrites = self.__listOfMostRecentQuestions(
            cursor, maxNumberOfResults, "QUESTIONS_ECRITES")
        ret["count"] += count
        ret["listOfQuestionsEcrites"].extend(listOfQuestionsEcrites)

        # ------------------------------------------------------
        # Then get the results for questions orales sans debat
        count, listOfQuestionsOralesSansDebat = self.__listOfMostRecentQuestions(
            cursor, maxNumberOfResults, "QUESTIONS_ORALES_SANS_DEBAT")
        ret["count"] += count
        ret["listOfQuestionsOralesSansDebat"].extend(
            listOfQuestionsOralesSansDebat)

        # ------------------------------------------------------
        # Then get the results for questions au gouvernement (avec debat)
        count, listOfQuestionsAuGouvernement = self.__listOfMostRecentQuestions(
            cursor, maxNumberOfResults, "QUESTIONS_AU_GOUVERNEMENT")
        ret["count"] += count
        ret["listOfQuestionsAuGouvernement"].extend(
            listOfQuestionsAuGouvernement)

        tempResult = []
        # Gather all results and give them a type key.
        for questionEcrite in listOfQuestionsEcrites:
            tempResult.append(
                {"type": "questionEcrite", "uid": questionEcrite["uid"], "score": questionEcrite["score"]})
        for questionOraleSansDebat in listOfQuestionsOralesSansDebat:
            tempResult.append(
                {"type": "questionOraleSansDebat", "uid": questionOraleSansDebat["uid"], "score": questionOraleSansDebat["score"]})
        for dossierLegislatif in listOfdossierLegislatif:
            tempResult.append(
                {"type": "dossierLegislatif", "uid": dossierLegislatif, "score": 0})
        for questionAuGouvernement in listOfQuestionsAuGouvernement:
            tempResult.append(
                {"type": "questionAuGouvernement", "uid": questionAuGouvernement["uid"], "score": questionAuGouvernement["score"]})

        ret["listOfResults"].extend(tempResult)

        connection.close()
        return json.dumps(ret)

    """__htmlEscape
				Escape some char string
				@params string : term to search
				@return :

	"""

    def __htmlEscape(self, string):
        try:
            ret = string.replace("'", "''")
        except:
            traceback.print_exc()
            print(string)
        return ret

    """getDocumentByUid
				return a dossier legislatif by its uid
				@params uid : uid of dossier
				@return :

	"""

    def getDocumentByUid(self, uid):
        connection = psycopg2.connect(database=self.__database, user=self.__userDatabase,
                                      password=self.__passwordDatabase, host=self.__hostDatabase, port=self.__portDatabase)
        connection.autocommit = True
        cursor = connection.cursor()

        tableDef = self.__dossierLegislatifDocumentTableDefinition

        ret = {}
        query = "SELECT "
        for key in tableDef["schema"].keys():
            query += key + ","
        query = query[:-1]
        query += " FROM DOSSIERS_LEGISLATIFS_DOCUMENT WHERE uid=%s;"

        try:
            cursor.execute(query, (uid,))
            entry = cursor.fetchone()
            listOfColumn = list(
                tableDef["schema"].keys())
            for i in range(len(entry)):
                ret[listOfColumn[i]] = entry[i]
        except:
            traceback.print_exc()
        connection.close()
        return ret

    """getDossierLegislatifByUid
				return a dossier legislatif by its uid
				@params uid : uid of dossier
				@return :

	"""

    def getDossierLegislatifByUid(self, uid):
        connection = psycopg2.connect(database=self.__database, user=self.__userDatabase,
                                      password=self.__passwordDatabase, host=self.__hostDatabase, port=self.__portDatabase)
        connection.autocommit = True
        cursor = connection.cursor()

        tableDef = self.__dossierLegislatifDossierParlementaireTableDefinition

        ret = {}
        query = "SELECT "
        for key in tableDef["schema"].keys():
            query += key + ","
        query = query[:-1]
        query += " FROM DOSSIERS_LEGISLATIFS_DOSSIER_PARLEMENTAIRE WHERE uid=%s;"

        try:
            cursor.execute(query, (uid,))
            entry = cursor.fetchone()
            listOfColumn = list(
                tableDef["schema"].keys())
            for i in range(len(entry)):
                ret[listOfColumn[i]] = entry[i]
        except:
            traceback.print_exc()
        connection.close()
        return ret

    """getQuestionOraleSansDebatByUid
				return a question ecrite by its uid
				@params uid : uid of question ecrite
				@return : json of the question

	"""

    def getQuestionOraleSansDebatByUid(self, uid):
        connection = psycopg2.connect(database=self.__database, user=self.__userDatabase,
                                      password=self.__passwordDatabase, host=self.__hostDatabase, port=self.__portDatabase)
        connection.autocommit = True
        cursor = connection.cursor()

        tableDef = self.__questionEcriteTableDefinition

        ret = {}
        query = "SELECT "
        for key in tableDef["schema"].keys():
            query += key + ","
        query = query[:-1]
        query += " FROM QUESTIONS_ORALES_SANS_DEBAT WHERE uid=%s;"

        try:
            cursor.execute(query, (uid,))
            entry = cursor.fetchone()
            listOfColumn = list(
                tableDef["schema"].keys())
            for i in range(len(entry)):
                ret[listOfColumn[i]] = entry[i]
        except:
            traceback.print_exc()
        connection.close()
        return ret

    """getQuestionEcriteByUid
				return a question ecrite by its uid
				@params uid : uid of question ecrite
				@return : json of the question

	"""

    def getQuestionEcriteByUid(self, uid):
        connection = psycopg2.connect(database=self.__database, user=self.__userDatabase,
                                      password=self.__passwordDatabase, host=self.__hostDatabase, port=self.__portDatabase)
        connection.autocommit = True
        cursor = connection.cursor()

        tableDef = self.__questionEcriteTableDefinition

        ret = {}
        query = "SELECT "
        for key in tableDef["schema"].keys():
            query += key + ","
        query = query[:-1]
        query += " FROM QUESTIONS_ECRITES WHERE uid=%s;"

        try:
            cursor.execute(query, (uid,))
            entry = cursor.fetchone()
            listOfColumn = list(
                tableDef["schema"].keys())
            for i in range(len(entry)):
                ret[listOfColumn[i]] = entry[i]
        except:
            traceback.print_exc()
        connection.close()
        return ret

    """getQuestionAuGouvernementByUid
				return a question au gouvernement (avec debat) by its uid
				@params uid : uid of question ecrite
				@return : json of the question

	"""

    def getQuestionAuGouvernementByUid(self, uid):
        connection = psycopg2.connect(database=self.__database, user=self.__userDatabase,
                                      password=self.__passwordDatabase, host=self.__hostDatabase, port=self.__portDatabase)
        connection.autocommit = True
        cursor = connection.cursor()

        tableDef = self.__questionAuGouvernementTableDefinition

        ret = {}
        query = "SELECT "
        for key in tableDef["schema"].keys():
            query += key + ","
        query = query[:-1]
        query += " FROM QUESTIONS_AU_GOUVERNEMENT WHERE uid=%s;"

        try:
            cursor.execute(query, (uid,))
            entry = cursor.fetchone()
            listOfColumn = list(
                tableDef["schema"].keys())
            for i in range(len(entry)):
                ret[listOfColumn[i]] = entry[i]
        except:
            traceback.print_exc()
        connection.close()
        return ret

    """getDossierLegislatifdocumentsByUid
				return a all documents of dossier legislatif by its uid
				@params uid : uid of dossier
				@return :

	"""

    def getDossierLegislatifdocumentsByUid(self, uid):
        connection = psycopg2.connect(database=self.__database, user=self.__userDatabase,
                                      password=self.__passwordDatabase, host=self.__hostDatabase, port=self.__portDatabase)
        connection.autocommit = True
        cursor = connection.cursor()

        tableDef = self.__dossierLegislatifDocumentTableDefinition

        ret = {}
        ret["documents"] = []
        query = "SELECT "
        for key in tableDef["schema"].keys():
            query += key + ","
        query = query[:-1]
        query += " FROM DOSSIERS_LEGISLATIFS_DOCUMENT WHERE dossierRef=%s ORDER BY dateDepot DESC;"

        try:
            cursor.execute(query, (uid,))
            for entry in cursor.fetchall():
                entryData = {}
                listOfColumn = list(
                    tableDef["schema"].keys())
                for i in range(len(entry)):
                    if type(entry[i]) == datetime.datetime:
                        entryData[listOfColumn[i]] = str(entry[i])
                    else:
                        entryData[listOfColumn[i]] = entry[i]
                ret["documents"].append(entryData)
        except:
            pass
        connection.close()
        return ret

    """getAmendementsByUid
				return a all amendements of a document by its uid
				@params uid : uid of dossier
				@return :

	"""

    def getAmendementsByUid(self, uid,  maxNumberOfAmendement=10):
        connection = psycopg2.connect(database=self.__database, user=self.__userDatabase,
                                      password=self.__passwordDatabase, host=self.__hostDatabase, port=self.__portDatabase)
        connection.autocommit = True
        cursor = connection.cursor()

        tableDef = self.__amendementTableDefinition

        ret = {}
        ret["amendements"] = []
        query = "SELECT "
        for key in tableDef["schema"].keys():
            query += key + ","
        query = query[:-1]
        query += " FROM AMENDEMENT WHERE texteLegislatifRef=%sORDER BY dateDepot DESC;"
        try:
            cursor.execute(query, (uid,))
            for entry in cursor.fetchall():
                entryData = {}
                listOfColumn = list(
                    tableDef["schema"].keys())
                for i in range(len(entry)):
                    if type(entry[i]) == datetime.datetime:
                        entryData[listOfColumn[i]] = str(entry[i])
                    else:
                        entryData[listOfColumn[i]] = entry[i]
                ret["amendements"].append(entryData)
        except:
            pass
        ret["numberOfAmendement"] = len(ret["amendements"])
        ret["amendements"] = ret["amendements"][:maxNumberOfAmendement]
        connection.close()
        return ret

    """getAmendementsQuery
				return a all amendements of a document by its uid, than meets the query
				@params uid : uid of dossier
				@return :

	"""

    def getAmendementsQuery(self, uidTexteLegislatifRef, term, maxNumberOfAmendement=10):
        connection = psycopg2.connect(database=self.__database, user=self.__userDatabase,
                                      password=self.__passwordDatabase, host=self.__hostDatabase, port=self.__portDatabase)
        connection.autocommit = True
        cursor = connection.cursor()

        tableDef = self.__amendementTableDefinition

        texteLegislatifRef = uidTexteLegislatifRef.replace(
            "'", "\\'").replace("--", "")
        processedQuery = term.replace("'", "\\'").replace("--", "")

        ret = {}
        ret["amendements"] = []
        ret["count"] = 0

        # First get the radicals (use for highlight in react)
        try:
            cursor.execute("SELECT to_tsvector('french', %s);",
                           (processedQuery,))
            ret["query"] = " ".join(cursor.fetchone()[0].split("'")[1::2])
        except:
            traceback.print_exc()

        # Then get the results
        query = "SELECT "
        for key in tableDef["schema"].keys():
            query += key + ","
        query = query[:-1]
        query += " FROM AMENDEMENT WHERE ts @@ to_tsquery('french',%s) AND texteLegislatifRef=%s;"

        count = 0

        # First try by the words adjacent
        processedQueryLogic = processedQuery.replace(" ", "<1>")
        try:
            cursor.execute(query, (processedQueryLogic, texteLegislatifRef,))
            for entry in cursor.fetchall():
                entryData = {}
                listOfColumn = list(
                    tableDef["schema"].keys())
                for i in range(len(entry)):
                    if type(entry[i]) == datetime.datetime:
                        entryData[listOfColumn[i]] = str(entry[i])
                    else:
                        entryData[listOfColumn[i]] = entry[i]
                if entryData not in ret["amendements"]:
                    ret["amendements"].append(entryData)
        except:
            traceback.print_exc()

        # Then try by the words anywhere
        processedQueryLogic = processedQuery.replace(" ", "&")
        try:
            cursor.execute(query, (processedQueryLogic, texteLegislatifRef,))
            for entry in cursor.fetchall():
                entryData = {}
                listOfColumn = list(
                    tableDef["schema"].keys())
                for i in range(len(entry)):
                    if type(entry[i]) == datetime.datetime:
                        entryData[listOfColumn[i]] = str(entry[i])
                    else:
                        entryData[listOfColumn[i]] = entry[i]
                if entryData not in ret["amendements"]:
                    ret["amendements"].append(entryData)
        except:
            traceback.print_exc()

        # Then try by any word
        processedQueryLogic = processedQuery.replace(" ", "|")
        try:
            cursor.execute(query, (processedQueryLogic, texteLegislatifRef,))
            for entry in cursor.fetchall():
                entryData = {}
                listOfColumn = list(
                    tableDef["schema"].keys())
                for i in range(len(entry)):
                    if type(entry[i]) == datetime.datetime:
                        entryData[listOfColumn[i]] = str(entry[i])
                    else:
                        entryData[listOfColumn[i]] = entry[i]
                if entryData not in ret["amendements"]:
                    ret["amendements"].append(entryData)
        except:
            traceback.print_exc()

        ret["numberOfAmendement"] = len(ret["amendements"])
        ret["amendements"] = ret["amendements"][:maxNumberOfAmendement]
        connection.close()
        return ret

    """__extractLastDateDossierParlementaire
				extract last updated date of a dossier parlementaire
				@params dossier : json of dossier
				@return :

	"""

    def __extractLastDateDossierParlementaire(self, dossier):
        lastDateString = "1970-01-01T01:00:00.000+00:00"
        lastDateDatetime = datetime.datetime.strptime(
            lastDateString, "%Y-%m-%dT%H:%M:%S.%f%z")

        try:
            for key, value in dossier.items():
                tempLastDatetime = None
                if isinstance(value, dict):
                    ret = self.__extractLastDateDossierParlementaire(value)
                    tempLastDatetime = ret["lastDateDatetime"]
                    tempLastDateString = ret["lastDateString"]
                elif isinstance(value, list):
                    for doc in value:
                        if isinstance(doc, dict):
                            ret = self.__extractLastDateDossierParlementaire(
                                doc)
                            tempLastDatetime = ret["lastDateDatetime"]
                            tempLastDateString = ret["lastDateString"]
                            if tempLastDatetime > lastDateDatetime:
                                lastDateDatetime = tempLastDatetime
                                lastDateString = tempLastDateString
                else:
                    if key == "dateActe" and value is not None:
                        tempLastDatetime = datetime.datetime.strptime(
                            value, "%Y-%m-%dT%H:%M:%S.%f%z")
                        tempLastDateString = value
                if tempLastDatetime is not None:
                    if tempLastDatetime > lastDateDatetime:
                        lastDateDatetime = tempLastDatetime
                        lastDateString = tempLastDateString
        except:
            traceback.print_exc()
            print(dossier)

        return {"value": lastDateString, "lastDateString": lastDateString, "lastDateDatetime": lastDateDatetime}
