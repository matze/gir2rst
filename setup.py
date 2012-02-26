from distutils.core import setup

setup(name='gir2rst', 
        version='0.1', 
        scripts=['bin/gir2rst'],
        packages=['gir2rst'],
        author='Matthias Vogelgesang',
        author_email='matthias.vogelgesang@gmail.com',
        url='http://github.com/matze/gir2rst',
        license='GPL v3',
        description='Generate ReST-based Sphinx documentation from GIR files',)
