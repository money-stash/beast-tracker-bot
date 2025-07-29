import os
from pytz import timezone
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()

TOKEN = "7754876747:AAHowtL14Mcu_M8mfCXix_8p9vaDWtNUS_g"
ADMIN_ID = [7742837753, 618500315, 123456789]
DB_PATH = "database/database.db"

us_tz = timezone("US/Eastern")
scheduler = AsyncIOScheduler(timezone=us_tz)
