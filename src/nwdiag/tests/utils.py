# -*- coding: utf-8 -*-

import os
from nwdiag.builder import ScreenNodeBuilder
from nwdiag.parser import parse_file
from blockdiag.tests.utils import BuilderTestCase as BlockdiagBuilderTestCase


class BuilderTestCase(BlockdiagBuilderTestCase):
    def build(self, filename):
        basedir = os.path.dirname(__file__)
        pathname = os.path.join(basedir, 'diagrams', filename)
        return ScreenNodeBuilder.build(parse_file(pathname))
