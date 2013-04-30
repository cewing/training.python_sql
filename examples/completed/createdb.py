import os
import sqlite3
from utils import show_table_metadata


DB_FILENAME = 'books.db'
SCHEMA_FILENAME = 'ddl.sql' # <- this is new
DB_IS_NEW = not os.path.exists(DB_FILENAME)

with sqlite3.connect(DB_FILENAME) as conn: # <- context mgr
    if DB_IS_NEW: # A whole new if clause:
        print 'Creating schema'
        with open(SCHEMA_FILENAME, 'rt') as f:
            schema = f.read()
        conn.executescript(schema)
    else:
        tablenames = ['author', 'book']
        cursor = conn.cursor()
        for name in tablenames:
            show_table_metadata(cursor, name)