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


class Stats(object):
    """Stats for a participant or a team"""
    def __init__(self, source, points=0, wins=0, rounds=0):
        self.source = source
        self.points = points
        self.wins = wins
        self.rounds = rounds

    @property
    def points_ratio(self):
        return (float(self.points) / self.rounds) if self.rounds else 0

    @property
    def wins_ratio(self):
        return (float(self.wins) / self.rounds) if self.rounds else 0

    def __cmp__(self, other):
        if self.wins_ratio == other.wins_ratio:
            if self.points_ratio == other.points_ratio:
                if self.rounds == other.rounds:
                    return 0
                elif self.rounds < other.rounds:
                    return -1
                else:
                    return 0
            elif self.points_ratio > other.points_ratio:
                return -1
            else:
                return 1
        elif self.wins_ratio > other.wins_ratio:
            return -1
        else:
            return 1

    def __repr__(self):
        return "{0} (wins:{1} [{2:.0f}%], rounds:{3}, points:{4} [{5}])".format(self.source.fullname, self.wins, self.wins_ratio * 100, self.rounds, self.points, self.points_ratio)
