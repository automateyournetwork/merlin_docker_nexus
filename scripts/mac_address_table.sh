pyats run job /python/Nexus9k_mac_address_table_job.py --testbed-file testbed/testbed_DevNet_Nexus9k_Sandbox.yaml
cp /Camelot/Show_MAC_Address_Table/*.* /var/www/html/
/usr/sbin/apachectl -D FOREGROUND