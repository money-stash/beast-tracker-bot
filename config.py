from pytz import timezone
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()

TOKEN = "8320007828:AAEP5V4hmMOXqLSY5mijPqqa0M5M5pQ-aU0"
ADMIN_ID = [7742837753, 618500315]
DB_PATH = "database/database.db"
DATA_JSON = "database/data.json"

us_tz = timezone("US/Eastern")
scheduler = AsyncIOScheduler(timezone=us_tz)
