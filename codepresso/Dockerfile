# https://github.com/linuxserver/docker-code-server
FROM lscr.io/linuxserver/code-server:latest

WORKDIR /app

ENV PUID=1000
ENV PGID=1000
ENV SUDO_PASSWORD=1234

#live server
#live preview
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs build-essential python3.10 && \
    npm install -g --unsafe-perm code-server --force && \
    code-server --install-extension ritwickdey.liveserver --force && \
    code-server --install-extension ms-vscode.live-server --force && \
    mv /config/.local/share/code-server/extensions/ /config/extensions

RUN apt-get update && apt-get install -y \
    unzip \
    curl

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    sudo ./aws/install && \
    npm install -g @vue/cli && \
    npm install vue && \
    rm -rf awscliv2.zip

COPY config/config.yaml /config/.config/code-server/config.yaml
COPY config/settings.json /config/data/User/settings.json

COPY app/main.py /app

EXPOSE 8443 5500 5001 3000 5173

#main.py 필요 없으면 지우기.
CMD ["python3", "/app/main.py"]



