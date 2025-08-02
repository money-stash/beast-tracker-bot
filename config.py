import os
from pytz import timezone
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()

TOKEN = "7682380679:AAFdq2roYQgRQX9XJu6fNpmH-sBVG2MMW0A"
ADMIN_ID = [7742837753, 618500315]
DB_PATH = "database/database.db"
DATA_JSON = "database/data.json"

us_tz = timezone("US/Eastern")
scheduler = AsyncIOScheduler(timezone=us_tz)
