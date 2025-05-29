### 실행 명령어

```bash
docker build -t {image-name} .
```

```bash
docker run -d -p 8443:8443 --name {container-name} {image-name}
```

```bash
docker run -d \
--name=code-server \
-e PUID=1000 \
-e PGID=1000 \
-e TZ=Etc/UTC \
-p 8443:8443 \
-v /path/to/code-server/config:/config \
--restart unless-stopped \
lscr.io/linuxserver/code-server:latest
```



```bash
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 204573508773.dkr.ecr.ap-northeast-2.amazonaws.com
docker build -t coderun-code-server:dev .
docker tag coderun-code-server:dev 204573508773.dkr.ecr.ap-northeast-2.amazonaws.com/coderun-code-server:dev
docker push 204573508773.dkr.ecr.ap-northeast-2.amazonaws.com/coderun-code-server:dev
```

```bash
cd codepresso/file_server
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 204573508773.dkr.ecr.ap-northeast-2.amazonaws.com
docker build -t s3-file-server .
docker tag s3-file-server:latest 204573508773.dkr.ecr.ap-northeast-2.amazonaws.com/s3-file-server:latest
docker push 204573508773.dkr.ecr.ap-northeast-2.amazonaws.com/s3-file-server:latest
```

```bash
cd codepresso/nginx
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 204573508773.dkr.ecr.ap-northeast-2.amazonaws.com
docker build -t code-server-nginx .
docker tag code-server-nginx:latest 204573508773.dkr.ecr.ap-northeast-2.amazonaws.com/code-server-nginx:latest
docker push 204573508773.dkr.ecr.ap-northeast-2.amazonaws.com/code-server-nginx:latest
```
