import os
from pytz import timezone
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()

TOKEN = "7754876747:AAFcB_ToTyvi-xg85rOJ9GJH5ZPxo_sYEvQ"
ADMIN_ID = [7742837753, 618500315]
DB_PATH = "database/database.db"
DATA_JSON = "database/data.json"

us_tz = timezone("US/Eastern")
scheduler = AsyncIOScheduler(timezone=us_tz)
ping = "ping"
