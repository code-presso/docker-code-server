#!/usr/bin/env bash
set -e

# code-server 실행
exec_code_server() {
  exec code-server "$@" &
  CODE_PID=$!
}

has_connections() {
  ss -tn state established "( dport = :${PORT:-8443} )" | tail -n +2 | grep -q .
}

# code-server 시작
exec_code_server --bind-addr 0.0.0.0:8443

# 주기적으로 연결 검사 → 없으면 프로세스 종료
while kill -0 $CODE_PID 2>/dev/null; do
  if ! has_connections; then
    echo "[`date`] no active sessions, shutting down"
    kill $CODE_PID
    break
  fi
  sleep 30  # 30초마다 확인
done

wait $CODE_PID
