#!/bin/bash
echo "Waiting for db"
appdeps.py --wait-secs 30 --port-wait db:5432 --file /opt/sfm-ui
if [ "$?" = "1" ]; then
    echo "Problem with application dependencies."
    exit 1
fi

echo "Writing local_settings"
echo "env={}" > /opt/sfm-ui/sfm/sfm/settings/local.py
env | grep 'SFM_\|\DB_' | sed 's/\(.*\)=\(.*\)/env["\1"]="\2"/' >> /opt/sfm-ui/sfm/sfm/settings/local.py
cat /tmp/local.py >> /opt/sfm-ui/sfm/sfm/settings/local.py

echo "Syncing db"
/opt/sfm-ui/sfm/manage.py syncdb --noinput

echo "Migrating db"
/opt/sfm-ui/sfm/manage.py migrate --noinput

echo "Running server"
#Not entirely sure why this is necessary, but it works.
/etc/init.d/apache2 start
#Make sure apache has started
/etc/init.d/apache2 status
while [ "$?" != "0" ];  do
    echo "Waiting for start"
    sleep 1
    /etc/init.d/apache2 status
done
echo "Stopping server"
/etc/init.d/apache2 graceful-stop
#Make sure apache has stopped
/etc/init.d/apache2 status
while [ "$?" = "0" ];  do
    echo "Waiting for stop"
    sleep 1
    /etc/init.d/apache2 status
done
echo "Starting server again"
apachectl -DFOREGROUND