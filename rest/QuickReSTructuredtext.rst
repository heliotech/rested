
ReST to html -- the official way
================================


Quick reStructuredText_.

.. _reStructuredText: https://docutils.sourceforge.io/docs/user/rst/quickref.html#section-structure

----------------------------------

*Italic* and **Bold.**

::

  # Preformatted,
  # For communicating code.

  # Yes, it can have spaces.

Here's a `link to Python.org.`

_ http://www.python.org/

Section structure
------------------

Section
"""""""""""

Section
````````

Section
::::::::

Section
~~~~~~~~

Lists
=====

**Bullet list:**

- Point A
- Point B
- Point C
- Point D

*Different one:*

+ Point 1
+ Point 2
+ Point 3

* Point 1
* Point 2
* Point 3




**Numbered list**:

#. Point 1
#. Point 2
#. Point 3
#. Point 4




**Definition list**:

term1
    Definition of term1
term2
    Definition of term2

Short break...

Another definition list:


Subject 0
    Definition of `subject 0`
Subject 1
    Definition of `subject 1`

    More on `subject 1`

    ...and even more, on `subject 1` -- whole in three paragraphs.
Subject 2
    Definition of `subject 2` Some long text... Some long text... Some long text... Some long text...Some long text... 
    Some long text... Some long text... Some long text...Some long text... Some long text... Some long text... 
    Some long text... Some long text... Some long text... Some long text... Some long text... (Total of 3 lines, 
    with `\\n` character each, but without any blank lines and every line indented.)
    
Yet another definition list:

ABC
    ABC stands for something, Some long text... Some long text... Some long text... Some long text... 
    or something different Some long text... Some long text... Some long text... Some long text... 
    entirely...Some long text... Some long text... Some long text... Some long text... Some long text... 
    



Some long text... Some long text... Some long text... Some long text...
Some long text... Some long text... Some long text... Some long text...
Some long text... Some long text... Some long text... Some long text...

:Developer:
    Khaz
:Application: ReSTed
:Year: 2021



-a                    option a
-b                    option b
-clong                option clong

A transition marker is a horizontal line
of 4 or more repeated punctuation
characters.

------------

A transition should not begin or end a
section or document, nor should two
transitions be immediately adjacent. 

Typical result
Footnote references, like [5]_.
Note that footnotes may get
rearranged, e.g., to the bottom of
the "page".

.. [5] A numerical footnote. Note
   there's no colon after the ``]``. 

Autonumbered footnotes are
possible, like using [#]_ and [#]_.

.. [#] This is the first one.
.. [#] This is the second one.

They may be assigned 'autonumber
labels' - for instance,
[#fourth]_ and [#third]_.

.. [#third] a.k.a. third_

.. [#fourth] a.k.a. fourth_ 

Auto-symbol footnotes are also
possible, like this: [*]_ and [*]_.

.. [*] This is the first one.
.. [*] This is the second one. 

Titles are targets, too
=======================
Implict references, like `Titles are
targets, too`_.