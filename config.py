import os
from pytz import timezone
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
DB_PATH = os.getenv("DB_PATH")

us_tz = timezone("Europe/Kyiv")
scheduler = AsyncIOScheduler(timezone=us_tz)
