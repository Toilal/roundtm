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


class InvalidResults(Exception):
    pass


class ReprMixin(object):
    """Mixin for quick __repr__ implementation based on attributes"""
    def __repr__impl__(self):
        return None

    def __repr__(self):
        return "<%s>" % self.__class__.__name__


class Participant(ReprMixin):
    """A Participant"""
    def __init__(self, firstName, lastName=None, women=False):
        if not lastName and firstName.index(' ') > -1:
            fullname = firstName.split(' ', 2)
            self.firstName = fullname[0]
            self.lastName = fullname[1]
        else:
            self.firstName = firstName
            self.lastName = lastName
        self.women = women

    @property
    def fullname(self):
        return self.firstName + ((" " + self.lastName) if self.lastName else "")

    def __repr__(self):
        return ReprMixin.__repr__(self) + " " + "{} {}".format(self.firstName, self.lastName)


class EventConfiguration(ReprMixin):
    """An Event"""
    def __init__(self, name, areas, generator='random', participant_count_per_team=1, team_count_per_match=2):
        self.name = name
        self.areas = areas
        self.generator = generator
        self.participant_count_per_team = participant_count_per_team
        self.team_count_per_match = team_count_per_match

    def __repr__(self):
        return ReprMixin.__repr__(self) + " " + "{} {}".format(self.name, self.areas)


class Team(ReprMixin):
    """A Team"""
    def __init__(self, *participants):
        self.participants = list(participants)

    @property
    def fullname(self):
        return "+".join([p.fullname for p in self.participants])

    def __eq__(self, y):
        for participant in self.participants:
            if not participant in y.participants:
                return False
        return True

    def __hash__(self):
        h = 1247
        for participant in self.participants:
            h = h + hash(participant)
        return h

    def __repr__(self):
        return ReprMixin.__repr__(self) + " " + "{}".format(self.participants,)


class Match(ReprMixin):
    """A Match"""
    def __init__(self, area, *teams):
        self.area = area
        self.teams = list(teams)
        self.result = []

    def best_team(self):
        best_i = None
        best_team = None
        for i in xrange(0, min(len(self.teams), len(self.result))):
            if best_i is None or self.result[i] > self.result[best_i]:
                best_team = self.teams[i]
                best_i = i
        return best_team

    def team_result(self, team):
        return self.result[self.teams.index(team)]

    def participant_result(self, participant):
        team = None
        for c_team in self.teams:
            if participant in c_team.participants:
                team = c_team
                break
        if team:
            return self.team_result(team)
        return None

    def check_results(self, round):
        if not self.result:
            raise InvalidResults("Empty result: %s - %s" % (round, self))
        if len(self.result) != len(self.teams):
            raise InvalidResults("Invalid result size: %s - %s" % (round, self))

    def __repr__(self):
        return ReprMixin.__repr__(self) + " " + "{} {} Result:{}".format(self.area, self.teams, self.result)


class Area(ReprMixin):
    """An Area"""
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return ReprMixin.__repr__(self) + " " + "{}".format(self.name)
