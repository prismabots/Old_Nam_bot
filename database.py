import sqlite3
import json
from datetime import datetime, timedelta
import utils


def cddb(fun, db=None, cr=None):
    if fun == "co":
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

        return db, cr
    elif fun == "cn":
        db.commit()
        cr.close()
        db.close()


def get_from_json():
    with open("config.json", "r") as config:
        config = json.load(config)
    return config


def is_server(guild_id):
    guild_id = guild_id.guild.id
    dbs = cddb(fun="co")
    columeName = "servers"

    dbs[1].execute(f"INSERT OR IGNORE INTO {columeName}(id) VALUES(?)", (guild_id,))
    cddb(fun="cn", db=dbs[0], cr=dbs[1])
    return True


def is_promo_server(guild_id):
    guild_id = guild_id.guild.id
    dbs = cddb(fun="co")
    columeName = "promo_servers"

    dbs[1].execute(f"INSERT OR IGNORE INTO {columeName}(id) VALUES(?)", (guild_id,))
    cddb(fun="cn", db=dbs[0], cr=dbs[1])
    return True


def is_admin(interaction):
    mainconfig = get_from_json()
    admin_id = interaction.user.id
    if admin_id in mainconfig["admins"]:
        return True
    else:
        return False


def getTodayTrades():
    dbs = cddb(fun="co")
    daystart = utils.getTime().replace(hour=0, minute=0, second=0, microsecond=0)

    dbs[1].execute("SELECT * FROM trades where open_date >= ? ORDER BY open_date", (daystart.timestamp(),))
    trades = dbs[1].fetchall()
    title = f"Trades Summary {daystart.strftime('%m/%d')}"
    cddb(fun="cn", db=dbs[0], cr=dbs[1])
    return trades, title


def getThisMonthTrades(justTime=False):
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
        return last_1_month, title

    return trades, title


def getThisWeekTrades(justTime=False):
    dbs = cddb(fun="co")
    now = utils.getTime().replace(hour=0, minute=0, second=0, microsecond=0)
    days_until_last_monday = now.weekday()
    last_monday = now - timedelta(days=days_until_last_monday)
    lastweek = last_monday.timestamp()
    title = f"Trades Summary (From {last_monday.strftime('%m/%d')} to {(last_monday + timedelta(days=7)).strftime('%m/%d')})"

    if justTime:
        cddb(fun="cn", db=dbs[0], cr=dbs[1])
        return last_monday, title

    dbs[1].execute("SELECT * FROM trades where open_date >= ? ORDER BY open_date", (lastweek,))
    trades = dbs[1].fetchall()

    cddb(fun="cn", db=dbs[0], cr=dbs[1])
    return trades, title


def getCustomTimeTrades(start, end):
    dbs = cddb(fun="co")
    start_date_object = utils.getTime(strTime=start)
    end_date_object = utils.getTime(strTime=end)

    dbs[1].execute(
        "SELECT * FROM trades WHERE open_date >= ? AND open_date <= ? ORDER BY open_date",
        (start_date_object.timestamp(), end_date_object.timestamp())
    )
    trades = dbs[1].fetchall()
    title = f"Trades Summary (From {start_date_object.strftime('%m/%d')} to {end_date_object.strftime('%m/%d')})"

    cddb(fun="cn", db=dbs[0], cr=dbs[1])
    return trades, title


def getDayStats(day, style=0):
    dbs = cddb(fun="co")
    start_date_object = utils.getTime(strTime=day)
    end_date_object = start_date_object + timedelta(days=1)
    dbs[1].execute("SELECT open_price,close_price FROM trades where ? <= open_date and open_date < ? ORDER BY open_date", (start_date_object.timestamp(), end_date_object.timestamp()))

    trades = dbs[1].fetchall()
    if trades:
        stats = sum((trade[1] - trade[0]) * 100 for trade in trades if trade[1] != 0)
        stats = float(f"{stats:.1f}")
    else:
        stats = 0

    cddb(fun="cn", db=dbs[0], cr=dbs[1])
    return (start_date_object.strftime("%A") if style == 0 else start_date_object.strftime("%m/%d"), stats)