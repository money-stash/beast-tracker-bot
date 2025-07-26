import os
from pytz import timezone
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()

TOKEN = "7682380679:AAFdq2roYQgRQX9XJu6fNpmH-sBVG2MMW0A"
ADMIN_ID = [7742837753, 618500315, 123456789]
DB_PATH = "database/database.db"

us_tz = timezone("Europe/Kyiv")
scheduler = AsyncIOScheduler(timezone=us_tz)
