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
import textwrap
import gir2rst.parser


def rst_h1(title, char='='):
    lines = char * len(title)
    return "%s\n%s\n%s\n\n" % (lines, title, lines)


def rst_h2(title, char='='):
    lines = char * len(title)
    return "%s\n%s\n\n" % (title, lines)


class RstFormatter(object):
    def __init__(self, filename, output):
        self.parser = gir2rst.parser.GirParser(filename)
        self.output = output
        self.wrapper = textwrap.TextWrapper(initial_indent='    ',
                subsequent_indent='    ')
        self.ns_core = string.Template('%s$tag' %
                gir2rst.parser.NS_CORE_PREFIX)
        self.ns_c = string.Template('%s$tag' % gir2rst.parser.NS_C_PREFIX)

    def write_rst(self):
        namespace = self.parser.get_namespace()
        title = "%s %s API reference" % (namespace.attrib['name'],
                namespace.attrib['version'])
        self.output.write(rst_h1(title))

        for class_element in self.parser.get_classes():
            self.output_class(class_element)
            constructor = self.parser.get_constructor(class_element)
            if constructor:
                self.output_constructor(constructor)

            for method in self.parser.get_methods(class_element):
                self.output_method(method)

    def print_lines(self, lines):
        if lines:
            for line in self.wrapper.wrap(lines):
                self.output.write(line + '\n')

    def output_class(self, class_element):
        pass

    def output_constructor(self, element, rtype):
        pass

    def output_method(self, element, rtype):
        pass


class RstCFormatter(RstFormatter):
    def __init__(self, filename, output):
        super(RstCFormatter, self).__init__(filename, output)

    def output_class(self, class_element):
        name = self.parser.get_c_type_attrib(class_element)
        self.output.write(rst_h2(name))
        self.output.write(".. c:type:: %s\n\n" % name)
        self.print_lines(self.parser.get_element_doc(class_element))
        self.output.write('\n\n')

    def output_constructor(self, element):
        self.output_method(element)

    def output_method(self, element):
        rtype = self.parser.get_return_type(element)
        c_name = element.attrib[self.ns_c.substitute(tag='identifier')]
        c_rtype = rtype.attrib[self.ns_c.substitute(tag='type')]
        self.output.write(".. c:function:: %s %s(" % (c_rtype, c_name))

        params = self.parser.get_parameters(element)
        param_names = [p.attrib['name'] for p in params]
        types = [self.parser.get_c_type_attrib(self.parser.get_type(param)) for
                param in params]

        tokens = [', '] * len(param_names)
        if tokens:
            tokens[-1] = ''

        zipped = zip(types, param_names, tokens)
        self.output.write("".join(["%s %s%s" % (a, b, c) for (a, b, c) in
            zipped]))
        self.output.write(")\n\n")

        self.print_lines(self.parser.get_element_doc(element))
        self.output.write('\n')

        param_descriptions = ["    :param %s: %s\n" % (p.attrib['name'],
            self.parser.get_element_doc(p)) for p in params]

        for desc in param_descriptions:
            self.output.write(desc)

        rval = self.parser.get_return_value(element)
        if self.parser.get_type(rval).attrib['name'] != 'none':
            self.output.write('\n    :returns: %s' %
                    self.parser.get_element_doc(rval))

        self.output.write('\n\n')
