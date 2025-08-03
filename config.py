import os
from pytz import timezone
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()

TOKEN = "7754876747:AAE0wnUih7111aqsGzb3wQFAAHrat6lg0gU"
ADMIN_ID = [7742837753, 618500315]
DB_PATH = "database/database.db"
DATA_JSON = "database/data.json"

us_tz = timezone("US/Eastern")
scheduler = AsyncIOScheduler(timezone=us_tz)
ping = "ping"
