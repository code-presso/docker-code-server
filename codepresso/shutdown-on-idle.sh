#!/usr/bin/env bash
set -e

# 설정
PORT=${PORT:-8443}
CHECK_INTERVAL=30
IDLE_LIMIT=$((10*60))
EXT_DIR=${EXT_DIR:-/config/extensions}
DATA_DIR=/config/data
CFG_FILE=/config/config.yaml
DEFAULT_WORKSPACE=/config/workspace
ABS_PROXY_BASE_PATH=/poc

last_active=$(date +%s)
#
## code-server 백그라운드 실행
#echo "$(date +'%F %T') [shutdown-on-idle.sh] launching code-server" \
#     "--user-data-dir ${DATA_DIR}" \
#     "--extensions-dir ${EXT_DIR}" \
#     "--config ${CFG_FILE}" \
#     "--auth none" \
#     "--bind-addr 0.0.0.0:${PORT}"
#code-server \
#  --user-data-dir "${DATA_DIR}" \
#  --extensions-dir "${EXT_DIR}" \
#  --config "${CFG_FILE}" \
#  --auth none \
#  --bind-addr "0.0.0.0:${PORT}" \
#  "$@" &
#CODE_PID=$!

has_conn() {
  ss -tn state established "( sport = :${PORT} )" | tail -n +2
}

# 루프
while kill -0 $CODE_PID 2>/dev/null; do
  if [ -n "$(has_conn)" ]; then
    # 세션 있으면 타이머 리셋
    last_active=$(date +%s)
    echo "$(date +'%F %T') [shutdown-on-idle.sh] active session detected, timer reset"
  else
    now=$(date +%s)
    elapsed=$(( now - last_active ))
    echo "$(date +'%F %T') [shutdown-on-idle.sh] no session, idle=${elapsed}s"
    if [ $elapsed -ge $IDLE_LIMIT ]; then
      echo "$(date +'%F %T') [shutdown-on-idle.sh] idle >= ${IDLE_LIMIT}s → shutting down"
      kill $CODE_PID
      break
    fi
  fi
  sleep $CHECK_INTERVAL
done


wait $CODE_PID
