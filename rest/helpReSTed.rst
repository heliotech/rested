======================================
ReSTed -- ReStructuredText editor help
======================================

1. Introduction
===============

This simple plain text editor is designed to convert text document, which conform to the reStructuredText 
standard, into a html document. The engine of the application was adopted from 
https://wiki.python.org/moin/reStructuredText. Besides plain text view, of the document, and resulting html
preview, the program offers editing of the CSS style sheet and view of the resulting html code.

2. Views
=========

The main window includes four tabs:

    1. `ReStructuredtext tab` -- for text contents edition.
    2. `CSS` tab -- for the html document style-sheet.
    3. `HTML view` -- for the preview of resulting HTML document.
    4. `Code` -- the contents of the resulting HTML code, for fine-tuning of the CSS style sheet.

3. Shortcuts
============

The usual shortcuts:
--------------------

File Menu
..........

``Ctrl+N``
    New rst document.

``Ctrl+O``
    Open an rst document.

``Ctrl+Shift+S``
    Save the rst document as...

``Ctrl+S``
    Save the rst document.

``Ctrl+Q``
    Quit.

Edit Menu
..........

``Ctrl+C``,
``Ctrl+X``
and ``Ctrl+P`` for copy, cut and paste, respectively.

Tools Menu
..........

``Ctrl+R``
    Convert the reStructuredtext document into html.

Shortcuts for the tab widget:
-----------------------------

``Ctrl+Tab``
    Next tab.

``Ctrl+Shift+Tab``
    Previous tab.

4. History
===========

    - version 1.0 -- fully functional application. Latest addition: files history through config parser.
    - versuib 1.1 -- custom `QPlainTextEdit` -> `MyTextEdit`:
        - `Tab` inserts 4 spaces,
        - `Enter` with continuation of the indentation and bulleted lists,

5. About the **restructuredtext**
=========================================

    - https://docutils.sourceforge.io/rst.html
    - https://en.wikipedia.org/wiki/ReStructuredText
    - https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html

6. Credits
==========

    - https://wiki.python.org/moin/reStructuredText
    - https://realpython.com/
    - https://stackoverflow.com/questions/19990026/change-text-selection-in-pyqt-qtextedit
    - https://www.informit.com/articles/article.aspx?p=1187104&seqNum=3
    - and great many programers, who shared their knowledge online. 