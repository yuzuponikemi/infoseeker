from core import job_function
from database import init_db

if __name__ == "__main__":
    init_db()
    job_function()
