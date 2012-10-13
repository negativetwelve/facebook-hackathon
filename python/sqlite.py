import sqlite3
db = sqlite3.connect('./../db/development.sqlite3')

for row in db.execute('SELECT * FROM events where word="c"'):
    print row