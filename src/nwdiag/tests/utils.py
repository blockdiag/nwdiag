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

import os

from blockdiag.tests.utils import BuilderTestCase as BlockdiagBuilderTestCase

from nwdiag.builder import ScreenNodeBuilder
from nwdiag.parser import parse_file


class BuilderTestCase(BlockdiagBuilderTestCase):
    def build(self, filename):
        basedir = os.path.dirname(__file__)
        pathname = os.path.join(basedir, 'diagrams', filename)
        return ScreenNodeBuilder.build(parse_file(pathname))
