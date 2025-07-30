FROM nginx:stable-alpine

# certs
COPY certs/coderun.crt /etc/nginx/certs/coderun.crt
COPY certs/coderun.key /etc/nginx/certs/coderun.key

# nginx conf
COPY conf/code-server.conf /etc/nginx/conf.d/code-server.conf

EXPOSE 8443
EXPOSE 443
