FROM lscr.io/linuxserver/code-server:latest

# 환경 변수 설정
ENV PUID=1000 \
    PGID=1000 \
    TZ=Etc/UTC \
    ABS_PROXY_BASE_PATH=/poc

USER root
RUN apt-get update \
 && apt-get install -y python3 python3-venv python3-pip \
 && rm -rf /var/lib/apt/lists/* \
    
# 볼륨 및 포트 노출
VOLUME ["/config"]
EXPOSE 8443

# 기본 엔트리포인트 (/init)와 CMD는 베이스 이미지가 자동으로 설정합니다.
