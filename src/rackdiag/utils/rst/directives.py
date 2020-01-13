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

from blockdiag.utils.compat import cmp_to_key
from blockdiag.utils.rst import directives
from docutils.parsers import rst

from rackdiag.elements import RackItem
from rackdiag.utils.rst.nodes import rackdiag as rackdiag_node

directive_options_default = dict(format='PNG',
                                 antialias=False,
                                 fontpath=None,
                                 outputdir=None,
                                 nodoctype=False,
                                 noviewbox=False,
                                 inline_svg=False,
                                 ignore_pil=False)
directive_options = {}


class RackdiagDirective(directives.BlockdiagDirective):
    name = "rackdiag"
    node_class = rackdiag_node

    @property
    def global_options(self):
        return directive_options

    def description_table(self, diagram):
        nodes = diagram.traverse_nodes
        widths = [25] + [50] * (len(RackItem.desctable) - 1)
        headers = [RackItem.attrname[name] for name in RackItem.desctable]

        descriptions = [n.to_desctable() for n in nodes()]
        descriptions.sort(key=cmp_to_key(directives.cmp_node_number))

        # records for total
        total = ['-', 'Total'] + [''] * (len(RackItem.desctable) - 2)
        total[2] = "%dU" % sum(n.colheight for n in nodes() if n.colheight)
        total[3] = "%.1fA" % sum(n.ampere for n in nodes() if n.ampere)
        total[4] = "%.1fkg" % sum(n.weight for n in nodes() if n.weight)
        descriptions.append(total)

        for i in range(len(headers) - 1, -1, -1):
            if any(desc[i] for desc in descriptions):
                pass
            else:
                widths.pop(i)
                headers.pop(i)
                for desc in descriptions:
                    desc.pop(i)

        return self._description_table(descriptions, widths, headers)


def setup(**kwargs):
    for key, value in directive_options_default.items():
        directive_options[key] = kwargs.get(key, value)

    rst.directives.register_directive("rackdiag", RackdiagDirective)
