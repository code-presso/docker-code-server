FROM lscr.io/linuxserver/code-server:latest

ENV PATH=/app/code-server/bin:$PATH

# 환경 변수 설정
ENV PUID=1000 \
    PGID=1000 \
    TZ=Etc/UTC \
    ABS_PROXY_BASE_PATH=/poc \
    EXT_DIR=/config/extensions

USER root
RUN apt-get update \
 && apt-get install -y  \
          python3 python3-venv python3-pip \
          default-jdk \
          golang-go \
          iproute2 \
#          build-essential gdb clang gcc g++ \
 && rm -rf /var/lib/apt/lists/* \
         # VS Code 확장 설치
         && code-server --extensions-dir ${EXT_DIR} --install-extension ms-python.python \
         && code-server --extensions-dir ${EXT_DIR} --install-extension redhat.java \
         && code-server --extensions-dir ${EXT_DIR} --install-extension golang.go 

#RUN curl -sSL https://dot.net/v1/dotnet-install.sh -o /tmp/dotnet-install.sh \
# && bash /tmp/dotnet-install.sh --channel 7.0 --install-dir /usr/share/dotnet \
# && ln -s /usr/share/dotnet/dotnet /usr/bin/dotnet \
# && rm /tmp/dotnet-install.sh
    
#RUN curl -fSL \
#          -o /tmp/cpptools.vsix \
#          "https://github.com/microsoft/vscode-cpptools/releases/download/v1.25.3/cpptools-linux-x64.vsix" \
#     && code-server --extensions-dir ${EXT_DIR} --install-extension /tmp/cpptools.vsix \
#     && rm /tmp/cpptools.vsix 
#    
#RUN curl -fSL \
#         -o /tmp/csharptools.vsix \
#         "https://github.com/muhammadsammy/free-vscode-csharp/releases/download/2.72.27/csharp-platform-neutral-2.72.27.vsix" \
#    && code-server --extensions-dir ${EXT_DIR} --install-extension /tmp/csharptools.vsix \
#    && rm /tmp/csharptools.vsix 
    
#Debugger for Java
RUN code-server --extensions-dir ${EXT_DIR} --install-extension vscjava.vscode-java-debug
RUN code-server --extensions-dir ${EXT_DIR} --install-extension franneck94.c-cpp-runner

RUN apt-get update \
     && apt-get install -y iproute2

COPY shutdown-on-idle.sh /usr/local/bin/shutdown-on-idle.sh
RUN chmod +x /usr/local/bin/shutdown-on-idle.sh

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

COPY config/config.yaml /config/config.yaml
COPY config/certs/coderun.crt /config/certs/coderun.crt
COPY config/certs/coderun.key /config/certs/coderun.key
COPY config/settings.json /config/settings.json

# 볼륨 및 포트 노출
VOLUME ["/config"]
EXPOSE 8443

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
#ENTRYPOINT ["/usr/local/bin/shutdown-on-idle.sh"]
CMD []
