import sqlite3

connection = sqlite3.connect('database.db') # db file

with open ('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First Post', 'First Post Content')
)

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Second Post Content')
)

connection.commit()
connection.close()