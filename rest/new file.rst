
ReST to html -- the official way
================================

*Italic* and **Bold.**

::

  # Preformatted,
  # For communicating code.

  # Yes, it can have spaces.

Here's a `link to Python.org.`

_ http://www.python.org/

Section Structure
==================

=====
Title
=====
Subtitle
--------
Titles are underlined (or over-
and underlined) with a printing
nonalphanumeric 7-bit ASCII
character. Recommended choices
are "``= - ` : ' " ~ ^ _ * + # < >``".
The underline/overline must be at
least as long as the title text.

A lone top-level (sub)section
is lifted up to be the document's
(sub)title.

Lists
=====

**Bullet list:**

- Point A
- Point B
- Point C
- Point D




**Numbered list**:

#. Point 1
#. Point 2
#. Point 3
#. Point 4




**Definition list**:

term 1
    Definition of term1
term 2
    Definition of term2
term 3 : classifier one : classifier two
    Definition 3.

Field list
==========

:Authors:
    777Tony J. (Tibs) Ibbs,
    David Goodger

    (and sundry other good-natured folks)

:Version: 1.0 of 2001/08/08
:Dedication: To my father. 

*My field list:*

:field0:
    description0 html: <br />
    description0.1

    description0.2

:field1:
    description1

:field2:
    description2

:longofield3:
    description3

Some long text... Some long text... Some long text... Some long text...
Some long text... Some long text... Some long text... Some long text...
Some long text... Some long text... Some long text... Some long text...

abc
def
ghi

Line Blocks
===========

| Line blocks are useful for addresses,
| verse, and adornment-free lists.
|
| Each new line begins with a
| vertical bar ("|").
|     Line breaks and initial indents
|     are preserved.
| Continuation lines are wrapped
  portions of long lines; they begin
  with spaces in place of vertical bars.

Block Quotes
=============

Block quotes are just:

    Indented paragraphs,

        and they may nest. 

Citations
==============

Citation references, like [CIT2002]_.
Note that citations may get
rearranged, e.g., to the bottom of
the "page".

Citation labels contain alphanumerics,
underlines, hyphens and fullstops.
Case is not significant.

Given a citation like [this]_, one
can also refer to it like this_.

Literal block
=============

This is a typical paragraph.  An indented literal block follows.

::

    for a in [5,4,3,2,1]:   # this is program code, shown as-is
        print a
    print "it's..."
    # a literal block continues until the indentation ends

This text has returned to the indentation of the first paragraph,
is outside of the literal block, and is therefore treated as an
ordinary paragraph.

**Expanded form:**

Paragraph:

::

    Literal block

**Partially minimized form:**

Paragraph: ::

    Literal block

**Fully minimized form:**

Paragraph::

    Literal block






.. rubric:: **References**

.. [CIT2002]    A citation
   (as often used in journals).
.. [this] here. 