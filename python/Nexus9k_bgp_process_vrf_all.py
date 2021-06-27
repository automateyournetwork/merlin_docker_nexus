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
from rich import print
from rich.panel import Panel
from rich.text import Text
from pyats import aetest
from pyats import topology
from pyats.log.utils import banner
from jinja2 import Environment, FileSystemLoader
from ascii_art import GREETING, LEARN, RUNNING, WRITING, FINISHED
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
        print(Panel.fit(Text.from_markup(GREETING)))
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
            # Genie learn().info for various functions
            # ---------------------------------------
            print(Panel.fit(Text.from_markup(LEARN)))

            # ---------------------------------------
            # Execute parser for various show commands
            # ---------------------------------------
            print(Panel.fit(Text.from_markup(RUNNING)))

            # show bgp process vrf all
            self.parsed_show_bgp_process_vrf_all = ParseShowCommandFunction.parse_show_command(steps, device, "show bgp process vrf all")

            # ---------------------------------------
            # Create JSON, YAML, CSV, MD, HTML, HTML Mind Map files from the Parsed Data
            # ---------------------------------------         
            with steps.start('Store data',continue_=True) as step:
                print(Panel.fit(Text.from_markup(WRITING)))
                
                print(self.parsed_show_bgp_process_vrf_all)
                # Show bgp process vrf all
                if self.parsed_show_bgp_process_vrf_all is not None:
                    sh_bgp_process_vrf_all_template = env.get_template('show_bgp_process_vrf_all.j2')

                    directory = "Show_BGP_Process_VRF_All"
                    file_name = "show_bgp_process_vrf_all"
                    
                    self.save_to_json_file(device, directory, file_name, self.parsed_show_bgp_process_vrf_all)
                    self.save_to_yaml_file(device, directory, file_name, self.parsed_show_bgp_process_vrf_all)              
                    
                    for filetype in filetype_loop:
                        parsed_output_type = sh_bgp_process_vrf_all_template.render(to_parse_bgp=self.parsed_show_bgp_process_vrf_all,filetype_loop_jinja2=filetype)

                        with open("Camelot/Show_BGP_Process_VRF_All/%s_show_bgp_process_vrf_all.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type)                                   

        # Goodbye Banner
        print(Panel.fit(Text.from_markup(FINISHED)))
     
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