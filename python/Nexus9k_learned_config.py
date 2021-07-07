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

            # ---------------------------------------
            # Execute learn for various functions
            # ---------------------------------------
            # Config
            self.learned_config = ParseConfigFunction.parse_learn(steps, device, "config")

            # ---------------------------------------
            # Create JSON, YAML, CSV, MD, HTML, HTML Mind Map files from the Parsed Data
            # ---------------------------------------         
            with steps.start('Store data',continue_=True) as step:              
                print(self.learned_config)
                # Learned config
                if self.learned_config is not None:
                    learned_config_template = env.get_template('learned_config.j2')                    
                    directory = "Learned_Config"
                    file_name = "learned_config"

                    self.save_to_json_file(device, directory, file_name, self.learned_config)
                    self.save_to_yaml_file(device, directory, file_name, self.learned_config)            

                    parsed_output_type = learned_config_template.render(to_parse_config=self.learned_config,filetype_loop_jinja2="html")

                    with open("Camelot/Learned_Config/%s_learned_config.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_type)                                  

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