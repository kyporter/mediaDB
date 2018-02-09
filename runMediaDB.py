from makeMediaDB import *
from guiFunctions import *
from tkinter import *
from tkinter import ttk

#build config

#read data from config
config = "mdConfig.txt"

class TypeButtons(ttk.Frame):
	def __init__(self, parent):
		super().__init__(parent)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.typelab = ttk.Label(self, text="Select Media Type:")
		self.typevar = IntVar()
		self.bookbutton = ttk.Radiobutton(self, text="Book", variable=self.typevar, value=1)
		self.moviebutton = ttk.Radiobutton(self, text="Movie", variable=self.typevar, value=2)
		self.musicbutton = ttk.Radiobutton(self, text="Music", variable=self.typevar, value=3)
		self.confbutton = ttk.Button(self, text="Create New Database", command=self.sendInfo)
		self.typelab.grid(column = 0, row=0, columnspan=3, sticky=N+W+S+E)

	def sendInfo(self):
		
		

class GetInfoWindow(ttk.Frame):
	def __init__(self,master=None):
		super().__init__(master)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)		

		self.namelab = ttk.Label(self, text="Username:")
		self.namevar = StringVar()
		self.namebox = ttk.Entry(self, textvariable=self.namevar, style='InfoFrame.TLabel')
		self.typelab = ttk.Label(self, text="Select Media Type:")
		self.typevar = IntVar()
		self.bookbutton = ttk.Radiobutton(self, text="Book", variable=self.typevar, value=1)
		self.moviebutton = ttk.Radiobutton(self, text="Movie", variable=self.typevar, value=2)
		self.musicbutton = ttk.Radiobutton(self, text="Music", variable=self.typevar, value=3)
		self.confbutton = ttk.Button(self, text="Create New Database", command=self.sendInfo)
		self.typelab.grid(column = 0, row=0, columnspan=3, sticky=N+W+S+E)

	def sendInfo(self):
		

		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.placeItems()

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

	newInstance = AppManager(currentDB)



	

	


#if config.name == None:
#display create database page

#display main


