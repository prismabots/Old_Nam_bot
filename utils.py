import random
import re
import pytz
import logging
from datetime import datetime, timezone

# Configure logging
logger = logging.getLogger(__name__)

def encode(cddb_func, table=None, num=6):
    """
    Generates a random numerical slug of a specified length.
    Optionally checks for uniqueness in a database table.
    """
    logger.info(f"Generating encode with table={table}, num={num}")
    try:
        # slug = hashlib.sha256(str(num).encode()).hexdigest()[:6].upper()
        start = int(f"1{0:0{num}}")
        end = int(f"1{0:0{num+1}}") - 1
        slug = random.choice(range(start, end))
        if table is None:
            logger.debug(f"Generated slug without table check: {slug}")
        else:
            dbs = cddb_func(fun="co")
            dbs[1].execute(f"SELECT id FROM {table} where id = ?", (slug,))
            check = dbs[1].fetchone()
            cddb_func(fun="cn", db=dbs[0], cr=dbs[1])
            if check is not None:
                logger.debug(f"Slug {slug} already exists, regenerating")
                return encode(cddb_func, table, num)  # Recurse if slug exists
            logger.debug(f"Generated unique slug: {slug}")

        return slug
    except Exception as e:
        logger.error(f"Error in encode: {e}")
        raise

def get_hex_color(input_text):
    """Converts a hexadecimal color string into an integer."""
    logger.info(f"Converting hex color: {input_text}")
    if input_text:
        try:
            color_int = int(input_text, 16)
            logger.debug(f"Hex color {input_text} converted to {color_int}")
            return color_int
        except ValueError as e:
            logger.warning(f"Invalid hex color string: {input_text}, error: {e}")
            pass  # handle invalid hex string
    return None

def getBiggerLenght(values):
    """Calculates the maximum string length from a list of values."""
    logger.info(f"Calculating max length for {len(values) if hasattr(values, '__len__') else 'unknown'} values")
    try:
        biggerLenth = 0
        for value in values:
            if len(str(value)) > biggerLenth:
                biggerLenth = len(str(value))
        logger.debug(f"Max length calculated: {biggerLenth}")
        return biggerLenth
    except TypeError as e:
        logger.error(f"Invalid values type in getBiggerLenght: {e}")
        return 0
    except Exception as e:
        logger.error(f"Error in getBiggerLenght: {e}")
        raise

def format_time(seconds):
    """Formats a duration in seconds into a human-readable string."""
    logger.info(f"Formatting time: {seconds} seconds")
    try:
        if not isinstance(seconds, (int, float)) or seconds < 0:
            logger.warning(f"Invalid seconds value: {seconds}")
            return "Invalid time"
            
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
    except Exception as e:
        logger.error(f"Error in format_time: {e}")
        return "Error formatting time"

def convert_to_seconds(time_str):
    """Converts a time string (e.g., "1d2h30m") into a total number of seconds."""
    logger.info(f"Converting time string to seconds: {time_str}")
    try:
        time_units = {
            's': 1, 'm': 60, 'h': 3600, 'd': 86400, 'w': 604800, 'mn': 86400 * 30,
        }
        total_seconds = 0
        matches = re.findall(r'(\d+)([smhdw]|mn)', time_str)

        if not matches:
            logger.warning(f"No valid time units found in: {time_str}")
            return None

        for value, unit in matches:
            total_seconds += int(value) * time_units[unit]

        logger.debug(f"Converted {time_str} to {total_seconds} seconds")
        return total_seconds
    except Exception as e:
        logger.error(f"Error converting time string '{time_str}': {e}")
        return None

def getTime(timeStamp = None , stampTime = None , strTime = None):
    """
    A utility function for handling time conversions and retrieval in the 'America/New_York' timezone.
    """
    logger.info(f"Getting time - timeStamp={timeStamp}, stampTime={stampTime}, strTime={strTime}")
    try:
        eastern_timezone = pytz.timezone("America/New_York")
        utc_now = datetime.utcnow()
        eastern_now = pytz.utc.localize(utc_now).astimezone(eastern_timezone)
        
        if timeStamp == True :
            timestamp = eastern_now.timestamp()
            logger.debug(f"Returning timestamp: {timestamp}")
            return timestamp

        elif stampTime != None :
            # Create a timezone-aware datetime object directly
            time = datetime.fromtimestamp(stampTime, tz=timezone.utc)
            # The year replacement might not be desired in all cases, but keeping original logic
            time = time.replace(year=utc_now.year) # This was missing assignment
            result = time.astimezone(eastern_timezone)
            logger.debug(f"Converted timestamp {stampTime} to {result}")
            return result

        elif strTime != None :
            try:
                date_format = "%m/%d" if len(strTime) <= 5 else "%m/%d/%y"
                time = datetime.strptime(strTime, date_format)
                result = eastern_timezone.localize(datetime(day=time.day, month=time.month, year=time.year if date_format.endswith('y') else utc_now.year))
                logger.debug(f"Parsed time string '{strTime}' to {result}")
                return result
            except (ValueError, TypeError) as e:
                logger.error(f"Error parsing time string '{strTime}': {e}")
                return None # Return None on parsing error
        else:
            logger.debug(f"Returning current eastern time: {eastern_now}")
            return eastern_now
    except Exception as e:
        logger.error(f"Unexpected error in getTime: {e}")
        raise