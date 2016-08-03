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
import requests


def get_action_id(xml_stream):
    dom = xml.dom.minidom.parse(xml_stream)
    node = dom.getElementsByTagName("ActionId")
    if len(node) is 0:
        return None
    return node[0].firstChild.nodeValue


def get_action_status(xml_stream, action_id):
    dom = xml.dom.minidom.parse(xml_stream)
    action_node = [node for node in dom.getElementsByTagName("Action") if node.getAttribute("ActionId") == action_id]
    if not action_node:
        return None
    action_progress = [node for node in action_node[0].childNodes if node.nodeName == 'ActionProgression']
    if not action_progress:
        return None
    return action_progress[0].getAttribute("Status")


def to_fusio_date(end_validation_date):
    """Convert a python date to fusio format: mm/dd/yyyy"""
    raise NotImplementedError


class FusioHandler(object):
    def __init__(self, config, stage, production_period):
        self.config = config
        self.stage = stage
        self.fusio_begin_date = to_fusio_date(production_period.start_validation_date)
        self.fusio_end_date = to_fusio_date(production_period.end_validation_date)
        self.production_period = production_period

    def _call_fusio_api(self, **kwargs):
        requests.post(self.stage['fusio_api'], **kwargs)

    def publish(self):
        self._data_update()

        self._regional_import()

        self._set_to_preproduction()

        if not self.stage.is_testing:
            self._set_to_production()

    def _data_update(self):
        """
        POST http://fusio_ihm/AR_UpdateData.php?dutype=update&CSP_IDE=5&serviceid=1
 + 'libelle service' (ronal_ + current dt ?)

        we post a file:
        files = {"file1": (zip_file_name, open(zip_dest_full_path, 'rb'), 'application/octet-stream')}

        """
        pass

    # http://bob/cgi-bin/fusio.dll/api?\
    # API?action=regionalimport&DateDebut=01/06/2016&DateFin=31/08/2016
    def _regional_import(self):
        self._call_fusio_api(action='regionalimport',
                             DataDebut=self.fusio_begin_date,
                             DateFin=self.fusio_end_date)

    # http://bob/cgi-bin/fusio.dll/api?\
    # API?action=settopreproduction
    def _set_to_preproduction(self):
        pass

    # http://bob/cgi-bin/fusio.dll/api?\
    # API?action=settoproduction
    def _set_to_production(self):
        pass

    # http://bob/cgi-bin/fusio.dll/info
    def _get_status(self):
        pass

