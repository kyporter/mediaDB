from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from makeMediaDB import *
import guiFunctions as gF
import random

#used for displayInfo
displayUnused = {'movie': "This video hasn't been watched yet!", 'book': "This hasn't been read yet!", 'music': "This hasn't been listened to yet!"}

#makes TCL-parseable list from regular list
def makeTclList(mvL):
	mvStr = ""
	mSize = len(mvL)
	mLim = mSize-1
	i = 0
	for i in range(0,mSize):
		mvStr += "{"
		mvStr += mvL[i]
		mvStr += "}"
		if i != mLim:
			mvStr += " "
	return mvStr

#finds item in list and returns index
#there is a builtin List method, but it raises valueError instead of returning None
def getInd(Listname, item):
	i = 0
	while i < len(Listname):
		if Listname[i] == item:
			return i
		i += 1
	return None

#Defines Main page genre boxes
class GenreFrame(ttk.Frame):
	def __init__(self, parent):
		super().__init__(parent, padding=5)
		self.Genres = parent.caller.getGenres()
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=3)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.g1lab = ttk.Label(self, text="Genre 1:")
		self.g2lab = ttk.Label(self, text="Genre 2:")
		self.g3lab = ttk.Label(self, text="Genre 3:")
		self.g1box = ttk.Combobox(self, values=self.Genres)
		self.g1box.state(['readonly'])
		self.g2box = ttk.Combobox(self, values=self.Genres)
		self.g2box.state(['readonly'])
		self.g3box = ttk.Combobox(self, values=self.Genres)
		self.g3box.state(['readonly'])
		self.g1lab.grid(column=0, row=0, pady=10)
		self.g2lab.grid(column=0, row=1, pady=10)
		self.g3lab.grid(column=0, row=2, pady=10)
		self.g1box.grid(column=1, row=0, pady=10, sticky=W+E)
		self.g2box.grid(column=1, row=1, pady=10, sticky=W+E)
		self.g3box.grid(column=1, row=2, pady=10, sticky=W+E)

#Defines unused and favorite buttons for both main and add/edit pages 
#vertical=False for main page, True for add/edit
class CheckbuttonFrame(ttk.Frame):
	def __init__(self, parent, vertical=False):
		super().__init__(parent, padding=5)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		if not vertical:
			self.columnconfigure(2, weight=1)
			self.columnconfigure(3, weight=1)
		self.rowconfigure(0, weight=1)
		if vertical:
			self.rowconfigure(1, weight=1)
		self.favlab = ttk.Label(self, text="Favorite")
		self.unwtlab = ttk.Label(self, text="Unused")
		self.favvar = IntVar()
		self.unwvar = IntVar()
		self.favbox = ttk.Checkbutton(self, variable=self.favvar, onvalue=1, offvalue=0)
		self.unwbox = ttk.Checkbutton(self, variable=self.unwvar, onvalue=1, offvalue=0)
		self.favlab.grid(column=0, row=0)   
		self.favbox.grid(column=1, row=0)
		if not vertical:
			self.unwtlab.grid(column=2, row=0)
			self.unwbox.grid(column=3, row=0)
		if vertical:
			self.unwtlab.grid(column=0, row=1)
			self.unwbox.grid(column=1, row=1)

#Defines format display for all pages
class FormatFrame(ttk.Frame):
	def __init__(self, parent):
		super().__init__(parent, padding=5)
		self.Formats = parent.caller.getFormats()
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=3)
		self.rowconfigure(0, weight=1)
		self.frmtlab = ttk.Label(self, text="Format(s):")
		self.frmtbox = Listbox(self, font=('gothic', 12), height=len(self.Formats), selectmode="extended", exportselection=0)
		self.popFormats()
		#self.scrollformats = ttk.Scrollbar(self, orient=VERTICAL, command=self.frmtbox.yview)
		#self.frmttbox.configure(yscrollcommand=self.scrollformats.set)
		self.frmtlab.grid(column=0, row=0)
		self.frmtbox.grid(column=1, row=0, sticky=N+W+S+E)
		#self.scrollformats.grid(column=2, row=0, sticky=N+S)
        
	def popFormats(self):
		for f in self.Formats:
			self.frmtbox.insert(END, f)

#Defines Keyword box for Main page
class KeywordFrame(ttk.Frame):
	def __init__(self, parent):
		super().__init__(parent, padding=5)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=3)
		self.rowconfigure(0, weight=1)
		self.keyword = StringVar()
		self.kwdlab = ttk.Label(self, text="Keyword(s):")
		self.kwdbox = ttk.Entry(self, textvariable=self.keyword)
		self.kwdlab.grid(column=0, row=0,pady=5)
		self.kwdbox.grid(column=1, row=0, pady=5, sticky=W+E)

#Defines button selections for Main page
class ButtonFrame(ttk.Frame):
	def __init__(self, parent):
		super().__init__(parent, padding=5)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		self.rowconfigure(0, weight=1)
		self.pkRand = ttk.Button(self, text="Random Choice", command=parent.pickRandomTitle)
		self.addNM = ttk.Button(self, text="Add New %s" % parent.caller.MEDIATYPE, command=parent.caller.addNewItem)
		self.editMv = ttk.Button(self, text="Edit Selection", command=parent.caller.editItem)
		self.pkRand.grid(column=0, row=0, padx=15)
		self.addNM.grid(column=1, row=0, padx=15)
		self.editMv.grid(column=2, row=0, padx=15)

#Defines title display for Main page, including item count, scroll bar and show detail button
class TitlesFrame(ttk.Frame):
#make sure all TitlesFrames are explicitly provided title list
	def __init__(self, parent, mvL):
		super().__init__(parent)
		self.columnconfigure(0, weight=5)
		self.columnconfigure(1, weight=1)
		self.rowconfigure(0, weight=5)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.showinfobtn = ttk.Button(self, text="Show Info")
		self.countvar = StringVar()
		self.countlab = ttk.Label(self, textvariable=self.countvar)
		self.titlelistvar = StringVar()
		self.titlelistbox = Listbox(self, font=('gothic', 12), height=10, listvariable=self.titlelistvar, exportselection=0)
		self.mvL = mvL
		self.popTitles()
		self.scrolltitles = ttk.Scrollbar(self, orient=VERTICAL, command=self.titlelistbox.yview)
		self.titlelistbox.configure(yscrollcommand=self.scrolltitles.set)
		self.titlelistbox.grid(column=0, row=0, sticky=N+W+S+E)
		self.scrolltitles.grid(column=1, row=0, sticky=N+S)
		self.countlab.grid(column=0, row=1, columnspan=2, sticky=W+E)
		self.showinfobtn.grid(column=0, row=2, columnspan=2)
        
	def popTitles(self,tL=None):
		if tL != None:
			self.mvL = tL
		mvStr = makeTclList(self.mvL)
		self.titlelistvar.set(mvStr) 
		countstring = " results displayed"
		countint = str(len(self.mvL))
		countstring = countint + countstring
		self.countvar.set(countstring)
            
	def getSelected(self):
		if len(self.mvL) == 0:
			return None
		titleind = self.titlelistbox.curselection()
		#print(titleind[0])
		title = self.titlelistbox.get(titleind[0])
		return title

#Defines show detail pop-up
class InfoFrame(ttk.Frame):
	def __init__(self,parent,boss,stylechc=None):
		super().__init__(parent, style=stylechc)
		self.caller = boss
		self.mediatype = boss.MEDIATYPE
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=3)
		#guaranteed 5 rows: blank, format, genre, watched/fave, ack button
		self.rows = 5
		self.formatlab = ttk.Label(self, text="Formats Available:", style='InfoFrame.TLabel')
		self.formatlistvar = StringVar()
		self.formatinfo = Listbox(self, bg='#bdf4ef', state=DISABLED, relief=FLAT, font=('gothic', 12), listvariable=self.formatlistvar, exportselection=0)
		self.genrelab = ttk.Label(self, text="Genres:", style='InfoFrame.TLabel')
		self.genrelistvar = StringVar()
		self.genreinfo = Listbox(self, bg='#bdf4ef', state=DISABLED, relief=FLAT, font=('gothic', 12), listvariable=self.genrelistvar, exportselection=0)
		self.ackbut = ttk.Button(self, text="Good to know", command=parent.destroy, style='InfoFrame.TButton')
		self.favvar = StringVar()
		self.favLab = ttk.Label(self, textvariable=self.favvar, style='InfoFrame.TLabel')
		self.unwvar = StringVar()
		self.unwLab = ttk.Label(self, textvariable=self.unwvar, style='InfoFrame.TLabel')

		#media-type display decisions
		self.showseries = False
		if not self.caller.isMusic():
			self.showseries = True
			self.serieslab = ttk.Label(self, text="In Series:", style='InfoFrame.TLabel')
			self.seriesvar = StringVar()
			self.seriesinfo = ttk.Label(self, textvariable=self.seriesvar, style='InfoFrame.TLabel')
			self.rows += 1
		self.showauthor = False
		if not self.caller.isMovie():
			self.showauthor = True
			self.authorlab = ttk.Label(self, text="By:", style='InfoFrame.TLabel')
			self.authorvar = StringVar()
			self.authorinfo = ttk.Label(self, textvariable=self.authorvar, style='InfoFrame.TLabel')
			self.rows += 1

		for i in range(0,self.rows):
			self.rowconfigure(i, weight=1)
		self.placeItems()
    
	def placeItems(self):
		self.genrelab.grid(column=0, row=1)
		self.genreinfo.grid(column=1, row=1)
		i = 2
		if self.showseries:
			self.serieslab.grid(column=0, row=i)
			self.seriesinfo.grid(column=1, row=i)
			i += 1
		if self.showauthor:
			self.authorlab.grid(column=0, row=i)
			self.authorinfo.grid(column=1, row=i)
			i += 1
		self.formatlab.grid(column=0, row=i)
		self.formatinfo.grid(column=1, row=i)
		i += 1
		self.favLab.grid(column=0, row=i)
		self.unwLab.grid(column=1, row=i)
		i += 1
		self.ackbut.grid(column=0, row=i, columnspan=2)
               
	def popGenre(self, gList):
		self.genreinfo.configure(height=len(gList))
		gnStr = makeTclList(gList)
		self.genrelistvar.set(gnStr)

	def popSeries(self, series):
		if self.showseries:
        		self.seriesvar.set(series)

	def popAuthor(self, author):
		if self.showauthor:
			self.authorvar.set(author)
        
	def popFormat(self, fList):
		self.formatinfo.configure(height=len(fList))
		fmtStr = makeTclList(fList)
		self.formatlistvar.set(fmtStr)
        
	def dispFave(self):
		self.favvar.set("This is a favorite!")
    
	def dispUnwatch(self):
		self.unwvar.set(displayUnused[self.mediatype])

#Not used in pages yet
class AuthorFrame(ttk.Frame):
	def __init__(self, parent, change=False):
		super().__init__(parent)
		self.parent = parent
		self.deity = parent.caller
		self.conn = self.deity.passConnection()
		self.cur = self.deity.passCursor()
		self.Authors = self.deity.getAuthors()
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=3)
		self.rowconfigure(0, weight=1)
		self.authlab = ttk.Label(self, text="Author:")
		self.authbox = ttk.Combobox(self, values=self.Authors)
		self.authbox.state(['readonly'])
		self.authlab.grid(column=0, row=0, pady=5)
		self.authbox.grid(column=1, row=0, pady=5, sticky=W+E)
		if change:
			self.rowconfigure(1, weight=1)
			self.addauthbutton = ttk.Button(self, text="+Author", command=self.addAuthor)
			self.addauthvar = StringVar()
			self.addauthbox = ttk.Entry(self, textvariable=self.addauthvar)
			self.addauthbutton.grid(column=0, row=1, pady=5)
			self.addauthbox.grid(column=1, row=1, pady=5, sticky=W+E)
        
	def addAuthor(self):
		newAuthor = self.addauthbox.get()
		self.addauthvar.set("")
		newAuthor = newAuthor.strip()
		if newAuthor == "":
			errMsg = "If you want to add an author, please provide a name ;)"
			messagebox.showerror(message=errMsg)
			return
		self.cur.execute("SELECT a_id FROM Authors WHERE name=?", (newAuthor,))
		self.conn.commit()
		if self.cur.fetchone() != None:
			return    
		self.cur.execute("INSERT INTO Authors(name) Values(?)", (newAuthor,))
		self.conn.commit()
		self.cur.execute("SELECT a_id FROM Authors WHERE name=?", (newAuthor,))
		self.conn.commit()
		aID = self.cur.fetchone()[0]
		self.deity.authorDict[newAuthor] = aID
		#print(newAuthor)
		self.deity.updateAuthorList()
		self.Authors = self.deity.getAuthors()
		self.authbox.configure(values=self.Authors)

#Controls Main page
class App(ttk.Frame):
    
	def __init__(self,boss,master=None):
		super().__init__(master, padding=5)
		self.caller = boss
		self.localTitleList = boss.getTitles()
		self.cur = boss.passCursor()
		self.conn = boss.passConnection()
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=2)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(4, weight=1)
		self.rowconfigure(5, weight=1)
		self.grid(column=0, row=0, sticky=N+W+S+E)
		self.makeMainSubFrames()
		self.genreframe.g1box.bind("<<ComboboxSelected>>", self.updateTitleList)
		self.genreframe.g2box.bind("<<ComboboxSelected>>", self.updateTitleList)
		self.genreframe.g3box.bind("<<ComboboxSelected>>", self.updateTitleList)
		self.srsframe.srsbox.bind("<<ComboboxSelected>>", self.updateTitleList)
		self.frmtframe.frmtbox.bind("<<ListboxSelect>>", self.updateTitleList)
		self.tlistframe.titlelistbox.bind("<<ListboxSelect>>", self.titleAction)
		self.chkbxframe.unwbox.configure(command=self.updateTitleList)
		self.chkbxframe.favbox.configure(command=self.updateTitleList)
		self.tlistframe.showinfobtn.configure(command=self.titleDisplay)
		self.keysrchframe.keyword.trace("w", self.runUpdate)

	def storeAppInfo(self):
		storedInfo = {}
		storedInfo['genres'] = [self.genreframe.g1box.get(), self.genreframe.g2box.get(), self.genreframe.g3box.get()]
		fInds = self.frmtframe.frmtbox.curselection()
		storedInfo['formats'] = [ self.frmtframe.Formats[f] for f in fInds ]
		storedInfo['fave'] = self.chkbxframe.favvar.get() 
		storedInfo['unused'] = self.chkbxframe.unwvar.get()
		storedInfo['keyword'] = self.keysrchframe.kwdbox.get()
		if not self.caller.isMusic():
			storedInfo['series'] = self.srsframe.srsbox.get()
		if not self.caller.isMovie():
			storedInfo['author'] = self.authframe.authbox.get()
		return storedInfo


	def restoreApp(self, storedInfo):
		self.genreframe.g1box.set(storedInfo['genres'][0])
		self.genreframe.g2box.set(storedInfo['genres'][1])
		self.genreframe.g3box.set(storedInfo['genres'][2])
		for fName in storedInfo['formats']:
			ind = getInd(self.frmtframe.Formats, fName)
			if ind == None:
				pass
			self.frmtframe.frmtbox.selection_set(ind)
		self.chkbxframe.favvar.set(storedInfo['fave'])
		self.chkbxframe.unwvar.set(storedInfo['unused'])
		self.keysrchframe.keyword.set(storedInfo['keyword'])
		if not self.caller.isMusic():
			self.srsframe.srsbox.set(storedInfo['series'])
		if not self.caller.isMovie():
			self.authframe.authbox.set(storedInfo['author'])
		self.updateTitleList()

        
	def makeMainSubFrames(self):
		self.genreframe = GenreFrame(self)
		self.genreframe.grid(column=0, row=0, sticky=N+W+S+E)
		i = 1

		if not self.caller.isMusic():
			self.srsframe = SeriesFrame(self)
			self.srsframe.grid(column=0, row=i, sticky=N+W+S+E)
			i += 1
		if not self.caller.isMovie():
			self.authframe = AuthorFrame(self)
			self.authframe.grid(column=0, row=i, sticky=N+W+S+E)
			i += 1

		self.chkbxframe = CheckbuttonFrame(self)
		self.chkbxframe.grid(column=0, row=i, sticky=N+W+S+E)
		i += 1        
		self.frmtframe = FormatFrame(self)
		self.frmtframe.grid(column=0, row=i, sticky=N+W+S+E)    
		i += 1    
		self.keysrchframe = KeywordFrame(self)
		self.keysrchframe.grid(column=0, row=i, sticky=N+W+S+E)
		i += 1        
		self.buttonframe = ButtonFrame(self)
		self.buttonframe.editMv.state(["disabled"])
		self.buttonframe.grid(column=0, row=i, columnspan=2, sticky=N+W+S+E)  
      
		self.tlistframe = TitlesFrame(self, self.localTitleList)
		self.tlistframe.showinfobtn.state(["disabled"])
		self.tlistframe.grid(column=1, row=0, rowspan=i, sticky=N+W+S+E)   
        
	#if no title selected, edit and show info buttons can't be used
	def titleAction(self, event=None):
		title = self.tlistframe.getSelected()
		if title != "":
			self.buttonframe.editMv.state(["!disabled"])
			self.tlistframe.showinfobtn.state(["!disabled"])
		else:
			self.buttonframe.editMv.state(["disabled"])
			self.tlistframe.showinfobtn.state(["disabled"])        

	def titleDisplay(self):
		title = self.tlistframe.getSelected()
		if title != "":
			self.displayInfo(title)

	#making tkinter interface happy by redirecting through a 4-arg method
	def runUpdate(self, blah1, blah2, blah3):
		self.updateTitleList()
        
	#show details in popup for selected title
	def displayInfo(self, title):
		infoDisp = Toplevel(self)
		infoDisp.title(title)
		infoDisp.minsize(50,50)
		infofrm = InfoFrame(infoDisp, self.caller, stylechc='InfoFrame.TFrame')
		mID = self.caller.titleDict[title]
		self.cur.execute("SELECT genre_name FROM Genres JOIN Item_is_a ON g_id=fg_id WHERE fi_id=?", (mID,))
		self.conn.commit()
		genNameTuples = self.cur.fetchall()
		self.cur.execute("SELECT format_name FROM Formats JOIN Item_on_a ON f_id=ff_id WHERE fi_id=?", (mID,))
		self.conn.commit()
		fmtNameTuples = self.cur.fetchall()

		if not self.caller.isMusic():
			self.cur.execute("SELECT series_name FROM Series JOIN Items ON s_id=fs_id WHERE i_id=?", (mID,))
			self.conn.commit()
			srsRes = self.cur.fetchone()
			srsName = "This %s stands alone" % self.caller.MEDIATYPE
			if srsRes != None:
				srsName = srsRes[0]
			infofrm.popSeries(srsName)
		
		if not self.caller.isMovie():
			self.cur.execute("SELECT name FROM Authors JOIN Items ON a_id=fa_id WHERE i_id=?", (mID,))
			self.conn.commit()
			autRes = self.cur.fetchone()
			autName = "Anonymous"
			if autRes != None:
				autName = autRes[0]
			infofrm.popAuthor(autName)

		self.cur.execute("SELECT favorite, unused FROM Items WHERE i_id=?", (mID,))
		self.conn.commit()
		res = self.cur.fetchone()
		fave = 0
		unwatch = 0
		if res != None:
			fave = res[0]
			unwatch = res[1]
		gList = [ g[0] for g in genNameTuples ]
		fList = [ f[0] for f in fmtNameTuples ]
		infofrm.popGenre(gList)
		infofrm.popFormat(fList)
		if fave == 1:
			infofrm.dispFave()
		#print(fave)
		#print(type(fave))
		if unwatch == 1:
			infofrm.dispUnwatch()
		#print(unwatch)
		#print(type(unwatch))
		infoDisp.rowconfigure(0, weight=1)
		infoDisp.columnconfigure(0, weight=1)
		infofrm.grid(row=0, column=0, sticky=N+W+S+E)

	def updateTitleList(self, event=None):
		#get variable values
		g1 = self.genreframe.g1box.get()
		g2 = self.genreframe.g2box.get()
		g3 = self.genreframe.g3box.get()

		sID = 0
		if not self.caller.isMusic():
			series = self.srsframe.srsbox.get()
			if series != "":
				sID = self.caller.seriesDict[series]
		
		aID = 0
		if not self.caller.isMovie():
			author = self.authframe.authbox.get()
			if author != "":
				aID = self.caller.authorDict[author]

		formats = self.frmtframe.frmtbox.curselection()
		fave = self.chkbxframe.favvar.get()
		unwatch = self.chkbxframe.unwvar.get()
		kword = self.keysrchframe.kwdbox.get().strip()
		fIDs = []
		if len(formats) > 0:
			for f in formats:
				fIDs.append(self.caller.formatDict[self.frmtframe.Formats[f]])
		gIDs = []
		if g1 != "":
			gIDs.append(self.caller.genreDict[g1])
		if g2 != "":
			gIDs.append(self.caller.genreDict[g2])
		if g3 != "":
			gIDs.append(self.caller.genreDict[g3])

		searchString = "SELECT title FROM Items"
		substrJn = []
		substrWhr = []
		substrOr = []
		if len(gIDs) > 0:
			i = 0
			for g in gIDs:
				substr = " JOIN Item_is_a iia" + str(i) + " ON i_id = iia" + str(i) + ".fi_id"
				substrJn.append(substr)
				substr = " iia" + str(i) + ".fg_id=" + str(g)
				substrWhr.append(substr)
				i += 1
		if sID != 0:
			substr = " fs_id=" + str(sID)
			substrWhr.append(substr)
		if aID != 0:
			substr = " fa_id=" + str(aID)
			substrWhr.append(substr)
		if fave == 1:
			substr = " favorite=1"
			substrWhr.append(substr)
		if unwatch == 1:
			substr = " unused=1"
			substrWhr.append(substr)
		if kword != "":
			kwordAlt = kword.capitalize()
			substr = " ((title LIKE '%" + kword + "%') OR (title LIKE '%" + kwordAlt + "%'))"
			substrWhr.append(substr)
		if len(fIDs) > 0:
			i = 0
			for f in fIDs:
				substr = " JOIN Item_on_a ioa" + str(i) + " ON i_id = ioa" + str(i) + ".fi_id"
				substrJn.append(substr)
				substr = " (ioa" + str(i) + ".ff_id=" + str(f) + ")"
				substrOr.append(substr)
				i += 1
		for j in substrJn:
			searchString += j
		whereSize = len(substrWhr)
		whereLim = whereSize-1
		if whereSize > 0:
			for i in range(whereSize):
				if i == 0:
					searchString += " WHERE"
				searchString += substrWhr[i]
				if i != (whereLim):
					searchString += " AND"
		orSize = len(substrOr)
		orLim = orSize-1
		if orSize > 0:
			for q in range(orSize):
				if q == 0:
					searchString += " AND ("
				searchString += substrOr[q]
				if q != (orLim):
					searchString += " OR"
				else:
					searchString += ")"
		#print(searchString)
		self.cur.execute(searchString)
		self.conn.commit()
		results = self.cur.fetchall()
		if len(results) == 0:
			self.localTitleList = []
		else:
			tempList = [ m[0] for m in results ]
			self.localTitleList = gF.articleSort(tempList)
		self.buttonframe.editMv.state(["disabled"])
		print(self.localTitleList)
		self.tlistframe.popTitles(self.localTitleList)

	def pickRandomTitle(self):
		curTitleList = self.localTitleList
		if len(curTitleList) == 0:
			errMsg = "What do you expect me to pick from? Change options so there are some choices available"
			messagebox.showerror(message=errMsg)
			return
		picked = random.choice(curTitleList)
		self.displayInfo(picked)
    
#Title display for Add and Edit pages
#edit=False for Add page, True for Edit page
class AddTitleFrame(ttk.Frame):
	def __init__(self, parent, edit=False):
		super().__init__(parent)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.rowconfigure(0, weight=1)   
		self.tlab = ttk.Label(self, text="Title:")
		self.titlevar = StringVar()
		self.tbox = ttk.Entry(self, width=40, textvariable=self.titlevar)
		self.tlab.grid(column=0, row=0)
		self.tbox.grid(column=1, row=0, sticky=W+E)
		if edit:
			self.rowconfigure(1, weight=1)
			self.edbut = ttk.Button(self, text="Edit Title", command=self.editTitle)
			self.edbut.grid(column=0, row=1, columnspan=2)
            
	def editTitle(self):
		self.tbox.state(['!readonly'])

#Defines series display for Main and Add/Edit pages
#change=False for main page, True for Add/Edit
class SeriesFrame(ttk.Frame):
	def __init__(self, parent, change=False):
		super().__init__(parent)
		self.parent = parent
		self.deity = parent.caller
		self.conn = self.deity.passConnection()
		self.cur = self.deity.passCursor()
		self.Series = self.deity.getSeries()
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=3)
		self.rowconfigure(0, weight=1)
		self.srslab = ttk.Label(self, text="Series:")
		self.srsbox = ttk.Combobox(self, values=self.Series)
		self.srsbox.state(['readonly'])
		self.srslab.grid(column=0, row=0, pady=5)
		self.srsbox.grid(column=1, row=0, pady=5, sticky=W+E)
		if change:
			self.rowconfigure(1, weight=1)
			self.addsrsbutton = ttk.Button(self, text="+Series", command=self.addSeries)
			self.addsrsvar = StringVar()
			self.addsrsbox = ttk.Entry(self, textvariable=self.addsrsvar)
			self.addsrsbutton.grid(column=0, row=1, pady=5)
			self.addsrsbox.grid(column=1, row=1, pady=5, sticky=W+E)

	def addSeries(self):
		newSeries = self.addsrsbox.get()
		self.addsrsvar.set("")
		newSeries = newSeries.strip()
		if newSeries == "":
			errMsg = "If you want to add a series, it does need a name ;)"
			messagebox.showerror(message=errMsg)
			return
		self.cur.execute("SELECT s_id FROM Series WHERE series_name=?", (newSeries,))
		self.conn.commit()
		if self.cur.fetchone() != None:
			return    
		self.cur.execute("INSERT INTO Series(series_name) Values(?)", (newSeries,))
		#conn.commit()
		self.cur.execute("SELECT s_id FROM Series WHERE series_name=?", (newSeries,))
		self.conn.commit()
		sID = self.cur.fetchone()[0]
		self.deity.seriesDict[newSeries] = sID
		#print(newSeries)
		self.deity.updateSeriesList()
		self.Series = self.deity.getSeries()
		self.srsbox.configure(values=self.Series)

#This is the genre listing frame that is in use by Add/Edit pages
class GenreListFrame(ttk.Frame):
	def __init__(self, parent):
		super().__init__(parent)
		self.deity = parent.caller
		self.conn = self.deity.passConnection()
		self.cur = self.deity.passCursor()
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.gllab = ttk.Label(self, text="Select Genre(s):")
		self.genrelistvar = StringVar()
		self.genrelistbox = Listbox(self, font=('gothic', 12), height=7, selectmode="extended", listvariable=self.genrelistvar, exportselection=0)
		self.popGenres()
		self.scrollgenres = ttk.Scrollbar(self, orient=VERTICAL, command=self.genrelistbox.yview)
		self.genrelistbox.configure(yscrollcommand=self.scrollgenres.set)
		self.gllab.grid(column=0, row=0)
		self.genrelistbox.grid(column=1, row=0, sticky=N+W+S+E, rowspan=2)
		self.scrollgenres.grid(column=2, row=0, sticky=N+S, rowspan=2)
		self.ngnvar = StringVar()
		self.ngnbox = ttk.Entry(self, textvariable=self.ngnvar)
		self.addngnbutton = ttk.Button(self, text="+Genre", command=self.updateGenres)
		self.ngnbox.grid(column=1, row=2, pady=5, columnspan=2, sticky=W+E)
		self.addngnbutton.grid(column=0, row=2, pady=5)

	def updateGenres(self):
		newGenre = self.ngnbox.get().capitalize()
		self.ngnvar.set("")
		if len(newGenre.split()) > 1:
			glist = newGenre.strip().split()
			newGenre = ''
			for word in glist:
				word = word.capitalize()
				newGenre += word
				newGenre += " "
		newGenre.strip()
		self.cur.execute("SELECT g_id FROM Genres WHERE genre_name=?", (newGenre,))
		self.conn.commit()
		if self.cur.fetchone() != None:
			return    
		self.cur.execute("INSERT INTO Genres(genre_name) Values(?)", (newGenre,))
		self.cur.execute("SELECT g_id FROM Genres WHERE genre_name=?", (newGenre,))
		self.conn.commit()
		gID = self.cur.fetchone()
		self.deity.genreDict[newGenre] = gID
		#print(newGenre)
		self.deity.updateGenreList()
		self.popGenres()
        
	def popGenres(self):
		self.Genres = self.deity.getGenres()
		genStr = makeTclList(self.Genres)
		self.genrelistvar.set(genStr) 

#Controls Add page
class AddApp(ttk.Frame):
	def __init__(self,boss,master=None):
		super().__init__(master, padding=5)
		self.caller = boss
		self.cur = boss.passCursor()
		self.conn = boss.passConnection()
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(4, weight=1)
		self.rowconfigure(5, weight=1)
		self.grid(column=0, row=0, sticky=N+W+S+E)
		self.makeAddSubFrames()
        
	def makeAddSubFrames(self):
		self.adtlframe = AddTitleFrame(self)
		self.adtlframe.grid(column=0, row=0, columnspan=2, sticky=N+W+S+E)
		self.genreframe = GenreListFrame(self)
		self.genreframe.grid(column=0, row=1, rowspan=2, sticky=N+W+S+E)
		self.chkbxframe = CheckbuttonFrame(self, vertical=True)
		self.chkbxframe.grid(column=1, row=1, sticky=N+W+S+E)
		self.frmtframe = FormatFrame(self)
		self.frmtframe.grid(column=0, row=3, rowspan=2, sticky=N+W+S+E)
		if not self.caller.isMusic():
			self.srsframe = SeriesFrame(self, True)
			self.srsframe.grid(column=1, row=3, sticky=N+W+S+E)
		if not self.caller.isMovie():	
			self.authframe = AuthorFrame(self, True)
			self.authframe.grid(column=1, row=4, sticky=N+W+S+E)
		self.addbtn = ttk.Button(self, text="Update Database Now", command=self.updateDB)
		self.addbtn.grid(column=0, row=5)
		self.canclbtn = ttk.Button(self, text="Cancel", command=self.cancel)
		self.canclbtn.grid(column=1, row=5)
        
	def cancel(self):
#FIXME: Retain selection on main page
		print("calling to end addApp")
		self.caller.makeMainPage()
        
	def updateDB(self):
		medType = self.caller.MEDIATYPE
		Genres = self.caller.getGenres()
		title = self.adtlframe.tbox.get().strip()
		errmsg = "In order to update database, a %s MUST have: title, at least one genre, and at least one format" % medType	
		if title == "":
			messagebox.showerror(message=errmsg)
			return
		self.cur.execute("SELECT i_id FROM Items WHERE title=?", (title,))
		self.conn.commit()
		if self.cur.fetchone() != None:
			dupErrMsg = { "movie" : "This title is already in database.\nPlease add identifying information to title, for example Title(Year) or Director's Title", "book" : "This title is already in database. \nPlease add identifying information to title, for example Title(Published Year) or Special Edition Title", "music" : "This title is already in database. \nPlease add identifying information to title, for example Title(Remastered)"}
			messagebox.showerror(dupErrMsg[medType])
			return
		genindex = self.genreframe.genrelistbox.curselection()
		if len(genindex) == 0 or (len(genindex) == 1 and Genres[genindex[0]] == ""):
			messagebox.showerror(message=errmsg)
			return
		#FIXME: add messagebox.askyesnocancel + handler: yes: continue, no: return, cancel: __main__() 
		#may need to be tkMessagebox
		#doubleCheck = messagebox(type=tkMessageBox.YESNOCANCEL, default=tkMessageBox.NO, icon=tkMessageBox.QUESTION, message="Do you want to add this item?", parent=self)
		doubleCheck = messagebox.askyesnocancel(default=messagebox.NO, message="Do you want to add this item? \n If not, select 'No' to return to main menu \n or 'Cancel' to continue editing", parent=self)
		if doubleCheck == False:
			self.caller.makeMainPage()
		elif doubleCheck == None:
			return
		print(doubleCheck)
		print("Continuing to add info")
		fmtindex = self.frmtframe.frmtbox.curselection()
		if len(fmtindex) == 0:
			messagebox.showerror(message=errmsg)
			return
		gIDs = []
		for i in genindex:
			if Genres[i] != "":
				gIDs.append(self.caller.genreDict[Genres[i]])
		fIDs = []
		for f in fmtindex:
			fIDs.append(self.caller.formatDict[self.frmtframe.Formats[f]])
		fave = self.chkbxframe.favvar.get()
		unwatch = self.chkbxframe.unwvar.get()
		sID = 0
		if not self.caller.isMusic():
			sID = self.caller.seriesDict[self.srsframe.srsbox.get()]
			if self.caller.isMovie():
				self.cur.execute("INSERT INTO Items(title, favorite, unused, fs_id) Values(?, ?, ?, ?)", (title, fave, unwatch, sID))
				self.conn.commit()
		aID = 0
		if not self.caller.isMovie():
			aID = self.caller.authorDict[self.authframe.authbox.get()]
			if self.caller.isMusic():
				self.cur.execute("INSERT INTO Items(title, favorite, unused, fa_id) Values(?, ?, ?, ?)", (title, fave, unwatch, aID))
			else:
				self.cur.execute("INSERT INTO Items(title, favorite, unused, fa_id, fs_id) Values(?, ?, ?, ?, ?)", (title, fave, unwatch, aID, sID))
			self.conn.commit()
		self.cur.execute("SELECT i_id FROM Items WHERE title=?", (title,))
		self.conn.commit()
		m_id = self.cur.fetchone()[0]
		self.caller.titleDict[title] = m_id
		self.caller.updateTitleList()
		for gid in gIDs:
			self.cur.execute("INSERT INTO Item_is_a(fg_id, fi_id) Values(?, ?)", (gid, m_id))
			self.conn.commit()
		for fid in fIDs:
			self.cur.execute("INSERT INTO Item_on_a(ff_id, fi_id) Values(?, ?)", (fid, m_id))
			self.conn.commit()
		self.caller.makeMainPage()

#Controls Edit page
class EditApp(ttk.Frame):
	def __init__(self, boss,m_id,master=None):
		super().__init__(master, padding=5)
		self.caller = boss
		self.cur = boss.passCursor()
		self.conn = boss.passConnection()
		self.selectedMID = m_id
		self.selectedTitle = ""
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(4, weight=1)
		self.grid(column=0, row=0, sticky=N+W+S+E)
		self.makeEditSubFrames()

	def makeEditSubFrames(self):
		self.tlframe = AddTitleFrame(self, edit=True)
		self.setTitle()
		self.tlframe.grid(column=0, row=0, sticky=N+W+S+E, columnspan=2)
		self.genreframe = GenreListFrame(self)
		self.setGenres()
		self.genreframe.grid(column=0, row=1, rowspan=2, sticky=N+W+S+E)
		self.chkbxframe = CheckbuttonFrame(self, vertical=True)
		self.setCheckbuttons()
		self.chkbxframe.grid(column=1, row=1, sticky=N+W+S+E, columnspan=2)
		self.frmtframe = FormatFrame(self)
		self.setFormats()
		self.frmtframe.grid(column=0, row=3, rowspan=2, sticky=N+W+S+E)
		if not self.caller.isMusic():
			self.srsframe = SeriesFrame(self, True)
			self.setSeries()
			self.srsframe.grid(column=1, row=3, sticky=N+W+S+E)
		if not self.caller.isMovie():
			self.authframe = AuthorFrame(self, True)
			self.setAuthor()
			self.authframe.grid(column=1, row=4, sticky=N+W+S+E)
		self.addbtn = ttk.Button(self, text="Edit Stored Information Now", command=self.updateDB)
		self.addbtn.grid(column=0, row=5)
		self.canclbtn = ttk.Button(self, text="Cancel", command=self.cancel)
		self.canclbtn.grid(column=1, row=5)
        
	def cancel(self):
		self.caller.makeMainPage()        
        
	def setTitle(self):
		self.cur.execute("SELECT title FROM Items WHERE i_id=?", (self.selectedMID,))
		self.conn.commit()
		titleres = self.cur.fetchone()
		if titleres != None:
			title = titleres[0]
		else:
			return
		self.tlframe.titlevar.set(title)
		self.tlframe.tbox.state(['readonly'])
		self.selectedTitle = title
        
	def setGenres(self):
		Genres = self.caller.getGenres()
		self.cur.execute("SELECT genre_name FROM Genres JOIN Item_is_a ON g_id=fg_id WHERE fi_id=?", (self.selectedMID,))
		self.conn.commit()
		prevGenres = self.cur.fetchall()
		for info in prevGenres:
			ind = getInd(Genres, info[0])
			if ind == None:
				return
		self.genreframe.genrelistbox.selection_set(ind)
        
	def setCheckbuttons(self):
		self.cur.execute("SELECT favorite, unused FROM Items WHERE i_id=?", (self.selectedMID,))
		self.conn.commit()
		infores = self.cur.fetchone()
		if infores == None:
			return
		if infores[0] == 1:
			self.chkbxframe.favvar.set(1)
		if infores[1] == 1:
			self.chkbxframe.unwvar.set(1)
        
	def setFormats(self):
		self.cur.execute("SELECT format_name FROM Formats JOIN Item_on_a ON f_id=ff_id WHERE fi_id=?", (self.selectedMID,))
		self.conn.commit()
		Formats = self.caller.getFormats()
		prevFrmts = self.cur.fetchall()
		for info in prevFrmts:
			ind = getInd(Formats, info[0])
			if ind == None:
				return
			self.frmtframe.frmtbox.selection_set(ind)
        
	def setSeries(self):
		self.cur.execute("SELECT series_name FROM Series JOIN Items ON s_id=fs_id WHERE i_id=?", (self.selectedMID,))
		self.conn.commit()
		Series = self.caller.getSeries()
		srsRes = self.cur.fetchone()
		if srsRes != None:
			srsInd = getInd(Series, srsRes[0])
		else:
			return
		if srsInd == None:
			return
		self.srsframe.srsbox.current([srsInd])
        
	def setAuthor(self):
		self.cur.execute("SELECT name FROM Authors JOIN Items ON a_id=fa_id WHERE i_id=?", (self.selectedMID,))
		self.conn.commit()
		Authors = self.caller.getAuthors()
		autRes = self.cur.fetchone()
		if autRes != None:
			autInd = getInd(Authors, autRes[0])
		else:
			return
		if autInd == None:
			return
		self.authframe.authbox.current([autInd])
        
	def updateDB(self):
		medType = self.caller.MEDIATYPE
		errmsg = "In order to update database, a %s MUST have: title, at least one genre, and at least one format" % medType
		title = self.selectedTitle
		if self.tlframe.tbox.instate(['!readonly']):
			title = self.tlframe.tbox.get().strip()
			if title == self.selectedTitle:
				pass
			elif title == "":
				messagebox.showerror(message=errmsg)
				return
			else:
				self.cur.execute("SELECT i_id FROM Items WHERE title=?", (title,))
				self.conn.commit()
				result = self.cur.fetchone()
				if result != None and result[0] != self.selectedMID:
					dupErrMsg = { "movie" : "This title is already in database.\nPlease add identifying information to title, for example Title(Year) or Director's Title", "book" : "This title is already in database. \nPlease add identifying information to title, for example Title(Published Year) or Special Edition Title", "music" : "This title is already in database. \nPlease add identifying information to title, for example Title(Remastered)"}
					messagebox.showerror(dupErrMsg[medType])
					return
				del self.caller.titleDict[self.selectedTitle]
				self.selectedTitle = title
				self.caller.titleDict[title] = self.selectedMID
				self.caller.updateTitleList()
		genindex = self.genreframe.genrelistbox.curselection()
		Genres = self.caller.getGenres()
		Formats = self.caller.getFormats()
		if len(genindex) == 0 or (len(genindex) == 1 and Genres[genindex[0]] == ""):
			messagebox.showerror(message=errmsg)
			return
		fmtindex = self.frmtframe.frmtbox.curselection()
		if len(fmtindex) == 0:
			messagebox.showerror(message=errmsg)
			return
		self.cur.execute("SELECT fg_id FROM Item_is_a WHERE fi_id=?", (self.selectedMID,))
		self.conn.commit()
		gRes = self.cur.fetchall()
		oldgIDs = []
		for r in gRes:
			oldgIDs.append(r[0])
		self.cur.execute("SELECT ff_id FROM Item_on_a WHERE fi_id=?", (self.selectedMID,))
		self.conn.commit()
		fRes = self.cur.fetchall()
		oldfIDs = []
		for r in fRes:
			oldfIDs.append(r[0])
		newgIDs = []
		newfIDs = []
		for g in genindex:
			if Genres[g] != "":
				newgIDs.append(self.caller.genreDict[Genres[g]])
		for f in fmtindex:
			newfIDs.append(self.caller.formatDict[Formats[f]])
		for g in newgIDs:
			if g not in oldgIDs:
				self.cur.execute("INSERT INTO Item_is_a(fg_id, fi_id) Values(?, ?)", (g, self.selectedMID))
				self.conn.commit()
		for f in newfIDs:
			if f not in oldfIDs:
				self.cur.execute("INSERT INTO Item_on_a(ff_id, fi_id) Values(?, ?)", (f, self.selectedMID))
				self.conn.commit()
		for g in oldgIDs:
			if g not in newgIDs:
				self.cur.execute("DELETE FROM Item_is_a WHERE fg_id=? AND fi_id=?", (g, self.selectedMID))
				self.conn.commit()
		for f in oldfIDs:
			if f not in newfIDs:
				self.cur.execute("DELETE FROM Item_on_a WHERE ff_id=? AND fi_id=?", (f, self.selectedMID))
				self.conn.commit()
		sID = 0
		if not self.caller.isMusic():
			sID = self.caller.seriesDict[self.srsframe.srsbox.get()]
		aID = 0
		if not self.caller.isMovie():
			aID = self.caller.authorDict[self.authframe.authbox.get()]
		fave = self.chkbxframe.favvar.get()
		unwatch = self.chkbxframe.unwvar.get()

		if self.caller.isMovie():
			self.cur.execute("UPDATE Items SET title=?, favorite=?, unused=?, fs_id=? WHERE i_id=?", (title, fave, unwatch, sID, self.selectedMID))
		elif self.caller.isMusic():
			self.cur.execute("UPDATE Items SET title=?, favorite=?, unused=?, fa_id=? WHERE i_id=?", (title, fave, unwatch, aID, self.selectedMID))
		elif self.caller.isBook():
			self.cur.execute("UPDATE Items SET title=?, favorite=?, unused=?, fa_id=?, fs_id=? WHERE i_id=?", (title, fave, unwatch, aID, sID, self.selectedMID))
		self.conn.commit()
		self.caller.makeMainPage()       








