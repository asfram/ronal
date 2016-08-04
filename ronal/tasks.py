#!/usr/bin/env python
#  Copyright (c) 2001-2016, Canal TP and/or its affiliates. All rights reserved.
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
import os
from clingon import clingon
import logging
from ronal.core import Handler


def get_files(input_dir):
    if not os.path.isdir(input_dir):
        raise Exception('config input directory {} does not exist, cannot do anything'.format(input_dir))

    files = [os.path.join(input_dir, filename) for filename in os.listdir(input_dir)]

    return files


def handle_data(config):
    input_dir = config.get('input_dir')
    files = get_files(input_dir)

    if not files:
        logging.debug('no file in input dir, stopping here')
        return

    handler = Handler(config)

    handler.route_data(files)


def load_config(config_file):
    if not os.path.exists(config_file):
        raise Exception('config file {} does not exist, cannot do anything'.format(config_file))

    import yaml
    with open(config_file, 'r') as f:
        return yaml.load(f)


@clingon.clize
def update_data_task(config_file='default_settings.yml'):
    try:
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger(__name__).debug('update_data_task')

        config = load_config(config_file)
        #once the config is loaded, we init again the logger
        log_config = config.get('loggers')
        if log_config:
            from logging import config as logging_config
            logging_config.dictConfig(log_config)

        handle_data(config)
    except:
        logging.exception('')
        raise
