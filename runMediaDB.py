from makeMediaDB import *
from guiFunctions import *
from tkinter import *
from tkinter import ttk
import os.path
import time

#build config

#read data from config
config = "mdConfig.txt"

#FIXME:medDict = {1: "book", 2: "movie", 3: "music"}
		
class GetInfoWindow(ttk.Frame):
	def __init__(self,infodict,grandmaster=None,master=None):
		super().__init__(master)
		self.m = master
		self.gm = grandmaster
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
		self.typevar = StringVar()
		self.bookbutton = ttk.Radiobutton(self, text="Book", variable=self.typevar, value="book")
		self.moviebutton = ttk.Radiobutton(self, text="Movie", variable=self.typevar, value="movie")
		self.musicbutton = ttk.Radiobutton(self, text="Music", variable=self.typevar, value="music")
		self.confbutton = ttk.Button(self, text="Create New Database", command=self.sendInfo)
		self.grid(column=0, row=0, sticky=N+W+S+E)
		self.namelab.grid(column=0, row=0, sticky=N+W+S+E)
		self.namebox.grid(column=1, row=0, columnspan=2, sticky=N+W+S+E)
		self.typelab.grid(column=0, row=1, columnspan=3)
		self.bookbutton.grid(column=0, row=2, sticky=N+W+S+E)
		self.moviebutton.grid(column=1, row=2, sticky=N+W+S+E)
		self.musicbutton.grid(column=2, row=2, sticky=N+W+S+E)
		self.confbutton.grid(column=1, row=3, sticky=N+W+S+E)
		self.mainloop()

	def sendInfo(self):
		self.dict['owner'] = self.namevar.get()
		self.dict['medtype'] = self.typevar.get()
		print(self.dict['owner'])
		print(self.dict['medtype'])
		self.gm.destroy()


def Run():
	infoDict = {}
	with open("mdConfig.txt", "r") as f:
		for line in f:
			splitLine = line.strip().split(":")
			if len(splitLine) == 2:
				infoDict[splitLine[0].lower()] = splitLine[1].lower()
#FIXME:
	print(infoDict['owner'], infoDict['dbname'], infoDict['medtype'])	


	if infoDict['owner'] == 'none' or infoDict['dbname'] == 'none' or infoDict['medtype'] == 'none':
		realroot = Tk()
		realroot.withdraw()
		temproot = Toplevel(realroot)
		temproot.title("Getting Started")
		temproot.minsize(100,100)
		infoWnd = GetInfoWindow(infoDict, grandmaster=realroot, master=temproot)
		if infoDict['owner'] == 'none' or infoDict['dbname'] == 'none' or infoDict['medtype'] == 'none':
			time.sleep(.1)
#FIXME:sanity check for blank info in window
		infoDict['dbname'] = infoDict['owner'].upper() + infoDict['medtype'].lower() + ".db"
	#errorcheck dupe dbnames
		#realroot.destroy()
		if os.path.isfile(infoDict['dbname']):
			pass
		else:
			MediaDB(infoDict['owner'], connectionName=infoDict['dbname'], mediaType=infoDict['medtype'])

	newInstance = AppManager(infoDict['dbname'], infoDict['medtype'])
	newInstance.makeMainPage()



if __name__ == '__main__':
	Run()	

	


#if config.name == None:
#display create database page

#display main


