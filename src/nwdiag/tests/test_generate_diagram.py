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
import nwdiag.command
from blockdiag.tests.test_generate_diagram import (
    get_diagram_files, testcase_generator
)


def test_generate():
    mainfunc = nwdiag.command.main
    basepath = os.path.dirname(__file__)
    files = get_diagram_files(basepath)
    options = []

    for testcase in testcase_generator(basepath, mainfunc, files, options):
        yield testcase
