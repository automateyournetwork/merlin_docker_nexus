pyats run job /python/Nexus9k_port_channel_summary_job.py --testbed-file testbed/testbed_DevNet_Nexus9k_Sandbox.yaml
cp /Camelot/Show_Port_Channel_Summary/*.* /var/www/html/
/usr/sbin/apachectl -D FOREGROUND