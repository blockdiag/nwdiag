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

import os
import sys
import codecs
from re import MULTILINE, DOTALL
from pprint import pformat
from funcparserlib.util import pretty_tree
from funcparserlib.lexer import make_tokenizer, Token, LexerError
from funcparserlib.parser import (some, a, maybe, many, finished, skip,
    oneplus, forward_decl, NoParseError)

from blockdiag.utils.namedtuple import namedtuple

ENCODING = 'utf-8'

Graph = namedtuple('Graph', 'type id stmts')
Network = namedtuple('Network', 'id stmts')
SubGraph = namedtuple('SubGraph', 'id stmts')
Node = namedtuple('Node', 'id attrs')
Attr = namedtuple('Attr', 'name value')
Edge = namedtuple('Edge', 'nodes attrs')
DefAttrs = namedtuple('DefAttrs', 'object attrs')


class ParseException(Exception):
    pass


def tokenize(str):
    'str -> Sequence(Token)'
    specs = [
        ('Comment', (r'/\*(.|[\r\n])*?\*/', MULTILINE)),
        ('Comment', (r'//.*',)),
        ('NL',      (r'[\r\n]+',)),
        ('Space',   (r'[ \t\r\n]+',)),
        ('Name',    (ur'[A-Za-z_\u0080-\uffff]'
                     ur'[A-Za-z_\-.0-9\u0080-\uffff]*',)),
        ('Op',      (r'([{};,=\[\]]|--)',)),
        ('IPAddr',  (r'([0-9]+(\.[0-9]+){3}|[:0-9a-fA-F]+)',)),
        ('Number',  (r'-?(\.[0-9]+)|([0-9]+(\.[0-9]*)?)',)),
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
    node_flatten = lambda l: sum([[l[0]]] + list(l[1:]), [])
    n = lambda s: a(Token('Name', s)) >> tokval
    op = lambda s: a(Token('Op', s)) >> tokval
    op_ = lambda s: skip(op(s))
    id = some(lambda t:
        t.type in ['Name', 'IPAddr', 'Number', 'String']).named('id') >> tokval
    make_graph_attr = lambda args: DefAttrs(u'graph', [Attr(*args)])
    make_edge = lambda x, x2, xs, attrs: Edge([x, x2] + xs, attrs)

    node_id = id  # + maybe(port)
    node_list = (
        node_id +
        many(op_(',') + node_id)
        >> node_flatten)
    a_list = (
        id +
        maybe(op_('=') + id) +
        skip(maybe(op(',')))
        >> unarg(Attr))
    attr_list = (
        many(op_('[') + many(a_list) + op_(']'))
        >> flatten)
    edge_rhs = op_('--') + node_id
    edge_stmt = (
        node_id +
        edge_rhs +
        many(edge_rhs) +
        attr_list
        >> unarg(make_edge))
    graph_attr = id + op_('=') + id >> make_graph_attr
    node_stmt = node_id + attr_list >> unarg(Node)
    # We use a forward_decl becaue of circular definitions like (stmt_list ->
    # stmt -> subgraph -> stmt_list)
    group_stmt = (
        graph_attr
        | node_stmt
    )
    group_stmt_list = many(group_stmt + skip(maybe(op(';'))))
    group = (
        skip(n('group')) +
        maybe(id) +
        op_('{') +
        group_stmt_list +
        op_('}')
        >> unarg(SubGraph))
    network_stmt = (
        graph_attr
        | group
        | node_stmt
    )
    network_stmt_list = many(network_stmt + skip(maybe(op(';'))))
    network = (
        skip(n('network')) +
        maybe(id) +
        op_('{') +
        network_stmt_list +
        op_('}')
        >> unarg(Network))
    stmt = (
        network
        | group
        | graph_attr
        | edge_stmt
        | node_stmt
    )
    stmt_list = many(stmt + skip(maybe(op(';'))))
    graph = (
        maybe(n('diagram')) +
        maybe(id) +
        op_('{') +
        stmt_list +
        op_('}')
        >> unarg(Graph))
    dotfile = graph + skip(finished)

    return dotfile.parse(seq)


def parse_string(string):
    try:
        return parse(tokenize(string))
    except LexerError, e:
        message = "Got unexpected token at line %d column %d" % e.place
        raise ParseException(message)
    except Exception, e:
        raise ParseException(str(e))


def parse_file(path):
    input = codecs.open(path, 'r', 'utf-8').read()
    return parse_string(input)
