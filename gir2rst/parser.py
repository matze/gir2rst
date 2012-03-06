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
        basic_type = element.find(self.ns_core.substitute(tag='type'))
        if basic_type is not None:
            return basic_type

        array_type = element.find(self.ns_core.substitute(tag='array'))
        return array_type

    def get_element_doc(self, element):
        return element.findtext(self.ns_core.substitute(tag='doc'))

    def get_constructor(self, class_element):
        return class_element.find(self.ns_core.substitute(tag='constructor'))

    def get_methods(self, class_element):
        return class_element.findall(self.ns_core.substitute(tag='method'))

    def get_method_c_name(self, meth_element):
        return meth_element.attrib[self.ns_c.substitute(tag='identifier')]

    def get_parameters(self, method_element):
        parameters_tag = self.ns_core.substitute(tag='parameters')
        parameter_tag = self.ns_core.substitute(tag='parameter')
        return method_element.findall('%s/%s' % (parameters_tag,
            parameter_tag))

    def get_parameter_names(self, meth_element):
        """Build a list of strings with parameters of a method."""
        params = self.get_parameters(meth_element)
        return [p.attrib['name'] for p in params if 'name' in p.attrib]

    def get_parameter_c_types(self, meth_element):
        """Build a list of strings with the types of all parameters."""
        params = self.get_parameters(meth_element)
        return [self.get_c_type_attrib(self.get_type(p)) for p in params]

    def get_return_value(self, method_element):
        return method_element.find(self.ns_core.substitute(tag='return-value'))

    def get_return_type(self, method_element):
        rvalue = self.get_return_value(method_element)
        return rvalue.find(self.ns_core.substitute(tag='type'))

    def get_return_c_type(self, meth_element):
        """Return the string representation of the C return type."""
        rtype = self.get_return_type(meth_element)
        if rtype is not None:
            return rtype.attrib[self.ns_c.substitute(tag='type')]
        else:
            return None
