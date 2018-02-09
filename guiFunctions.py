from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from makeMediaDB import *
from guiClasses import *
import sqlite3 as s3


def isArticle(word):
	articles = ["A", "The", "An", "Stephen King's", "Wes Craven's"]
	if word in articles:
		return True
	return False

def articleSort(titleList):
	alessList = []
	for item in titleList:
		itemsplit = item.split(maxsplit=1)
		if len(itemsplit) == 2 and isArticle(itemsplit[0]):
			newitem = (itemsplit[1],itemsplit[0]+" ")
		else:
			newitem = (item, "")
		alessList.append(newitem)
	newList = sorted(alessList, key=lambda word: word[0])
	finList = [ i[1]+i[0] for i in newList ]
	return finList

class AppManager:
	
	def __init__(self, dbname, mtype):
		self.DBNAME = dbname
		self.MEDIATYPE = mtype
		self.running = 0
		self.storedApp = None
		self.startConnection()
		self.makeDicts()
		#FIXME? self.makeMainPage()
		self.theStyle = ttk.Style()
		self.theStyle.theme_use('classic')
		self.theStyle.configure('.', font=('gothic', 12))
		self.theStyle.configure('.', foreground='#1c4363', background='#ffedcc')
		self.theStyle.configure('InfoFrame.TFrame', foreground='#bdf4ef', background='#bdf4ef')
		self.theStyle.configure('InfoFrame.TLabel', foreground='#000000', background='#bdf4ef')
		self.theStyle.configure('InfoFrame.TButton', foreground='#bdf4ef', background='#0b413d')


	def startConnection(self):
		self.conn = s3.connect(DBNAME)
		self.c = self.conn.cursor()
		self.running = 1		


	def makeDicts(self):
		self.titleDict = {}
		self.genreDict = {}
		self.formatDict = {}
		self.seriesDict = {}
		self.authorDict = {}

		self.c.execute("SELECT title, i_id FROM Items")
		self.conn.commit()
		title_info = self.c.fetchall()
		if len(title_info) > 0:
			self.titleDict = { t[0]:t[1] for t in title_info }

		self.c.execute("SELECT genre_name, g_id FROM Genres")
		self.conn.commit()
		genre_info = self.c.fetchall()
		if len(genre_info) > 0:
			self.genreDict = { g[0]:g[1] for g in genre_info }
		self.genreDict[""] = 0

		self.c.execute("SELECT format_name, f_id FROM Formats")
		self.conn.commit()
		format_info = self.c.fetchall()
		if len(format_info) > 0:
			self.formatDict = { f[0]:f[1] for f in format_info }

		if self.MEDIATYPE != 'music':
			self.c.execute("SELECT series_name, s_id FROM Series")
			self.conn.commit()
			series_info = self.c.fetchall()
			if len(series_info) > 0:
				self.seriesDict = { s[0]:s[1] for s in series_info }
			self.seriesDict[""] = 0

		if MEDIATYPE != 'movie':
			self.c.execute("SELECT name, a_id FROM Authors")
			self.conn.commit()
			author_info = self.c.fetchall()
			if len(author_info) > 0:
				self.authorDict = { a[0]:a[1] for a in author_info }
			self.authorDict[""] = 0

		self.Genres = sorted(self.genreDict)
		self.Titles = articleSort(self.titleDict)
		self.Formats = sorted(self.formatDict)
		self.Series = sorted(self.seriesDict)
		self.Authors = sorted(self.authorDict)

	def passCursor(self):
		return self.c

	def passConnection(self):
		return self.conn

	def updateTitleList(self):
		self.Titles = articleSort(self.titleDict)
		
	def updateGenreList(self):
		self.Genres = sorted(self.genreDict)
		
	def updateFormatList(self):
		self.Formats = sorted(self.formatDict)
		
	def updateSeriesList(self):
		self.Series = sorted(self.seriesDict)

	def updateAuthorList(self):
		self.Authors = sorted(self.authorDict)

	def getTitles(self):
		return self.Titles

	def getGenres(self):
		return self.Genres

	def getFormats(self):
		return self.Formats

	def getSeries(self):
		return self.Series

	def getAuthors(self):
		return self.Authors

	def isMovie(self):
		return self.MEDIATYPE == 'movie'

	def isBook(self):
		return self.MEDIATYPE == 'book'

	def isMusic(self):
		return self.MEDIATYPE == 'music'

	def addNewItem(self):
		self.storedApp = self.theApp
		self.theApp = AddApp(self,m_id)
		self.theApp.master.title("MyMediaDB Add %s Page" % self.MEDIATYPE.capitalize())
		self.theApp.master.minsize(100,500)
		self.theApp.master.rowconfigure(0, weight=1)
		self.theApp.master.columnconfigure(0, weight=1)
		self.theApp.mainloop()

	def makeMainPage(self):
		if self.storedApp == None:
			self.theApp = MainApp(self)
			self.theApp.master.title("MyMediaDB Main Page")
			self.theApp.master.minsize(100,500)
			self.theApp.master.rowconfigure(0, weight=1)
			self.theApp.master.columnconfigure(0, weight=1)
		else:
			self.theApp = self.storedApp
		self.theApp.mainloop()

	def editItem(self):
		title = self.theApp.tlistframe.getSelected()
		m_id = self.movieDict[title]
		self.storedApp = self.theApp
		self.theApp = EditApp(self,m_id)
		self.theApp.master.title("MyMediaDB Edit Information Page")
		self.theApp.master.minsize(100,500)
		self.theApp.master.rowconfigure(0, weight=1)
		self.theApp.master.columnconfigure(0, weight=1)
		self.theApp.mainloop()





