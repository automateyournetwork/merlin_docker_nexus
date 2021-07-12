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
            # Execute parser for various show commands
            # ---------------------------------------
            self.parsed_show_vlan = ParseShowCommandFunction.parse_show_command(steps, device, "show vlan")

            # ---------------------------------------
            # Create JSON, YAML, CSV, MD, HTML, HTML Mind Map files from the Parsed Data
            # ---------------------------------------         
            with steps.start('Store data',continue_=True) as step:              
                if self.parsed_show_vlan is not None:
                    show_vlan_elastic_template = env.get_template('elastic_standards.j2')
                    show_vlan_elastic = show_vlan_elastic_template.render(to_normalize_for_elastic=self.parsed_show_vlan)
                    # ----------------
                    # Store vlan in Elastic
                    # ----------------
                    es.index(index='%s_show_vlan' % device.alias.lower(), id=unique_id, 
                             body=show_vlan_elastic)
                                                 
                    sh_vlan_template = env.get_template('show_vlan.j2')

                    directory = "Show_VLAN"
                    file_name = "show_vlan"
                    self.save_to_json_file(device, directory, file_name, self.parsed_show_vlan)
                    self.save_to_yaml_file(device, directory, file_name, self.parsed_show_vlan)              
                    
                    for filetype in filetype_loop:
                        parsed_output_type = sh_vlan_template.render(to_parse_vlan=self.parsed_show_vlan['vlans'],device_alias = device.alias,filetype_loop_jinja2=filetype)

                        with open("Camelot/Show_VLAN/%s_show_vlan.%s" % (device.alias,filetype), "w") as fh:
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