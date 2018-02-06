from makeMediaDB import *
from guiFunctions import *

#build config

#read data from config
config = "mdConfig.txt"

def __main__():
	infoDict = {}
	with open("mdConfig.txt", "r") as f:
		for line in f:
			splitLine = line.strip().split(":")
			if len(splitLine) == 2:
				infoDict[splitLine[0].lower()] = splitLine[1].lower()
	
	if infoDict['owner'] == 'none':
		infoDict['owner'] = requestOwner()

	if infoDict['dbname'] == 'none':
		infoDict['dbname'] = getDbName()

	if infoDict['medtype'] == 'none':
		infoDict['medtype'] = getType()
	
	#errorcheck dupe dbnames
	currentDB = MediaDB(infoDict['owner'], connectionName=infoDict['dbname'], mediaType=infoDict['medtype'])

	newInstance = RunApp(currentDB)



	

	


#if config.name == None:
#display create database page

#display main


