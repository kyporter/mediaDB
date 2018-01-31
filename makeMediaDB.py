import sqlite3 as s3

mvGenres = ['Horror', 'Drama', 'Action', 'Comedy']
bkGenres = ['Fiction', 'Non-Fiction']
mcGenres = ['Pop', 'Classic', 'Rock', 'Rap']

Class MediaDB:

	def __init__(self, connectionName='testmoviedb.db', mediaType='movie'):
		self.mType = mediaType
		#start connection
		self.conn = s3.connect(connectionName)
		#create cursor
		self.c = self.conn.cursor()

	def makeTables(self):
		#create tables:
		#Series
		c.execute("CREATE TABLE Series(s_id INTEGER PRIMARY KEY, series_name text UNIQUE)")
		conn.commit()

		#Movies
		c.execute("CREATE TABLE Movies(m_id INTEGER PRIMARY KEY, title text, favorite integer DEFAULT 0, unwatched integer, fs_id integer DEFAULT 0, FOREIGN KEY(fs_id) REFERENCES Series(s_id))")
		conn.commit()

		#Genres
		c.execute("CREATE TABLE Genres(g_id INTEGER PRIMARY KEY, genre_name text UNIQUE)")
		conn.commit()

		#Movie_is_a
		c.execute("CREATE TABLE Movie_is_a(fm_id integer, fg_id integer, FOREIGN KEY(fm_id) REFERENCES Movies(m_id), FOREIGN KEY(fg_id) REFERENCES Genres(g_id))")
		conn.commit()

		#Formats
		c.execute("CREATE TABLE Formats(f_id INTEGER PRIMARY KEY, format_name text UNIQUE)")
		conn.commit()

		#Movie_on_a
		c.execute("CREATE TABLE Movie_on_a(fm_id integer, ff_id integer, FOREIGN KEY(fm_id) REFERENCES Movies(m_id), FOREIGN KEY(ff_id) REFERENCES Formats(f_id))")
		conn.commit()

#prepop genres
genreList = [('Horror',), ('Comedy',), ('Action',), ('Drama',), ('Science Fiction',), ('Animated',)]
c.executemany("INSERT INTO Genres(genre_name) Values (?)", genreList)
conn.commit()

#prepop formats
formatList = [('4K',), ('DVD',), ('VHS',)]
c.executemany("INSERT INTO Formats(format_name) Values (?)", formatList)
conn.commit()

conn.close()
