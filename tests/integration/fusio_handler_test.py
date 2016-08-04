# coding=utf-8
# Copyright (c) 2001-2016, Canal TP and/or its affiliates. All rights reserved.
#
# This file is part of Navitia,
# the software to build cool stuff with public transport.
#
# Hope you'll enjoy and contribute to this project,
#     powered by Canal TP (www.canaltp.fr).
# Help us simplify mobility and open public transport:
#     a non ending quest to the responsive locomotion way of traveling!
#
# LICENCE: This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Stay tuned using
# twitter @navitia
# IRC #navitia on freenode
# https://groups.google.com/d/forum/navitia
# www.navitia.io

import pytest
from ronal import fusio_handler


@pytest.fixture(scope="module")
def data_update():
    return """<?xml version="1.0" encoding="ISO-8859-1"?>
        <serverfusio>
            <address/>
            <version>Version 1.10.85.200</version>
            <sendaction>dataupdate</sendaction>
            <result>-1</result>
            <ActionId>1607281547155684</ActionId>
        </serverfusio>"""


@pytest.fixture(scope="module")
def regional_import():
    return """<?xml version="1.0" encoding="ISO-8859-1"?>
        <serverfusio>
            <address/>
            <version>Version 1.10.85.200</version>
            <sendaction>regionalimport</sendaction>
            <result>-1</result>
            <ActionId>1607281557392012</ActionId>
        </serverfusio>"""


@pytest.fixture(scope="module")
def preproduction():
    return """<?xml version="1.0" encoding="ISO-8859-1"?>
        <serverfusio>
            <address/>
            <version>Version 1.10.85.200</version>
            <sendaction>settopreproduction</sendaction>
            <result>-1</result>
            <ActionId>1607281600236970</ActionId>
        </serverfusio>"""


@pytest.fixture(scope="module")
def production():
    return """<?xml version="1.0" encoding="ISO-8859-1"?>
        <serverfusio>
            <address/>
            <version>Version 1.10.85.200</version>
            <sendaction>settoproduction</sendaction>
            <result>-1</result>
            <ActionId>1607281601141652</ActionId>
        </serverfusio>"""


@pytest.fixture(scope="module")
def info():
    return """<?xml version="1.0" encoding="ISO-8859-1"?>
        <Info title="Information sur projet régional">
            <ActionList ActionCount="4" TerminatedCount="1" WaitingCount="2" AbortedCount="0" WorkingCount="1" \
            ThreadSuspended="False">
                <Action ActionType="Mise à jour" ActionCaption="dataupdate" \
                ActionDesc="" Contributor="NAN - Nantes Métropole (TAN)" ContributorId="5" \
                ActionId="1607281547155684" LastError="">
                    <PostDate><Year>2016</Year><Month>07</Month><Day>28</Day></PostDate>
                    <PostTime><Hour>15</Hour><Minute>47</Minute><Second>15</Second></PostTime>
                    <WorkStartDate><Year>2016</Year><Month>07</Month><Day>28</Day></WorkStartDate>
                    <WorkStartTime><Hour>15</Hour><Minute>47</Minute><Second>17</Second></WorkStartTime>
                    <MiddleDuration><Day>0</Day><Hour>00</Hour><Minute>00</Minute><Second>00</Second></MiddleDuration>
                    <WorkDuration><Day>0</Day><Hour>00</Hour><Minute>03</Minute><Second>09</Second></WorkDuration>
                    <ActionProgression Status="Terminated" Description="" StepCount="5" CurrentStep="5"/>
                </Action>
                <Action ActionType="Import" ActionCaption="regionalimport" \
                ActionDesc="Chargement des données topologiques" Contributor="" ContributorId="-1" \
                ActionId="1607281557392012" LastError="">
                    <PostDate><Year>2016</Year><Month>07</Month><Day>28</Day></PostDate>
                    <PostTime><Hour>15</Hour><Minute>57</Minute><Second>39</Second></PostTime>
                    <WorkStartDate><Year>2016</Year><Month>07</Month><Day>28</Day></WorkStartDate>
                    <WorkStartTime><Hour>15</Hour><Minute>57</Minute><Second>39</Second></WorkStartTime>
                    <MiddleDuration><Day>0</Day><Hour>00</Hour><Minute>00</Minute><Second>00</Second></MiddleDuration>
                    <WorkDuration><Day>0</Day><Hour>00</Hour><Minute>00</Minute><Second>00</Second></WorkDuration>
                    <ActionProgression Status="Working" Description="" StepCount="25" CurrentStep="1"/>
                </Action>
                <Action ActionType="Mise en pré-production" ActionCaption="settopreproduction" \
                ActionDesc="" Contributor="" ContributorId="-1" ActionId="1607281600236970" LastError="">
                    <PostDate><Year>2016</Year><Month>07</Month><Day>28</Day></PostDate>
                    <PostTime><Hour>16</Hour><Minute>00</Minute><Second>23</Second></PostTime>
                    <WorkStartDate><Year>1899</Year><Month>12</Month><Day>30</Day></WorkStartDate>
                    <WorkStartTime><Hour>00</Hour><Minute>00</Minute><Second>00</Second></WorkStartTime>
                    <MiddleDuration><Day>0</Day><Hour>00</Hour><Minute>00</Minute><Second>00</Second></MiddleDuration>
                    <WorkDuration><Day>0</Day><Hour>00</Hour><Minute>00</Minute><Second>00</Second></WorkDuration>
                    <ActionProgression Status="Waiting" Description="" StepCount="0" CurrentStep="0"/>
                </Action>
                <Action ActionType="Mise en production" ActionCaption="settoproduction" \
                ActionDesc="" Contributor="" ContributorId="-1" ActionId="1607281601141652" LastError="">
                    <PostDate><Year>2016</Year><Month>07</Month><Day>28</Day></PostDate>
                    <PostTime><Hour>16</Hour><Minute>01</Minute><Second>14</Second></PostTime>
                    <WorkStartDate><Year>1899</Year><Month>12</Month><Day>30</Day></WorkStartDate>
                    <WorkStartTime><Hour>00</Hour><Minute>00</Minute><Second>00</Second></WorkStartTime>
                    <MiddleDuration><Day>0</Day><Hour>00</Hour><Minute>00</Minute><Second>00</Second></MiddleDuration>
                    <WorkDuration><Day>0</Day><Hour>00</Hour><Minute>00</Minute><Second>00</Second></WorkDuration>
                    <ActionProgression Status="Waiting" Description="" StepCount="0" CurrentStep="0"/>
                </Action>
            </ActionList>
        </Info>"""


@pytest.fixture(scope="module")
def invalid_xml():
    return """<?xml version="1.0" encoding="ISO-8859-1"?>
        <serverfusio>
            <address/>
            <version>Version 1.10.85.200</version>
            <sendaction>settoproduction</sendaction>
            <result>-1</result>
            <ActionId>1607281601141652</ActionId>
        """


@pytest.fixture(scope="module")
def no_action():
    return """<?xml version="1.0" encoding="ISO-8859-1"?>
        <Info title="Information sur projet régional">
            <ActionList ThreadSuspended="False" WorkingCount="0" AbortedCount="0" WaitingCount="0" \
            TerminatedCount="0" ActionCount="0"/>
        </Info>"""


def test_parse_xml(info, invalid_xml):
    from xml.etree.cElementTree import Element
    assert isinstance(fusio_handler._parse_xml(info), Element)

    with pytest.raises(Exception):
        fusio_handler._parse_xml(invalid_xml)


def test_get_action_id(data_update, regional_import, preproduction, production, no_action):
    assert fusio_handler.get_action_id(data_update) == '1607281547155684'
    assert fusio_handler.get_action_id(regional_import) == '1607281557392012'
    assert fusio_handler.get_action_id(preproduction) == '1607281600236970'
    assert fusio_handler.get_action_id(production) == '1607281601141652'
    assert fusio_handler.get_action_id(no_action) is None


def test_get_action_status(info):
    # dataupdate
    assert fusio_handler.get_action_status(info, '1607281547155684') == 'Terminated'
    assert fusio_handler.get_action_status(info, '1607281557392012') == 'Working'
    assert fusio_handler.get_action_status(info, '1607281600236970') == 'Waiting'
    assert fusio_handler.get_action_status(info, '1607281601141652') == 'Waiting'
    assert fusio_handler.get_action_status(info, '0123456789') is None


def test_get_action_id_and_status(info, no_action):
    expected = {
        '1607281547155684': 'Terminated',
        '1607281557392012': 'Working',
        '1607281600236970': 'Waiting',
        '1607281601141652': 'Waiting'
    }

    assert fusio_handler.get_action_id_and_status(info) == expected
    assert fusio_handler.get_action_id_and_status(no_action) == {}
