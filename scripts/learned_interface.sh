pyats run job /python/Nexus9k_learned_interface_job.py --testbed-file testbed/testbed_DevNet_Nexus9k_Sandbox.yaml
cp /Camelot/Learned_Interface/*.* /var/www/html/
/usr/sbin/apachectl -D FOREGROUND