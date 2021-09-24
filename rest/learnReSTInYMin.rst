.. class:: title

============================================
Learn ReST in Y Minutes
============================================

.. Lines starting with two dots are special commands. But if no command can be found, the line is considered as a comment

.. class:: note

(source: https://learnxinyminutes.com/docs/rst/)

.. contents:: Table of Contents

----

=========================================================
Main titles are written using equals signs over and under
=========================================================

Note that each character, including spaces, needs an equals sign above and below.

Titles also use equals signs but are only underneath
====================================================

Subtitles with dashes
---------------------

Formatting
----------- 

You can put text in *italic* or in **bold**, you can "mark" text as code with double backquote ``print()``.

Special characters can be escaped using a backslash, e.g. \\ or \*.

Lists
-------

Lists are similar to Markdown, but a little more involved.

Remember to line up list symbols (like - or \*) with the left edge of the previous text block, and remember to use blank lines to separate new lists from parent lists:    

- First item
- Second item

  - Sub item

- Third item

or

* First item
* Second item

  * Sub item

* Third item

Tables
-------

Tables are really easy to write:

=========== ========
Country     Capital
=========== ========
France      Paris
Japan       Tokyo
=========== ========

More complex tables can be done easily (merged columns and/or rows) but I suggest you to read the complete doc for this :)

Links
--------

There are multiple ways to make links:

- By adding an underscore after a word : Github_ and by adding the target URL after the text (this way has the advantage of not inserting unnecessary URLs in the visible text).
- By typing a full comprehensible URL : https://github.com/ (will be automatically converted to a link)
- By making a more Markdown-like link: `Github <https://github.com/>`_ .

.. _Github: https://github.com/