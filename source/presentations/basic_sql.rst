Basic SQL
=========

.. class:: center

A quick overview of SQL: History, Concepts, and Syntax

What is SQL
-----------

.. class:: center

**SQL == Structured Query Language**

.. class:: incremental

* First invented in the early 1970s at IBM
* Based on *Relational Algebra* and *Tuple Relational Calculus*
* Used to get at data stored in their ``System-R`` database management system
* Picked up by *Relational Software* (now *Oracle*) in the late 1970s
* ``Oracle V2``, the first commercial Relational Database released in 1979
* IBM followed with ``System/38``, ``SQL/DS`` and ``DB2`` between 1979 and
  1983

.. class:: image-credit

source: http://en.wikipedia.org/wiki/SQL

What is SQL
-----------

SQL, and Relational Database Management Systems (RDBMS) have been the de-facto
standard for data persistence for 30+ years

.. class:: incremental

Currently, there are more than 100 RDBMS available, both proprietary and
open-source.

.. class:: incremental

Most, if not all, include some implementation of SQL as their query language.

.. class:: image-credit

source: http://en.wikipedia.org/wiki/List_of_relational_database_management_systems

Big Players in SQL
------------------

There are a number of RDBMS that you will run into regularly


**Commercial / Proprietary**

.. class:: incremental small

* MS SQL Server
* Oracle
* MySQL Enterprise (Oracle)

**Open Source**

.. class:: incremental small

* PostgreSQL
* MariaDB (MySQL community)
* SQLite

SQL/RDBMS Concepts - Tables
---------------------------

.. class:: incremental

A table consists of *rows* (also called *records*) and *columns*

.. class:: incremental

Each row/record represents a single item

.. class:: incremental

Each column represents a data point

.. class:: incremental

Most tables will have one column which is considered the *primary key*

.. class:: incremental

This value will uniquely identify a single row out of all the rows in the
table

An Example
----------

Here is an example table which represents people in a system:

.. class:: incremental center

+----+------------+------------+-----------+
| id | username   | first_name | last_name |
+====+============+============+===========+
|  1 | wont_u_b   | Fred       | Rogers    |
+----+------------+------------+-----------+
|  4 | neuroman   | William    | Gibson    |
+----+------------+------------+-----------+
|  5 | race       | Roger      | Bannon    |
+----+------------+------------+-----------+
|  6 | harrywho   | Harry      | Houdini   |
+----+------------+------------+-----------+
|  7 | whitequeen | Emma       | Frost     |
+----+------------+------------+-----------+
|  8 | shadowcat  | Kitty      | Pryde     |
+----+------------+------------+-----------+

SQL/RDBMS Concepts - Relations
------------------------------

You can *model* things using tables like this.  Adding columns for all sorts
of different data points

.. class:: incremental

But what happens when not all of the items in a table share the *same* data
points?

.. class:: incremental

Or what if some of the items need to have more than one of a particular data
point?

.. class:: incremental

Leaving columns empty in a row wastes memory and slows down querying.  Use
*relations* to solve these types of problems

Types of Relations
------------------

There are three basic types of relationships:

.. class:: incremental small

One-to-one relationships
  Best used to represent aspects of an item which are not *core* to it. Like
  user (id, password) -> user_profile (preferences, name, address)

.. class:: incremental small

Many-to-one relationships
  Used to represent relationships of ownership or belonging. Like product ->
  manufacturer or book -> author

.. class:: incremental small

Many-to-many relationships
  Used to represent associations or membership.  Like users -> groups or 
  items -> orders

SQL Relations - ∞ -> 1
----------------------

Many-to-one relationships are modelled using *Foreign Keys*

.. class:: incremental

The *many* table has a column which holds the *primary key* of the row from
the *one* table:

.. class:: incremental

Consider the relationship of books to author:

Books -> Author
---------------

**People**:

.. class:: small

+----+-----------+------------+-----------+
| id | username  | first_name | last_name |
+====+===========+============+===========+
|  4 | neuroman  | William    | Gibson    |
+----+-----------+------------+-----------+
|  6 | harrywho  | Harry      | Houdini   |
+----+-----------+------------+-----------+

**Books**:

.. class:: small

+----+-----------------------------------+--------+
| id | title                             | author |
+====+===================================+========+
|  1 | Miracle Mongers and their Methods | 6      |
+----+-----------------------------------+--------+
|  2 | The Right Way to Do Wrong         | 6      |
+----+-----------------------------------+--------+
|  3 | Pattern Recognition               | 4      |
+----+-----------------------------------+--------+

SQL Relations - 1 -> 1
----------------------

One-to-one relationships are really just a special case of Many-to-one, and
are also modelled with *Foreign Keys*

.. class:: incremental

In this case, the column on the related table which holds the *primary key* of
the target table has an additional *unique* constraint, so that only one
related record can exist

.. class:: incremental

The classic purpose is for data that doesn't need to be accessed often, and
is unique per record

.. class:: incremental

Consider the example of birth records:

Birth Record -> Person
----------------------

**People**:

.. class:: small

+----+-----------+------------+-----------+
| id | username  | first_name | last_name |
+====+===========+============+===========+
|  1 | wont_u_b  | Fred       | Rogers    |
+----+-----------+------------+-----------+
|  4 | neuroman  | William    | Gibson    |
+----+-----------+------------+-----------+
|  5 | race      | Roger      | Bannon    |
+----+-----------+------------+-----------+

**Birth Records**:

.. class:: small

+----+--------+----------------+--------------+
| id | person | date           | place        |
+====+========+================+==============+
|  1 | 1      | March 20, 1928 | Latrobe, PA  |
+----+--------+----------------+--------------+
|  2 | 4      | March 17, 1948 | Conway, SC   |
+----+--------+----------------+--------------+
|  3 | 5      | April 1, 1954  | Wilmette, IL |
+----+--------+----------------+--------------+

SQL Relations - ∞ -> ∞
----------------------

Many-to-many relations are a bit trickier.

.. class:: incremental

You can't have a multi-valued field, so there's no way to define a *foreign
key*-like construct that would work

.. class:: incremental

Instead, this relationship is modelled using a *join table*, which has two
*foreign key* fields, one for each side of the relation.

.. class:: incremental

Beyond these two, other columns can add data points describing the qualities
of the relation itself

Group Memberships
-----------------

.. container:: column-left small

    **People**:

    +----+------------+------------+-----------+
    | id | username   | first_name | last_name |
    +====+============+============+===========+
    |  7 | whitequeen | Emma       | Frost     |
    +----+------------+------------+-----------+
    |  8 | shadowcat  | Kitty      | Pryde     |
    +----+------------+------------+-----------+

.. container:: column-right small

    **Groups**:

    +----+---------------+
    | id | name          |
    +====+===============+
    |  1 | Hellfire Club |
    +----+---------------+
    |  2 | X-Men         |
    +----+---------------+

.. container:: small incremental

    **Membership**:

    +----+--------+-------+--------+
    | id | person | group | active |
    +====+========+=======+========+
    |  1 | 7      | 1     | False  |
    +----+--------+-------+--------+
    |  2 | 7      | 2     | True   |
    +----+--------+-------+--------+
    |  3 | 8      | 2     | True   |
    +----+--------+-------+--------+

SQL Syntax
----------

The syntax of SQL can be broken into *constructs*:

.. class:: incremental small

 * **Statements** are discreet units that perform some action, like inserting
   records or querying
 * **Clauses** are sub-units of statements which indicate some action or
   condition
 * **Expressions** are elements that produce values, either unitary or as
   tables themselves
 * **Predicates** are conditionals which produce some boolean or three-valued
   truth value

.. image:: img/sql_anatomy.png
    :align: center
    :width: 700px
    :class: incremental

.. class:: image-credit incremental

image: CC-BY-SA by Ferdna http://en.wikipedia.org/wiki/File:SQL_ANATOMY_wiki.svg

SQL Syntax - Subsets
--------------------

SQL statements can be thought of as belonging to one of several *subsets*

.. class:: incremental

Data Definition
  Statements in this subset concern the structure of the database itself:

.. code-block:: sql
    :class: small incremental

    CREATE TABLE "jos_groups" (
      "group_id" character varying(32) NOT NULL,
      "name" character varying(255) NOT NULL,
      "description" text NOT NULL
    )

SQL Syntax - Subsets
--------------------

SQL statements can be thought of as belonging to one of several *subsets*

Data Manipulation
  Statements in this subset concern the altering of data within the database:

.. code-block:: sql
    :class: small incremental

    UPDATE people
        SET first_name='Bill'
        WHERE id=4;

SQL Syntax - Subsets
--------------------

SQL statements can be thought of as belonging to one of several *subsets*

Data Query
  Statements in this subset concern the retrieval of data from within the 
  database:

.. code-block:: sql
    :class: small incremental

    SELECT user_id, COUNT(*) c 
      FROM (SELECT setting_value AS interests, user_id
              FROM user_settings 
              WHERE setting_name = 'interests') raw_uid
      GROUP BY user_id HAVING c > 1;

