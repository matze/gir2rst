# gir2rst - Create Sphinx documentation from GIR files
# Copyright (C) 2012 Matthias Vogelgesang
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import string
from xml.etree import ElementTree

NS_CORE_PREFIX = '{http://www.gtk.org/introspection/core/1.0}'
NS_C_PREFIX = '{http://www.gtk.org/introspection/c/1.0}'


class GirParser(object):
    def __init__(self, filename):
        self.tree = ElementTree.ElementTree()
        self.tree.parse(filename)
        self.ns_core = string.Template('%s$tag' % (NS_CORE_PREFIX))
        self.ns_c = string.Template('%s$tag' % (NS_C_PREFIX))

    def get_namespace(self):
        return self.tree.find(self.ns_core.substitute(tag='namespace'))

    def get_classes(self):
        ns_tag = self.ns_core.substitute(tag='namespace')
        class_tag = self.ns_core.substitute(tag='class')
        return self.tree.findall('%s/%s' % (ns_tag, class_tag))

    def get_class_name(self, class_element):
        return class_element.attrib['name']

    def get_c_type_attrib(self, element):
        if element is None:
            return None
        return element.attrib[self.ns_c.substitute(tag='type')]

    def get_type(self, element):
        return element.find(self.ns_core.substitute(tag='type'))

    def get_element_doc(self, element):
        return element.findtext(self.ns_core.substitute(tag='doc'))

    def get_constructor(self, class_element):
        return class_element.find(self.ns_core.substitute(tag='constructor'))

    def get_methods(self, class_element):
        return class_element.findall(self.ns_core.substitute(tag='method'))

    def get_parameters(self, method_element):
        parameters_tag = self.ns_core.substitute(tag='parameters')
        parameter_tag = self.ns_core.substitute(tag='parameter')
        return method_element.findall('%s/%s' % (parameters_tag,
            parameter_tag))

    def get_return_value(self, method_element):
        return method_element.find(self.ns_core.substitute(tag='return-value'))

    def get_return_type(self, method_element):
        rvalue = self.get_return_value(method_element)
        return rvalue.find(self.ns_core.substitute(tag='type'))
