import os
import sqlite3

DB_FILENAME = 'books.db'
DB_IS_NEW = not os.path.exists(DB_FILENAME)
conn =  sqlite3.connect(DB_FILENAME)

if DB_IS_NEW:
    print 'Need to create database and schema'
else:
    print 'Database exists, assume schema does, too.'

conn.close()