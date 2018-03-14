import platform
from makeMediaDB import *
from guiFunctions import *
from tkinter import *
from tkinter import ttk, font
import os.path
import time

#build config

#read data from config
config = "mdConfig.txt"
entryYPad = 10
entryXPad = 30
labelXPad = 10
radButtonYPad = 10
radButtonXPad = 10
buttonYPad = 10
buttonXPad = 20



#FIXME:medDict = {1: "book", 2: "movie", 3: "music"}
		
class GetInfoWindow(ttk.Frame):
	def __init__(self,infodict,grandmaster=None,master=None):
		super().__init__(master)
		self.m = master
		self.gm = grandmaster
		self.theStyle = ttk.Style()
		self.checkOS()
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		self.rowconfigure(0, weight=1) #name
		self.rowconfigure(1, weight=1) #radiobutton label
		self.rowconfigure(2, weight=1) #radiobuttons		
		self.rowconfigure(3, weight=1) #confirmation button
		self.dict = infodict
		self.namelab = ttk.Label(self, text="Username:", style='InfoFrame.TLabel')
		self.namevar = StringVar()
		self.namebox = ttk.Entry(self, font=self.entryFont, textvariable=self.namevar)
		self.typelab = ttk.Label(self, text="Select Media Type:")
		self.typevar = StringVar()
		self.bookbutton = ttk.Radiobutton(self, text="Book", variable=self.typevar, value="book")
		self.moviebutton = ttk.Radiobutton(self, text="Movie", variable=self.typevar, value="movie")
		self.musicbutton = ttk.Radiobutton(self, text="Music", variable=self.typevar, value="music")
		self.confbutton = ttk.Button(self, text="Open Database", command=self.sendInfo)
		self.grid(column=0, row=0, sticky=N+W+S+E)
		self.namelab.grid(column=0, row=0, sticky=N+W+S+E, ipady=entryYPad, ipadx=labelXPad)
		self.namebox.grid(column=1, row=0, columnspan=2, sticky=N+W+S+E, ipady=entryYPad, ipadx=entryXPad)
		self.typelab.grid(column=0, row=1, columnspan=3, sticky=N+W+S+E)
		self.bookbutton.grid(column=0, row=2, sticky=N+W+S+E, ipady=radButtonYPad, ipadx=radButtonXPad)
		self.moviebutton.grid(column=1, row=2, sticky=N+W+S+E, ipady=radButtonYPad, ipadx=radButtonXPad)
		self.musicbutton.grid(column=2, row=2, sticky=N+W+S+E, ipady=radButtonYPad, ipadx=radButtonXPad)
		self.confbutton.grid(column=0, row=3, columnspan=3, sticky=N+W+S+E, ipady=buttonYPad, ipadx=buttonXPad)
		self.mainloop()

	def checkOS(self):
		localSys = platform.system()
		if localSys == 'Windows':
			self.theStyle.configure('.', font=('Palatino Linotype', 14))
			self.entryFont = font.Font(family="Palatino Linotype", size=14)
			self.theStyle.theme_use('classic')
		else:
			self.theStyle.configure('.', font=('bitstream charter', 14))
			self.entryFont = font.Font(family="Bitstream Charter", size=14)
			self.theStyle.theme_use('default') #Linux options: clam, alt, default, classic

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
		infoDict['dbname'] = infoDict['owner'] + infoDict['medtype'].lower() + ".db"
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


