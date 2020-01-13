# -*- coding: utf-8 -*-
#  Copyright 2011 Takeshi KOMIYA
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from __future__ import print_function

import os
import unittest

from rackdiag.builder import ScreenNodeBuilder
from rackdiag.parser import parse_string


def build(filename):
    def decorator(fn):
        def func(self):
            testdir = os.path.dirname(__file__)
            pathname = os.path.join(testdir, 'diagrams', filename)

            code = open(pathname).read()
            tree = parse_string(code)
            self.diagram = ScreenNodeBuilder.build(tree)

            return fn(self)

        func.__name__ = fn.__name__
        return func

    return decorator


class TestBuildDiagram(unittest.TestCase):
    def assertAttributes(self, **attributes):
        for rack in self.diagram.racks:
            for node in rack.nodes:
                print(node, node.label)

                for key, attribute in attributes.items():
                    value = attribute.get(node.label)
                    self.assertEqual(value, getattr(node, key))

    @build('simple.diag')
    def test_simple(self):
        positions = {'server 1': (0, 41),
                     'server 2': (0, 40),
                     'server 3': (0, 39),
                     'server 4': (0, 38)}

        self.assertAttributes(xy=positions)

    @build('autonumber.diag')
    def test_autonumber(self):
        positions = {'server 1': (0, 41),
                     'server 2': (0, 40),
                     'server 3': (0, 38),
                     'server 4': (0, 37)}

        self.assertAttributes(xy=positions)

    @build('multi_rackitem.diag')
    def test_multi_rackitem(self):
        positions = {'UPS 1': (0, 9), 'UPS 2': (6, 9),
                     'server 1': (0, 8), 'server 2': (3, 7),
                     'server 3': (0, 6), 'server 4': (3, 5),
                     'server 5': (6, 5), 'server 6': (9, 5),
                     'server 7': (0, 2), 'server 8': (4, 3),
                     'server 9': (8, 3)}
        colheights = {'UPS 1': 3, 'UPS 2': 3,
                      'server 1': 1, 'server 2': 2,
                      'server 3': 2, 'server 4': 2,
                      'server 5': 2, 'server 6': 2,
                      'server 7': 3, 'server 8': 1,
                      'server 9': 1}

        self.assertAttributes(xy=positions, colheight=colheights)

    @build('multi_racks.diag')
    def test_multi_racks(self):
        positions = {'server 1': (0, 41), 'server 2': (0, 40),
                     'server 3': (0, 39), 'server 4': (0, 38),
                     'server 5': (1, 41), 'server 6': (1, 40),
                     'server 7': (1, 39), 'server 8': (1, 38)}

        self.assertAttributes(xy=positions)
