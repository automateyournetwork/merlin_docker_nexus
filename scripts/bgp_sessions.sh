pyats run job /python/Nexus9k_bgp_sessions_job.py --testbed-file testbed/testbed_DevNet_Nexus9k_Sandbox.yaml
cp /Camelot/Show_BGP_Sessions/*.* /var/www/html/
/usr/sbin/apachectl -D FOREGROUND