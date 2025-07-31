#!/usr/bin/env bash
set -e

# Configuration
PORT=${PORT:-8443}
CHECK_INTERVAL=30
IDLE_LIMIT=$((30*60))

last_active=$(date +%s)


echo "$(date +'%F %T') [shutdown-on-idle] started, watching port ${PORT}"

while true; do
  # find the code-server PID
  CODE_PID=$(pgrep -f "code-server.*--bind-addr 0.0.0.0:${PORT}" || true)
  if [ -z "$CODE_PID" ]; then
    echo "$(date +'%F %T') [shutdown-on-idle] code-server not yet started; retrying in ${CHECK_INTERVAL}s."
    sleep "$CHECK_INTERVAL"
    continue
  fi

  # check for any established connections
  if ss -tn state established "( sport = :${PORT} )" | tail -n +2 | grep -q .; then
    last_active=$(date +%s)
    echo "$(date +'%F %T') [shutdown-on-idle] active session detected, resetting timer."
  else
    now=$(date +%s)
    elapsed=$(( now - last_active ))
    echo "$(date +'%F %T') [shutdown-on-idle] no sessions, idle=${elapsed}s."
    if [ "$elapsed" -ge "$IDLE_LIMIT" ]; then
      echo "$(date +'%F %T') [shutdown-on-idle] idle ≥ ${IDLE_LIMIT}s – shutting down code-server."
      kill 1
      exit 0
    fi
  fi

  sleep "$CHECK_INTERVAL"
done
