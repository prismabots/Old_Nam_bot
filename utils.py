import random
import re
import pytz
from datetime import datetime, timezone

def encode(cddb_func, table=None, num=6):
    """
    Generates a random numerical slug of a specified length.
    Optionally checks for uniqueness in a database table.
    """
    # slug = hashlib.sha256(str(num).encode()).hexdigest()[:6].upper()
    start = int(f"1{0:0{num}}")
    end = int(f"1{0:0{num+1}}") - 1
    slug = random.choice(range(start, end))
    if table is None:
        pass
    else:
        dbs = cddb_func(fun="co")
        dbs[1].execute(f"SELECT id FROM {table} where id = ?", (slug,))
        check = dbs[1].fetchone()
        cddb_func(fun="cn", db=dbs[0], cr=dbs[1])
        if check is not None:
            return encode(cddb_func, table, num)  # Recurse if slug exists

    return slug

def get_hex_color(input_text):
    """Converts a hexadecimal color string into an integer."""
    if input_text:
        try:
            return int(input_text, 16)
        except ValueError:
            pass  # handle invalid hex string
    return None

def getBiggerLenght(values):
    """Calculates the maximum string length from a list of values."""
    biggerLenth = 0
    for value in values:
        if len(str(value)) > biggerLenth:
            biggerLenth = len(str(value))
    return biggerLenth

def format_time(seconds):
    """Formats a duration in seconds into a human-readable string."""
    if seconds < 60:
        return f"{seconds} seconds"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''}"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''}"
    else:
        days = seconds // 86400
        return f"{days} day{'s' if days > 1 else ''}"

def convert_to_seconds(time_str):
    """Converts a time string (e.g., "1d2h30m") into a total number of seconds."""
    try:
        time_units = {
            's': 1, 'm': 60, 'h': 3600, 'd': 86400, 'w': 604800, 'mn': 86400 * 30,
        }
        total_seconds = 0
        matches = re.findall(r'(\d+)([smhdw]|mn)', time_str)

        for value, unit in matches:
            total_seconds += int(value) * time_units[unit]

        return total_seconds
    except:
        return None

def getTime(timeStamp = None , stampTime = None , strTime = None):
    """
    A utility function for handling time conversions and retrieval in the 'America/New_York' timezone.
    """
    eastern_timezone = pytz.timezone("America/New_York")
    utc_now = datetime.utcnow()
    eastern_now = pytz.utc.localize(utc_now).astimezone(eastern_timezone)
    if timeStamp == True :
        return eastern_now.timestamp()

    elif stampTime != None :
        # Create a timezone-aware datetime object directly
        time = datetime.fromtimestamp(stampTime, tz=timezone.utc)
        # The year replacement might not be desired in all cases, but keeping original logic
        time = time.replace(year=utc_now.year) # This was missing assignment
        return time.astimezone(eastern_timezone)

    elif strTime != None :
        try:
            date_format = "%m/%d" if len(strTime) <= 5 else "%m/%d/%y"
            time = datetime.strptime(strTime, date_format)
            return eastern_timezone.localize(datetime(day=time.day, month=time.month, year=time.year if date_format.endswith('y') else utc_now.year))
        except (ValueError, TypeError):
            return None # Return None on parsing error
    else:
        return eastern_now