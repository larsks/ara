#   Copyright 2016 Red Hat, Inc. All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

from ansible.constants import get_config, load_config_file
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

DEFAULT_DATABASE = os.path.expanduser('~/.ara/ansible.sqlite')
config, file = load_config_file()
DATABASE = get_config(config, 'ara', 'database', 'ARA_DATABASE',
                      DEFAULT_DATABASE)

# TODO (dmsimard): Figure out the best place and way to initialize the
#                  database if it hasn't been created yet.
try:
    if not os.path.exists(os.path.dirname(DATABASE)):
        os.makedirs(os.path.dirname(DATABASE))
except Exception as e:
    raise IOError("Unable to ensure database directory exists. " + str(e))

app = Flask(__name__)
app.config['DATABASE'] = DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{0}".format(DATABASE)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from ara import views, models
