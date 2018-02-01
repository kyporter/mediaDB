#build config

#read data from config
config = "mdConfig.txt"

def __main__():
	infoDict = {}
	with open("mdConfig.txt", "r") as f:
		for line in f:
			splitLine = line.strip().split(":")
			if len(splitLine) == 2:
				infoDict[splitLine[0]] = splitLine[1]


#if config.name == None:
#display create database page

#display main


