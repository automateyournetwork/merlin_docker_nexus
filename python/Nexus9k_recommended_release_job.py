'''
To run the job:

$ pyats run job Nexus9k_recommended_release_job.py --testbed-file testbed/testbed_cisco_api.yaml

'''

import os
from genie.testbed import load

def main(runtime):

    # ----------------
    # Load the testbed
    # ----------------
    if not runtime.testbed:
        # If no testbed is provided, load the default one.
        # Load default location of Testbed
        testbedfile = os.path.join('testbed/testbed_cisco_api.yaml')
        testbed = load(testbedfile)
    else:
        # Use the one provided
        testbed = runtime.testbed

    # Find the location of the script in relation to the job file
    testscript = os.path.join(os.path.dirname(__file__), 'Nexus9k_recommended_release.py')

    # run script
    runtime.tasks.run(testscript=testscript, testbed=testbed)