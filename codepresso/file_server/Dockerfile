# Base 이미지
FROM python:3.11-slim

# 1) AWS CLI v2 설치 (ECS Task Role 지원)
USER root
RUN apt-get update && \
    apt-get remove -y awscli && \
    apt-get install -y curl unzip && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o /tmp/awscliv2.zip && \
    unzip /tmp/awscliv2.zip -d /tmp && \
    /tmp/aws/install && \
    rm -rf /tmp/aws /tmp/awscliv2.zip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 2) FastAPI 및 Uvicorn 설치
RUN pip install --no-cache-dir fastapi uvicorn apscheduler

# 3) AWS 리전 환경 변수 설정 (선택)
ENV AWS_REGION=ap-northeast-2 \
    AWS_DEFAULT_REGION=ap-northeast-2

# 4) 비루트 유저 생성 및 전환
RUN useradd -u 1000 appuser
USER appuser

# 5) 애플리케이션 복사 및 워킹 디렉터리 설정
WORKDIR /app
COPY main.py .
COPY scheduler.py .

# 6) 포트 노출 및 실행 명령어
EXPOSE 5000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
