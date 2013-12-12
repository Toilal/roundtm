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

import logging


import yaml
import os

from .objects import Participant, Match, Team, Area, EventConfiguration,\
    ReprMixin
from .generators import manager
from .stats import Stats
from roundtm.objects import InvalidResults

log = logging.getLogger(__name__)


class Event(object):
    """Load and save everything related to an event."""
    def __init__(self, path):
        self.path = path
        self._load()

    def next_round(self):
        """Go to next round, using the provided generator"""
        # reload everything
        self._load()
        self.check_results()

        generator = manager.get(self.configuration.generator)
        matches = generator.generate(self)

        round = self._add_round(matches)

    def ranking(self):
        self._load()
        participants_stats, team_stats = self._stats()
        participants_stats.sort(cmp=Stats.__cmp__)
        return participants_stats

    def check_results(self):
        for previous_round in self.rounds:
            previous_round.check_results()

    def _stats(self):
        self._load()

        participants_stats = {}
        teams_stats = {}

        for round in self.rounds:
            try:
                round.check_results()
            except InvalidResults as e:
                log.warn("Skip %s, %s" % (round, e))
                continue
            inactive_participants = set(round.participants)
            for match in round.matches:
                best_team = match.best_team()
                for i in xrange(0, min(len(match.teams), len(match.result))):
                    result = match.result[i]
                    team = match.teams[i]
                    team_stats = teams_stats.get(team)
                    if not team_stats:
                        team_stats = Stats(team)
                        teams_stats[team] = team_stats
                    team_stats.points = team_stats.points + result
                    if team == best_team:
                        team_stats.wins = team_stats.wins + 1
                    team_stats.rounds = team_stats.rounds + 1
                    for participant in team.participants:
                        inactive_participants.remove(participant)
                        participant_stats = participants_stats.get(participant)
                        if not participant_stats:
                            participant_stats = Stats(participant)
                            participants_stats[participant] = participant_stats
                        participant_stats.points = participant_stats.points + result
                        if team == best_team:
                            participant_stats.wins = participant_stats.wins + 1
                        participant_stats.rounds = participant_stats.rounds + 1

            for inactive_participant in inactive_participants:
                participant_stats = participants_stats.get(inactive_participant)
                if not participant_stats:
                    participant_stats = Stats(inactive_participant)
                    participants_stats[inactive_participant] = participant_stats
                participant_stats.inactive_rounds = participant_stats.inactive_rounds + 1

        return list(participants_stats.values()), list(teams_stats.values())

    def _load(self):
        """Loads data from filesystem. If not exists, the project will be created."""
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.configuration = self._load_event_configuration()
        self.participants = self._load_participants()
        self._participants_dict = {}
        for participant in self.participants:
            self._participants_dict[participant.fullname] = participant
        self.rounds = self._load_rounds()
        log.info("Project loaded: %s, %i participants, %i rounds" % (self.configuration, len(self.participants), len(self.rounds)))

    def _save(self):
        """Save data to filesystem."""
        self._save_event()
        self._save_participants()
        self._save_rounds()
        log.info("Project saved: %s, %i participants, %i rounds" % (self.configuration, len(self.participants), len(self.rounds)))

    def _load_event_configuration(self):
        with open(os.path.join(self.path, 'configuration.yaml')) as f:
            event_yaml = yaml.load(f)
            area_names = event_yaml.pop('areas')
            areas = []
            for area_name in area_names:
                area = Area(area_name)
                areas.append(area)
            return EventConfiguration(areas=areas, **event_yaml)

    def _load_participants(self):
        with open(os.path.join(self.path, 'participants.yaml')) as f:
            participants = []
            participants_yaml = yaml.load(f)
            for participant_yaml in participants_yaml:
                p = None
                if isinstance(participant_yaml, dict):
                    p = Participant(**participant_yaml)
                else:
                    p = Participant(participant_yaml)
                participants.append(p)
            return participants

    def _load_rounds(self):
        i = 1
        rounds = []
        while True:
            if Round.exists(self.path, i):
                rounds.append(Round(self, i))
            else:
                break
            i += 1
        return rounds

    def _save_event_configuration(self):
        with open(os.path.join(self.path, 'configuration.yaml'), 'w') as f:
            data = {}
            data["name"] = self.configuration.name
            data["areas"] = [area.name for area in self.configuration.areas]
            yaml.safe_dump(data, f)

    def _save_participants(self):
        with open(os.path.join(self.path, 'participants.yaml'), 'w') as f:
            data = []
            for participant in self.participants:
                data.append(participant.firstName + ((" " + participant.lastName) if participant.lastName else ""))
            yaml.safe_dump(data, f)

    def _save_rounds(self):
        for round_project in self.rounds:
            round_project.save()

    def _add_round(self, matches):
        round_project = Round(self, len(self.rounds) + 1)
        for match in matches:
            round_project.add_match(match)
        round_project._save()
        self.rounds.append(round_project)
        return round_project


class Round(ReprMixin):
    def __init__(self, project, number):
        self.project = project
        self.number = number
        self._load()

    def check_results(self):
        for match in self.matches:
            match.check_results(self)

    def add_match(self, match):
        self.matches.append(match)
        for team in match.teams:
            for participant in team.participants:
                self.participants.append(participant)

    @classmethod
    def filename(cls, filename, number):
        return '%i-%s' % (number, filename)

    @classmethod
    def exists(cls, path, number):
        return os.path.exists(os.path.join(path, Round.filename('matches.yaml', number)))

    def _load(self):
        if not os.path.exists(self.project.path):
            os.makedirs(self.project.path)
        self.matches, self.participants = self._load_matches()

    def _save(self):
        matches_data = []
        participants = []
        for participant in self.project.participants:
            participants.append(participant.fullname)
        data = {"matches": matches_data, "participants": participants}
        for match in self.matches:
            match_data = []
            match_data.append(match.area.name)
            for team in match.teams:
                team_data = []
                for participant in team.participants:
                    team_data.append(participant.fullname)
                match_data.append(team_data)
            match_data.append(match.result)
            matches_data.append(match_data)
        with open(os.path.join(self.project.path, Round.filename('matches.yaml', self.number)), 'w') as f:
            yaml.safe_dump(data, f)

    def _load_matches(self):
        """Load matches and participants from round matches.yaml file"""
        matches_path = os.path.join(self.project.path, Round.filename('matches.yaml', self.number))
        if os.path.exists(matches_path):
            with open(os.path.join(self.project.path, Round.filename('matches.yaml', self.number))) as f:
                matches = []
                data_yaml = yaml.load(f)
                matches_yaml = data_yaml["matches"]
                participants_yaml = data_yaml["participants"]
                for match_yaml in matches_yaml:
                    area = match_yaml.pop(0)
                    result = match_yaml.pop(len(match_yaml) - 1)

                    teams = []
                    for team in match_yaml:
                        participants = []
                        for participant_name in team:
                            participant = self.project._participants_dict.get(participant_name)
                            if not participant:
                                participant = Participant(participant_name)
                            participants.append(participant)
                        teams.append(Team(*participants))
                    match = Match(area, *teams)
                    match.result = result
                    matches.append(match)

                participants = []
                for participant_name in participants_yaml:
                    participant = self.project._participants_dict.get(participant_name)
                    if not participant:
                        participant = Participant(participant_name)
                    participants.append(participant)
                return matches, participants
        else:
            return [], []

    def __repr__(self):
        return ReprMixin.__repr__(self) + " " + "{}".format(self.number)
