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
    >>> createdb.main()
    Need to create database and schema
    >>> reload(createdb)
    <module 'createdb' from 'createdb.pyc'>
    >>> createdb.main()
    Database exists, assume schema does, too.

.. class:: incremental

Let's see how this works

edit createdb.py
----------------

.. class:: small

Open ``createdb.py`` in your favorite text editor:

.. code-block:: python
    :class: small

    import os
    import sqlite3

    DB_FILENAME = 'books.db'
    DB_IS_NEW = not os.path.exists(DB_FILENAME)

    def main():
        conn =  sqlite3.connect(DB_FILENAME)
        if DB_IS_NEW:
            print 'Need to create database and schema'
        else:
            print 'Database exists, assume schema does, too.'
        conn.close()

    if __name__ == '__main__':
        main()

Set Up The Schema
-----------------

Make the following changes to ``createdb.py``:

.. code-block:: python
    :class: small

    DB_FILENAME = 'books.db'
    SCHEMA_FILENAME = 'ddl.sql' # <- this is new
    DB_IS_NEW = not os.path.exists(DB_FILENAME)

    def main():
        with sqlite3.connect(DB_FILENAME) as conn: # <- context mgr
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

    Then run the script from the command line to try it out::
    
        $ python2.7 createdb.py
        Creating schema
        $ python2.7 createdb.py
        Database exists, assume schema does, too.

Introspect the Database
-----------------------

Add the following to ``createdb.py``:

.. code-block:: python
    :class: small

    # in the imports, add this line:
    from utils import show_table_metadata

    else:
        # in the else clause, replace the print statement with this:
        print "Database exists, introspecting:"
        tablenames = ['author', 'book']
        cursor = conn.cursor()
        for name in tablenames:
            print "\n"
            show_table_metadata(cursor, name)

.. class: incremental

Then try running ``python2.7 createdb.py`` again

My Results
----------

.. class:: small

::

    $ python2.7 createdb.py
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


Let's load up some data. Fire up your interpreter and type:

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

Alright!  We've got data in there.  Let's make it more efficient

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

.. class:: small

Transactions let you group a number of operations together, allowing you to
make sure they worked *before* you actually push the results into the
database.

.. class:: incremental small

In SQLite3, operations that belong to the Data Manipulation subset
(``INSERT``, ``UPDATE``, ``DELETE``) require an explicit ``commit`` unless
auto-commit has been enabled.

.. class:: incremental small

So far, commits have been hidden from us by the ``with`` statement. The
context manager takes care of committing when the context closes (at the end 
of the ``with`` statement)

.. class:: incremental small

Let's add some code so we can see the effect of transactions.

Populating the Database
-----------------------

Let's start by seeing what happens when you try to look for newly added data
before the ``insert`` transaction is committed.

.. class:: incremental

Begin by quitting your interpreter and deleting ``books.db``.  

.. class:: incremental

Then re-create the database, empty::

    $ python2.7 createdb.py
    Creating schema

Setting Up the Test
-------------------

.. class:: small

In ``populatedb.py``, add this code at the end of the file:

.. code-block:: python
    :class: small

    with sqlite3.connect(DB_FILENAME) as conn1:
        print "\nOn conn1, before insert:"
        show_authors(conn1)
        
        authors = ([author] for author in AUTHORS_BOOKS.keys())
        cur = conn1.cursor()
        cur.executemany(author_insert, authors)
        print "\nOn conn1, after insert:"
        show_authors(conn1)
        
        with sqlite3.connect(DB_FILENAME) as conn2:
            print "\nOn conn2, before commit:"
            show_authors(conn2)
            
            conn1.commit()
            print "\nOn conn2, after commit:"
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

Rollback
--------

That's all well and good, but what happens if an error occurs?

.. class:: incremental

Transactions can be rolled back in order to wipe out partially completed work.

.. class:: incremental

Like with commit, using ``connect`` as a context manager in a ``with``
statement will automatically rollback for exceptions.

.. class:: incremental

Let's rewrite our populatedb script so it explicitly commits or rolls back a
transaction depending on exceptions occurring

edit populatedb.py (slide 1)
----------------------------

.. class:: small

First, add the following function above the ``if __name__ == '__main__'``
block:

.. code-block:: python
    :class: small
    
    def populate_db(conn):
        authors = ([author] for author in AUTHORS_BOOKS.keys())
        cur = conn.cursor()
        cur.executemany(author_insert, authors)
        
        for author in AUTHORS_BOOKS.keys():
            params = ([book, author] for book in AUTHORS_BOOKS[author])
            cur.executemany(book_insert, params)


edit populatedb.py (slide 2)
----------------------------

.. class:: small

Then, in the runner:

.. code-block:: python
    :class: small

    with sqlite3.connect(DB_FILENAME) as conn1:
        with sqlite3.connect(DB_FILENAME) as conn2:
            try:
                populate_db(conn1)
                print "\nauthors and books on conn2 before commit:"
                show_authors(conn2)
                show_books(conn2)
            except Exception:
                conn1.rollback()
                print "\nauthors and books on conn2 after rollback:"
                show_authors(conn2)
                show_books(conn2)
                raise
            else:
                conn1.commit()
                print "\nauthors and books on conn2 after commit:"
                show_authors(conn2)
                show_books(conn2)

Try it Out
----------

Remove ``books.db`` and recrete the database, then run our script:

.. class:: small

::

    $ rm books.db
    $ python2.7 createdb.py
    Creating schema
    $ python2.7 populatedb.py

.. class:: small incremental

::

    authors and books on conn2 after rollback:
    no rows returned
    no rows returned
    Traceback (most recent call last):
      File "populatedb.py", line 57, in <module>
        populate_db(conn1)
      File "populatedb.py", line 46, in populate_db
        cur.executemany(book_insert, params)
    sqlite3.InterfaceError: Error binding parameter 0 - probably unsupported type.

Oooops, Fix It
--------------

.. class:: small

Okay, we got an error, and the transaction was rolled back correctly.

.. container:: incremental small

    Open ``utils.py`` and find this:

    .. code-block:: python 

        'Susan Cooper': ["The Dark is Rising", ["The Greenwitch"]],

.. container:: incremental small

    Fix it like so:
    
    .. code-block:: python
    
        'Susan Cooper': ["The Dark is Rising", "The Greenwitch"],

.. class:: small incremental

It appears that we were attempting to bind a list as a parameter.  Ooops.

Try It Again
------------

.. container:: small

    Now that the error in our data is repaired, let's try again::

        $ python2.7 populatedb.py

.. class:: small incremental

::

    Reporting authors and books on conn2 before commit:
    no rows returned
    no rows returned
    Reporting authors and books on conn2 after commit:
    (1, u'China Mieville')
    (2, u'Frank Herbert')
    (3, u'Susan Cooper')
    (4, u'J.R.R. Tolkien')
    (5, u"Madeline L'Engle")
    (1, u'Perdido Street Station', 1)
    (2, u'The Scar', 1)
    (3, u'King Rat', 1)
    (4, u'Dune', 2)
    (5, u"Hellstrom's Hive", 2)
    (6, u'The Dark is Rising', 3)
    (7, u'The Greenwitch', 3)
    (8, u'The Hobbit', 4)
    (9, u'The Silmarillion', 4)
    (10, u'A Wrinkle in Time', 5)
    (11, u'A Swiftly Tilting Planet', 5)

Isolation
---------

So far, our transactions have been managed.  Either explicitly by us, or 
automatically by the context manager statement ``with``

.. class:: incremental

This behavior is the result of an aspect of the database connection called the
**isolation level**. There are three isolation levels available:  

.. class:: incremental small

* **DEFERRED** - Locks the database once changes have begun to be written to
  the filesystem.  Read-only operations are not blocked
* **IMMEDIATE** - Locks the database as soon as a transaction is begun.  
  Read-only operations are not blocked
* **EXCLUSIVE** - Locks the database as soon as a transaction is begun. This
  blocks any read-only operations as well

.. class:: incremental

The default level is **DEFERRED**

Autocommit
----------

The isolation level of a connection can be set with a keyword argument provided
to the ``connect`` constructor:

.. code-block:: python

    con = sqlite3.connect('mydb.db', isolation_level="EXCLUSIVE")

.. class:: incremental

If you explicitly set this argument to ``None``, you can enable *autocommit*
behavior.  

.. class:: incremental

If autocommit is enabled, then any DML operations that occur on a connection 
will be immediately committed

Testing Autocommit
------------------

.. container:: small

    First, edit ``populatedb.py``:

    .. code-block:: python

        with sqlite3.connect(DB_FILENAME,
                             isolation_level=None) as conn1:
            with sqlite3.connect(DB_FILENAME,
                                 isolation_level=None) as conn2:

.. class:: incremental small

Next, undo your changes to ``utils.py`` so that the error we had will happen
again

.. container:: incremental small

    Finally, delete books.db, recreate it and test the populate script::

        $ rm books.db
        $ python2.7 createdb.py
        Creating schema
        $ python2.7 populatedb.py

The Result
----------

.. class:: small

::

    authors and books on conn2 after rollback:
    (1, u'China Mieville')
    (2, u'Frank Herbert')
    (3, u'Susan Cooper')
    (4, u'J.R.R. Tolkien')
    (5, u"Madeline L'Engle")
    (1, u'Perdido Street Station', 1)
    (2, u'The Scar', 1)
    (3, u'King Rat', 1)
    (4, u'Dune', 2)
    (5, u"Hellstrom's Hive", 2)
    (6, u'The Dark is Rising', 3)
    Traceback (most recent call last):
      File "populatedb.py", line 57, in <module>
        populate_db(conn1)
      File "populatedb.py", line 46, in populate_db
        cur.executemany(book_insert, params)
    sqlite3.InterfaceError: Error binding parameter 0 - probably unsupported type.

EXCLUSIVE isolation
-------------------

There's not a whole lot of difference between the default "DEFERRED" isolation
level and "IMMEDIATE"

.. class:: incremental

There's quite a large difference, though for the "EXCLUSIVE" level.  

.. class:: incremental

Open ``threaded.py`` in your editors.  

.. class:: incremental

This is an example of using our existing database population setup in a
threaded environment.  One thread will load the database, the other will read
it.  

.. class:: incremental

Take a few moments to review the control flow here.  What should happen?

Testing It
----------

First, re-fix the bug in our ``utils.py`` file so that we don't get errors
when running this test.

.. container:: incremental

    Then, kill the old database, recreate it and run our new script:

    ::

        $ rm books.db
        $ python2.7 createdb.py
        Creating schema
        $ python2.7 threaded.py

The Results
-----------

.. class:: small

::

    2013-04-30 15:37:37,556 (Writer    ) connecting
    2013-04-30 15:37:37,556 (Reader    ) waiting to sync
    2013-04-30 15:37:37,556 (Writer    ) connected
    2013-04-30 15:37:37,557 (Writer    ) changes made
    2013-04-30 15:37:37,557 (Writer    ) waiting to sync
    2013-04-30 15:37:39,556 (MainThread) sending sync event
    2013-04-30 15:37:39,557 (Reader    ) beginning read
    2013-04-30 15:37:39,557 (Reader    ) beginning read
    2013-04-30 15:37:39,557 (Writer    ) PAUSING
    2013-04-30 15:37:42,559 (Writer    ) CHANGES COMMITTED
    2013-04-30 15:37:42,590 (Reader    ) selects issued
    (1, u'China Mieville')
    (2, u'Frank Herbert')
    (3, u'Susan Cooper')
    (4, u'J.R.R. Tolkien')
    (5, u"Madeline L'Engle")
    2013-04-30 15:37:42,590 (Reader    ) results fetched
    2013-04-30 15:37:42,590 (Reader    ) beginning read
    2013-04-30 15:37:42,590 (Reader    ) selects issued
    (1, u'Perdido Street Station', 1)
    (2, u'The Scar', 1)
    (3, u'King Rat', 1)
    (4, u'Dune', 2)
    (5, u"Hellstrom's Hive", 2)
    (6, u'The Dark is Rising', 3)
    (7, u'The Greenwitch', 3)
    (8, u'The Hobbit', 4)
    (9, u'The Silmarillion', 4)
    (10, u'A Wrinkle in Time', 5)
    (11, u'A Swiftly Tilting Planet', 5)
    2013-04-30 15:37:42,591 (Reader    ) results fetched

The End
-------

There's a lot more about both the DB API and SQLite that could be said.

.. class:: incremental

Unfortunately, that's all the time we have for tonight.

.. class:: incremental

Thanks very much for your attention.

.. class:: incremental big-centered

**Questions?**

