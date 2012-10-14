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

import re
import codecs
from re import MULTILINE, DOTALL
from funcparserlib.lexer import make_tokenizer, Token, LexerError
from funcparserlib.parser import (some, a, maybe, many, finished, skip)
from blockdiag.utils.namedtuple import namedtuple

ENCODING = 'utf-8'

Graph = namedtuple('Graph', 'type id stmts')
RackItem = namedtuple('RackItem', 'number label attrs')
Attr = namedtuple('Attr', 'name value')
Rack = namedtuple('Rack', 'id stmts')
DefAttrs = namedtuple('DefAttrs', 'object attrs')
AttrPlugin = namedtuple('AttrPlugin', 'name attrs')


class ParseException(Exception):
    pass


def tokenize(str):
    'str -> Sequence(Token)'
    specs = [
        ('Comment', (r'/\*(.|[\r\n])*?\*/', MULTILINE)),
        ('Comment', (r'(//|#).*',)),
        ('NL',      (r'[\r\n]+',)),
        ('Space',   (r'[ \t\r\n]+',)),
        ('RackItem', (r':[^\r\n\[]+',)),
        ('Units',   (r'([0-9]+U|[0-9]+(?:\.[0-9]+)?(A|kg))',)),
        ('Number',  (r'[0-9]+',)),
        ('Name',    (ur'[A-Za-z_0-9\u0080-\uffff]'
                     ur'[A-Za-z_\-.0-9\u0080-\uffff]*',)),
        ('Op',      (r'[{}:;,=\[\]]',)),
        ('String',  (r'(?P<quote>"|\').*?(?<!\\)(?P=quote)', DOTALL)),
    ]
    useless = ['Comment', 'NL', 'Space']
    t = make_tokenizer(specs)
    return [x for x in t(str) if x.type not in useless]


def parse(seq):
    'Sequence(Token) -> object'
    unarg = lambda f: lambda args: f(*args)
    tokval = lambda x: x.value
    flatten = lambda list: sum(list, [])
    n = lambda s: a(Token('Name', s)) >> tokval
    op = lambda s: a(Token('Op', s)) >> tokval
    op_ = lambda s: skip(op(s))
    id = some(lambda t: t.type in ['Name', 'Number', 'String', 'Units']
              ).named('id') >> tokval
    number = some(lambda t: t.type == 'Number').named('number') >> tokval
    rackitem = some(lambda t: t.type == 'RackItem').named('rackitem') >> tokval
    make_graph_attr = lambda args: DefAttrs(u'graph', [Attr(*args)])

    racklabel = lambda text: re.sub("^:\s*(.*?)\s*;?$", "\\1", text)
    make_rackitem = lambda no, text, attr: RackItem(no, racklabel(text), attr)

    a_list = (
        id +
        maybe(op_('=') + id) +
        skip(maybe(op(',')))
        >> unarg(Attr))
    attr_list = (
        many(op_('[') + many(a_list) + op_(']'))
        >> flatten)
    graph_attr = id + op_('=') + id >> make_graph_attr
    rackitem_stmt = (
        number +
        rackitem +
        attr_list
        >> unarg(make_rackitem))

    # rack definition
    rack_stmt = (
        rackitem_stmt
        | a_list
        | graph_attr
    )
    rack_stmt_list = many(rack_stmt + skip(maybe(op(';'))))
    rack = (
        skip(n('rack')) +
        maybe(id) +
        op_('{') +
        rack_stmt_list +
        op_('}')
        >> unarg(Rack))

    # plugin definition
    plugin_stmt = (
        skip(n('plugin')) +
        id +
        attr_list
        >> unarg(AttrPlugin))

    stmt = (
        rack
        | rackitem_stmt
        | plugin_stmt
        | a_list
    )
    stmt_list = many(stmt + skip(maybe(op(';'))))
    graph = (
        maybe(n('diagram') | n('rackdiag')) +
        maybe(id) +
        op_('{') +
        stmt_list +
        op_('}')
        >> unarg(Graph))
    dotfile = graph + skip(finished)

    return dotfile.parse(seq)


def sort_tree(tree):
    def weight(node):
        if isinstance(node, (Attr, DefAttrs, AttrPlugin)):
            return 1
        else:
            return 2

    def compare(a, b):
        return cmp(weight(a), weight(b))

    if hasattr(tree, 'stmts'):
        tree.stmts.sort(compare)
        for stmt in tree.stmts:
            sort_tree(stmt)

    return tree


def parse_string(string):
    try:
        tree = parse(tokenize(string))
        return sort_tree(tree)
    except LexerError, e:
        message = "Got unexpected token at line %d column %d" % e.place
        raise ParseException(message)
    except Exception, e:
        raise ParseException(str(e))


def parse_file(path):
    input = codecs.open(path, 'r', 'utf-8').read()
    return parse_string(input)
