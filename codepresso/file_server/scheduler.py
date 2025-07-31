import os
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from subprocess import run

scheduler = AsyncIOScheduler()

USER_BUCKET = 'codepresso-global-user-multi-file'
LOCAL_ROOT_PATH = '/config/workspace/'
ENV = os.environ['ENV']
USER_UUID = os.environ['USER_UUID']
TASK_ID = os.environ['TASK_ID']
S3_KEY_ROOT_PATH = 'backup'

# 2) 실제 수행할 비동기 작업
async def backup_to_s3():
    s3_key = f"{ENV}/{S3_KEY_ROOT_PATH}/{USER_UUID}/{TASK_ID}/"
    s3_path = f"s3://{USER_BUCKET}/{s3_key}"
    command = ["aws", "s3", "sync", LOCAL_ROOT_PATH, s3_path]
    print(f"[BACKUP] 시작 tid={TASK_ID}, command={' '.join(command)}")

    try:
        result = run(command, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[BACKUP] 성공 tid={TASK_ID}")
        else:
            print(f"[BACKUP] 실패 tid={TASK_ID}, stdout={result.stdout.strip()}, stderr={result.stderr.strip()}")

    except Exception as e:
        print(f"[TASK_ID] 예외 발생 tid={TASK_ID}: {e}")

# 3) 잡(job) 등록 함수
def init_scheduler(loop):
    scheduler = AsyncIOScheduler(event_loop=loop)

    # 클로저로 잡힌 loop를 job에서 사용
    def job_func():
        # loop.create_task는 이 루프가 돌고 있을 때만 동작
        loop.create_task(backup_to_s3())

    scheduler.add_job(job_func, 'interval', minutes=5)
    return scheduler

# 4) 앱 시작/종료 시 호출할 헬퍼
def start():
    init_scheduler().start()
    print("Scheduler started")

def shutdown():
    scheduler.shutdown()
    print("Scheduler shut down")
