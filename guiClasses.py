from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from makeMediaDB import *
from guiFunctions import *
import random

def makeTclList(mvL):
    mvStr = ""
    mSize = len(mvL)
    mLim = mSize-1
    for i in range(mSize):
        mvStr += "{"
        mvStr += mvL[i]
        mvStr += "}"
        if i != mLim:
            mvStr += " "
    return mvStr

def getInd(Listname, item):
    i = 0
    while i < len(Listname):
        if Listname[i] == item:
            return i
        i += 1
    return None

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
        self.unwtlab = ttk.Label(self, text="Unwatched")
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

class FormatFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=5)
		self.Formats = parent.caller.getFormats()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=1)
        self.frmtlab = ttk.Label(self, text="Format(s):")
        self.frmtbox = Listbox(self, font=('gothic', 12), height=len(Formats), selectmode="extended", exportselection=0)
        self.popFormats()
        #self.scrollformats = ttk.Scrollbar(self, orient=VERTICAL, command=self.frmtbox.yview)
        #self.frmttbox.configure(yscrollcommand=self.scrollformats.set)
        self.frmtlab.grid(column=0, row=0)
        self.frmtbox.grid(column=1, row=0, sticky=N+W+S+E)
        #self.scrollformats.grid(column=2, row=0, sticky=N+S)
        
    def popFormats(self):
        for f in self.Formats:
            self.frmtbox.insert(END, f)

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

class ButtonFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=5)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.pkRand = ttk.Button(self, text="Random Choice", command=parent.caller.pickRandomTitle)
        self.addNM = ttk.Button(self, text="Add New Movie", command=parent.caller.addNewItem)
        self.editMv = ttk.Button(self, text="Edit Selection", command=parent.caller.editItem)
        self.pkRand.grid(column=0, row=0, padx=15)
        self.addNM.grid(column=1, row=0, padx=15)
        self.editMv.grid(column=2, row=0, padx=15)

class TitlesFrame(ttk.Frame):

#make sure all TitlesFrames are explicitly providing title list
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
        self.popTitles(mvL)
        self.scrolltitles = ttk.Scrollbar(self, orient=VERTICAL, command=self.titlelistbox.yview)
        self.titlelistbox.configure(yscrollcommand=self.scrolltitles.set)
        self.titlelistbox.grid(column=0, row=0, sticky=N+W+S+E)
        self.scrolltitles.grid(column=1, row=0, sticky=N+S)
        self.countlab.grid(column=0, row=1, columnspan=2, sticky=W+E)
        self.showinfobtn.grid(column=0, row=2, columnspan=2)
        
    def popTitles(self, mvL):
        mvStr = makeTclList(mvL)
        self.titlelistvar.set(mvStr) 
        countstring = " results displayed"
        countint = str(len(mvL))
        countstring = countint + countstring
        self.countvar.set(countstring)
            
    def getSelected(self):
        titleind = self.titlelistbox.curselection()
        #print(titleind[0])
        title = self.titlelistbox.get(titleind[0])
        return title

class InfoFrame(ttk.Frame):
    
    def __init__(self,parent,stylechc=None):
        super().__init__(parent, style=stylechc)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rows = 5
        self.formatlab = ttk.Label(self, text="Formats Available:", style='InfoFrame.TLabel')
        self.formatlistvar = StringVar()
        self.formatinfo = Listbox(self, bg='#bdf4ef', state=DISABLED, relief=FLAT, font=('gothic', 12), listvariable=self.formatlistvar, exportselection=0)
        self.genrelab = ttk.Label(self, text="Genres:", style='InfoFrame.TLabel')
        self.genrelistvar = StringVar()
        self.genreinfo = Listbox(self, bg='#bdf4ef', state=DISABLED, relief=FLAT, font=('gothic', 12), listvariable=self.genrelistvar, exportselection=0)
		self.showseries = False
		if !parent.caller.isMusic():
			self.showseries = True
		    self.serieslab = ttk.Label(self, text="In Series:", style='InfoFrame.TLabel')
		    self.seriesvar = StringVar()
		    self.seriesinfo = ttk.Label(self, textvariable=self.seriesvar, style='InfoFrame.TLabel')
			self.rows += 1

		self.showauthor = False
		if !parent.caller.isMovie():
			self.showauthor = True
			self.authorlab = ttk.Label(self, text="By:", style='InfoFrame.TLabel')
			self.authorvar = StringVar()
			self.authorinfo = ttk.Label(self, textvariable=self.authorvar, style='InfoFrame.TLabel')
			self.rows += 1

        self.ackbut = ttk.Button(self, text="Good to know", command=parent.destroy, style='InfoFrame.TButton')
        self.favvar = StringVar()
        self.favLab = ttk.Label(self, textvariable=self.favvar, style='InfoFrame.TLabel')
        self.unwvar = StringVar()
        self.unwLab = ttk.Label(self, textvariable=self.unwvar, style='InfoFrame.TLabel')
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
			i++
		if self.showauthor:
			self.authorlab.grid(column=0, row=i)
			self.authorinfo.grid(column=1, row=i)
			i++
        self.formatlab.grid(column=0, row=i)
        self.formatinfo.grid(column=1, row=i)
		i++
        self.favLab.grid(column=0, row=i)
        self.unwLab.grid(column=1, row=i)
		i++
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
        self.unwvar.set("This movie hasn't been watched yet!")

class AuthorFrame(ttk.frame):
    def __init__(self, parent, change=False):
        super().__init__(parent)
		self.deity = parent
		self.Authors = parent.caller.getAuthors()
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
        self.deity.cur.execute("SELECT a_id FROM Authors WHERE name=?", (newAuthor,))
        self.deity.conn.commit()
        if self.deity.cur.fetchone() != None:
            return    
        self.deity.cur.execute("INSERT INTO Authors(name) Values(?)", (newAuthor,))
        self.deity.conn.commit()
        self.deity.cur.execute("SELECT a_id FROM Authors WHERE name=?", (newAuthor,))
        self.deity.conn.commit()
        aID = self.deity.cur.fetchone()[0]
        self.deity.authorDict[newAuthor] = aID
        #print(newAuthor)
#problematic: in parent's caller
        updateAuthorList()
        self.authbox.configure(values=self.Authors)


class App(ttk.Frame):
    
    def __init__(self,boss,master=None):
        super().__init__(master, padding=5)
		self.caller = boss
        self.localTitleList = boss.getTitles()
		self.titleDict = boss.getTitleDict()
		self.formatDict = boss.getFormatDict()
		self.genreDict = boss.getGenreDict()
		self.authorDict = boss.getAuthorDict()
		self.seriesDict = boss.getSeriesDict()
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
        
    def makeMainSubFrames(self):
        self.genreframe = GenreFrame(self)
        self.genreframe.grid(column=0, row=0, sticky=N+W+S+E)
        self.srsframe = SeriesFrame(self)
        self.srsframe.grid(column=0, row=1, sticky=N+W+S+E)
        self.chkbxframe = CheckbuttonFrame(self)
        self.chkbxframe.grid(column=0, row=2, sticky=N+W+S+E)        
        self.frmtframe = FormatFrame(self)
        self.frmtframe.grid(column=0, row=3, sticky=N+W+S+E)        
        self.keysrchframe = KeywordFrame(self)
        self.keysrchframe.grid(column=0, row=4, sticky=N+W+S+E)        
        self.buttonframe = ButtonFrame(self)
        self.buttonframe.editMv.state(["disabled"])
        self.buttonframe.grid(column=0, row=5, columnspan=2, sticky=N+W+S+E)        
        self.tlistframe = TitlesFrame(self, self.localTitleList)
        self.tlistframe.showinfobtn.state(["disabled"])
        self.tlistframe.grid(column=1, row=0, rowspan=5, sticky=N+W+S+E)   
        
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
    
    def runUpdate(self, blah1, blah2, blah3):
        self.updateTitleList()
        
    def displayInfo(self, title):
        infoDisp = Toplevel(self)
        infoDisp.title(title)
        infoDisp.minsize(50,50)
        infofrm = InfoFrame(infoDisp, stylechc='InfoFrame.TFrame')
        mID = self.caller.getTitleDict()[title]
        self.cur.execute("SELECT genre_name FROM Genres JOIN Item_is_a ON g_id=fg_id WHERE fi_id=?", (mID,))
        self.conn.commit()
        genNameTuples = self.cur.fetchall()
        self.cur.execute("SELECT format_name FROM Formats JOIN Item_on_a ON f_id=ff_id WHERE fi_id=?", (mID,))
        self.conn.commit()
        fmtNameTuples = self.cur.fetchall()

		if !self.caller.isMusic():
		    self.cur.execute("SELECT series_name FROM Series JOIN Items ON s_id=fs_id WHERE i_id=?", (mID,))
		    self.conn.commit()
		    srsRes = self.cur.fetchone()
		    srsName = "This movie stands alone"
		    if srsRes != None:
		        srsName = srsRes[0]
        	infofrm.popSeries(srsName)
		
		if !self.caller.isMovie():
			self.cur.execute("SELECT name FROM Authors JOIN Items ON a_id=fa_id WHERE i_id=?", (mID,))
			self.conn.commit()
			autRes = self.cur.fetchone()
			autName = "Anonymous"
			if autRes != None:
				autName = autRes[0]
			infofrm.popAuthor(autName)

        self.cur.execute("SELECT favorite, unwatched FROM Items WHERE i_id=?", (mID,))
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
		if !self.caller.isMusic():
        	series = self.srsframe.srsbox.get()
		    if series != "":
		        sID = self.seriesDict[series]
		
		aID = 0
		if !self.caller.isMovie():
			author = self.authframe.authbox.get()
			if author != "":
				aID = self.authorDict[author]

        formats = self.frmtframe.frmtbox.curselection()
        fave = self.chkbxframe.favvar.get()
        unwatch = self.chkbxframe.unwvar.get()
        kword = self.keysrchframe.kwdbox.get().strip()
        fIDs = []
        if len(formats) > 0:
            for f in formats:
                fIDs.append(self.formatDict[self.frmtframe.Formats[f]])
        gIDs = []
        if g1 != "":
            gIDs.append(self.genreDict[g1])
        if g2 != "":
            gIDs.append(self.genreDict[g2])
        if g3 != "":
            gIDs.append(self.genreDict[g3])

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
            substr = " unwatched=1"
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
        print(searchString)
        c.execute(searchString)
        conn.commit()
        results = c.fetchall()
        if len(results) == 0:
            self.localTitleList = []
        else:
            tempList = [ m[0] for m in results ]
            self.localTitleList = articleSort(tempList)
        self.buttonframe.editMv.state(["disabled"])
        self.tlistframe.popTitles(self.localTitleList)
            

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

class AddGenreFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
		self.deity = parent
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)     

        self.ngnbox = ttk.Entry(self)
        self.addngnbutton = ttk.Button(self, text="+Genre", command=self.updateGenres)

        self.ngnbox.grid(column=1, row=0, pady=5, sticky=W+E)
        self.addngnbutton.grid(column=0, row=0, pady=5)
        
    def updateGenres(self):
        newGenre = self.ngnbox.get().capitalize()
        if len(newGenre.split()) > 1:
            glist = newGenre.strip().split()
            newGenre = ''
            for word in glist:
                word = word.capitalize()
                newGenre += word
                newGenre += " "
        newGenre.strip()
        self.deity.cur.execute("SELECT g_id FROM Genres WHERE genre_name=?", (newGenre,))
        self.deity.conn.commit()
        if self.deity.cur.fetchone() != None:
            return    
        self.deity.cur.execute("INSERT INTO Genres Value(?)", (newGenre,))
        self.deity.cur.execute("SELECT g_id FROM Genres WHERE genre_name=?", (newGenre,))
        self.deity.conn.commit()
        gID = self.deity.cur.fetchone()
        genreDict[newGenre] = gID
        #print(newGenre)
        updateGenreList()
        self.box.configure(values=Genres)

class SeriesFrame(ttk.Frame):
    def __init__(self, parent, change=False):
        super().__init__(parent)
		self.deity = parent
		self.Series = parent.caller.getSeries()
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
        self.deity.cur.execute("SELECT s_id FROM Series WHERE series_name=?", (newSeries,))
        self.deity.conn.commit()
        if self.deity.cur.fetchone() != None:
            return    
        self.deity.cur.execute("INSERT INTO Series(series_name) Values(?)", (newSeries,))
        #conn.commit()
        self.deity.cur.execute("SELECT s_id FROM Series WHERE series_name=?", (newSeries,))
        self.deity.conn.commit()
        sID = self.deity.cur.fetchone()[0]
        self.deity.seriesDict[newSeries] = sID
        #print(newSeries)
#problematic; method is in parent's caller
        updateSeriesList()
#new series isn't in self.Series
        self.srsbox.configure(values=self.Series)

class GenreListFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
		self.deity = parent
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
        self.deity.cur.execute("SELECT g_id FROM Genres WHERE genre_name=?", (newGenre,))
        self.deity.conn.commit()
        if self.deity.cur.fetchone() != None:
            return    
        self.deity.cur.execute("INSERT INTO Genres(genre_name) Values(?)", (newGenre,))
        self.deity.cur.execute("SELECT g_id FROM Genres WHERE genre_name=?", (newGenre,))
        self.deity.conn.commit()
        gID = self.deity.cur.fetchone()
        self.deity.genreDict[newGenre] = gID
        #print(newGenre)
#method is in parent's caller
        updateGenreList()
#local Genres isn't updates
        self.popGenres()
        
    def popGenres(self):
        genStr = makeTclList(self.Genres)
        self.genrelistvar.set(genStr) 

class AddApp(ttk.Frame):
    def __init__(self,boss,master=None):
        super().__init__(master, padding=5)
		self.caller = boss
		self.titleDict = boss.getTitleDict()
		self.formatDict = boss.getFormatDict()
		self.genreDict = boss.getGenreDict()
		self.authorDict = boss.getAuthorDict()
		self.seriesDict = boss.getSeriesDict()
		self.cur = boss.passCursor()
		self.conn = boss.passConnection()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
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
        self.frmtframe.grid(column=0, row=3, sticky=N+W+S+E)
        self.srsframe = SeriesFrame(self, True)
        self.srsframe.grid(column=1, row=3, sticky=N+W+S+E, columnspan=2)
        self.addbtn = ttk.Button(self, text="Update Database Now", command=self.updateDB)
        self.addbtn.grid(column=0, row=4)
        self.canclbtn = ttk.Button(self, text="Cancel", command=self.cancel)
        self.canclbtn.grid(column=1, row=4)
        
    def cancel(self):
        self.caller.makeMainPage()
        
    def updateDB(self):
        title = self.adtlframe.tbox.get().strip()
	#make media-neutral
        errmsg = "In order to update database, a movie MUST have: title, at least one genre, and at least one format"	
        if title == "":
            messagebox.showerror(message=errmsg)
            return
        self.cur.execute("SELECT i_id FROM Items WHERE title=?", (title,))
        self.conn.commit()
        if self.cur.fetchone() != None:
#make media-neutral
            dupErrMsg = "This title is already in database.\nPlease add identifying information to tile, for example Title(Year) or Director's Title"
            messagebox.showerror(dupErrMsg)
            return
        genindex = self.genreframe.genrelistbox.curselection()
        if len(genindex) == 0 or (len(genindex) == 1 and Genres[genindex[0]] == ""):
            messagebox.showerror(message=errmsg)
            return
    #messagebox.askyesnocancel + handler: yes: continue, no: return, cancel: __main__()
        fmtindex = self.frmtframe.frmtbox.curselection()
        if len(fmtindex) == 0:
            messagebox.showerror(message=errmsg)
            return
        gIDs = []
        for i in genindex:
            if Genres[i] != "":
#add dicts
                gIDs.append(self.genreDict[Genres[i]])
        fIDs = []
        for f in fmtindex:
            fIDs.append(self.formatDict[self.frmtframe.Formats[f]])
        fave = self.chkbxframe.favvar.get()
        unwatch = self.chkbxframe.unwvar.get()
		sID = 0
 		if !self.caller.isMusic():
        	sID = seriesDict[self.srsframe.srsbox.get()]
			if self.caller.isMovie():
        		self.cur.execute("INSERT INTO Items(title, favorite, unwatched, fs_id) Values(?, ?, ?, ?)", (title, fave, unwatch, sID))
        		self.conn.commit()
		if !self.caller.isMovie():
#add authframe to AddApp
			aID = authorDict[self.authframe.authbox.get()]
			if self.caller.isMusic():
				self.cur.execute("INSERT INTO Items(title, favorite, unwatched, fa_id) Values(?, ?, ?, ?)", (title, fave, unwatch, aID))
			else:
				self.cur.execute("INSERT INTO Items(title, favorite, unwatched, fa_id, fs_id) Values(?, ?, ?, ?, ?)", (title, fave, unwatch, aID, sID))
			self.conn.commit()
        self.cur.execute("SELECT i_id FROM Items WHERE title=?", (title,))
        self.conn.commit()
        m_id = self.cur.fetchone()[0]
        self.titleDict[title] = m_id
#parent's method, local dict
        updateTitleList()
        for gid in gIDs:
            c.execute("INSERT INTO Item_is_a(fg_id, fi_id) Values(?, ?)", (gid, m_id))
            conn.commit()
        for fid in fIDs:
            c.execute("INSERT INTO Item_on_a(ff_id, fi_id) Values(?, ?)", (fid, m_id))
            conn.commit()
        self.caller.makeMainPage()


class EditApp(ttk.Frame):
    def __init__(self, boss,m_id,master=None):
        super().__init__(master, padding=5)
		self.caller = boss
		self.titleDict = boss.getTitleDict()
		self.formatDict = boss.getFormatDict()
		self.genreDict = boss.getGenreDict()
		self.authorDict = boss.getAuthorDict()
		self.seriesDict = boss.getSeriesDict()
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
        self.makeAddSubFrames()

    def makeAddSubFrames(self):
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
        self.frmtframe.grid(column=0, row=3, sticky=N+W+S+E)
        self.srsframe = SeriesFrame(self, True)
        self.setSeries()
        self.srsframe.grid(column=1, row=3)
        self.addbtn = ttk.Button(self, text="Edit Stored Information Now", command=self.updateDB)
        self.addbtn.grid(column=0, row=4)
        self.canclbtn = ttk.Button(self, text="Cancel", command=self.cancel)
        self.canclbtn.grid(column=1, row=4)
        
    def cancel(self):
        __main__()        
        
    def setTitle(self):
        c.execute("SELECT title FROM Movies WHERE m_id=?", (self.selectedMID,))
        conn.commit()
        titleres = c.fetchone()
        if titleres != None:
            title = titleres[0]
        else:
            return
        self.tlframe.titlevar.set(title)
        self.tlframe.tbox.state(['readonly'])
        self.selectedTitle = title
        
    def setGenres(self):
        c.execute("SELECT genre_name FROM Genres JOIN Movie_is_a ON g_id=fg_id WHERE fm_id=?", (self.selectedMID,))
        conn.commit()
        prevGenres = c.fetchall()
        for info in prevGenres:
            ind = getInd(Genres, info[0])
            if ind == None:
                return
            self.genreframe.genrelistbox.selection_set(ind)
        
    def setCheckbuttons(self):
        c.execute("SELECT favorite, unwatched FROM Movies WHERE m_id=?", (self.selectedMID,))
        conn.commit()
        infores = c.fetchone()
        if infores == None:
            return
        if infores[0] == 1:
            self.chkbxframe.favvar.set(1)
        if infores[1] == 1:
            self.chkbxframe.unwvar.set(1)
        
    def setFormats(self):
        c.execute("SELECT format_name FROM Formats JOIN Movie_on_a ON f_id=ff_id WHERE fm_id=?", (self.selectedMID,))
        conn.commit()
        prevFrmts = c.fetchall()
        for info in prevFrmts:
            ind = getInd(Formats, info[0])
            if ind == None:
                return
            self.frmtframe.frmtbox.selection_set(ind)
        
    def setSeries(self):
        c.execute("SELECT series_name FROM Series JOIN Movies ON s_id=fs_id WHERE m_id=?", (self.selectedMID,))
        conn.commit()
        srsRes = c.fetchone()
        if srsRes != None:
            srsInd = getInd(Series, srsRes[0])
        else:
            return
        if srsInd == None:
            return
        self.srsframe.srsbox.current([srsInd])
        
    def updateDB(self):
        title = self.selectedTitle
        if self.tlframe.tbox.instate(['!readonly']):
            title = self.tlframe.tbox.get().strip()
            if title == "":
                errmsg = "In order to update database, a movie MUST have: title, at least one genre, and at least one format"
                messagebox.showerror(message=errmsg)
                return
            c.execute("SELECT m_id FROM Movies WHERE title=?", (title,))
            conn.commit()
            result = c.fetchone()
            if result != None and result[0] != self.selectedMID:
                errMsg = "This title is already in database. \nPlease add identifying information, for example Title(Year) or Director's Title"
                messagebox.showerror(errMsg)
                return
            del movieDict[self.selectedTitle]
            self.selectedTitle = title
            movieDict[title] = self.selectedMID
            updateMovieList()
        genindex = self.genreframe.genrelistbox.curselection()
        if len(genindex) == 0 or (len(genindex) == 1 and Genres[genindex[0]] == ""):
            errmsg = "In order to update database, a movie MUST have: title, at least one genre, and at least one format"
            messagebox.showerror(message=errmsg)
            return
        fmtindex = self.frmtframe.frmtbox.curselection()
        if len(fmtindex) == 0:
            errmsg = "In order to update database, a movie MUST have: title, at least one genre, and at least one format"
            messagebox.showerror(message=errmsg)
            return
        c.execute("SELECT fg_id FROM Movie_is_a WHERE fm_id=?", (self.selectedMID,))
        conn.commit()
        gRes = c.fetchall()
        oldgIDs = []
        for r in gRes:
            oldgIDs.append(r[0])
        c.execute("SELECT ff_id FROM Movie_on_a WHERE fm_id=?", (self.selectedMID,))
        conn.commit()
        fRes = c.fetchall()
        oldfIDs = []
        for r in fRes:
            oldfIDs.append(r[0])
        newgIDs = []
        newfIDs = []
        for g in genindex:
            if Genres[g] != "":
                newgIDs.append(genreDict[Genres[g]])
        for f in fmtindex:
            newfIDs.append(formatDict[Formats[f]])
        for g in newgIDs:
            if g not in oldgIDs:
                c.execute("INSERT INTO Movie_is_a(fg_id, fm_id) Values(?, ?)", (g, self.selectedMID))
                conn.commit()
        for f in newfIDs:
            if f not in oldfIDs:
                c.execute("INSERT INTO Movie_on_a(ff_id, fm_id) Values(?, ?)", (f, self.selectedMID))
                conn.commit()
        for g in oldgIDs:
            if g not in newgIDs:
                c.execute("DELETE FROM Movie_is_a WHERE fg_id=? AND fm_id=?", (g, self.selectedMID))
                conn.commit()
        for f in oldfIDs:
            if f not in newfIDs:
                c.execute("DELETE FROM Movie_on_a WHERE ff_id=? AND fm_id=?", (f, self.selectedMID))
                conn.commit()
        sID = seriesDict[self.srsframe.srsbox.get()]
        fave = self.chkbxframe.favvar.get()
        unwatch = self.chkbxframe.unwvar.get()
        c.execute("UPDATE Movies SET title=?, favorite=?, unwatched=?, fs_id=? WHERE m_id=?", (title, fave, unwatch, sID, self.selectedMID))
        conn.commit()
        __main__()        
