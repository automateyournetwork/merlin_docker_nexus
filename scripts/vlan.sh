pyats run job /python/Nexus9k_vlan_job.py --testbed-file testbed/testbed_DevNet_Nexus9k_Sandbox.yaml
cp /Camelot/Show_VLAN/*.* /var/www/html/
/usr/sbin/apachectl -D FOREGROUND