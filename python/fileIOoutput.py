""" This is just here to test SQL output """

import sqlite3

if __name__ == '__main__':
    conn = sqlite3.connect("../db/development.db")
    c = conn.cursor()

    t = ('<BACK>',)
    c.execute('SELECT * FROM info WHERE word=?', t)
    everything = c.fetchall()
    for line in everything:
        print line
    c.close()
