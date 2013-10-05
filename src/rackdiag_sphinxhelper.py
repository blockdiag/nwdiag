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

__all__ = [
    'core', 'utils'
]

import rackdiag.parser
import rackdiag.builder
import rackdiag.drawer
core = rackdiag

import rackdiag.utils.rst.nodes
import rackdiag.utils.rst.directives
utils = rackdiag.utils

import blockdiag.utils.bootstrap
utils.bootstrap = blockdiag.utils.bootstrap

import blockdiag.utils.compat
utils.compat = blockdiag.utils.compat

import blockdiag.utils.fontmap
utils.fontmap = blockdiag.utils.fontmap
