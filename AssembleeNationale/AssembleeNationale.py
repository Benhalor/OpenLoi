import os
import sys
import time
import json
import shutil
import html
import zipfile
import traceback
import datetime
import psycopg2
import requests


class AssembleeNationale:

    """Constructor
                    Creation of the object with default values
                    @params verbose : integer specifying the amount of text written in the console by this lib.
                            0 : nothing
                            1 : important informations
                            2 : everything

    """

    def __init__(self, verbose=0, setup=False):
        self.__verbose = verbose
        self.__sourceList = sourceList = {
            "DOSSIERS_LEGISLATIFS": {"link": "https://data.assemblee-nationale.fr/static/openData/repository/15/loi/dossiers_legislatifs/Dossiers_Legislatifs_XV.json.zip", "pollingFrequency": 1000000},
            "AGENDA": {"link": "http://data.assemblee-nationale.fr/static/openData/repository/15/vp/seances/seances_publique_excel.csv", "pollingFrequency": 10},
            "AMENDEMENTS": {"link": "https://data.assemblee-nationale.fr/static/openData/repository/15/loi/amendements_legis/Amendements_XV.json.zip", "pollingFrequency": 1000000},
            "DEBATS_EN_SEANCE_PUBLIQUE": {"link": "https://data.assemblee-nationale.fr/static/openData/repository/15/vp/syceronbrut/syseron.xml.zip", "pollingFrequency": 1000000},
            "VOTES": {"link": "https://data.assemblee-nationale.fr/static/openData/repository/15/loi/scrutins/Scrutins_XV.json.zip", "pollingFrequency": 1000000},
            "QUESTIONS_AU_GOUVERNEMENT": {"link": "https://data.assemblee-nationale.fr/static/openData/repository/15/questions/questions_gouvernement/Questions_gouvernement_XV.json.zip", "pollingFrequency": 100000},
            "QUESTIONS_ORALES_SANS_DEBAT": {"link": "https://data.assemblee-nationale.fr/static/openData/repository/15/questions/questions_orales_sans_debat/Questions_orales_sans_debat_XV.json.zip", "pollingFrequency": 100000},
            "QUESTIONS_ECRITES": {"link": "https://data.assemblee-nationale.fr/static/openData/repository/15/questions/questions_ecrites/Questions_ecrites_XV.json.zip", "pollingFrequency": 1000000},
            "REUNIONS": {"link": "https://data.assemblee-nationale.fr/static/openData/repository/15/vp/reunions/Agenda_XV.json.zip", "pollingFrequency": 1000000},

        }

        self.__dossierLegislatifTableDefinition = {
            "tableName": "DOSSIERS_LEGISLATIFS",
            "schema": {
                "uid": {"path": "document:uid", "htmlEscape": False, "type": "VARCHAR ( 20 ) PRIMARY KEY", },
                "dateCreation": {"path": "document:cycleDeVie:chrono:dateCreation", "htmlEscape": False, "type": "TIMESTAMP WITH TIME ZONE"},
                "dateDepot": {"path": "document:cycleDeVie:chrono:dateDepot", "htmlEscape": False, "type": "TIMESTAMP WITH TIME ZONE"},
                "datePublication": {"path": "document:cycleDeVie:chrono:datePublication", "htmlEscape": False, "type": "TIMESTAMP WITH TIME ZONE"},
                "datePublicationWeb": {"path": "document:cycleDeVie:chrono:datePublicationWeb", "htmlEscape": False, "type": "TIMESTAMP WITH TIME ZONE"},
                "denominationStructurelle": {"path": "document:denominationStructurelle", "htmlEscape": True, "type": "VARCHAR ( 200 )"},
                "titrePrincipal": {"path": "document:titres:titrePrincipal", "htmlEscape": True, "type": "VARCHAR ( 2000 )"},
                "titrePrincipalCourt": {"path": "document:titres:titrePrincipalCourt", "htmlEscape": True, "type": "VARCHAR ( 2000 )"},
                "dossierRef": {"path": "document:dossierRef", "htmlEscape": True, "type": "VARCHAR ( 200 )"},
                "notice": {"path": "document:notice:formule", "htmlEscape": True, "type": "VARCHAR ( 2000 )"}
            }
        }
        self.__tableList = [self.__dossierLegislatifTableDefinition]

        self.__database = 'assembleenationale'

        # Setup database for the first time if requiered by user
        if setup:
            self.setupDatabase()

        self.__jsonReadOK = 0
        self.__jsonReadNOK = 0
        self.__count = 0

    """setupDatabase
			Setup the postgredatabase with the schema
			@params  : 

	"""

    def setupDatabase(self):
        # establishing the connection on the postgres database
        connection = psycopg2.connect(
            database="postgres", user='postgres', password='password', host='localhost', port='5432'
        )
        connection.autocommit = True
        cursor = connection.cursor()

        # Create database AssembleeNationale if not exists
        try:
            cursor.execute("CREATE database " + self.__database+";")
            self.__debugPrint("Database "+self.__database +
                              " created successfully...")
        except psycopg2.errors.DuplicateDatabase:
            self.__debugPrint("Database "+self.__database+" already exists")

        # Connect on the new database
        connection = psycopg2.connect(
            database=self.__database, user='postgres', password='password', host='localhost', port='5432'
        )
        connection.autocommit = True
        cursor = connection.cursor()

        for tableDef in self.__tableList:
            # Drop existing tables todo remove
            """try:
                    query = "DROP TABLE "+tableDef["tableName"]
                    cursor.execute(query)
                    print("Table "+tableDef["tableName"]+" drop successfully...")
            except:
                    pass"""

            try:
                query = "CREATE TABLE "+tableDef["tableName"]+"("
                columnString = ""
                for columnName, columnDef in tableDef["schema"].items():
                    columnString += columnName + " "+columnDef["type"]+","
                query += columnString[:-1]+");"
                cursor.execute(query)
                print("Table "+tableDef["tableName"] +
                      " created successfully...")
            except psycopg2.errors.DuplicateTable:
                print("Table "+tableDef["tableName"]+" already exists")

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

    def processSources(self, dataDirectory, sourceList):

        for path in sourceList:
            if path[-9:] == "excel.csv":
                self.__processExcelCsv(path)
            if path[-3:] == "zip":
                self.__processZip(path)

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
            self.__uploadToDossierLegislatif(
                directoryToExtract+"/json/document", table=sourceName)
            print("json OK:"+str(self.__jsonReadOK))
            print("json NOK:"+str(self.__jsonReadNOK))
            print("json count:"+str(self.__count))
            pass
        elif sourceName == "AGENDA":
            pass
        elif sourceName == "AMENDEMENTS":
            pass
        elif sourceName == "DEBATS_EN_SEANCE_PUBLIQUE":
            pass
        elif sourceName == "VOTES":
            pass
        elif sourceName == "QUESTIONS_AU_GOUVERNEMENT":
            pass
        elif sourceName == "QUESTIONS_ORALES_SANS_DEBAT":

            pass
        elif sourceName == "QUESTIONS_ECRITES":
            pass
        elif sourceName == "REUNIONS":
            pass

    """__unicodeEscape
				Recursively escape badly encoded unicode char for all files in a given directory
				@params path : path of the directory
				@return : 
					
	"""

    def __unicodeEscape(self, directory):
        for root, subdirs, files in os.walk(directory):
            for fileName in files:
                path = os.path.join(root, fileName)
                with open(path, 'rb') as source_file:
                    contents = source_file.read()
                    with open(path, 'wb') as dest_file:
                        dest_file.write(contents.decode(
                            'unicode_escape').encode('utf-8'))
                        self.__count += 1

    """__uploadToDossierLegislatif
				Recursively explore the foler dossierLegislatif and upload to db
				@params path : path of the directory
				@return : 
					
	"""

    def __uploadToDossierLegislatif(self, directory, table="DOSSIERS_LEGISLATIFS"):
        connection = psycopg2.connect(
            database=self.__database, user='postgres', password='password', host='localhost', port='5432'
        )
        connection.autocommit = True
        cursor = connection.cursor()

        for root, subdirs, files in os.walk(directory):
            for fileName in files:
                path = os.path.join(root, fileName)
                with open(path, 'r') as sourceFile:
                    text = sourceFile.read()
                    try:
                        doc = json.loads(text)
                        try:
                            query = self.__buildQueryFromDef(
                                doc, self.__dossierLegislatifTableDefinition)
                            cursor.execute(query)
                            self.__jsonReadOK += 1
                        except psycopg2.errors.UniqueViolation:
                            pass
                            #print("Insert in "+table+" already exists")
                        except:
                            print(path)
                            traceback.print_exc()
                    except:
                        self.__jsonReadNOK += 1

    """__buildQueryFromDef
				Build a query to insert an element from a dict defining the table
				@params doc : json doc (data)
				@params tableDef : dict defining the table
				@return : 
					
	"""

    def __buildQueryFromDef(self, doc, tableDef):
        query = ""
        query += "INSERT INTO "+tableDef["tableName"]+"("
        columnString = ""
        valuesString = ""
        for columnName, columnDef in tableDef["schema"].items():
            try:
                docPath = doc
                for pathIter in columnDef["path"].split(":"):
                    docPath = docPath[pathIter]
                if docPath is not None:
                    columnString += columnName+","
                    if columnDef["htmlEscape"]:
                        valuesString += "\'"+html.escape(docPath)+"\',"
                    else:
                        valuesString += "\'"+docPath+"\',"
            except KeyError:
                pass
            except:
                tracebacl.print_exc()

        query += columnString[:-1] + ") VALUES (" + valuesString[:-1]+");"
        return query

    """search
				search a term in tables
				@params term : term to search
				@return : 
					
	"""

    def search(self, term, listOfTables=None):
        listOfTables = 0
        connection = psycopg2.connect(
            database=self.__database, user='postgres', password='password', host='localhost', port='5432'
        )
        connection.autocommit = True
        cursor = connection.cursor()

        try:
            query = "ALTER TABLE DOSSIERS_LEGISLATIFS ADD COLUMN ts tsvector GENERATED ALWAYS AS (to_tsvector('french', titrePrincipal)) STORED;"
            cursor.execute(query)
        except:
            pass
        try:
            query = "CREATE INDEX ts_idx ON DOSSIERS_LEGISLATIFS USING GIN (ts);"
            cursor.execute(query)
        except:
            pass

        query = "SELECT "
        for key in self.__dossierLegislatifTableDefinition["schema"].keys():
            query += key + ","
        query = query[:-1]
        query += " FROM DOSSIERS_LEGISLATIFS WHERE ts @@ to_tsquery('french','" + \
            term+"');"
        cursor.execute(query)
        ret = {}
        ret["data"] = []
        for entry in cursor.fetchall():
            entryData = {}
            entryData["type"] = "DOSSIERS_LEGISLATIFS"
            listOfColumn = list(
                self.__dossierLegislatifTableDefinition["schema"].keys())
            for i in range(len(entry)):
                entryData[listOfColumn[i]] = entry[i]
            ret["data"].append(entryData)
        return json.dumps(ret, default=str)
