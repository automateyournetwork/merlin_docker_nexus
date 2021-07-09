pyats run job /python/Nexus9k_recommended_release_job.py --testbed-file testbed/testbed_DevNet_Nexus9k_Sandbox.yaml
cp /Camelot/Recommended_Release/*.* /var/www/html/
/usr/sbin/apachectl -D FOREGROUND