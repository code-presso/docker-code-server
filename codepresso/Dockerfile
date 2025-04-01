# https://github.com/linuxserver/docker-code-server
FROM lscr.io/linuxserver/code-server:latest

WORKDIR /app

ENV PUID=1000
ENV PGID=1000
ENV SUDO_PASSWORD=1234

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    sudo \
    default-jdk \
    && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && sudo ./aws/install \
    && rm -rf awscliv2.zip


# node
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash - && \
        apt-get install -y nodejs build-essential

# py
RUN apt-get install -y python3.10

# c, c++
RUN apt-get install -y gcc make g++

# go
RUN wget https://go.dev/dl/go1.21.0.linux-amd64.tar.gz \
     && tar -xvf go1.21.0.linux-amd64.tar.gz -C /usr/local 
ENV PATH=$PATH:/usr/local/go/bin

# java
ENV GRADLE_VERSION=8.3
RUN curl -sL https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip -o gradle.zip \
    && mkdir /opt/gradle \
    && unzip gradle.zip -d /opt/gradle \
    && rm gradle.zip \
    && ln -s /opt/gradle/gradle-${GRADLE_VERSION}/bin/gradle /usr/local/bin/gradle

# vue
RUN npm install -g @vue/cli && \
    npm install vue

#extension live-server(삭제_ritwickdey), live-priview, java, go, clangd
RUN npm install -g --unsafe-perm code-server --force \
    && code-server --install-extension ritwickdey.liveserver --force \
    && code-server --install-extension ms-vscode.live-server --force \
    && code-server --install-extension vscjava.vscode-java-pack --force \
    && code-server --install-extension golang.go --force \
    && code-server --install-extension llvm-vs-code-extensions.vscode-clangd --force
    

RUN mv /config/.local/share/code-server/extensions/ /config/extensions

COPY config/config.yaml /config/.config/code-server/config.yaml
COPY config/settings.json /config/data/User/settings.json

COPY app/main.py /app

EXPOSE 8443

#main.py 필요 없으면 지우기.
CMD ["python3", "/app/main.py"]
#CMD ["code-server", "--bind-addr", "0.0.0.0:8443"]
