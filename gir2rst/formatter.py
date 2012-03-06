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

import re
import string
import textwrap
import gir2rst.parser


def _rst_h1(title, char='='):
    lines = char * len(title)
    return "%s\n%s\n%s\n\n" % (lines, title, lines)


def _rst_h2(title, char='='):
    lines = char * len(title)
    return "%s\n%s\n\n" % (title, lines)


def _fix_references(s):
    # TODO: cache the regular expressions
    if s:
        s = re.sub(r'\s(\w+)\(\)', r' :c:func:`\1()`', s)
        s = re.sub(r'\s@(\w+)', r' ``\1``', s)
        s = re.sub(r'\s#(\w+)', r' :c:type:`\1`', s)
        s = s.replace('%NULL', '``NULL``')
        return s
    return None


class RstFormatter(object):
    def __init__(self, filename, output, title=None):
        self.parser = gir2rst.parser.GirParser(filename)
        self.output = output
        self.title = title
        self.wrapper = textwrap.TextWrapper(initial_indent='    ',
                subsequent_indent='    ')
        self.ns_core = string.Template('%s$tag' %
                gir2rst.parser.NS_CORE_PREFIX)
        self.ns_c = string.Template('%s$tag' % gir2rst.parser.NS_C_PREFIX)

    def write_rst(self):
        namespace = self.parser.get_namespace()
        if self.title:
            self.output.write(_rst_h1(self.title % namespace.attrib))
        else:
            title = "%s %s API reference" % (namespace.attrib['name'],
                    namespace.attrib['version'])
            self.output.write(_rst_h1(title))

        for class_element in self.parser.get_classes():
            self.output_class(class_element)
            ctor = self.parser.get_constructor(class_element)
            if ctor:
                self.output_constructor(class_element, ctor)

            for method in self.parser.get_methods(class_element):
                self.output_method(class_element, method)

    def print_lines(self, lines):
        if lines:
            for line in self.wrapper.wrap(lines):
                self.output.write(line + '\n')

    def output_class(self, class_element):
        pass

    def output_constructor(self, class_element, ctor_element):
        pass

    def output_method(self, class_element, meth_element):
        pass

    def output_param_list(self, type_names, param_names):
        """Output (t1 n1, t2 n2, ..., tm nm) for each (ti, ni) in the product
        of type_names and param_names.
        """
        commas = [', '] * len(param_names)
        if commas:
            commas[-1] = ''

        zipped = zip(type_names, param_names, commas)
        self.output.write("".join(["%s %s%s" % t for t in zipped]))
        self.output.write(")\n\n")

    def output_param_description(self, func_element):
        """Output parameter description like ':param foo: foo description'."""
        params = self.parser.get_parameters(func_element)
        param_descriptions = ["    :param %s: %s\n" % (p.attrib['name'],
            _fix_references(self.parser.get_element_doc(p))) for p in params if
            'name' in p.attrib]

        if params:
            self.output.write('\n')

        for desc in param_descriptions:
            self.output.write(desc)

    def output_return_value(self, meth_element):
        """Output the return value like ':returns: return value description'.
        """
        rval = self.parser.get_return_value(meth_element)
        rval_type = self.parser.get_type(rval)
        if 'name' in rval_type.attrib and rval_type.attrib['name'] != 'none':
            doc = self.parser.get_element_doc(rval)
            self.output.write('\n    :returns: %s\n' % _fix_references(doc))
        self.output.write('\n\n')

    def output_doc(self, element):
        """Output the doc element that is associated with a class or a
        method."""
        pass

    def output_method_body(self, element):
        self.output_doc(element)
        self.output_param_description(element)
        self.output_return_value(element)


class RstCFormatter(RstFormatter):
    def __init__(self, filename, output, title=None):
        super(RstCFormatter, self).__init__(filename, output, title)

    def output_class(self, class_element):
        name = self.parser.get_c_type_attrib(class_element)
        self.output.write(_rst_h2(name))
        self.output.write(".. c:type:: %s\n\n" % name)
        self.output_doc(class_element)
        self.output.write('\n\n')

    def _output_c_header(self, element):
        name = self.parser.get_method_c_name(element)
        rtype = self.parser.get_return_c_type(element)
        self.output.write(".. c:function:: %s %s(" % (rtype, name))

    def output_constructor(self, class_element, ctor_element):
        param_names = self.parser.get_parameter_names(ctor_element)
        type_names = self.parser.get_parameter_c_types(ctor_element)

        self._output_c_header(ctor_element)
        self.output_param_list(type_names, param_names)
        self.output_method_body(ctor_element)

    def output_method(self, class_element, meth_element):
        # We extend the parameter and type list with a self object as this is
        # not listed and thus implied in the .gir files.
        class_name = self.parser.get_c_type_attrib(class_element)
        param_names = self.parser.get_parameter_names(meth_element)
        param_names.insert(0, 'self')
        type_names = self.parser.get_parameter_c_types(meth_element)
        type_names.insert(0, '%s*' % class_name)

        self._output_c_header(meth_element)
        self.output_param_list(type_names, param_names)
        self.output_method_body(meth_element)

    def output_doc(self, element):
        doc = self.parser.get_element_doc(element)
        self.print_lines(_fix_references(doc))
