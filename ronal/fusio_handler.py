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
import logging
import os
import xml.etree.cElementTree as ElementTree

def _parse_xml(raw_xml):
    try:
        root = ElementTree.fromstring(raw_xml)
    except ElementTree.ParseError as e:
        raise Exception("invalid xml: {}".format(e.message))

    return root


def get_action_id_and_status(raw_xml):
    """
    Return a dictionary of ActionId and Status from the "info" api of Fusio
    Example:
    {
        '1607281547155684': 'Terminated',
        '1607281557392012': 'Working',
        '1607281600236970': 'Waiting',
        '1607281601141652': 'Waiting'
    }
    """
    root = _parse_xml(raw_xml)

    return {a.get('ActionId'): a.find('ActionProgression').get('Status') for a in root.iter('Action')}


def get_action_id(raw_xml):
    root = _parse_xml(raw_xml)
    action_id_element = root.find('ActionId')

    return None if action_id_element is None else action_id_element.text


def get_action_status(raw_xml, action_id):
    dict_action_status = get_action_id_and_status(raw_xml)

    return dict_action_status.get(action_id)


def to_fusio_date(datetime):
    """Convert a python date to fusio format: mm/dd/yyyy"""
    return datetime.strftime('%m/%d/%Y')


class FusioHandler(object):
    def __init__(self, config, stage, production_period):
        self.config = config
        self.stage = stage
        self.fusio_begin_date = to_fusio_date(production_period.start_validation_date)
        self.fusio_end_date = to_fusio_date(production_period.end_validation_date)
        self.production_period = production_period

    def _fusio_url(self):
        return '{}//cgi-bin/fusio.dll'.format(self.stage['fusio']['ihm_url'])

    def _call_fusio_api(self, api, **kwargs):
        rep = requests.get('{fusio}{api}'.format(fusio=self._fusio_url(), api=api),
                            data=kwargs)

        if rep.status_code != 200:
            raise Exception('fusio query failed: {}'.format(rep))

        logging.debug('reponse  {}'.format(rep.content))
        return get_action_id(rep.content)

    def _call_fusio_api_and_wait(self, api, **kwargs):
        action = self._call_fusio_api(api, **kwargs)

        # TODO fassi :)
        # we need to call fusio to get the status of this action
        # and retry until this action is finished (and raise an error if the action fail)

    def _call_fusio_ihm(self, url, files):
        try:
            logging.debug('request to fusio ihm with {}'.format(url))
            response = requests.post(url, files=files)
        except requests.exceptions.ConnectionError:
            logging.exception('error connecting: url {}'.format(url))
            return None
        except requests.RequestException:
            logging.exception('error sending data from fusio')
            return None
        else:
            if response.status_code == 200:
                return response
            else:
                logging.error('error sending from fusio: status code {}'.format(
                    response.status_code))
                return None

    def publish(self):
        self._data_update(self.config['backup_dir'])

        self._regional_import()

        self._set_to_preproduction()

        if not self.stage['is_testing']:
            self._set_to_production()
        logging.info('data published')

    def _data_update(self, backup_dir):

        files = [os.path.join(backup_dir, filename) for filename in os.listdir(backup_dir)]

        if len(files) != 1:
            logging.info('it must have a file')
            return None
        file_to_post = {'file1': (backup_dir, open(files[0], 'rb'), 'application/octet-stream')}

        payload = {
            'CSP_IDE': '{}'.format(self.config['fusio']['contributor_id']),
            'action': 'dataupdate',
            'dutype': 'update',
            'serviceid': '{}'.format(self.config['fusio']['service_id']),
            'MAX_FILE_SIZE': '2000000',
            'isadapted': '0',
            'libelle': '{}'.format('unlibelle'),
            'date_deb': '{}'.format(self.fusio_begin_date),
            'date_fin': '{}'.format(self.fusio_end_date),
            'login': '{}'.format(self.stage['fusio']['ihm_login']),
            'password': '{}'.format(self.stage['fusio']['ihm_password'])
        }
        import urllib
        fusio_url = '{url_ihm_fusio}/AR_Response.php?{query}'.format(url_ihm_fusio=self.stage['fusio']['ihm_url'], query=urllib.urlencode(payload))

        return self._call_fusio_ihm(fusio_url, file_to_post)


    def _regional_import(self):
        self._call_fusio_api(api='/api',
                             action='regionalimport',
                             DataDebut=self.fusio_begin_date,
                             DateFin=self.fusio_end_date)

    def _set_to_preproduction(self):
        logging.info('pushing the data to preprod')
        self._call_fusio_api_and_wait('/api', action='settopreproduction')

    def _set_to_production(self):
        logging.info('pushing the data to prod')
        self._call_fusio_api_and_wait('/api', action='settoproduction')
