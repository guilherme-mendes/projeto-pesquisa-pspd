#!/bin/bash

WSGI_MODULE=wsgi                               # WSGI module name
NAME="producer"                    # Name of the application
NUM_WORKERS=${NUM_WORKERS:-3}                  # How many worker processes should Gunicorn spawn
USER=root                                      # The user to run as
GROUP=root                                     # The group to run as
PORT=${PORT:-80}                               # Communication will occur through this UNIX socket
WORKER_TIMEOUT=${WORKER_TIMEOUT:-60}           # Gunicorn worker timeout (in seconds)
NUM_THREADS=${NUM_THREADS:-2}                  # How many threads each worker can spawn to deal async requests
RELOAD=${DEVELOPMENT_MODE:-true}

echo "Starting $NAME as `whoami` in port $PORT"
date
echo "Gunicorn Workers: $NUM_WORKERS"
echo "Gunicorn Threads: $NUM_THREADS"
echo "Gunicorn Worker Timeout: $WORKER_TIMEOUT"
echo "Development Mode: $RELOAD"

# Start your Flask Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${WSGI_MODULE} \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user $USER --group $GROUP \
  --bind 0.0.0.0:$PORT \
  --log-level info \
  # --access-logfile $ACCESS_LOG_FILE \
  --timeout $WORKER_TIMEOUT \
  --threads $NUM_THREADS \
  `if [ $RELOAD == True ]; then echo "--reload"; fi`  # Optionally enable auto reload on source code changes