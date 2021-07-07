pyats run job /python/Nexus9k_bgp_process_vrf_all_job.py --testbed-file testbed/testbed_DevNet_Nexus9k_Sandbox.yaml
cp /Camelot/Show_BGP_Process_VRF_All/*.* /var/www/html/
/usr/sbin/apachectl -D FOREGROUND