# ----------------
# Copyright
# ----------------
# Written by John Capobianco, March 2021
# Copyright (c) 2021 John Capobianco

# ----------------
# Python
# ----------------
import os
import sys
import yaml
import time
import json
import shutil
import logging
from pyats import aetest
from pyats import topology
from pyats.log.utils import banner
from jinja2 import Environment, FileSystemLoader
from general_functionalities import ParseShowCommandFunction, ParseLearnFunction, ParseConfigFunction, ParseDictFunction
import uuid
from elasticsearch import Elasticsearch

# ----------------
# Get logger for script
# ----------------

log = logging.getLogger(__name__)

# ----------------
# Filetypes 
# ----------------

filetype_loop = ["csv","md","html"]

# ----------------
# Template Directory
# ----------------

template_dir = 'templates/cisco/nxos'
env = Environment(loader=FileSystemLoader(template_dir))

# ----------------
# Define Elastic
# ---------------

es = Elasticsearch([{'host': 'elasticsearch', 'port': '9200'}], http_auth=('elastic', 'hhymkRPkY1NZBeuO9WIP'))

# ----------------
# AE Test Setup
# ----------------
class common_setup(aetest.CommonSetup):
    """Common Setup section"""
    @aetest.subsection
    def connect_to_devices(self, testbed):
        """Connect to all the devices"""
        testbed.connect(learn_hostname=True)

# ----------------
# Test Case #1
# ----------------
class Collect_Information(aetest.Testcase):
    """Parse all the commands"""

    @aetest.test
    def parse(self, testbed, section, steps):
        """ Testcase Setup section """
        # ---------------------------------------
        # Loop over devices
        # ---------------------------------------
        for device in testbed:
            unique_id = uuid.uuid4().hex

            # ---------------------------------------
            # Execute learn for various functions
            # ---------------------------------------
            # Interface
            self.learned_interface = ParseLearnFunction.parse_learn(steps, device, "interface")

            # ---------------------------------------
            # Create JSON, YAML, CSV, MD, HTML, HTML Mind Map files from the Parsed Data
            # ---------------------------------------         
            with steps.start('Store data',continue_=True) as step:              
                # Learned interface
                if self.learned_interface is not None:
                    
                    learned_interface_elastic_template = env.get_template('elastic_standards.j2')
                    learned_interface_elastic = learned_interface_elastic_template.render(to_normalize_for_elastic=self.learned_interface)

                    # ----------------
                    # Store Interface in Elastic
                    # ----------------
                    elastic_index_result = es.index(index='%s_learned_interface' % device.alias.lower(), id=unique_id, 
                             body=learned_interface_elastic)

                    learned_interface_template = env.get_template('learned_interface.j2')
                    directory = "Learned_Interface"
                    file_name = "learned_interface"

                    self.save_to_json_file(device, directory, file_name, self.learned_interface)
                    self.save_to_yaml_file(device, directory, file_name, self.learned_interface)            

                    for filetype in filetype_loop:
                        parsed_output_type = learned_interface_template.render(to_parse_interface=self.learned_interface,filetype_loop_jinja2=filetype)

                        with open("Camelot/Learned_Interface/%s_learned_interface.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type)                                  

                        if filetype == "html":
                            with open("/var/www/html/index.html", "w") as fh:
                                fh.write(parsed_output_type) 
    
    def save_to_json_file(self, device, directory, file_name, content):
        file_path = "Camelot/{}/{}_{}.json".format(directory, device.alias, file_name)
        with open(file_path, "w") as json_file:
            json.dump(content, json_file, indent=4, sort_keys=True)
            json_file.close()
    
    def save_to_yaml_file(self, device, directory, file_name, content):
        file_path = "Camelot/{}/{}_{}.yaml".format(directory, device.alias, file_name)
        with open(file_path, "w") as yml_file:
            yaml.dump(content, yml_file, allow_unicode=True)
            yml_file.close()