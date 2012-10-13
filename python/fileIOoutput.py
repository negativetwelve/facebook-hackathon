""" This is just here to test SQL output """

import sqlite3

if __name__ == '__main__':
    conn = sqlite3.connect("../db/development.sqlite3")
    c = conn.cursor()

    t = ('Miss',)
    c.execute('SELECT * FROM events WHERE event_type=?', t)
    everything = c.fetchall()
    for line in everything:
        print line
    c.close()
