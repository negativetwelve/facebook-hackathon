import sqlite3

if __name__ == '__main__':
    conn = sqlite3.connect("testing.db")
    c = conn.cursor()

    t = ('<TAB>',)
    c.execute('SELECT * FROM info WHERE word=?', t)
    while True:
        test = c.fetchone()
        if test is None:
            break
        print test

    c.close()
