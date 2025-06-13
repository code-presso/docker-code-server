#!/usr/bin/env bash
set -e

mkdir -p /config/data
touch   /config/data/shutdown-on-idle.log

# 1) idle 종료 스크립트를 백그라운드로 실행
echo "$(date +'%F %T') [entrypoint] starting idle monitor"
exec /usr/local/bin/shutdown-on-idle.sh &

/usr/local/bin/shutdown-on-idle.sh 2>&1 | tee -a /config/data/shutdown-on-idle.log &
echo "$(date +'%F %T') [entrypoint] idle monitor launched in background"

# 2) 원래의 code-server 실행 (lscr.io/linuxserver/code-server 기본 ENTRYPOINT인 /init 호출)
echo "$(date +'%F %T') [entrypoint] exec original init: $@"
exec /init "$@"
