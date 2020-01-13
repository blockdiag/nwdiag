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
from collections import namedtuple
from re import DOTALL, MULTILINE

from blockdiag.parser import create_mapper, oneplus_to_list
from funcparserlib.lexer import LexerError, Token, make_tokenizer
from funcparserlib.parser import a, finished, many, maybe, skip, some

Diagram = namedtuple('Diagram', 'id stmts')
Network = namedtuple('Network', 'id stmts')
Group = namedtuple('Group', 'id stmts')
Node = namedtuple('Node', 'id attrs')
Attr = namedtuple('Attr', 'name value')
Edge = namedtuple('Edge', 'from_node edge_type to_node attrs')
Peer = namedtuple('Peer', 'edges')
Route = namedtuple('Route', 'edges')
Extension = namedtuple('Extension', 'type name attrs')
Statements = namedtuple('Statements', 'stmts')


class ParseException(Exception):
    pass


def tokenize(string):
    """str -> Sequence(Token)"""
    # flake8: NOQA
    specs = [                                                           # NOQA
        ('Comment', (r'/\*(.|[\r\n])*?\*/', MULTILINE)),                # NOQA
        ('Comment', (r'(//|#).*',)),                                    # NOQA
        ('NL',      (r'[\r\n]+',)),                                     # NOQA
        ('Space',   (r'[ \t\r\n]+',)),                                  # NOQA
        ('Name',    ('[A-Za-z_\u0080-\uffff]' +                         # NOQA
                     '[A-Za-z_\\-.0-9\u0080-\uffff]*',)),               # NOQA
        ('Op',      (r'([{};,=\[\]]|--|->)',)),                         # NOQA
        ('IPAddr',  (r'([0-9]+(\.[0-9]+){3}|[:0-9a-fA-F]+)',)),         # NOQA
        ('Number',  (r'-?(\.[0-9]+)|([0-9]+(\.[0-9]*)?)',)),            # NOQA
        ('String',  (r'(?P<quote>"|\').*?(?<!\\)(?P=quote)', DOTALL)),  # NOQA
    ]
    useless = ['Comment', 'NL', 'Space']
    t = make_tokenizer(specs)
    return [x for x in t(string) if x.type not in useless]


def parse(seq):
    """Sequence(Token) -> object"""
    id_tokens = ['Name', 'IPAddr', 'Number', 'String']

    tokval = lambda x: x.value
    op = lambda s: a(Token('Op', s)) >> tokval
    op_ = lambda s: skip(op(s))
    _id = some(lambda t: t.type in id_tokens) >> tokval
    keyword = lambda s: a(Token('Name', s)) >> tokval

    def make_peer(first, edge_type, second, followers, attrs):
        edges = [Edge(first, edge_type, second, attrs)]

        from_node = second
        for edge_type, to_node in followers:
            edges.append(Edge(from_node, edge_type, to_node, attrs))
            from_node = to_node

        return Peer(edges)

    def make_route(first, edge_type, second, followers, attrs):
        edges = [Edge(first, edge_type, second, attrs)]

        from_node = second
        for edge_type, to_node in followers:
            edges.append(Edge(from_node, edge_type, to_node, attrs))
            from_node = to_node

        return Route(edges)

    #
    # parts of syntax
    #
    node_list = (
        _id +
        many(op_(',') + _id)
        >> create_mapper(oneplus_to_list)
    )
    option_stmt = (
        _id +
        maybe(op_('=') + _id)
        >> create_mapper(Attr)
    )
    option_list = (
        maybe(op_('[') + option_stmt + many(op_(',') + option_stmt) + op_(']'))
        >> create_mapper(oneplus_to_list, default_value=[])
    )

    #  node statement::
    #     A;
    #     B [attr = value, attr = value];
    #
    node_stmt = (
        _id + option_list
        >> create_mapper(Node)
    )

    #  peer network statement::
    #     A -- B;
    #
    edge_stmt = (
        _id +
        op('--') +
        _id +
        many(op('--') + _id) +
        option_list
        >> create_mapper(make_peer)
    )

    #  attributes statement::
    #     default_shape = box;
    #     default_fontsize = 16;
    #
    attribute_stmt = (
        _id + op_('=') + _id
        >> create_mapper(Attr)
    )

    #  extension statement (class, plugin)::
    #     class red [color = red];
    #     plugin attributes [name = Name];
    #
    extension_stmt = (
        (keyword('class') | keyword('plugin')) +
        _id +
        option_list
        >> create_mapper(Extension)
    )

    #  group statement::
    #     group {
    #        A;
    #     }
    #
    group_inline_stmt = (
        attribute_stmt |
        node_stmt
    )
    group_inline_stmt_list = (
        many(group_inline_stmt + skip(maybe(op(';'))))
    )
    group_stmt = (
        skip(keyword('group')) +
        maybe(_id) +
        op_('{') +
        group_inline_stmt_list +
        op_('}')
        >> create_mapper(Group)
    )

    #  network statement::
    #     network {
    #        A;
    #     }
    #
    network_inline_stmt = (
        attribute_stmt |
        group_stmt |
        node_stmt
    )
    network_inline_stmt_list = (
        many(network_inline_stmt + skip(maybe(op(';'))))
    )
    network_stmt = (
        skip(keyword('network')) +
        maybe(_id) +
        op_('{') +
        network_inline_stmt_list +
        op_('}')
        >> create_mapper(Network)
    )

    #  route statement::
    #     route {
    #       A -> B -> C;
    #     }
    #
    route_inline_stmt = (
        _id +
        op_('->') +
        _id +
        many(op_('->') + _id) +
        option_list
        >> create_mapper(make_route)
    )
    route_stmt = (
        skip(keyword('route')) +
        maybe(_id) +
        op_('{') +
        network_inline_stmt_list +
        op_('}')
        >> create_mapper(Network)
    )

    #
    # diagram statement::
    #     nwdiag {
    #        A;
    #     }
    #
    diagram_id = (
        (keyword('diagram') | keyword('nwdiag')) +
        maybe(_id)
        >> list
    )
    diagram_inline_stmt = (
        extension_stmt |
        network_stmt |
        group_stmt |
        attribute_stmt |
        route_stmt |
        edge_stmt |
        node_stmt
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
