pyats run job /python/Nexus9k_ip_int_brief_job.py --testbed-file testbed/testbed_DevNet_Nexus9k_Sandbox.yaml
cp /Camelot/Show_IP_Interface_Brief/*.* /var/www/html/
/usr/sbin/apachectl -D FOREGROUND