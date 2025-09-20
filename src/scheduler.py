from apscheduler.schedulers.blocking import BlockingScheduler
from core import job_function
from database import init_db

if __name__ == "__main__":
    init_db()
    
    scheduler = BlockingScheduler(timezone="Asia/Tokyo")
    scheduler.add_job(job_function, 'cron', hour=8, minute=0)
    
    print("スケジューラーを開始します。Ctrl+Cで終了します。")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass