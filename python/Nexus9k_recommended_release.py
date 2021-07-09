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
import requests
from pyats import aetest
from pyats import topology
from pyats.log.utils import banner
from jinja2 import Environment, FileSystemLoader
from general_functionalities import ParseShowCommandFunction

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

template_dir = 'templates/cisco/api'
env = Environment(loader=FileSystemLoader(template_dir))

# ----------------
# AE Test Setup
# ----------------
class common_setup(aetest.CommonSetup):
    """Common Setup section"""
    @aetest.subsection
    def connect_to_devices(self, testbed):
        """Connect to all the devices"""
        testbed.connect()

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
            # Execute parser for various show commands
            # ---------------------------------------

            # Show Version
            self.parsed_show_version = ParseShowCommandFunction.parse_show_command(steps, device, "show version")
            # ---------------------------------------
            # Send Version / Serial Numbers to Cisco APIs 
            # Create JSON, YAML, CSV, MD, HTML, HTML Mind Map files from the Parsed API Data
            # ---------------------------------------         
            
            with steps.start('Store data',continue_=True) as step:              
                # Show version
                if hasattr(self, 'parsed_show_version'):
                    recommended_release_template = env.get_template('recommended_release.j2')

                    with open("api_credentials/cisco.yaml", 'r') as f:
                        api_credentials = yaml.safe_load(f)

                    recommended_release_api_username = api_credentials['APIs']['recommended_release']['recommended_release_api_username']
                    recommended_release_api_password = api_credentials['APIs']['recommended_release']['recommended_release_api_password']

                    oauth_token_raw = requests.post("https://cloudsso.cisco.com/as/token.oauth2?grant_type=client_credentials&client_id=%s&client_secret=%s" % (recommended_release_api_username,recommended_release_api_password))
                    oauth_token_json = oauth_token_raw.json()
                    oauth_headers = {"Authorization": "%s %s" % (oauth_token_json['token_type'],oauth_token_json['access_token'])}

                    for version,value in self.parsed_show_version.items():
                        with steps.start('Calling API',continue_=True) as step:
                            try:
                                recommended_release_raw = requests.get("https://api.cisco.com/software/suggestion/v2/suggestions/software/productIds/N9K-C9504", headers=oauth_headers)
                        
                                recommended_release_json = recommended_release_raw.json()

                                with open("Camelot//Recommended_Release/%s_recommended_release.json" % device.alias, "w") as fid:
                                  json.dump(recommended_release_json, fid, indent=4, sort_keys=True)

                                with open("Camelot//Recommended_Release/%s_recommended_release.yaml" % device.alias, "w") as yml:
                                  yaml.dump(recommended_release_json, yml, allow_unicode=True)

                                for filetype in filetype_loop:
                                    parsed_output_type = recommended_release_template.render(to_parse_recommended=recommended_release_json['productList'],installed_version=value['software']['system_version'],filetype_loop_jinja2=filetype)

                                    with open("Camelot/Recommended_Release/%s_recommended_release.%s" % (device.alias,filetype), "w") as fh:
                                        fh.write(parsed_output_type)

                                    if filetype == "html":
                                        with open("/var/www/html/index.html", "w") as fh:
                                            fh.write(parsed_output_type)

                            except Exception as e:
                                step.failed('Could not parse it correctly\n{e}'.format(e=e))                           

