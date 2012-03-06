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

You can also get the latest release from the Python Package Index ::

    pip install gir2rst


Usage
-----

The command line tool ``gir2rst`` will parse the provided .gir files and output
the resulting Sphinx documentation on stdout::

    usage: gir2rst [-h] [--version] [-t TITLE] [-o FILE] [input [input ...]]

    Generate Sphinx documentation from GObject Introspection GIR files.

    positional arguments:
      input       .gir input files

      optional arguments:
        -h, --help  show this help message and exit
        --version
        -t TITLE    override the title [available variables: #version (escape with
                    '\')]
        -o FILE     write to FILE or stdout if omitted
