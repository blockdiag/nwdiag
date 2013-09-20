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

from __future__ import division


def gcd(*args):
    if len(args) == 0:
        return 0
    elif len(args) == 1:
        return args[0]
    elif len(args) == 2:
        if args[1] == 0:
            return args[0]
        else:
            return gcd(args[1], args[0] % args[1])
    else:
        return gcd(gcd(*args[:-1]), args[-1])


def lcm(*args):
    if len(args) == 0:
        return 0
    elif len(args) == 1:
        return args[0]
    elif len(args) == 2:
        return args[0] * args[1] // gcd(*args)
    else:
        return lcm(lcm(*args[:-1]), args[-1])
