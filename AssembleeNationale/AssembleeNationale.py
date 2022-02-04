import os
import time
import json
import shutil
import zipfile
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
	def __init__(self, verbose=0):
		self.__verbose = verbose
		self.__sourceList = sourceList = {
			"DOSSIERS_LEGISLATIFS": {"link":"https://data.assemblee-nationale.fr/static/openData/repository/15/loi/dossiers_legislatifs/Dossiers_Legislatifs_XV.json.zip", "pollingFrequency":10000},
			"AGENDA":{"link":"http://data.assemblee-nationale.fr/static/openData/repository/15/vp/seances/seances_publique_excel.csv", "pollingFrequency":10},
			"AMENDEMENTS":{"link":"https://data.assemblee-nationale.fr/static/openData/repository/15/loi/amendements_legis/Amendements_XV.json.zip", "pollingFrequency":10000},
			"DEBATS_EN_SEANCE_PUBLIQUE":{"link":"https://data.assemblee-nationale.fr/static/openData/repository/15/vp/syceronbrut/syseron.xml.zip", "pollingFrequency":10000},
			"VOTES":{"link":"https://data.assemblee-nationale.fr/static/openData/repository/15/loi/scrutins/Scrutins_XV.json.zip", "pollingFrequency":10000},
			"QUESTIONS_AU_GOUVERNEMENT":{"link":"https://data.assemblee-nationale.fr/static/openData/repository/15/questions/questions_gouvernement/Questions_gouvernement_XV.json.zip", "pollingFrequency":10000},
			"QUESTIONS_ORALES_SANS_DEBAT":{"link":"https://data.assemblee-nationale.fr/static/openData/repository/15/questions/questions_orales_sans_debat/Questions_orales_sans_debat_XV.json.zip", "pollingFrequency":10},
			"QUESTIONS_ECRITES":{"link":"https://data.assemblee-nationale.fr/static/openData/repository/15/questions/questions_ecrites/Questions_ecrites_XV.json.zip", "pollingFrequency":10000},
			"REUNIONS":{"link":"https://data.assemblee-nationale.fr/static/openData/repository/15/vp/reunions/Agenda_XV.json.zip", "pollingFrequency":10000},

		}

		self.__database = 'assembleenationale'
		self.setupDatabase()


	"""setupDatabase
			Setup the postgredatabase with the schema
			@params  : 

	"""
	def setupDatabase(self):
		#establishing the connection on the postgres database
		connection = psycopg2.connect(
		   database="postgres", user='postgres', password='password', host='localhost', port= '5432'
		)
		connection.autocommit = True
		cursor = connection.cursor()

		# Create database AssembleeNationale if not exists
		try:
		   cursor.execute("CREATE database "+ self.__database+";")
		   self.__debugPrint("Database "+self.__database+" created successfully...")
		except psycopg2.errors.DuplicateDatabase:
		   self.__debugPrint("Database "+self.__database+" already exists")

		# Connect on the new database
		connection = psycopg2.connect(
		   database=self.__database, user='postgres', password='password', host='localhost', port= '5432'
		)
		connection.autocommit = True
		cursor = connection.cursor()

		# Create table DOSSIERS_LEGISLATIFS
		table = "DOSSIERS_LEGISLATIFS"
		try:
		   query = """CREATE TABLE """+table+""" (
		      uid VARCHAR ( 20 ) PRIMARY KEY,
		      dateCreation TIMESTAMP NOT NULL,
		      dateDepot TIMESTAMP NOT NULL,
		      datePublication TIMESTAMP NOT NULL,
		      datePublicationWeb TIMESTAMP NOT NULL,
		      denominationStructurelle VARCHAR ( 200 ) NOT NULL,
		      dossierRef VARCHAR ( 200 ) NOT NULL,
		      titrePrincipal VARCHAR ( 500 ) NOT NULL,
		      titrePrincipalCourt VARCHAR ( 500 ) NOT NULL,
		      notice VARCHAR ( 500 ) NOT NULL
		   );
		   """
		   cursor.execute(query)
		   print("Table "+table+" created successfully...")
		except psycopg2.errors.DuplicateTable:
		   print("Table "+table+" already exists")

	"""downloadSources
			Download files from a source list and store them in a specified directory
			@params sourceList : a dict with all source lists. sourceList = {"name1": {"link":"link1", "pollingFrequency1":pollingFrequency1},...}
			@params dataDirectory : directory to store datas
			@params pollingFrequency : Download only if last version of the local file is older than pollingFrequency. In s
			@return : a dict {"duration":downloadDuration, "updatedSources":updatedSources}
				
	"""
	def downloadSources(self, dataDirectory, sourceList = None):

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
				self.__debugPrint("Start downloading "+dataName+"...", end = "", level=1)
				sourceFile = requests.get(sourceLink, allow_redirects=True)
				f = open(dataName, 'wb')
				f.write(sourceFile.content)
				f.close()
				updatedSources.append(dataName)
				self.__debugPrint("Finished")
			else:
				updatedSources.append(dataName)
				self.__debugPrint("Download of "+dataName+" is skipped, because file is not older than "+str(pollingFrequency)+"s.")

		downloadDuration = time.time()-startDownloadTime
		self.__debugPrint("Download was made in "+str(downloadDuration)+"s")

		return {"duration":downloadDuration, "updatedSources":updatedSources}


	"""__debugPrint
			Private method that print debug informations only if verbose mode is activated
			@params string : string to be printed
			@params level (optionnal): level of verbose
	"""

	def __debugPrint(self, string, end = "\n", level=1):
		if self.__verbose >= level:
			print(string, end = end, flush=True)


	"""processSources
			Download files from a source list and store them in a specified directory
			@params dataDirectory : directory to store datas
			@params sourceList : a list of path of file to process
			@return : 
				
	"""
	def processSources(self, dataDirectory, sourceList):

		for path in sourceList:
			if path[-9:]=="excel.csv":
				self.__processExcelCsv(path)
			if path[-3:]=="zip":
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
	def __processZip(self, path, replace = False):
		directoryToExtract = path.split(".")[0]

		# Remove older extracted zip
		try:
			if replace:
				self.__debugPrint("Remove old directory: " + directoryToExtract+"...", end = "", level=1)
				shutil.rmtree(directoryToExtract)
				self.__debugPrint("Finished", level=1)
		except:
			pass

		# Extract zip
		if (not os.path.exists(directoryToExtract)) or replace:
			self.__debugPrint("Start unzipping "+path+"...", end = "", level=1)
			with zipfile.ZipFile(path, 'r') as zipRef:
				zipRef.extractall(directoryToExtract)
				self.__debugPrint("Finished", level=1)
		else:
			print("not unzipping"+path)

		sourceName = directoryToExtract.split("/")[-2]
		if sourceName == "DOSSIERS_LEGISLATIFS":
			self.__unicodeEscape(directoryToExtract)
			self.__uploadToDossierLegislatif(directoryToExtract+"/json/document/")
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
		for fileName in os.listdir(directory):
			path = directory+"/"+fileName
			if os.path.isdir(path):
				self.__unicodeEscape(path)
			elif os.path.isfile(path):
				with open(path, 'rb') as source_file:
					contents = source_file.read()
					with open(path, 'wb') as dest_file:
						dest_file.write(contents.decode('unicode_escape').encode('utf-8'))

	"""__uploadToDossierLegislatif
				Recursively explore the foler dossierLegislatif and upload to db
				@params path : path of the directory
				@return : 
					
	"""
	def __uploadToDossierLegislatif(self, directory):
		for fileName in os.listdir(directory):
			path = directory+"/"+fileName
			if os.path.isdir(path):
				self.__uploadToDossierLegislatif(path)
			elif os.path.isfile(path):
				with open(path, 'r') as sourceFile:
					text = sourceFile.read()
					print(text)
					json.loads(text)
					