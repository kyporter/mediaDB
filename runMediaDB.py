from makeMediaDB import *
from guiFunctions import *
from tkinter import *
from tkinter import ttk
import os.path
import time

#build config

#read data from config
config = "mdConfig.txt"

medDict = {1: "book", 2: "movie", 3: "music"}
		
class GetInfoWindow(ttk.Frame):
	def __init__(self,infodict,master=None):
		super().__init__(master)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		self.rowconfigure(0, weight=1) #name
		self.rowconfigure(1, weight=1) #radiobutton label
		self.rowconfigure(2, weight=1) #radiobuttons		
		self.rowconfigure(3, weight=1) #confirmation button
		self.dict = infodict
		self.namelab = ttk.Label(self, text="Username:")
		self.namevar = StringVar()
		self.namebox = ttk.Entry(self, textvariable=self.namevar, style='InfoFrame.TLabel')
		self.typelab = ttk.Label(self, text="Select Media Type:")
		self.typevar = IntVar()
		self.bookbutton = ttk.Radiobutton(self, text="Book", variable=self.typevar, value=1)
		self.moviebutton = ttk.Radiobutton(self, text="Movie", variable=self.typevar, value=2)
		self.musicbutton = ttk.Radiobutton(self, text="Music", variable=self.typevar, value=3)
		self.confbutton = ttk.Button(self, text="Create New Database", command=self.sendInfo)
		self.placeItems()
		#self.mainloop()

	def sendInfo(self):
		self.dict['owner'] = self.namevar
		self.dict['medtype'] = medDict[self.typevar]
		self.destroy




def Run():
	infoDict = {}
	with open("mdConfig.txt", "r") as f:
		for line in f:
			splitLine = line.strip().split(":")
			if len(splitLine) == 2:
				infoDict[splitLine[0].lower()] = splitLine[1].lower()
	
	if infoDict['owner'] == 'none' || infoDict['dbname'] == 'none' || infoDict['medtype'] == 'none':
		infoWnd = GetInfoWindow(infoDict)
		while infoWnd != None:
			time.sleep(.1)
		infoDict['dbname'] = infoDict['owner'].upper() + infoDict['medtype'].lower() + ".db"
	#errorcheck dupe dbnames
		if os.path.isfile(infoDict['dbname']):
			continue
		MediaDB(infoDict['owner'], connectionName=infoDict['dbname'], mediaType=infoDict['medtype'])

	newInstance = AppManager(infoDict['dbname'], infoDict['medtype'])
	newInstance.makeMainPage()



if __name__ == '__main__':
	Run()	

	


#if config.name == None:
#display create database page

#display main


