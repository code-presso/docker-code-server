FROM lscr.io/linuxserver/code-server:latest

ENV PATH=/app/code-server/bin:$PATH

USER root

RUN apt-get update \
 && apt-get install -y \
    python3 python3-venv python3-pip \
    default-jdk \
    golang-go \
    iproute2 \
 && rm -rf /var/lib/apt/lists/*
    
# VS Code 확장 설치는 별도 RUN으로 분리
RUN code-server --extensions-dir ${EXT_DIR} --install-extension ms-python.python \
 && code-server --extensions-dir ${EXT_DIR} --install-extension redhat.java \
 && code-server --extensions-dir ${EXT_DIR} --install-extension golang.go \
 && code-server --extensions-dir ${EXT_DIR} --install-extension vmware.vscode-spring-boot \
 && code-server --extensions-dir ${EXT_DIR} --install-extension franneck94.c-cpp-runner \
 && code-server --extensions-dir ${EXT_DIR} --install-extension vscjava.vscode-java-debug

    
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
 && apt-get install -y nodejs

COPY shutdown-on-idle.sh /usr/local/bin/shutdown-on-idle.sh
RUN chmod +x /usr/local/bin/shutdown-on-idle.sh

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

COPY config/config.yaml /config/config.yaml
COPY config/certs/coderun.crt /config/certs/coderun.crt
COPY config/certs/coderun.key /config/certs/coderun.key
COPY config/settings.json /config/settings.json
