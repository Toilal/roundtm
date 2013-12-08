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


from .objects import Match, Team

from random import shuffle

import abc


class Generator(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def generate(self, event):
        """Generates a list of matches for a round.

        :return: list of matches"""
        return []


class Random(Generator):
    def generate(self, event):
        matches = Generator.generate(self, event)

        participants = list(event.participants)
        shuffle(participants)

        for area in event.configuration.areas:
            if len(participants) >= event.configuration.participant_count_per_team * event.configuration.team_count_per_match:
                teams = []
                for i in xrange(0, event.configuration.team_count_per_match):
                    team_participants = []
                    for j in xrange(0, event.configuration.participant_count_per_team):
                        team_participants.append(participants.pop())
                    teams.append(Team(*team_participants))

                match = Match(area, *teams)
                matches.append(match)
            else:
                break

        return matches


class GeneratorManager(object):
    def __init__(self):
        self.generators = {'random': Random()}

    def get(self, generator):
        return self.generators[generator]

manager = GeneratorManager()
