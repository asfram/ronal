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
        self.create_dir(output_dir)

        for filename in files:
            shutil.move(filename, self.config.get('output_dir'))

    def create_dir(self, directory):
        """create directory if needed"""
        if not os.path.exists(directory):
            os.makedirs(directory)

    def is_important_data_modification(self, files):
        """
        return True is the data update is small enough to be put in production without a manual testing
        """
        return True

    def get_last_dataset_production_date(self, stage):
        """
        fetch from navitia the last dataset production period
        """
        raise NotImplementedError

    def get_stage(self, important_modification):
        if important_modification:
            return self.config.get('stage', {}).get('testing')
        return self.config.get('stage', {}).get('production')

    def route_to_stage(self, important_modification):
        stage = self.get_stage(important_modification)
        logging.info('routing to {}'.format(stage))

        last_production_date = self.get_last_dataset_production_date(stage)

        # TODO :)
