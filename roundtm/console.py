#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# RoundTM - A Round based Tournament Manager
# Copyright (c) 2013 Rémi Alvergnat <toilal.dev@gmail.com>
#
# RoundTM is free software; you can redistribute it and/or modify it under
# the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# RoundTM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.
#
# You should have received a copy of the Lesser GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import unicode_literals
from .events import Event


class Console(object):
    """Controls an Event with console."""
    def __init__(self, event):
        self._event = event

    def next_round(self):
        """Go to next round, using the provided strategy"""
        return self._event.next_round()

    def ranking(self):
        """Display current ranking"""
        i = 1
        for stat in self._event.ranking():
            print "[%s] %s" % (i, stat)
            i += 1


def load(path):
    """Load a project in console mode.

    :return: class `Console`, a control object for console usage (IPython)
    """
    return Console(Event(path))
