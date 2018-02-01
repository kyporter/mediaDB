from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from makeMediaDB import *
import random

import sqlite3 as s3

global DBNAME = 'testmoviedb.db'
global MEDIATYPE = 'movie'
global running = 0
global titleDict
titleDict = {}
global genreDict
genreDict = {}
global formatDict
formatDict = {}
global seriesDict
seriesDict = {}
global authorDict
authorDict = {}
global myapp


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

def makeDicts():
	c.execute("SELECT title, i_id FROM Items")
	conn.commit()
	title_info = c.fetchall()
	if len(title_info) > 0:
	    titleDict = { t[0]:t[1] for t in title_info }

	c.execute("SELECT genre_name, g_id FROM Genres")
	conn.commit()
	genre_info = c.fetchall()
	if len(genre_info) > 0:
	    genreDict = { g[0]:g[1] for g in genre_info }
	genreDict[""] = 0

	c.execute("SELECT format_name, f_id FROM Formats")
	conn.commit()
	format_info = c.fetchall()
	if len(format_info) > 0:
	    formatDict = { f[0]:f[1] for f in format_info }

	if MEDIATYPE != 'music':
		c.execute("SELECT series_name, s_id FROM Series")
		conn.commit()
		series_info = c.fetchall()
		if len(series_info) > 0:
		    seriesDict = { s[0]:s[1] for s in series_info }
		seriesDict[""] = 0

	if MEDIATYPE != 'movie':
		c.execute("SELECT name, a_id FROM Authors")
		conn.commit()
		author_info = c.fetchall()
		if len(author_info) > 0:
			authorDict = { a[0]:a[1] for a in author_info }
		authorDict[""] = 0

	global Genres
	Genres = sorted(genreDict)

	global Titles
	Titles = articleSort(titleDict)

	global Formats
	Formats = sorted(formatDict)

	global Series
	Series = sorted(seriesDict)

	global Authors
	Authors = sorted(authorDict)


def updateTitleList():
    global Titles
    Titles = sorted(titleDict)
    
def updateGenreList():
    global Genres
    Genres = sorted(genreDict)
    
def updateFormatList():
    global Formats
    Formats = sorted(formatDict)
    
def updateSeriesList():
    global Series
    Series = sorted(seriesDict)

def updateAuthorList():
	global Authors
	Authors = sorted(authorDict)



def addNewItem():
    global myapp
    myapp = AddApp()
    myapp.master.title("MyMediaDB Add {} Page", MEDIATYPE.capitalize())
    myapp.master.minsize(100,500)
    myapp.master.rowconfigure(0, weight=1)
    myapp.master.columnconfigure(0, weight=1)
    myapp.mainloop()

def startConnection():
	global running
	global conn
	global c
	conn = s3.connect(DBNAME)
	c = conn.cursor()
	running = 1

def makeMainPage(runDB):
	global DBNAME = runDB.getName()
	global MEDIATYPE = runDB.getType()

	if running != 1:
		startConnection()

	makeDicts()

    global myapp
    myapp = App()
    myapp.master.title("MyMediaDB Main Page")
    myapp.master.minsize(100,500)
    myapp.master.rowconfigure(0, weight=1)
    myapp.master.columnconfigure(0, weight=1)
    myapp.mainloop()

def editSelectMovie():
    global edapp
    title = myapp.tlistframe.getSelected()
    m_id = movieDict[title]
    edapp = myapp #???
    edapp = EditApp(m_id)
    edapp.master.title("MyMediaDB Edit Information Page")
    edapp.master.minsize(100,500)
    edapp.master.rowconfigure(0, weight=1)
    edapp.master.columnconfigure(0, weight=1)
    edapp.mainloop()

def pickRandomTitle():
    curTitleList = myapp.localTitleList
    if len(curTitleList) == 0:
        errMsg = "What do you expect me to pick from? Change options so there are some choices available"
        messagebox.showerror(message=errMsg)
        return
    picked = random.choice(curTitleList)
    myapp.displayInfo(picked)



mystyle = ttk.Style()
mystyle.theme_use('classic')
mystyle.configure('.', font=('gothic', 12))
mystyle.configure('.', foreground='#1c4363', background='#ffedcc')
mystyle.configure('InfoFrame.TFrame', foreground='#bdf4ef', background='#bdf4ef')
mystyle.configure('InfoFrame.TLabel', foreground='#000000', background='#bdf4ef')
mystyle.configure('InfoFrame.TButton', foreground='#bdf4ef', background='#0b413d')

__main__()
