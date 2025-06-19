#!/usr/bin/env bash
set -e

touch   /var/log/shutdown-on-idle.log

echo "$(date +'%F %T') [entrypoint] starting idle monitor..."
/usr/local/bin/shutdown-on-idle.sh 2>&1 \
    | tee -a /var/log/shutdown-on-idle.log &
echo "$(date +'%F %T') [entrypoint] idle monitor running in background."

echo "$(date +'%F %T') [entrypoint] executing original init: $@"
exec /init "$@"
