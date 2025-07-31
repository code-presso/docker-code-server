
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 204573508773.dkr.ecr.ap-northeast-2.amazonaws.com

docker build -t coderun-code-server:base .

docker tag coderun-code-server:base 204573508773.dkr.ecr.ap-northeast-2.amazonaws.com/coderun-code-server:base

docker push 204573508773.dkr.ecr.ap-northeast-2.amazonaws.com/coderun-code-server:base
