# Copyright (c) 2001-2016, Canal TP and/or its affiliates. All rights reserved.
#
# This file is part of Navitia,
#     the software to build cool stuff with public transport.
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
import logging
import os
import shutil
import requests
from ronal.fusio_handler import FusioHandler


def call_navitia(url, auth=()):
    try:
        response = requests.get(url, auth=auth)
    except requests.exceptions.ConnectionError:
        logging.exception('error connecting: url {}'.format(url))
        return None
    except requests.RequestException:
        logging.exception('error fetching from navitia the last dataset production period')
        return None
    else:
        if response.status_code == 200:
            return response
        else:
            logging.error('error fetching from navitia the last dataset production period: status code {}'.format(
                response.status_code))
            return None


def create_dir(directory):
    """create directory if needed"""
    if not os.path.exists(directory):
        os.makedirs(directory)


def _create_production_period(datasets):
    dataset = next(iter(datasets.get('datasets', [])), None)
    if dataset:
        start_validation_date = dataset.get('start_validation_date')
        end_validation_date = dataset.get('end_validation_date')
        return ProductionPeriod(start_validation_date, end_validation_date)
    raise Exception('error fetching from navitia the last dataset production period: no datasets')


class ProductionPeriod(object):
    def __init__(self, start_validation_date, end_validation_date):
        from datetime import datetime

        self.start_validation_date = datetime.strptime(start_validation_date, '%Y%m%dT%H%M%S')
        self.end_validation_date =  datetime.strptime(end_validation_date, '%Y%m%dT%H%M%S')


class Handler(object):
    def __init__(self, config):
        self.config = config

    def route_data(self, files):
        self.backup_files(files)

        important_modification = self.is_important_data_modification(files)

        self.route_to_stage(important_modification)

    def backup_files(self, files):
        """
        backup file to file system (without history for the moment)
        """
        output_dir = self.config.get('output_dir')
        create_dir(output_dir)

        for filename in files:
            shutil.move(filename, output_dir)

    def is_important_data_modification(self, files):
        """
        return True is the data update is small enough to be put in production without a manual testing
        """
        return True

    def get_last_dataset_production_date(self, stage):
        """
        fetch from a navitia contibutor datasets the production period
        """
        navitia_parameters = stage['navitia']
        coverage = self.config['coverage']
        contributor_id = self.config['contributor_id']
        navitia_url = '{base_url}/v1/coverage/{coverage}/contributors/{contrib}/datasets'\
            .format(base_url=navitia_parameters['url'], coverage=coverage, contrib=contributor_id)
        navitia_url_auth = (navitia_parameters.get('token'), '')
        navitia_response = call_navitia(navitia_url, navitia_url_auth)

        return _create_production_period(navitia_response.json())

    def get_stage(self, important_modification):
        if important_modification:
            stage = self.config.get('stage', {}).get('testing')
            stage['is_testing'] = True
        else:
            stage = self.config.get('stage', {}).get('production')
            stage['is_testing'] = False
        return stage

    def route_to_stage(self, important_modification):
        stage = self.get_stage(important_modification)
        logging.info('routing to {}'.format(stage))

        # fetch from navitia the last datasets production period of a given contributor
        last_production_date = self.get_last_dataset_production_date(stage)
        logging.debug(last_production_date)

        fusio_handler = FusioHandler(self.config, stage, last_production_date)

        fusio_handler.publish()
