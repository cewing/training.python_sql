Using Python's ``sqlite3`` Module
=================================

.. class:: center

**A walk through the Standard Library's reference implementation of DB API 2**

Assumptions
-----------

I assume that you have a Python interpreter on your own machines. I'll used
Python 2.7 in my examples, but they will work equally well in 2.6 and almost
as well in 2.5 or earlier.

.. class:: incremental

I am also assuming that you will be following along. You learn best by doing,
so *do*.

.. class:: incremental

A reminder that the resources I'll be referencing are available in the
``examples`` directory of this repository:

.. class:: small incremental

::

    $ git clone git://github.com/cewing/training.python_sql.git

Getting Started
---------------

Start by moving to the ``examples`` folder, opening a Python interpreter and
importing the sqlite3 module:

.. class:: small incremental

(create an examples folder if you don't have the repo cloned)

.. class:: incremental 

::

    $ cd examples
    $ python2.7
    Python 2.7.1 (r271:86832, Apr  4 2011, 22:22:40)
    [GCC 4.2.1 (Apple Inc. build 5664)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import sqlite3

Learning About the Module
-------------------------

.. class:: small

We can poke the module a bit to learn about it:

.. code-block:: python
    :class: incremental small

    >>> sqlite3.sqlite_version
    '3.6.12'
    >>> sqlite3.apilevel
    '2.0'
    >>> sqlite3.paramstyle
    'qmark'
    >>> sqlite3.threadsafety
    1

.. container:: incremental small

    ===== =====================================
    level meaning
    ===== =====================================
    0     Not safe
    1     Safe at Module level only
    2     Safe at Module and Connection
    3     Safe at Module, Connection and Cursor
    ===== =====================================

Connecting
----------

SQLite3 is a file-based system, and it will create the file it needs if one
doesn't exist. We can create a sqlite3 database just by attempting to connect
to it:

.. code-block:: python
    :class: small incremental

    >>> import createdb
    Need to create database and schema
    >>> reload(createdb)
    Database exists, assume schema does, too.
    <module 'createdb' from 'createdb.pyc'>

.. class:: incremental

Let's see how this works

``createdb.py``
---------------

Open ``createdb.py`` in your favorite text editor:

.. code-block:: python
    :class: small incremental

    import os
    import sqlite3

    DB_FILENAME = 'books.db'
    DB_IS_NEW = not os.path.exists(DB_FILENAME)
    conn =  sqlite3.connect(DB_FILENAME)

    if DB_IS_NEW:
        print 'Need to create schema'
    else:
        print 'Database exists, assume schema does, too.'

    conn.close()

Set Up The Schema
-----------------

Make the following changes to ``createdb.py``:

.. code-block:: python
    :class: small

    DB_FILENAME = 'books.db'
    SCHEMA_FILENAME = 'ddl.sql' # <- this is new
    DB_IS_NEW = not os.path.exists(DB_FILENAME)

    with sqlite3.connect(DB_FILENAME) as conn: # <- context mgr (2.6+)
        if DB_IS_NEW: # A whole new if clause:
            print 'Creating schema'
            with open(SCHEMA_FILENAME, 'rt') as f:
                schema = f.read()
            conn.executescript(schema)
        else:
            print 'Database exists, assume schema does, too.'
    
    # delete the `conn.close()` that was here.

Verify Your Work
----------------

Quit your python interpreter and delete the file ``books.db`` that should be
in the ``examples`` folder

.. container:: incremental

    Then restart your interpreter and try it out

    .. code-block:: python
        :class: small

        >>> import createdb
        Creating schema
        >>> reload(createdb)
        Database exists, assume schema does, too.
        <module 'createdb' from 'createdb.pyc'>

Introspect the Database
-----------------------

Add the following to ``createdb.py``:

.. code-block:: python
    :class: small

    # in the imports, add this line:
    from utils import show_table_metadata

    else:
        # in the else clause, replace the print statement with this:
        tablenames = ['author', 'book']
        cursor = conn.cursor()
        for name in tablenames:
            show_table_metadata(cursor, name)

.. class: incremental

Quit your interpreter again, then restart it and again ``import createdb``

My Results
----------

.. code-block:: python
    :class: small

    >>> import createdb
    Table Metadata for 'author':
    cid        | name       | type       | notnull    | dflt_value | pk         |
    -----------+------------+------------+------------+------------+------------+-
    0          | authorid   | INTEGER    | 1          | None       | 1          |
    -----------+------------+------------+------------+------------+------------+-
    1          | name       | TEXT       | 0          | None       | 0          |
    -----------+------------+------------+------------+------------+------------+-


    Table Metadata for 'book':
    cid        | name       | type       | notnull    | dflt_value | pk         |
    -----------+------------+------------+------------+------------+------------+-
    0          | bookid     | INTEGER    | 1          | None       | 1          |
    -----------+------------+------------+------------+------------+------------+-
    1          | title      | TEXT       | 0          | None       | 0          |
    -----------+------------+------------+------------+------------+------------+-
    2          | author     | INTEGER    | 1          | None       | 0          |
    -----------+------------+------------+------------+------------+------------+-

Inserting Data
--------------


We'll come back to the utility method. First, let's load up some data. In your
interpreter, type:

.. code-block:: python
    :class: small
    
    >>> import sqlite3
    >>> insert = """
    ... INSERT INTO author (name) VALUES("Iain M. Banks");"""
    >>> with sqlite3.connect("books.db") as conn:
    ...     cur = conn.cursor()
    ...     cur.execute(insert)
    ...     cur.rowcount
    ...     cur.close()
    ...     
    <sqlite3.Cursor object at 0x10046e880>
    1
    >>> 

.. class:: incremental

Did that work?

Querying Data
-------------

Let's query our database to find out:

.. code-block:: python
    :class: small

    >>> query = """
    ... SELECT * from author;"""
    >>> with sqlite3.connect("books.db") as conn:
    ...     cur = conn.cursor()
    ...     cur.execute(query)
    ...     rows = cur.fetchall()
    ...     for row in rows:
    ...         print row
    ...
    <sqlite3.Cursor object at 0x10046e8f0>
    (1, u'Iain M. Banks')

.. class:: incremental

Alright!  We've got a bit of data in there.  Let's make it more efficient

Parameterized Statements
------------------------

Try this:

.. code-block:: python
    :class: small

    >>> insert = """
    ... INSERT INTO author (name) VALUES(?);"""
    >>> authors = [["China Mieville"], ["Frank Herbert"],
    ... ["J.R.R. Tolkien"], ["Susan Cooper"], ["Madeline L'Engle"]]
    >>> with sqlite3.connect("books.db") as conn:
    ...     cur = conn.cursor()
    ...     cur.executemany(insert, authors)
    ...     print cur.rowcount
    ...     cur.close()
    ...
    <sqlite3.Cursor object at 0x10046e8f0>
    5

Check Your Work
---------------

Again, query the database:

.. code-block:: python
    :class: small

    >>> query = """
    ... SELECT * from author;"""
    >>> with sqlite3.connect("books.db") as conn:
    ...     cur = conn.cursor()
    ...     cur.execute(query)
    ...     rows = cur.fetchall()
    ...     for row in rows:
    ...         print row
    ...
    <sqlite3.Cursor object at 0x10046e8f0>
    (1, u'Iain M. Banks')
    ...
    (4, u'J.R.R. Tolkien')
    (5, u'Susan Cooper')
    (6, u"Madeline L'Engle")

Transactions
------------

Transactions allow you to group a number of operations together, testing to
make sure they worked *before* pushing the results into the database

.. class:: incremental

In SQLite3, transactions require an explicit ``commit`` if the operation belongs
to the Data Manipulation subset (``INSERT``, ``UPDATE``, ``DELETE``)

.. class:: incremental

So far, transactions have been hidden from us by the ``with`` statement.

.. class:: incremental

Let's see the effect of transactions more directly.

Populating the Database
-----------------------

Let's start by seeing what happens when you try to look for newly added data
before the ``insert`` transaction is committed.

.. class:: incremental

Begin by quitting your interpreter and deleting ``books.db``.  

.. class:: incremental

Then re-start your interpreter and re-create the database, empty:

.. code-block:: python
    :class: incremental small

    >>> import createdb
    Creating schema

Setting Up the Test
-------------------

.. class:: small

In ``populatedb.py``, add this code at the end of the file:

.. code-block:: python
    :class: small

    with sqlite3.connect(DB_FILENAME) as conn1:
        print "On conn1, before insert:"
        show_authors(conn1)
        
        authors = ([author] for author in AUTHORS_BOOKS.keys())
        cur = conn1.cursor()
        cur.executemany(author_insert, authors)
        print "On conn1, after insert:"
        show_authors(conn1)
        
        with sqlite3.connect(DB_FILENAME) as conn2:
            print "On conn2, before commit:"
            show_authors(conn2)
            
            conn1.commit()
            print "On conn2, after commit:"
            show_authors(conn2)

Running the Test
----------------

.. class:: small

Quit your python interpreter and run the ``populatedb.py`` script:

.. class:: small

::

    $ python2.7 populatedb.py
    On conn1, before insert:
    no rows returned
    On conn1, after insert:
    (1, u'China Mieville')
    (2, u'Frank Herbert')
    (3, u'Susan Cooper')
    (4, u'J.R.R. Tolkien')
    (5, u"Madeline L'Engle")
    On conn2, before commit:
    no rows returned
    On conn2, after commit:
    (1, u'China Mieville')
    (2, u'Frank Herbert')
    (3, u'Susan Cooper')
    (4, u'J.R.R. Tolkien')
    (5, u"Madeline L'Engle")

SNIPPETS
--------

1. Demo transaction rollback by adding a unicode character to Miéville's name
without fixing the string to be unicode.

show how this blows up, then fix it by rolling back the transaction explicitly

2. Demo subqueries by inserting authors, then inserting books using the author's
names to look up authorid and insert it

3. Talk about isolation levels and how to use them. (probably not enough time
to demo for real)

