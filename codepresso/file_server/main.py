from fastapi import FastAPI, Query
from typing import List
from subprocess import run
from fastapi.responses import JSONResponse
import os

app = FastAPI()

@app.put("/sync")
async def sync_from_s3(
    bucketName: str = Query(...),
    env: str = Query(...),
    taskId: List[int] = Query(...),
    destination: str = Query("/config/workspace")  # Set default value here
):
    results = []

    for tid in taskId:
        s3_path = f"s3://{bucketName}/{env}/{tid}"
        command = ["aws", "s3", "sync", s3_path, destination]

        try:
            result = run(command, capture_output=True, text=True)

            # Recursively set permissions to be readable and writable by all
            for root, dirs, files in os.walk(destination):
                for d in dirs:
                    os.chmod(os.path.join(root, d), 0o777)
                for f in files:
                    os.chmod(os.path.join(root, f), 0o666)

            results.append({
                "taskId": tid,
                "stdout": "ok" if result.returncode == 0 else result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "returncode": result.returncode
            })
        except Exception as e:
            results.append({
                "taskId": tid,
                "error": str(e)
            })

    return JSONResponse(content=results)

@app.get("/health")
async def health_check():
    # You can add more checks here like database, services, etc.
    return JSONResponse(content={"status": "ok"}, status_code=200)
