#!/bin/bash

(
IFS=$'\n'
# save initial env into file
for l in `env`
do
       echo "export $l" >> /etc/environment
       echo "$l" >> /mnt/.env
done
)


cd /mnt/src/
#Create Procfile for honcho process manager
if [ $DEBUG -eq 1 ]; then
# for more info see: http://honcho.readthedocs.org/en/latest/using_procfiles.html#buffered-output
echo "PYTHONUNBUFFERED=true" >> /mnt/.env
cat >Procfile <<EOM
server: gunicorn  --worker-class=gthread --threads=4 --graceful-timeout 1500 --timeout 2000 --bind=0.0.0.0:8888 --log-level=debug --log-file=/var/log/out.log  --access-logfile=/var/log/access.log main:app 2>>/var/log/out.log
EOM
else
cat >Procfile <<EOM
server: gunicorn --worker-class=gthread --threads=4 --graceful-timeout 1500 --timeout 2000 --bind=0.0.0.0:8888 --log-level=info --log-file=/var/log/out.log  --access-logfile=/var/log/access.log main:app 2>>/var/log/out.log
EOM
fi

# run honcho process manager without forking, to solve PID1 problem for graceful shutdown
# http://www.techbar.me/stopping-docker-containers-gracefully/
exec honcho start
