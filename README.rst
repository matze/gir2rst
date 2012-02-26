gir2rst
=======

gir2rst provides a package and command-line tool to create Sphinx documentation
from GObject-Introspection files.


Installation
------------

Fetch the latest version from Github ::

    git clone git://github.com/matze/gir2rst.git

and install with::

    python setup.py install


Usage
-----

The command line tool ``gir2rst`` will parse the provided .gir files and output
the resulting Sphinx documentation on stdout::

    gir2rst /home/user/path/to/gir/Library-x.y.gir

