# -*- coding: utf-8 -*-

# Copyright (c) 2008/2009 Andrey Vlasovskikh
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

r'''A DOT language parser using funcparserlib.

The parser is based on [the DOT grammar][1]. It is pretty complete with a few
not supported things:

* Ports and compass points
* XML identifiers

At the moment, the parser builds only a parse tree, not an abstract syntax tree
(AST) or an API for dealing with DOT.

  [1]: http://www.graphviz.org/doc/info/lang.html
'''

import io
import re
from collections import namedtuple
from re import DOTALL, MULTILINE

from blockdiag.parser import create_mapper, oneplus_to_list
from funcparserlib.lexer import LexerError, Token, make_tokenizer
from funcparserlib.parser import a, finished, many, maybe, skip, some

Diagram = namedtuple('Diagram', 'id stmts')
FieldItem = namedtuple('FieldItem', 'begin end label attrs')
Attr = namedtuple('Attr', 'name value')
Extension = namedtuple('Extension', 'type name attrs')


class ParseException(Exception):
    pass


def tokenize(string):
    """str -> Sequence(Token)"""
    # flake8: NOQA
    specs = [                                                                          # NOQA
        ('Comment',         (r'/\*(.|[\r\n])*?\*/', MULTILINE)),                       # NOQA
        ('Comment',         (r'(//|#).*',)),                                           # NOQA
        ('NL',              (r'[\r\n]+',)),                                            # NOQA
        ('Number',          (r'[0-9]+',)),                                             # NOQA
        ('QuotedFieldItem', (r'(?<=[:*\-])\s*(?P<quote>"|\').*?(?<!\\)(?P=quote)',)),  # NOQA
        ('FieldItem',       (r'(?<=[:*\-])\s*[^\r\n\[;}]+',)),                         # NOQA
        ('Space',           (r'[ \t\r\n]+',)),                                         # NOQA
        ('Name',            ('[A-Za-z_0-9\u0080-\uffff]' +                             # NOQA
                             '[A-Za-z_\\-.0-9\u0080-\uffff]*',)),                      # NOQA
        ('Op',              (r'[{}:;,*\-=\[\]]',)),                                    # NOQA
        ('String',          (r'(?P<quote>"|\').*?(?<!\\)(?P=quote)', DOTALL)),         # NOQA
    ]
    useless = ['Comment', 'NL', 'Space']
    t = make_tokenizer(specs)
    return [x for x in t(string) if x.type not in useless]


def parse(seq):
    """Sequence(Token) -> object"""
    fielditem_tokens = ['QuotedFieldItem', 'FieldItem']

    tokval = lambda x: x.value
    op = lambda s: a(Token('Op', s)) >> tokval
    op_ = lambda s: skip(op(s))
    _id = some(lambda t: t.type in ['Name', 'Number', 'String']) >> tokval
    keyword = lambda s: a(Token('Name', s)) >> tokval
    number = some(lambda t: t.type == 'Number').named('number') >> tokval
    field_item = some(lambda t: t.type in fielditem_tokens) >> tokval

    def make_num_field_item(_from, to, text, attr):
        return FieldItem(_from, to, text.strip(), attr)

    def make_nonnum_field_item(text, attr):
        return FieldItem(None, None, text.strip(), attr)

    #
    # parts of syntax
    #
    option_stmt = (
        _id +
        maybe(op_('=') + _id)
        >> create_mapper(Attr)
    )
    option_list = (
        maybe(op_('[') + option_stmt + many(op_(',') + option_stmt) + op_(']'))
        >> create_mapper(oneplus_to_list, default_value=[])
    )

    #  field statement::
    #     1: A
    #     2-3: B [attr = value, attr = value];
    #     * C [attr = value, attr = value];
    #     * D [attr = value, attr = value];
    #
    numbered_field_item_stmt = (
        number +
        maybe(op_('-') + number) +
        op_(':') +
        field_item +
        option_list
        >> create_mapper(make_num_field_item)
    )
    nonnumbered_field_item_stmt = (
        (op_('-') | op_('*')) +
        field_item +
        option_list
        >> create_mapper(make_nonnum_field_item)
    )
    field_item_stmt = (
        numbered_field_item_stmt |
        nonnumbered_field_item_stmt
    )

    #  attributes statement::
    #     default_shape = box;
    #     default_fontsize = 16;
    #
    attribute_stmt = (
        _id + op_('=') + _id
        >> create_mapper(Attr)
    )

    #  extension statement (plugin)::
    #     plugin attributes [name = Name];
    #
    extension_stmt = (
        keyword('plugin') +
        _id +
        option_list
        >> create_mapper(Extension)
    )

    #
    # diagram statement::
    #     packetdiag {
    #        A;
    #     }
    #
    diagram_id = (
        (keyword('diagram') | keyword('packetdiag')) +
        maybe(_id)
        >> list
    )
    diagram_inline_stmt = (
        extension_stmt |
        field_item_stmt |
        attribute_stmt
    )
    diagram_inline_stmt_list = (
        many(diagram_inline_stmt + skip(maybe(op(';'))))
    )
    diagram = (
        maybe(diagram_id) +
        op_('{') +
        diagram_inline_stmt_list +
        op_('}')
        >> create_mapper(Diagram)
    )
    dotfile = diagram + skip(finished)

    return dotfile.parse(seq)


def sort_tree(tree):
    def weight(node):
        if isinstance(node, (Attr, Extension)):
            return 1
        else:
            return 2

    if hasattr(tree, 'stmts'):
        tree.stmts.sort(key=lambda x: weight(x))
        for stmt in tree.stmts:
            sort_tree(stmt)

    return tree


def parse_string(string):
    try:
        tree = parse(tokenize(string))
        return sort_tree(tree)
    except LexerError as e:
        message = "Got unexpected token at line %d column %d" % e.place
        raise ParseException(message)
    except Exception as e:
        raise ParseException(str(e))


def parse_file(path):
    code = io.open(path, 'r', encoding='utf-8-sig').read()
    return parse_string(code)
