from distutils.core import setup

CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Software Development :: Documentation",
    "Topic :: Text Processing :: Markup"
]

with open('README.rst') as fp:
    LONG_DESCRIPTION = fp.read()

setup(
    name='gir2rst', 
    version='0.1', 
    packages=['gir2rst'],
    scripts=['bin/gir2rst'],
    author='Matthias Vogelgesang',
    author_email='matthias.vogelgesang@gmail.com',
    url='http://github.com/matze/gir2rst',
    keywords=['rst', 'gir'],
    license='GPL v3',
    classifiers=CLASSIFIERS,
    description='ReST-based Sphinx documentation from GIR files',
    long_description=LONG_DESCRIPTION
)
