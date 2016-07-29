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

import xml.dom.minidom


def get_action_id(xml_stream):
    dom = xml.dom.minidom.parse(xml_stream)
    node = dom.getElementsByTagName("ActionId")
    if len(node) is 0:
        return None
    return node[0].firstChild.nodeValue

class FusioHandler(object):
    def __init__(self, config):
        self.config = config

    # http://bob/cgi-bin/fusio.dll/api?\
    # API?action=dataupdate&contributorid=5&dutype=update&serviceid=3&libelle=maj auto\
    # &DateDebut=01/01/2016&DateFin=31/12/2016&filename=http://bob//receivedFile/maj_auto.zip
    def data_update(self):
        pass

    # http://bob/cgi-bin/fusio.dll/api?\
    # API?action=regionalimport&DateDebut=01/06/2016&DateFin=31/08/2016
    def regional_import(self):
        pass

    # http://bob/cgi-bin/fusio.dll/api?\
    # API?action=settopreproduction
    def set_to_preproduction(self):
        pass

    # http://bob/cgi-bin/fusio.dll/api?\
    # API?action=settoproduction
    def set_to_production(self):
        pass

    # http://bob/cgi-bin/fusio.dll/info
    def get_status(self, action_id):
        pass

