import os
from subprocess import run
from typing import List
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

import asyncio
from scheduler import init_scheduler, shutdown

app = FastAPI()

@app.put("/sync")
async def sync_from_s3(
        bucketName: str = Query(..., description="S3 버킷 이름"),
        env: str = Query(..., description="환경명 (dev, prod 등)"),
        taskId: List[int] = Query(..., description="동기화할 task ID 리스트"),
        destination: str = Query("/config/workspace", description="동기화 대상 디렉터리")
):
    print(f"[SYNC] 요청 수신 bucket={bucketName}, env={env}, taskIds={taskId}, dest={destination}")
    results = []

    for tid in taskId:
        s3_path = f"s3://{bucketName}/{env}/{tid}"
        command = ["aws", "s3", "sync", s3_path, destination]
        print(f"[SYNC] 시작 tid={tid}, command={' '.join(command)}")

        try:
            result = run(command, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"[SYNC] 성공 tid={tid}")
            else:
                print(f"[SYNC] 실패 tid={tid}, stdout={result.stdout.strip()}, stderr={result.stderr.strip()}")

            # 파일 권한 설정
            for root, dirs, files in os.walk(destination):
                for d in dirs:
                    os.chmod(os.path.join(root, d), 0o777)
                for f in files:
                    os.chmod(os.path.join(root, f), 0o777)

            results.append({
                "taskId": tid,
                "stdout": "ok" if result.returncode == 0 else result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "returncode": result.returncode
            })
        except Exception as e:
            print(f"[SYNC] 예외 발생 tid={tid}: {e}")
            results.append({
                "taskId": tid,
                "error": str(e)
            })

    return JSONResponse(content=results)

@app.put("/submit")
async def submit_to_s3(
        bucketName: str = Query(..., description="S3 버킷 이름"),
        env: str = Query(..., description="환경명 (dev, prod 등)"),
        userUUID: str = Query(..., description="사용자 UUID"),
        taskId: List[int] = Query(..., description="제출할 task ID 리스트"),
        domainType: str = Query(..., description="도메인 타입"),
        domainId: int = Query(..., description="도메인 ID")
):
    source_base = "/config/workspace"
    print(f"[SUBMIT] 요청 수신 bucket={bucketName}, env={env}, user={userUUID}, taskIds={taskId}, domain={domainType}/{domainId}")

    results = []

    for tid in taskId:
        local_path = os.path.join(source_base, str(tid))
        s3_key = f"{env}/{domainType}/{domainId}/{userUUID}/{tid}/submit_answer/"
        s3_path = f"s3://{bucketName}/{s3_key}"
        command = ["aws", "s3", "sync", local_path, s3_path]
        print(f"[SUBMIT] 시작 tid={tid}, command={' '.join(command)}")

        try:
            result = run(command, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"[SUBMIT] 성공 tid={tid}")
            else:
                print(f"[SUBMIT] 실패 tid={tid}, stdout={result.stdout.strip()}, stderr={result.stderr.strip()}")

            results.append({
                "taskId": tid,
                "stdout": "ok" if result.returncode == 0 else result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "returncode": result.returncode
            })
        except Exception as e:
            print(f"[SUBMIT] 예외 발생 tid={tid}: {e}")
            results.append({
                "taskId": tid,
                "error": str(e)
            })

    return JSONResponse(content=results)
    
@app.get("/health")
async def health_check():
    print("[HEALTH] Health check OK")
    return JSONResponse(content={"status": "ok"}, status_code=200)


@app.on_event("startup")
async def on_startup():
    loop = asyncio.get_running_loop()
    init_scheduler(loop).start()

@app.on_event("shutdown")
async def on_shutdown():
    shutdown()
