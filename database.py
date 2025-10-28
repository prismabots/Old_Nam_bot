import sqlite3
import json
import logging
from datetime import datetime, timedelta
import utils

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def cddb(fun, db=None, cr=None):
    logger.info(f"cddb called with fun={fun}")
    try:
        if fun == "co":
            logger.debug("Opening database connection")
            db = sqlite3.connect("data.db")
            cr = db.cursor()
            cr.execute("""
                CREATE TABLE IF NOT EXISTS servers (
                    id INTEGER PRIMARY KEY,
                    config TEXT DEFAULT '{}'
                )
            """)
            cr.execute("""
                CREATE TABLE IF NOT EXISTS promo_servers (
                    id INTEGER PRIMARY KEY,
                    config TEXT DEFAULT '{}'
                )
            """)
            cr.execute("""
                CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY,
                    status INTEGER ,
                    stock TEXT ,
                    strike INTEGER ,
                    direetion INTEGER ,
                    open_price INTEGER ,
                    close_price INTEGER DEFAULT 0 ,
                    open_date INTEGER , 
                    close_date INTEGER DEFAULT 0 ,
                    expiry TEXT
                )
            """)
            logger.debug("Database tables created/verified successfully")
            return db, cr
        elif fun == "cn":
            if db is None or cr is None:
                logger.error("Attempted to close database with None values")
                return
            logger.debug("Closing database connection")
            db.commit()
            cr.close()
            db.close()
            logger.debug("Database connection closed successfully")
    except sqlite3.Error as e:
        logger.error(f"Database error in cddb: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in cddb: {e}")
        raise


def get_from_json():
    logger.info("Getting configuration from config.json")
    try:
        with open("config.json", "r") as config:
            config = json.load(config)
        logger.debug("Configuration loaded successfully")
        return config
    except FileNotFoundError:
        logger.error("config.json file not found")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in config.json: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error reading config.json: {e}")
        raise


def is_server(guild_id):
    logger.info(f"Checking if server exists: guild_id={guild_id}")
    try:
        guild_id = guild_id.guild.id
        dbs = cddb(fun="co")
        columeName = "servers"

        dbs[1].execute(f"INSERT OR IGNORE INTO {columeName}(id) VALUES(?)", (guild_id,))
        cddb(fun="cn", db=dbs[0], cr=dbs[1])
        logger.debug(f"Server {guild_id} verified/inserted successfully")
        return True
    except AttributeError as e:
        logger.error(f"Invalid guild_id object: {e}")
        raise
    except Exception as e:
        logger.error(f"Error in is_server: {e}")
        raise


def is_promo_server(guild_id):
    logger.info(f"Checking if promo server exists: guild_id={guild_id}")
    try:
        guild_id = guild_id.guild.id
        dbs = cddb(fun="co")
        columeName = "promo_servers"

        dbs[1].execute(f"INSERT OR IGNORE INTO {columeName}(id) VALUES(?)", (guild_id,))
        cddb(fun="cn", db=dbs[0], cr=dbs[1])
        logger.debug(f"Promo server {guild_id} verified/inserted successfully")
        return True
    except AttributeError as e:
        logger.error(f"Invalid guild_id object: {e}")
        raise
    except Exception as e:
        logger.error(f"Error in is_promo_server: {e}")
        raise


def is_admin(interaction):
    logger.info(f"Checking admin status for user: {interaction.user.id}")
    try:
        mainconfig = get_from_json()
        admin_id = interaction.user.id
        
        if "admins" not in mainconfig:
            logger.warning("'admins' key not found in config.json")
            return False
            
        is_admin_user = admin_id in mainconfig["admins"]
        logger.debug(f"User {admin_id} admin status: {is_admin_user}")
        return is_admin_user
    except AttributeError as e:
        logger.error(f"Invalid interaction object: {e}")
        return False
    except Exception as e:
        logger.error(f"Error in is_admin: {e}")
        return False


def getTodayTrades():
    logger.info("Retrieving today's trades")
    try:
        dbs = cddb(fun="co")
        daystart = utils.getTime().replace(hour=0, minute=0, second=0, microsecond=0)

        dbs[1].execute("SELECT * FROM trades where open_date >= ? ORDER BY open_date", (daystart.timestamp(),))
        trades = dbs[1].fetchall()
        title = f"Trades Summary {daystart.strftime('%m/%d')}"
        cddb(fun="cn", db=dbs[0], cr=dbs[1])
        logger.debug(f"Retrieved {len(trades)} trades for today")
        return trades, title
    except Exception as e:
        logger.error(f"Error in getTodayTrades: {e}")
        raise


def getThisMonthTrades(justTime=False):
    logger.info(f"Retrieving this month's trades (justTime={justTime})")
    try:
        dbs = cddb(fun="co")
        last_1_month = utils.getTime().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        dbs[1].execute("SELECT * FROM trades where open_date >= ? ORDER BY open_date", (last_1_month.timestamp(),))
        trades = dbs[1].fetchall()
        if last_1_month.month == 12:
            next_month = last_1_month.replace(month=1, year=last_1_month.year + 1).strftime('%m/%d/%y')
        else:
            next_month = last_1_month.replace(month=last_1_month.month + 1)
        title = f"Trades Summary (From {last_1_month.strftime('%m/%d')} to {next_month})"

        cddb(fun="cn", db=dbs[0], cr=dbs[1])
        
        if justTime:
            logger.debug("Returning time information only")
            return last_1_month, title

        logger.debug(f"Retrieved {len(trades)} trades for this month")
        return trades, title
    except Exception as e:
        logger.error(f"Error in getThisMonthTrades: {e}")
        raise


def getThisWeekTrades(justTime=False):
    logger.info(f"Retrieving this week's trades (justTime={justTime})")
    try:
        dbs = cddb(fun="co")
        now = utils.getTime().replace(hour=0, minute=0, second=0, microsecond=0)
        days_until_last_monday = now.weekday()
        last_monday = now - timedelta(days=days_until_last_monday)
        lastweek = last_monday.timestamp()
        title = f"Trades Summary (From {last_monday.strftime('%m/%d')} to {(last_monday + timedelta(days=7)).strftime('%m/%d')})"

        if justTime:
            cddb(fun="cn", db=dbs[0], cr=dbs[1])
            logger.debug("Returning time information only")
            return last_monday, title

        dbs[1].execute("SELECT * FROM trades where open_date >= ? ORDER BY open_date", (lastweek,))
        trades = dbs[1].fetchall()

        cddb(fun="cn", db=dbs[0], cr=dbs[1])
        logger.debug(f"Retrieved {len(trades)} trades for this week")
        return trades, title
    except Exception as e:
        logger.error(f"Error in getThisWeekTrades: {e}")
        raise


def getCustomTimeTrades(start, end):
    logger.info(f"Retrieving custom time trades: start={start}, end={end}")
    try:
        dbs = cddb(fun="co")
        start_date_object = utils.getTime(strTime=start)
        end_date_object = utils.getTime(strTime=end)
        
        if start_date_object is None or end_date_object is None:
            logger.error(f"Invalid date format: start={start}, end={end}")
            raise ValueError("Invalid date format")

        dbs[1].execute(
            "SELECT * FROM trades WHERE open_date >= ? AND open_date <= ? ORDER BY open_date",
            (start_date_object.timestamp(), end_date_object.timestamp())
        )
        trades = dbs[1].fetchall()
        title = f"Trades Summary (From {start_date_object.strftime('%m/%d')} to {end_date_object.strftime('%m/%d')})"

        cddb(fun="cn", db=dbs[0], cr=dbs[1])
        logger.debug(f"Retrieved {len(trades)} trades for custom time range")
        return trades, title
    except Exception as e:
        logger.error(f"Error in getCustomTimeTrades: {e}")
        raise


def getDayStats(day, style=0):
    logger.info(f"Getting day stats for: day={day}, style={style}")
    try:
        dbs = cddb(fun="co")
        start_date_object = utils.getTime(strTime=day)
        
        if start_date_object is None:
            logger.error(f"Invalid date format: day={day}")
            raise ValueError("Invalid date format")
            
        end_date_object = start_date_object + timedelta(days=1)
        dbs[1].execute("SELECT open_price,close_price FROM trades where ? <= open_date and open_date < ? ORDER BY open_date", (start_date_object.timestamp(), end_date_object.timestamp()))

        trades = dbs[1].fetchall()
        if trades:
            stats = sum((trade[1] - trade[0]) * 100 for trade in trades if trade[1] != 0)
            stats = float(f"{stats:.1f}")
        else:
            stats = 0

        cddb(fun="cn", db=dbs[0], cr=dbs[1])
        logger.debug(f"Day stats calculated: {stats}% for {len(trades)} trades")
        return (start_date_object.strftime("%A") if style == 0 else start_date_object.strftime("%m/%d"), stats)
    except Exception as e:
        logger.error(f"Error in getDayStats: {e}")
        raise