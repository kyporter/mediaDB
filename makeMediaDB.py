import sqlite3 as s3

genres = {'Movie': [('Horror',), ('Comedy',), ('Action',), ('Drama',), ('Science Fiction',), ('Animated',)], 'Written': [('Fiction',), ('Non-Fiction',)], 'Music': [('Pop',), ('Classical',), ('Rock',), ('Rap',)]}

formats = {'Movie': [('4K',), ('DVD',), ('VHS',)], 'Written': [('eBook',), ('Paperback',), ('Magazine',)], 'Music': [('mp4',), ('CD',), ('Record',)]}


Class MediaDB:

	def __init__(self, owner, connectionName='testmoviedb.db', mediaType='movie'):
		self.deity = owner
		self.mType = mediaType
		#start connection
		self.conn = s3.connect(connectionName)
		#create cursor
		self.c = self.conn.cursor()
		self.makeTables
		self.populateInfo
		self.conn.close()

	def makeTables(self):
		#create tables:	
		if self.mType != 'Music':
			#Series
			c.execute("CREATE TABLE Series(s_id INTEGER PRIMARY KEY, series_name text UNIQUE)")
			conn.commit()

		#Items
		c.execute("CREATE TABLE Items(i_id INTEGER PRIMARY KEY, title text, favorite integer DEFAULT 0, unused integer, fs_id integer DEFAULT 0, FOREIGN KEY(fs_id) REFERENCES Series(s_id))")
		conn.commit()

		if self.mType != 'Movie':
			c.execute("CREATE TABLE Authors(a_id INTEGER PRIMARY KEY, name text")
			c.execute("ALTER TABLE Items ADD COLUMN fa_id {integer} DEFAULT {0}, FOREIGN KEY(fa_id) REFERENECES Authors(a_id)")
			conn.commit()

		#Genres
		c.execute("CREATE TABLE Genres(g_id INTEGER PRIMARY KEY, genre_name text UNIQUE)")
		conn.commit()

		#Item_is_a
		c.execute("CREATE TABLE Item_is_a(fi_id integer, fg_id integer, FOREIGN KEY(fi_id) REFERENCES Items(i_id), FOREIGN KEY(fg_id) REFERENCES Genres(g_id))")
		conn.commit()

		#Formats
		c.execute("CREATE TABLE Formats(f_id INTEGER PRIMARY KEY, format_name text UNIQUE)")
		conn.commit()

		#Movie_on_a
		c.execute("CREATE TABLE Item_on_a(fi_id integer, ff_id integer, FOREIGN KEY(fi_id) REFERENCES Items(m_id), FOREIGN KEY(ff_id) REFERENCES Formats(f_id))")
		conn.commit()

	def populateInfo(self):

		#prepop genres
		genreList = genres[self.mType]
		c.executemany("INSERT INTO Genres(genre_name) Values (?)", genreList)
		conn.commit()

		#prepop formats
		formatList = formats[self.mType]
		c.executemany("INSERT INTO Formats(format_name) Values (?)", formatList)
		conn.commit()
