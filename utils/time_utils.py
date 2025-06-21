from datetime import datetime
import pytz


def get_us_date():
    eastern = pytz.timezone("US/Eastern")
    now = datetime.now(eastern)
    return now.strftime("%d-%m-%Y %H:%M")
