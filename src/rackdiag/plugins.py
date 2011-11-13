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

from blockdiag.plugins import NodeHandler


class NodeAttributes(NodeHandler):
    def __init__(self, diagram, **kwargs):
        super(NodeAttributes, self).__init__(diagram, **kwargs)

        Unit = diagram._DiagramNode
        for name, label in kwargs.items():
            if label is None:
                label = name
            if name not in Unit.desctable:
                Unit.desctable.insert(-1, name)

            Unit.attrname[name] = label
            setattr(Unit, name, None)
