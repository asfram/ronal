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
        logging.exception(
            'error fetching from navitia the last dataset production period')
        return None
    else:
        if response.status_code == 200:
            return response
        else:
            logging.error('error fetching from navitia the last dataset production period: status code {}'.format(
                response.status_code))
            return None


def purge_dir(directory):
    """create directory if needed"""
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        files = [os.path.join(directory, filename)
                 for filename in os.listdir(directory)]
        for file in files:
            os.remove(file)


def _create_dataset_period(datasets):
    dataset = next(iter(datasets.get('datasets', [])), None)
    if dataset:
        start_validation_date = dataset.get('start_validation_date')
        end_validation_date = dataset.get('end_validation_date')
        return ProductionPeriod(start_validation_date, end_validation_date)
    raise Exception(
        'error fetching from navitia the last dataset production period: no datasets')

def _create_publication_period(navitia_response):
    start_validation_date = navitia_response['status']['start_production_date']
    end_validation_date = navitia_response['status']['end_production_date']
    return ProductionPeriod(start_validation_date, end_validation_date)

class ProductionPeriod(object):

    def __init__(self, start_validation_date, end_validation_date):
        from datetime import datetime

        if len(start_validation_date)>8:
            self.start_validation_date = datetime.strptime(
                start_validation_date, '%Y%m%dT%H%M%S')
        else:
            self.start_validation_date = datetime.strptime(
                start_validation_date, '%Y%m%d')

        if len(start_validation_date)>8:
            self.end_validation_date = datetime.strptime(
                end_validation_date, '%Y%m%dT%H%M%S')
        else:
            self.end_validation_date = datetime.strptime(
                end_validation_date, '%Y%m%d')

class Handler(object):

    def __init__(self, config):
        self.config = config

    def route_data(self, files):
        self.backup_files(files)
        self.route_to_stage(self.config.get('stage', {}).get('testing'))
        if not self.is_important_data_modification(files) :
            self.route_to_stage(self.config.get('stage', {}).get('production'))

    def backup_files(self, files):
        """
        backup file to file system (without history for the moment)
        """
        backup_dir = self.config.get('backup_dir')
        purge_dir(backup_dir)

        for filename in files:
            shutil.move(filename, backup_dir)

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

        return _create_dataset_period(navitia_response.json())

    def get_navitia_production_date(self, stage):
        """
        fetch from the navitia status the publication period of the global dataset
        """
        navitia_parameters = stage['navitia']
        coverage = self.config['coverage']
        navitia_url = '{base_url}/v1/coverage/{coverage}/status/'\
            .format(base_url=navitia_parameters['url'], coverage=coverage)
        navitia_url_auth = (navitia_parameters.get('token'), '')
        navitia_response = call_navitia(navitia_url, navitia_url_auth)

        return _create_publication_period(navitia_response.json())

    def route_to_stage(self, stage):
        logging.info('routing to {}'.format(stage))

        # fetch from navitia the last datasets production period of a given
        # contributor
        last_dataset_date = self.get_last_dataset_production_date(stage)
        last_publication_date = self.get_navitia_production_date(stage)
        logging.debug("dates used for the DataUpdate : " +str(last_dataset_date))
        logging.debug("dates used for the Import : " +str(last_publication_date))

        fusio_handler = FusioHandler(self.config, stage, last_dataset_date, last_publication_date)

        fusio_handler.publish()
