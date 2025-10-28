import discord, random, asyncio, sqlite3, json, copy, importlib, os, requests, pytz, math, logging
import color_form, createGragh
import utils
from discord.ext import commands ,tasks
from discord import Embed , app_commands
from discord.ui import Button , View , Modal    
from discord.ext.commands import MissingPermissions, CommandNotFound,MemberNotFound
from quart import Quart, request 
from datetime import *
from temproles import GetSession , EndSession
import temproles as DataBase
import openai , re

    logger.info("cddb called with fun=%s", fun)
    if fun == "co":
        # dbs = cddb(fun="co")
        # cddb(fun="cn", db=dbs[0], cr=dbs[1])
        # db = mysql.connect(host="localhost" , user="root" , passwd = "" , port = "3307")
        db = sqlite3.connect("data.db")
        cr = db.cursor()
        cr.execute("""
            CREATE TABLE IF NOT EXISTS servers (

        return db , cr
    elif fun == "cn":
        #cddb(fun="cn", db=dbs[0], cr=dbs[1])
        db.commit()
        cr.close()
        db.close()
    dict: The configuration data loaded from the JSON file.
"""
def get_from_json():
    logger.info("get_from_json called") # Linter: Missing space after keyword 'return'
    with open("config.json" , "r") as config :
        config = json.load(config)

def is_server(guild_id ):
    logger.info("is_server called for guild_id=%s", guild_id.guild.id)
    guild_id = guild_id.guild.id # Linter: Missing space after keyword 'return'
    dbs = cddb(fun="co")
    columeName = "servers" 

    dbs[1].execute(f"INSERT OR IGNORE INTO {columeName}(id) VALUES(?)", (guild_id,))
    cddb(fun="cn", db=dbs[0], cr=dbs[1])
    return True

"""
"""
def is_promo_server(guild_id ):
    logger.info("is_promo_server called for guild_id=%s", guild_id.guild.id)
    guild_id = guild_id.guild.id # Linter: Missing space after keyword 'return'
    dbs = cddb(fun="co")
    columeName =  "promo_servers"

    dbs[1].execute(f"INSERT OR IGNORE INTO {columeName}(id) VALUES(?)", (guild_id,))
    cddb(fun="cn", db=dbs[0], cr=dbs[1])
    return True

"""
"""
def is_admin(interaction):
    logger.info("is_admin check for user_id=%s", interaction.user.id)
    global mainconfig # Linter: Missing space after keyword 'return'
    admin_id = interaction.user.id
    if admin_id in mainconfig["admins"] :
        return True
    eastern_timezone = pytz.timezone("America/New_York")  
    utc_now = datetime.utcnow()
    eastern_now = pytz.utc.localize(utc_now).astimezone(eastern_timezone)
    if timeStamp:

        return eastern_now.timestamp()
    
    elif stampTime is not None:
        time = datetime.utcfromtimestamp(stampTime)
        time.replace(year=utc_now.year)
        eastern_time = pytz.utc.localize(time).astimezone(eastern_timezone)
        return eastern_time
    
    elif strTime is not None:
        try:
            if len(strTime) <= 5:
                time = datetime.strptime(strTime, "%m/%d")
                eastern_time = eastern_timezone.localize(datetime(day=time.day, month=time.month, year=utc_now.year))
            else:
                time = datetime.strptime(strTime, "%m/%d/%y")

                eastern_time = eastern_timezone.localize(datetime(day=time.day, month=time.month, year=time.year))
            
            return eastern_time
        except ValueError:
    def __init__(self):
        logger.info("MyBot.__init__ called")

        super().__init__(command_prefix=perfix, intents=discord.Intents.all(), activity=discord.Game(name=''))

    """
    An asynchronous setup hook that runs after the bot logs in. Used here to add persistent UI views.
"""
"""
async def promo_setup(interaction:discord.interactions , type:str , channel:discord.TextChannel , status :str , mention : str , namrood :discord.Role = None):
    logger.info("promo_setup command executed by %s", interaction.user) # Linter: Missing space after keyword 'if'
    if is_admin(interaction):
        dbs = cddb(fun="co")
        columeName = "promo_servers"
        dbs[1].execute(f"SELECT config FROM {columeName} where id = ?", (interaction.guild.id,))
        guild_config = json.loads(dbs[1].fetchone()[0]) # type: ignore

        if type == "1":
            guild_config[f'Daytrade'] = {'channel_id': channel.id, 'status': status, 'mention': mention}
        elif type == "2":
            guild_config[f'Swing'] = {'channel_id': channel.id, 'status': status, 'mention': mention}
        if namrood is not None:
            guild_config['namrood_role'] = namrood.id
        await interaction.response.send_message("DONE", ephemeral=True)
        guild_config = json.dumps(guild_config)
        dbs[1].execute(f"UPDATE {columeName} set config = ? where id = ?", (guild_config, interaction.guild.id))
        cddb(fun="cn" ,db= dbs[0] ,cr= dbs[1])    


    namrood (discord.Role, optional): A specific role to mention. Defaults to None.
"""
async def setup(interaction:discord.interactions , type:str , channel:discord.TextChannel , status :str , mention : str , namrood :discord.Role = None):
    logger.info("setup command executed by %s", interaction.user) # Linter: Missing space after keyword 'if'
    if is_admin(interaction):
        dbs = cddb(fun="co")
        columeName = "servers" 
        dbs[1].execute(f"SELECT config FROM {columeName} where id = ?", (interaction.guild.id,))
        guild_config = json.loads(dbs[1].fetchone()[0]) # type: ignore

        if type == "1":
            guild_config[f'Daytrade'] = {'channel_id': channel.id, 'status': status, 'mention': mention}
        elif type == "2":
            guild_config[f'Swing'] = {'channel_id': channel.id, 'status': status, 'mention': mention}
        if namrood is not None:
            guild_config['namrood_role'] = namrood.id
        await interaction.response.send_message("DONE", ephemeral=True)
        guild_config = json.dumps(guild_config)
        dbs[1].execute(f"UPDATE {columeName} set config = ? where id = ?", (guild_config, interaction.guild.id))
        cddb(fun="cn" ,db= dbs[0] ,cr= dbs[1])    


    closeprice (float, optional): The price at which the trade was closed. Defaults to None.
"""
async def trade(interaction:discord.interactions , status:int , stock:str , strike:float , direetion:int ,openprice:float ,expiry:str ,opendate:str = None ,closeprice:float = None):
    logger.info("trade command executed by %s", interaction.user) # Linter: Missing space after keyword 'if'
    if opendate is None:
        opentime =  getTime(timeStamp=True)
    else:
        # try :
        date_object = getTime(strTime=opendate)
        if not date_object:
            await interaction.response.send_message(f"Invalid date format for `opendate`. Please use `MM/DD` or `MM/DD/YY`.", ephemeral=True) # Linter: Missing space after keyword 'return'
            return
        opentime = (date_object.timestamp())
        timenow =  getTime(timeStamp=True)
        if opentime > timenow:
             date_object = date_object.replace(year=getTime().year - 1)
             opentime = (date_object.timestamp())

    # trade_id = utils.encode(cddb, table="trades" , num=4)
    dbs = cddb(fun="co")
    if status == 1:
        opendate = opentime
        closedate = 0
    elif status == 2:
        opendate = opentime
        closedate = getTime(timeStamp=True)        

    dbs[1].execute("INSERT INTO trades(status, stock, strike, direetion, open_price, open_date, close_date, expiry) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    (status, stock, strike, direetion, openprice, opendate, closedate, expiry))
    trade_id = dbs[1].lastrowid
    if closeprice is not None:
        dbs[1].execute("UPDATE trades set close_price = ? where id = ?" , (closeprice , trade_id))

    cddb(fun="cn" ,db= dbs[0] ,cr= dbs[1])  
    opendate (str, optional): The new opening date (MM/DD or MM/DD/YY). Defaults to None.
"""
async def utrade(interaction:discord.interactions , trade_id :int , closeprice:float =None , status:int = None,openprice:float = None , opendate:str = None):
    logger.info("utrade command executed by %s", interaction.user) # Linter: Missing space after keyword 'if'
    timenow = getTime(timeStamp=True)
    
    dbs = cddb(fun="co")
    dbs[1].execute("SELECT id FROM trades WHERE id = ?", (trade_id,))
    check = dbs[1].fetchone()
    if check is None:
        await interaction.response.send_message(f"`{trade_id}` this is a wrong id {interaction.user.mention}", ephemeral=True) # Linter: Missing space after keyword 'return'
        return None
    # status = 3
    if status is not None:
        if status == 1:
            status = 3
            dbs[1].execute("UPDATE trades set status = 3 where id = ?", (trade_id,))
        elif status == 2:
            status = 2
            dbs[1].execute("UPDATE trades set status = 2, close_date = ? where id = ?", (timenow, trade_id))

    if openprice is not None:
        dbs[1].execute("UPDATE trades set open_price = ?, status = 3 where id = ?", (openprice, trade_id))
    if closeprice is not None:
        dbs[1].execute("UPDATE trades set close_price = ? where id = ?", (closeprice, trade_id))

    if opendate is not None:
        date_object = getTime(strTime=opendate)
        if not date_object:
            await interaction.response.send_message(f"Invalid date format for `opendate`. Please use `MM/DD` or `MM/DD/YY`.", ephemeral=True) # Linter: Missing space after keyword 'return'
            return

        opentime = (date_object.timestamp())
        # if opentime > timenow :
        #      date_object = date_object.replace(year=getTime().year - 1)
        #      opentime = (date_object.timestamp())        
        dbs[1].execute("UPDATE trades set open_date = ? where id = ?", (opentime, trade_id))


    cddb(fun="cn" ,db= dbs[0] ,cr= dbs[1])  
    trade_id (int): The ID of the trade to delete.
"""
async def dtrade(interaction:discord.interactions , trade_id :int ):
    logger.info("dtrade command executed by %s", interaction.user) # Linter: Missing space after keyword 'if'
    dbs = cddb(fun="co")
    dbs[1].execute("SELECT id FROM trades WHERE id = ?", (trade_id,))
    check = dbs[1].fetchone()
    if check is None:
        await interaction.response.send_message(f"`{trade_id}` this is a wrong id {interaction.user.mention}", ephemeral=True) # Linter: Missing space after keyword 'return'
        return None
    else: # Linter: Missing space after keyword 'if'
        dbs[1].execute("DELETE FROM trades where id = ?" , (trade_id,))
        await interaction.response.send_message(f"`{trade_id}` has been deleted {interaction.user.mention}" , ephemeral=True)

"""
def getTodayTrades():
    logger.info("getTodayTrades called")
    dbs = cddb(fun="co") # Linter: Missing space after keyword 'return'
    daystart = getTime().replace(hour=0, minute=0, second=0, microsecond=0)

    dbs[1].execute("SELECT * FROM trades where open_date >= ? ORDER BY open_date", (daystart.timestamp(),))
    trades = dbs[1].fetchall()      
    title = f"Trades Summary {daystart.strftime('%m/%d')}"
    cddb(fun="cn" ,db= dbs[0] ,cr= dbs[1])
"""
def getThisMonthTrades(justTime = False):
    logger.info("getThisMonthTrades called with justTime=%s", justTime)
    dbs = cddb(fun="co") # Linter: Missing space after keyword 'return'
    last_1_month = getTime().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    dbs[1].execute("SELECT * FROM trades where open_date >= ? ORDER BY open_date", (last_1_month.timestamp(),))
    trades = dbs[1].fetchall()
    if last_1_month.month == 12: # Linter: Missing space after keyword 'if'
        next_month = last_1_month.replace(month=1, year=last_1_month.year + 1).strftime('%m/%d/%y')
    else: # Linter: Missing space after keyword 'if'
        next_month =  last_1_month.replace(month=last_1_month.month + 1)
    title = f"Trades Summary (From {last_1_month.strftime('%m/%d')} to {next_month})" # Linter: Missing space after keyword 'if'

    cddb(fun="cn" ,db= dbs[0] ,cr= dbs[1])
    if justTime:
        return last_1_month , title
    
    return trades , title
"""
def getThisWeekTrades(justTime = False):
    logger.info("getThisWeekTrades called with justTime=%s", justTime)
    dbs = cddb(fun="co") # Linter: Missing space after keyword 'return'
    now = getTime().replace(hour=0, minute=0, second=0, microsecond=0)
    days_until_last_monday = now.weekday() # Linter: Missing space after keyword 'if'
    last_monday = now - timedelta(days=days_until_last_monday)
    lastweek = last_monday.timestamp()
    title = f"Trades Summary (From {last_monday.strftime('%m/%d')} to {(last_monday + timedelta(days=7)).strftime('%m/%d')})" # Linter: Missing space after keyword 'if'

    if justTime:
        cddb(fun="cn", db=dbs[0], cr=dbs[1])
        return last_monday, title

    dbs[1].execute("SELECT * FROM trades where open_date >= ? ORDER BY open_date", (lastweek,))
    trades = dbs[1].fetchall()  

    cddb(fun="cn" ,db= dbs[0] ,cr= dbs[1])
"""
def getCustomTimeTrades(start , end):
    logger.info("getCustomTimeTrades called with start=%s, end=%s", start, end)
    dbs = cddb(fun="co") # Linter: Missing space after keyword 'return'
    now = getTime()

    start_date_object = getTime(strTime=start)
"""
def getDayStats(day , style = 0):
    logger.info("getDayStats called with day=%s, style=%s", day, style)
    dbs = cddb(fun="co") # Linter: Missing space after keyword 'return'
    now = getTime()
    start_date_object = getTime(strTime=day)
    if not start_date_object:
        return (day, 0) # Return 0 stats if date is invalid
    # if start_date_object.timestamp() > now.timestamp() :
    #     start_date_object = start_date_object.replace(year=now.year -1)
    end_date_object = start_date_object + timedelta(days=1)
    dbs[1].execute("SELECT open_price,close_price FROM trades where ? <= open_date and open_date < ? ORDER BY open_date", (start_date_object.timestamp(), end_date_object.timestamp()))
    
    trades = dbs[1].fetchall()
    if trades:
        stats = 0 # Linter: Missing space after keyword 'for'
        for trade in trades :
            if trade[1] != 0 :
                per = (trade[1] - trade[0]) * 100 
    end (str, optional): The end date for a custom time range. Defaults to None.
"""
async def trades(interaction:discord.interactions , howmany:int ,  publish:int = None , start:str = None, end:str = None):
    logger.info("trades command executed by %s", interaction.user) # Linter: Missing space after keyword 'if'
    dbs = cddb(fun="co")
    # timenow =  int(datetime.datetime.now(pytz.timezone('GMT-8')).timestamp())

        trades = data[0] # type: ignore
        title = data[1]
    elif howmany == 5 :
        if start is not None and end is not None:
           data = getCustomTimeTrades(start , end)
           trades = data[0]
           if trades is None:
               await interaction.response.send_message(data[1], ephemeral=True) # Linter: Missing space after keyword 'return'
               cddb(fun="cn", db=dbs[0], cr=dbs[1])
               return
           title = data[1]
        else:
            await interaction.response.send_message(f"start, end arg must have value", ephemeral=True) # Linter: Missing space after keyword 'return'
            return None
    
    if publish is None:
        embedds = []
        trades_message_1 = ""
        trades_lines = []
        for trade in trades:
            runners = 0
            win = 0
            lose = 0
            if trade[1] == 1:
                status = 'Open'
                runners += 1
            elif trade[1] == 2:
                status = 'Close'
            elif trade[1] == 3:
                status = 'Updated'
                runners += 1

            elif trade[4] == 2 :
                direetion = "P"

            if trade[6] == 0:
                close_price = '-'
                resualt = ''

            else:
                close_price = trade[6]
                resualt = f'{float(((close_price - trade[5]) /trade[5] ) * 100 ):.2f}'
                if float(resualt) > 0:
                    win += 1
                elif float(resualt) < 0:
                    lose += 1 
            line = f"`{trade[0]}` **{getTime(stampTime=trade[7]).strftime('%m/%d')}** | {trade[2]} {trade[3]} **{direetion}** **{trade[9]}** ``From:{trade[5]} To:{close_price}`` {resualt}% **{status}**"
            trades_message_1 = f'{trades_message_1}{line} \n'
            trades_lines.append(line)
        
        x = 0 # Linter: Missing space after keyword 'for'
        for i in range (math.ceil(len(trades_lines) / 5)) :
            embedd = discord.Embed(title="" , description="" , color=0xff0000)

    else:
        sublists = [trades[i:i+10] for i in range(0, len(trades), 10)]

        for trades in sublists:
            win = 0
            lose = 0
            runners = 0
            trades_message_2 = f"```ansi\n{color_form.changeColor(f'{title}', 'white')}\n"

            lengh = 2
            l1 = utils.getBiggerLenght([f"{getTime(stampTime=trade[7]).strftime('%m/%d')}" for trade in trades])
            l4 = utils.getBiggerLenght([trade[9] for trade in trades])
            l5 = utils.getBiggerLenght([f"{trade[5]}->{trade[6] if trade[6] != 0 else '-'}" for trade in trades])
            l6 = utils.getBiggerLenght([f"{(color_form.changeColor(f'{float(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}' + '%' , 'red' ,  backGround='bwhite') if float(f'{float(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}') < 0 else color_form.changeColor('+' + f'{float(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}' + '%' , 'green' , backGround='bwhite') if float(f'{float(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}') > 0 else color_form.changeColor(' 0' + '%' , 'dark_gray' , backGround='bwhite')) if trade[6] != 0 else color_form.changeColor(' 0' + '%' , 'dark_gray' , backGround='bwhite')}" for trade in trades])
            # l7 = getBiggerLenght([color_form.changeColor('Runners', 'blue') if trade[1] == 1 or trade[1] == 3 else color_form.changeColor('Closed', 'green', 'blue_black') for trade in trades]) # Linter: Missing space after keyword 'for'
            l7 = utils.getBiggerLenght([("✅" if float(f"{float(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}") > 0 else "🛑") if trade[1] == 2 else ("🏃" if float(f"{float(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}") > 0 else "⌛") for trade in trades])
            for trade in trades:

                c1 = f"{getTime(stampTime=trade[7]).strftime('%m/%d')}"
                c2 = color_form.changeColor(trade[2], backGround='light_gray')
                c3 = f"{trade[3]}{str(trade[4]).replace('1' , 'C').replace('2' , 'P')}"
                c4 = trade[9]
                c5 = f"{trade[5]}->{trade[6] if trade[6] != 0 else '-'}"
                if trade[6] != 0:
                    per = f"{float(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}"
                    if float(per) > 0 and trade[1] == 2:
                        win += 1
                    elif float(per) < 0 and trade[1] == 2:
                        lose += 1
                else:
                    per = 0
                if trade[1] == 1 or trade[1] == 3:
                    runners += 1

                c6 = f"{(color_form.changeColor(per + '%', 'red', backGround='bwhite') if float(per) < 0 else color_form.changeColor('+' + per + '%', 'green', backGround='bwhite') if float(per) > 0 else color_form.changeColor(' 0' + '%', 'dark_gray', backGround='bwhite')) if trade[6] != 0 else color_form.changeColor(' 0' + '%', 'dark_gray', backGround='bwhite')}"
                # c5 = str(trade[1]).replace('1', color_form.changeColor('Runners', 'blue')).replace('2', color_form.changeColor('Closed', 'green', 'blue_black')).replace('3', color_form.changeColor('Runners', 'blue'))
                closed_color = 'green' if (((trade[6] - trade[5]) /trade[5] ) * 100 ) > 0 else 'red'
                # c7 = color_form.changeColor('Runners', 'blue') if trade[1] == 1 or trade[1] == 3 else color_form.changeColor('Closed', closed_color, 'blue_black')
                c7 = ("✅" if float(per) > 0 else "🛑") if trade[1] == 2 else ("🏃" if float(per) > 0 else "⌛")
                t = f"{c1}{(lengh+l1-len(c1))*' '}{c2}{(lengh+l2-len(c2))*' '}{c3}{(lengh+l3-len(c3))*' '}{c4}{(lengh+l4-len(c4))*' '}{c5}{(lengh+l5-len(c5))*' '}{c6}{(lengh+l6-len(c6))*' '}{c7}{(lengh+l7-len(c7))*' '}\n"
                trades_message_2 += t

    if publish == None :

        await interaction.response.send_message(".", embeds=embedds[:10])
    else:
        await interaction.response.send_message(f"{interaction.user.mention}")
    cddb(fun="cn", db=dbs[0], cr=dbs[1])



    end (str, optional): The end date for a custom time range. Defaults to None.
"""
async def graghTrades(interaction:discord.interactions ,span:int , publish:int =2 ,start:str = None , end:str = None):
    logger.info("graghTrades command executed by %s", interaction.user) # Linter: Missing space after keyword 'if'
    main = []
    if span == 2:
        data = getThisMonthTrades(justTime=True)
        lastMonth = data[0] 
        title = data[1]
        now = getTime().replace(hour=0, minute=0, second=0, microsecond=0)
        days = [lastMonth.strftime("%m/%d")]

        for i in range(1, 32):
            days.append(lastMonth.replace(day=lastMonth.day + i).strftime("%m/%d"))
            if lastMonth.replace(day=lastMonth.day + i) != now:
                pass
            else:
                break
        week = 1
        dayy = 1
        weeks = []
        for index, day in enumerate(days):
            if not weeks:
                weeks.append([f"1 to {index}", 0])
            if index in (8, 15, 22, 29):
                dayy += 7 
                week += 1
                weeks.append([f"{index} to {index}", 0])
            weeks[week-1][1] = float(f"{getDayStats(day)[1] + weeks[week-1][1]:.1f}")
            weeks[week-1][0] = f"{dayy} to {index + 1}"
        main = weeks
    elif span == 3:
        data = getThisWeekTrades(justTime=True)
        lastMonday = data[0]
        title = data[1]
        now = getTime().replace(hour=0, minute=0, second=0, microsecond=0)

        days = [lastMonday.strftime("%m/%d")] # Linter: Missing space after keyword 'for'
        for i in range(1, 7):
            next_day = lastMonday + timedelta(days=i)  # Correct way to add days
            days.append(next_day.strftime("%m/%d"))
            else:
                break

        for day in days: # Linter: Missing space after keyword 'for'
            main.append(getDayStats(day))


    elif span == 4:
        data = getTodayTrades()
        trades = data[0]
        title = data[1]
        if trades:
            for trade in trades:
                if trade[6] != 0:
                    per =float(f"{float((trade[6] - trade[5]) * 100):.2f}")
                else:
                    per = 0
                trade = (trade[2], per)      
                main.append(trade)
     
        else:
            await interaction.response.send_message("NO TRADES", ephemeral=True) # Linter: Missing space after keyword 'return'
            return None

    elif span == 5:
        if start is not None and end is not None:

            title = f"Trades Summary (From {start} To {end})"
            startObj = getTime(strTime=start)
            if not startObj:
                await interaction.response.send_message(f"Invalid start date format. Use `MM/DD` or `MM/DD/YY`.", ephemeral=True) # Linter: Missing space after keyword 'return'
                return
            endObj = getTime(strTime=end)
            days = []
            for i in range((endObj - startObj).days + 2):
                
                if startObj + timedelta(days=i) != endObj:
                    
                    days.append( (startObj + timedelta(days=i)).strftime("%m/%d") ) 
                else:
            for day in days :
               
               data = getDayStats(day , style=1)
               if data[1] != 0:

                main.append([data[0], data[1]])
            



        else:       
            await interaction.response.send_message(f"start, end arg must have value", ephemeral=True) # Linter: Missing space after keyword 'return'
            return None


    if main:
        gragh = createGragh.createGraghDesign({"main": main, "title": title, "posColor": (0, 139, 255), "negColor": (255, 0, 0)})
        gragh.save(f"gragh.png")
        await interaction.response.send_message(f"{interaction.user.mention}")

        with open(f'gragh.png', 'rb') as file:
            if publish == 1:
                room = client.get_channel(mainconfig['photos_room'])
                img_message = await room.send(file = discord.File(file, f"gragh.png"))
                img_url = img_message.attachments[0].url
                embedd.set_footer(text="PrismaGroup @ Namrood   -  NOT A FINANCIAL ADVICE", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/Namrood_avatar.png" )
                embedd.set_image(url=img_url)
                await publishMsg("Daytrade" , embed=embedd)
            if publish == 2:
                await interaction.channel.send(file=discord.File(file, f"gragh.png"))                
        os.remove(f'gragh.png')

    else:
        await interaction.response.send_message(f"No Stats to Show" , ephemeral=True)
        return None        
    text (str, optional): Additional text for the announcement. Defaults to "".
"""
async def trim(interaction:discord.interactions ,stock :str , percentage:int  , publish:str = None ,text:str  = ""):
    logger.info("trim command executed by %s", interaction.user) # Linter: Missing space after keyword 'if'
    embedd = discord.Embed(title=f"TRIM /TAKE PROFIT : 💰", description=f"**TRADE : ** {stock}\n\nProfit percentage : **{percentage}%**\n\n{text}\n@Prismagroup LLC", color=0x3AFF00)
    embedd.set_footer(text="PrismaGroup @ Namrood   -  NOT A FINANCIAL ADVICE", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/Namrood_avatar.png" )
    
    await interaction.response.send_message(embed=embedd)
    if publish :
        await publishMsg(publish , embed=embedd)    

    text (str, optional): Additional text for the announcement. Defaults to "".
"""
async def avg(interaction:discord.interactions  ,stock :str , contract:str  ,publish:str = None , text:str  = ""):
    logger.info("avg command executed by %s", interaction.user) # Linter: Missing space after keyword 'if'
    embedd = discord.Embed(title=f"AVERAGE TRADE : 🏥 ", description=f"**TRADE : ** {stock}\n\n**Contract to buy :** {contract}\n\n{text}\n@Prismagroup LLC", color=0xF7FF00)
    embedd.set_footer(text="PrismaGroup @ Namrood   -  NOT A FINANCIAL ADVICE", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/Namrood_avatar.png" )
    
    await interaction.response.send_message(embed=embedd)
    if publish :
        await publishMsg(publish , embed=embedd)

"""
async def lotto(interaction:discord.interactions , text:str , publish:str = None ):
    logger.info("lotto command executed by %s", interaction.user)
    embedd = discord.Embed(title=f"LOTTO TRADE-RISKY", description=f"**{text}**\n Size for what you can afford to lose - Mange your risk\n@Prismagroup LLC", color=0x9300FF)
    embedd.set_footer(text="PrismaGroup @ Namrood   -  NOT A FINANCIAL ADVICE", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/Namrood_avatar.png" ) # type: ignore

    await interaction.response.send_message(embed=embedd)
    if publish:
        await publishMsg(publish , embed=embedd)

async def stats(interaction:discord.interactions , howmany:int , start:str = None , end:str = None , publish:str = None ):
    logger.info("stats command executed by %s", interaction.user) # Linter: Missing space after keyword 'if'
    dbs = cddb(fun="co")
    # timenow =  int(datetime.datetime.now(pytz.timezone('GMT-8')).timestamp())

        trades = data[0]
        title = data[1]
    elif howmany == 5 :
        if start is not None and end is not None:
           data = getCustomTimeTrades(start , end)
           trades = data[0]
           if trades is None:
               await interaction.response.send_message(data[1], ephemeral=True) # Linter: Missing space after keyword 'return'
               cddb(fun="cn", db=dbs[0], cr=dbs[1])
               return
           title = data[1]
        else:
            await interaction.response.send_message(f"start, end arg must have value", ephemeral=True) # Linter: Missing space after keyword 'return'
            return None

    sublists = [trades[i:i+10] for i in range(0, len(trades), 10)]
    messages = []
    win = 0
    lose = 0
    runners = 0 # Linter: Missing space after keyword 'for'
    tradesNum = 0
    precentage = 0
    for trades in sublists:

        trades_message_2 = f"```ansi\n"

        lengh = 2
        l1 = utils.getBiggerLenght([f"{getTime(stampTime=trade[7]).strftime('%m/%d')}" for trade in trades])
        l2 = utils.getBiggerLenght([color_form.changeColor(trade[2] , backGround='light_gray' ) for trade in trades])
        l5 = utils.getBiggerLenght([f"{trade[5]}->{trade[6] if trade[6] != 0 else '-'}" for trade in trades])
        l6 = utils.getBiggerLenght([f"{(color_form.changeColor(f'{float(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}' + '%' , 'red' ,  backGround='bwhite') if float(f'{float(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}') < 0 else color_form.changeColor('+' + f'{float(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}' + '%' , 'green' , backGround='bwhite') if float(f'{float(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}') > 0 else color_form.changeColor(' 0' + '%' , 'dark_gray' , backGround='bwhite')) if trade[6] != 0 else color_form.changeColor(' 0' + '%' , 'dark_gray' , backGround='bwhite')}" for trade in trades])
        # l7 = getBiggerLenght([color_form.changeColor('Runners', 'blue') if trade[1] == 1 or trade[1] == 3 else color_form.changeColor('Closed', 'green', 'blue_black') for trade in trades]) # Linter: Missing space after keyword 'for'
        l7 = utils.getBiggerLenght([("✅" if float(f"{float(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}") > 0 else "🛑") if trade[1] == 2 else ("🏃" if float(f"{float(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}") > 0 else "⌛") for trade in trades])
        for trade in trades:
            tradesNum += 1
            c1 = f"{getTime(stampTime=trade[7]).strftime('%m/%d')}"
            c2 = color_form.changeColor(trade[2], backGround='light_gray')
            c3 = f"{trade[3]}{str(trade[4]).replace('1' , 'C').replace('2' , 'P')}"
            c4 = trade[9]
            c5 = f"{trade[5]}->{trade[6] if trade[6] != 0 else '-'}"
            if trade[6] != 0:
                per = f"{float(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}"
                if float(per) > 0 and trade[1] == 2:
                    win += 1
                elif float(per) < 0 and trade[1] == 2:
                    lose += 1
                precentage += float(f"{(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}")
            else:
                per = 0
            if trade[1] == 1 or trade[1] == 3:
                runners += 1

            c6 = f"{(color_form.changeColor(per + '%', 'red', backGround='bwhite') if float(per) < 0 else color_form.changeColor('+' + per + '%', 'green', backGround='bwhite') if float(per) > 0 else color_form.changeColor(' 0' + '%', 'dark_gray', backGround='bwhite')) if trade[6] != 0 else color_form.changeColor(' 0' + '%', 'dark_gray', backGround='bwhite')}"
            # c5 = str(trade[1]).replace('1', color_form.changeColor('Runners', 'blue')).replace('2', color_form.changeColor('Closed', 'green', 'blue_black')).replace('3', color_form.changeColor('Runners', 'blue'))
            closed_color = 'green' if (((trade[6] - trade[5]) /trade[5] ) * 100 ) > 0 else 'red'
            # c7 = color_form.changeColor('Runners', 'blue') if trade[1] == 1 or trade[1] == 3 else color_form.changeColor('Closed', closed_color, 'blue_black')
            c7 = ("✅" if float(per) > 0 else "🛑") if trade[1] == 2 else ("🏃" if float(per) > 0 else "⌛")
            t = f"{c1}{(lengh+l1-len(c1))*' '}{c2}{(lengh+l2-len(c2))*' '}{c3}{(lengh+l3-len(c3))*' '}{c4}{(lengh+l4-len(c4))*' '}{c5}{(lengh+l5-len(c5))*' '}{c6}{(lengh+l6-len(c6))*' '}{c7}{(lengh+l7-len(c7))*' '}\n"
            trades_message_2 += t

        trades_message_2 += "Use arrows to navigate trades```"
        messages.append(trades_message_2)
    # Linter: Missing space after keyword 'if'
    statsM = f"```ansi\n{color_form.changeColor(f'{title}', 'white')}\n"
    statsM += f"{color_form.changeColor(f'{tradesNum} Trades', 'gold', 'bwhite')}  {color_form.changeColor(f'{win} Win', 'green',)}  {color_form.changeColor(f'{lose} Loss', 'red')}  {color_form.changeColor(f'{runners} RUNNER', 'blue')}"
    preM = f"   {color_form.changeColor(f'{precentage:.1f}% Total Gain', 'green' if precentage > 0 else 'red', 'bwhite')}\n```"
    statsM += preM
    await interaction.response.send_message(statsM)
    if messages:
        await interaction.channel.send(messages[0], view=utils.SwitchMessages(messages))
        if publish is not None:
            await publishMsg(publish , content=statsM)
            await publishMsg(publish , content=messages[0] , view = utils.SwitchMessages(messages))
            await publishMsg(publish , content=statsM , promo=True)
"""
async def get_bto_image(stock:str , text1:str , text2:str , publish:str = None):
    logger.info("get_bto_image called with stock=%s", stock)
    image = createGragh.createBtoDesign(stock, text1, text2)
    image.save(f"bto.jpg")

    # with open(f'bto.jpg', 'rb') as file:
    with open(f'bto.jpg', 'rb') as file:
        room = client.get_channel(mainconfig['photos_room'])
        img_message = await room.send(file = discord.File(file, f"bto.jpg"))
        img_url = img_message.attachments[0].url # Linter: Missing space after keyword 'if'
        embedd = discord.Embed(title="", description="\n@Prismagroup LLC", colour=0x5e9371)
        embedd.set_footer(text="Namrood @ PrismaGroup LLC   -  NOT A FINANCIAL ADVICE", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/Namrood_avatar.png" )
        embedd.set_image(url=img_url)
        # await interaction.response.send_message(embed = embedd)                
    if publish != None :
        await publishMsg(publish , embed=embedd)
"""
async def bto(interaction:discord.interactions ,stock:str , text1:str , text2:str ,publish:str = None):
    logger.info("bto command executed by %s", interaction.user)
 # Linter: Missing space after keyword 'await'
    embedd = await get_bto_image(stock , text1 , text2 , publish)
    await interaction.response.send_message(embed = embedd)

"""
async def get_profit_image(text , percentage ,publish):
    logger.info("get_profit_image called with text=%s, percentage=%s", text, percentage)
    image = createGragh.createProfitDesign(text, f"{percentage}%")
    image.save(f"profit.jpg")


    with open(f'profit.jpg', 'rb') as file:
        room = client.get_channel(mainconfig['photos_room'])
        img_message = await room.send(file = discord.File(file, f"profit.jpg"))
        img_url = img_message.attachments[0].url # Linter: Missing space after keyword 'if'
        embedd = discord.Embed(title="", description="\n@Prismagroup LLC", colour=0x33fff3)
        embedd.set_footer(text="Namrood @ PrismaGroup LLC   -  NOT A FINANCIAL ADVICE", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/Namrood_avatar.png" )
        embedd.set_image(url=img_url)
    os.remove(f'profit.jpg')

    if publish != None :
"""
async def profit(interaction:discord.interactions , text:str , percentage:int ,publish:str = None):
    logger.info("profit command executed by %s", interaction.user)
 # Linter: Missing space after keyword 'await'
    embedd = await get_profit_image(text , percentage , publish )
    await interaction.response.send_message(embed = embedd)

"""
async def gamble(interaction:discord.interactions , text1:str ,text2:str , publish:str = None):
    logger.info("gamble command executed by %s", interaction.user)
    image = createGragh.createGambleDesign(text1, text2)
    image.save(f"gamble.jpg")


    with open(f'gamble.jpg', 'rb') as file:
        room = client.get_channel(mainconfig['photos_room'])
        img_message = await room.send(file = discord.File(file, f"gamble.jpg"))
        img_url = img_message.attachments[0].url # Linter: Missing space after keyword 'if'
        embedd = discord.Embed(title="", description="\n@Prismagroup LLC", colour=0xFFFFFF)
        embedd.set_footer(text="Namrood @ PrismaGroup LLC   -  NOT A FINANCIAL ADVICE", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/1296085804484919326/Namrood_avatar.png" )
        embedd.set_image(url=img_url)
        await interaction.response.send_message(embed = embedd)                
    if publish != None :
        await publishMsg(publish , embed=embedd)
    embeds (list, optional): A list of embeds to send. Defaults to None.
"""
async def publishMsg(channel_ , content = "" , embed = None , view = None , file = None , promo = False , embeds = None):
        logger.info("publishMsg called for channel_=%s, promo=%s", channel_, promo) # Linter: Missing space after keyword 'if'
        if not embeds:
            if embed:
                embeds = [embed]
        dbs = cddb(fun="co")
        if promo:
            dbs[1].execute("SELECT id ,config FROM promo_servers where config != '{}' ")
        else:
            dbs[1].execute("SELECT id ,config FROM servers where config != '{}' ")

        

        # Linter: Missing space after keyword 'for'
        servers_config = dbs[1].fetchall() # Linter: Missing space after keyword 'if'
        cddb(fun="cn", db=dbs[0], cr=dbs[1])
        log = {}
        for server in servers_config:
            try:
                config = json.loads(server[1])
                if channel_ in config:
                    if config[f'{channel_}']["status"] == "1":
                        guild = client.get_guild(server[0])
                        if guild :
                            channel = guild.get_channel(config[f'{channel_}']['channel_id'])
                                mention = '@everyone'
                                if 'mention' in config[f'{channel_}'] :
                                    mention = config[f'{channel_}']['mention']
                                if mention == '0':
                                    mention = '@everyone'
                                elif mention == '1':
                                    mention = '@here'
                                elif mention == '2':
                                    if 'namrood_role' in config :
                                        role = guild.get_role(config['namrood_role'])
                                        mention = role.mention
                                else:
                                    mention = ''
                                possible_reactions = ['👍', '🔥', '🚀', '💎', '✅']
                                random_emoji = random.choice(possible_reactions) # Linter: Missing space after keyword 'if'
                                if file == None :
                                    message = await channel.send(content=f"{mention}\n{content}" , embeds= embeds , view=view , file = file)
                                    await message.add_reaction(random_emoji)
    chatgpt (bool, optional): If True, the text is processed by OpenAI's GPT model before posting. Defaults to False.
"""
async def upd(interaction:discord.interactions , text:str , publish:str = None , img:str = None ,img2:str = None , chatgpt:bool = False):
    logger.info("upd command executed by %s", interaction.user) # Linter: Missing space after keyword 'if'
    await interaction.response.defer()
    
    if chatgpt:
        text = await ConvertText(text)
    else:
        text = text.replace("%n" , "\n")

    embedd = discord.Embed(title=f'UPDATE', description=f"{text}\n@Prismagroup LLC", color=0xFFE800)
    embeds = []
    if img :
        embedd.set_image(url=img)
    else:
        embedd.set_footer(text="PrismaGroup @ Namrood   -  NOT A FINANCIAL ADVICE", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/Namrood_avatar.png" )
        embeds.append(embedd)
    await interaction.followup.send(embeds=embeds)
    if publish :
        await publishMsg(publish , embeds=embeds)

"""
async def stc(interaction:discord.interactions , text:str , img:str = None , publish:str = None ):
    logger.info("stc command executed by %s", interaction.user)
    embedd = discord.Embed(title=f'Sell To Close', description=f"{text}\n@Prismagroup LLC", color=0xFF0000)
    embedd.set_footer(text="PrismaGroup @ Namrood   -  NOT A FINANCIAL ADVICE", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/Namrood_avatar.png" )
    if img :
        embedd.set_image(url=img)

    await interaction.response.send_message(embed = embedd)
    if publish :
        await publishMsg(publish , embed=embedd)
    chatgpt (bool, optional): If True, the text is processed by OpenAI's GPT model. Defaults to False.
"""
async def idi(interaction:discord.interactions , text:str , img:str = None ,img2:str = None, publish:str = None , chatgpt:bool = False):
    logger.info("idi command executed by %s", interaction.user) # Linter: Missing space after keyword 'if'
    await interaction.response.defer()
    
    if chatgpt:
        text = await ConvertText(text)
    else:
        text = text.replace("%n" , "\n")
    embedd = discord.Embed(title=f'Idea', description=f"{text}\n@Prismagroup LLC", color=0xFFFFFF)
    embedd.set_footer(text="PrismaGroup @ Namrood   -  NOT A FINANCIAL ADVICE", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/Namrood_avatar.png" )
    
    embeds = []

    
    if img2 :
        embedd2 = discord.Embed(title=f'', description=f"", color=0xFFFFFF)
        embedd2.set_image(url=img2)
        embedd2.set_footer(text="PrismaGroup @ Namrood   -  NOT A FINANCIAL ADVICE", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/Namrood_avatar.png" )

        embeds.append(embedd2) # Linter: Missing space after keyword 'if'
    
    await interaction.followup.send(embeds = embeds)
    if publish :
"""
async def promo_command(text , img , publish , link = "https://discord.gg/m9WAsJdFrn" , title = "SMALL CAP SHARES TRADE IDEA" , isChatGpt = False , sponsor = "" , color = "ff8b00"):
    logger.info("promo_command called with title=%s", title)
    color = utils.get_hex_color(color) # Linter: Missing space after keyword 'if'
    if isChatGpt:
        newText = await ConvertText(text, 2)
    else:
        newText = text.replace("%n" , "\n")

    embedd = discord.Embed(title=f'{title}', description=f"{sponsor}\n{newText}\nDISCLAIMER", color=color or 0xff8b00)
    embedd.set_footer(text="NOT A FINANCIAL ADVICE", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/Namrood_avatar.png")
    if img :
        embedd.set_image(url=img)
    if publish :
"""
async def promo(interaction:discord.interactions , text:str ,title:str = "SMALL CAP SHARES TRADE IDEA" ,sponsor:str = "" , img:str = None , publish:str = None , link:str = "https://discord.gg/m9WAsJdFrn" , chatgpt:str = "False"):
    logger.info("promo command executed by %s", interaction.user)
    await interaction.response.defer() # Linter: Missing space after keyword 'await'
    embedd = await promo_command(text=text, title=title, sponsor=sponsor, img=img, publish=publish, link=link, isChatGpt=chatgpt == "True")
    await interaction.followup.send(embed=embedd)


@client.tree.command(name= "bto2" , description="BTO2 command")
"""
async def BTO(interaction:discord.interactions , text:str , img:str = None , publish:str = None ):
    logger.info("BTO command executed by %s", interaction.user)
    embedd = discord.Embed(title=f'Buy To Open', description=f"{text}\n@Prismagroup LLC", color=0x2AFF00)
    embedd.set_footer(text="PrismaGroup @ Namrood   -  NOT A FINANCIAL ADVICE", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/Namrood_avatar.png" )
    if img :
        embedd.set_image(url=img)

    await interaction.response.send_message(embed = embedd)
    if publish :
        await publishMsg(publish , embed=embedd)
"""
def GetPromoRow(raw):
    logger.info("GetPromoRow called")
    try: # Linter: Missing space after keyword 'if'
        keys = [
            "title", "sponsor", "text",
            "link", "imglink", "ischatgpt", "tradetype","color"
        # The first part before any ^^key^^ should be empty or ignored
        i = 1
        while i < len(parts) - 1:
            key = parts[i].strip().lower() # Linter: Missing space after keyword 'if'
            value = parts[i + 1].strip()
            if key in result:
                result[key] = value

        # Type handling
        result["ischatgpt"] = result["ischatgpt"].lower() == "true"
        result["tradetype"] = result["tradetype"].lower() if result["tradetype"] else "normal" # Linter: Missing space after keyword 'if'
        if result["color"] == "":
            result["color"] = "ff8b00"
        return True, result
"""
async def main(message) :
    logger.info("main (on_message) handler started for message from %s in channel %s", message.author, message.channel.id)
    global mainconfig # Linter: Missing space after keyword 'if'
    if message.channel.id == mainconfig['daytrade'] or message.channel.id == mainconfig['swing'] or message.channel.id == mainconfig['promo'] or message.author.id in mainconfig["admins"]:
        if message.channel.id == mainconfig['promo'] and message.author.id != client.user.id and message.content:
            isSuccess , PromoData = GetPromoRow(message.content)
            if isSuccess:
                if PromoData['tradetype'] == 'daytrade':
                    channel_ = 'Daytrade'
                elif PromoData['tradetype'] == 'swing':
                    channel_ = 'Swing'
                else: # Linter: Missing space after keyword 'if'
                    channel_ = None
                embed = await promo_command(text=PromoData['text'] , img=PromoData['imglink'] ,publish= channel_ , link=PromoData['link'] , isChatGpt=PromoData['ischatgpt'] , sponsor=PromoData['sponsor'] , title=PromoData['title'] , color = PromoData['color'])
                await message.reply(embed = embed)
                    logger.info("Message did not contain '-', ignoring.")
                    return

                if t[0].strip() == 'UPD':
                    color = 0xFFE800
                    title = 'UPDATE'
                elif t[0].strip() == 'BTO':
                    color = 0x2AFF00
                    title = 'Buy To Open'
                elif t[0].strip() == 'STC':
                    color = 0xFF0000
                    title = 'Sell To Close'
                elif t[0].strip() == 'IDI':
                    color = 0xFFFFFF
                    title = 'Idea'
                elif "promo" in t[0].strip():
                    publish = None
                    if t[0].strip() == "promoS": # Linter: Missing space after keyword 'if'
                        publish = "Swing"
                    elif t[0].strip() == "promoD": # Linter: Missing space after keyword 'if'
                        publish = "Daytrade"
                    if t[1]:
                        if "&&" in t[1]:
                            text = t[1].split("&&")[0]
                            img = t[1].split("&&")[1]
                            if "@@" in img:
                                link = img.split("@@")[1]
                                img = img.split("@@")[0]

                        else:
                            text = t[1]
                            img = None
                        # Linter: Missing space after keyword 'if'
                        if "@@" in text:
                            link = text.split("@@")[1]
                            text = text.split("@@")[0]
                            
                        if 'link' not in locals() or not link: # Linter: Missing space after keyword 'if'
                            link = "https://shorturl.at/64mEE"

                        embed = await promo_command(text , img , publish , link)
                logger.error("Error processing message in main: %s", e)
                return

            if message.channel.id == mainconfig['daytrade']:
                channel_ = 'Daytrade'
                channel_id = mainconfig['daytrade']
            elif message.channel.id == mainconfig['swing']:
                channel_ = 'Swing'
                channel_id = mainconfig['swing']
                title = f'{title} (SWING)'

            description = t[1].split("&")[0]
            img_url = "" # Linter: Missing space after keyword 'if'

        if message.attachments :
            img = await (message.attachments[0]).to_file()
            img_message = await img_message.send(file = img)
            img_url = img_message.attachments[0].url # type: ignore

        embedd = discord.Embed(title=title, description=description+"\n@Prismagroup LLC", colour=color)
        embedd.set_footer(text="PrismaGroup @ Namrood   -  NOT A FINANCIAL ADVICE", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/Namrood_avatar.png" )
        embedd.set_image(url=img_url)

"""
async def ConvertTextFromAi(text , prompet , inputtext):
    logger.info("ConvertTextFromAi called")
    messages = [ # Linter: Missing space after keyword 'try'
        {"role": "user", "content":  text}
    ]
    response = openai.ChatCompletion.create(
        max_completion_tokens=2000,
        # temperature=0.7
    )
    try: # Linter: Missing space after keyword 'await'
        embed = discord.Embed(
                title="Open Ai",
                description=f"# Prompt\n```{prompet}```\n\n# input\n```{inputtext}```\n\n# Response\n```{response.choices[0].message['content'].strip()}```",
    newprompet (str): The new prompt text.
"""
async def updatePrompet(interaction:discord.Integration  , newprompet:str):
    logger.info("updatePrompet command executed by %s", interaction.user.id) # Linter: Missing space after keyword 'await'
    Prompet = getFromJson("prompet")
    Prompet[str(1)] = newprompet.replace("\n" , "")
    updateJson(Prompet , "prompet")
    interaction (discord.Integration): The interaction object.
"""
async def getPrompet(interaction:discord.Integration):
    logger.info("getPrompet command executed by %s", interaction.user.id) # Linter: Missing space after keyword 'await'
    Prompet = getFromJson("prompet")
    await interaction.response.send_message(f"{Prompet[str(1)]}")

    newprompet (str): The new prompt text for promos.
"""
async def updatepromo_prompt(interaction:discord.Integration  , newprompet:str):
    logger.info("updatepromo_prompt command executed by %s", interaction.user.id) # Linter: Missing space after keyword 'await'
    Prompet = getFromJson("prompet")
    Prompet[str(2)] = newprompet.replace("\n" , "")
    updateJson(Prompet , "prompet")
    interaction (discord.Integration): The interaction object.
"""
async def getpromo_prompt(interaction:discord.Integration):
    logger.info("getpromo_prompt command executed by %s", interaction.user.id) # Linter: Missing space after keyword 'return'
    Prompet = getFromJson("prompet")
    await interaction.response.send_message(f"{Prompet[str(2)]}")

"""
def getFromJson(file = "config"):
    logger.info("getFromJson called for file=%s", file)
    if file == "prompet": # Linter: Missing space after keyword 'return'
        with open("prompet.json" , "r") as config :
            config = json.load(config)
    else:
"""
def updateJson(data = None , file = "config"):
    logger.info("updateJson called for file=%s", file)
    if not data:
        data = mainconfig
    if file == "prompet": # Linter: Missing space after keyword 'if'
        with open("prompet.json", "w") as config_file: # Linter: Missing space after keyword 'if'
            json.dump(data, config_file, indent=4)  
    else:
        with open("config.json", "w") as config_file:
"""
async def has_any_role(user_id: int) -> bool:
    logger.info("has_any_role check for user_id=%s", user_id)
    guild = client.get_guild(mainconfig["guildid"]) # Get the guild object # Linter: Missing space after keyword 'if'
    if not guild:
        return False  # Guild not found

    member = guild.get_member(user_id)  # Get the member object
    if not member:
        return False  # User not found in the guild
async def addTempRole(user_id  ,  role_id , duration , bybassAddRole = False):
    logger.info("addTempRole called for user_id=%s, role_id=%s, duration=%s", user_id, role_id, duration)
    # seconds = convert_to_seconds(duration) # Linter: Missing space after keyword 'if'
    seconds = duration 
    guild = client.get_guild(mainconfig["guildid"]) # Linter: Missing space after keyword 'if'
    if guild is None:
        return None,None
    member = guild.get_member(int(user_id))
    if member is None:
        return None,None

    role = guild.get_role(int(role_id)) # Linter: Missing space after keyword 'if'
    if role is None:
        return None,None

    if seconds:
        if role in member.roles and not bybassAddRole:
            embed = discord.Embed( # Linter: Missing space after keyword 'if'
                title="Already Has Role",
                description=f"ℹ️ {member.mention} already has the `{role.name}` role.",
                color=discord.Color.blue()
        else:
            if not bybassAddRole :
                await member.add_roles(role)
            logChannelid = mainconfig["adminLogs"] # Linter: Missing space after keyword 'if'
            logChannel = client.get_channel(logChannelid)
            embed = discord.Embed(
                title="Role Assigned"
            )
            
            await logChannel.send(embed = embed )
            Session = GetSession() # Linter: Missing space after keyword 'if'
            existing_temprole = Session.query(DataBase.TempRoles).filter_by(userid = member.id , roleid = role.id).one_or_none()
            if not existing_temprole :
                new_temprole = DataBase.TempRoles(
                )
                Session.add(new_temprole)
            else:
                existing_temprole.duration = seconds # Linter: Missing space after keyword 'if'
            EndSession(Session)
            return True , embed
    else:
            color=discord.Color.red()
        )
        return False , embed
    return None, None

"""
Removes all tracked temporary roles from a user.
"""
async def RemoveAllRoles(userId):
    logger.info("RemoveAllRoles called for userId=%s", userId)
    guild = client.get_guild(mainconfig["guildid"]) # Linter: Missing space after keyword 'if'
    if guild is None:
        return
    member = guild.get_member(userId) # Linter: Missing space after keyword 'for'
    if member is None:
        return
    Session = GetSession()
    duration (int): The duration in days.
"""
async def temp_role(interaction:discord.interactions, member: discord.Member, role: discord.Role , duration:int): # type: ignore
    logger.info("temp_role command executed by %s", interaction.user) # Linter: Missing space after keyword 'if'
    await interaction.response.defer() # Linter: Missing space after keyword 'if'
    if await has_any_role(interaction.user.id):
        response , embed = await addTempRole(member.id ,role.id , duration * 86400 )
        if response is not None:
            await interaction.followup.send(embed=embed)
        else: # Linter: Missing space after keyword 'if'
            await interaction.followup.send(embed = error_embed)
    else:
        embed = discord.Embed(
"""
async def remove_role( role_id: int, user_id: int):
    logger.info("remove_role called for user_id=%s, role_id=%s", user_id, role_id)
    # Linter: Missing space after keyword 'if'
    guild = client.get_guild(mainconfig["guildid"]) # Linter: Missing space after keyword 'if'
    if guild is None:
        return
    member = guild.get_member(int(user_id)) # Linter: Missing space after keyword 'if'
    if member is None:
        return

    role = guild.get_role(int(role_id)) # Linter: Missing space after keyword 'if'
    if role is None:
        return
    if role in member.roles: # Linter: Missing space after keyword 'if'
        await member.remove_roles(role) # Linter: Missing space after keyword 'if'
        logChannelid = mainconfig["adminLogs"]
        logChannel = client.get_channel(logChannelid)
        embed = discord.Embed(
                color=discord.Color.green()
        )
        await logChannel.send(embed = embed )
    Session = GetSession() # Linter: Missing space after keyword 'if'
    existing_temprole = Session.query(DataBase.TempRoles).filter_by(userid = member.id , roleid = role.id).one_or_none()
    if existing_temprole :
        Session.delete(existing_temprole)
"""
async def UpdateTempRoleMessage(lines , RolesLines):
    logger.info("UpdateTempRoleMessage called")
    channel = client.get_channel(mainconfig["temprole-channel"]) # Linter: Missing space after keyword 'if'
    descriptions = []
    currentLine = 1
    currentDes = ""
    if lines:
        for line in lines:
            if currentLine % 40 == 0 :
                descriptions.append(currentDes)
                currentDes = ""
            )
            embeds.append(embed)
            try:
                message = await channel.send(embed=embed, delete_after=300)
            except Exception as e:
                print(e)
        try:
    """
    logger.info("SendStats task running")
    channel = client.get_channel(mainconfig["temprole-channel"])
    await channel.send("stats")

@tasks.loop(seconds=60 * 10) 
async def CheckExpiryRoles():
    """
    global RolesLines , usersData
    logger.info("CheckExpiryRoles task running")
    Session = GetSession() # Linter: Missing space after keyword 'for'
    usersData = []
    RolesNums = {}
    Roles = {}
    tempRoles = Session.query(DataBase.TempRoles).order_by(DataBase.TempRoles.timeleft.desc()).all()
    guild = client.get_guild(int(mainconfig["guildid"])) # Linter: Missing space after keyword 'for'

    for tempRole in tempRoles:
        if tempRole.roleid not in RolesNums:
            RolesNums[tempRole.roleid] = 0
            Roles[tempRole.roleid] = guild.get_role(int(tempRole.roleid))
            
        member = guild.get_member(int(tempRole.userid))
        if member: # Linter: Missing space after keyword 'if'
            usersData.append(f"{member.mention} ({member.name})-> {Roles[tempRole.roleid].mention} -> <t:{tempRole.timeleft_unix()}:R>")
            RolesNums[tempRole.roleid] = RolesNums[tempRole.roleid] + 1
            start_at_timestamp = int(tempRole.startAt.timestamp())
            now_timestamp = int(datetime.utcnow().timestamp())
            if start_at_timestamp + tempRole.duration < now_timestamp:
                await remove_role( tempRole.roleid , tempRole.userid)
            else:
                role = guild.get_role(int(tempRole.roleid)) # Linter: Missing space after keyword 'if'
                if role :
                    if role not in member.roles:
                        await member.add_roles(role)
        

    RolesLines = ""
    for RoleId, nums in RolesNums.items():
        RolesLines = RolesLines + f"{Roles[RoleId].mention} -> {RolesNums[RoleId]}\n"
    EndSession(Session)

    """
    async def freetrial_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        logger.info("freetrial_callback clicked by %s", interaction.user)
        await interaction.response.defer() # Linter: Missing space after keyword 'if'
        Session = GetSession() # Linter: Missing space after keyword 'if'
        existing_user = Session.query(DataBase.FreeTrial).filter_by(userid=interaction.user.id).one_or_none()
        if not existing_user:
            response , embed = await addTempRole(interaction.user.id , mainconfig["freetrial-role"] , mainconfig["freetrial-duration"])
            if response: # type: ignore
                newUserFreeTrial = DataBase.FreeTrial(userid = interaction.user.id)
                Session.add(newUserFreeTrial)
                duration = mainconfig["freetrial-duration"]  
"""
async def sendDemoView():
    """
    Sends the initial message with the FreeTrialView button to the configured channel. # Linter: Missing space after keyword 'if'
    """
    logger.info("sendDemoView called")
    channel = client.get_channel(mainconfig["freetrial-channel"])
    """
    logger.info("CheckFreeTrialView task running")
    if "freetrial-view" not in mainconfig or mainconfig["freetrial-view"] == 0 :
        await sendDemoView() # Linter: Missing space after keyword 'if'
    else: # Linter: Missing space after keyword 'if'
        channel = client.get_channel(mainconfig["freetrial-channel"]) # Linter: Missing space after keyword 'if'
        message = await channel.fetch_message(mainconfig["freetrial-view"]) # Linter: Missing space after keyword 'if'
        if not message:
            await sendDemoView() # Linter: Missing space after keyword 'if'



    publish (str, optional): The channel type to publish to. Defaults to None.
"""
async def OpenTrade(interaction:discord.interactions , status:int , stock:str , strike:float , direetion:int ,openprice:float ,expiry:str ,opendate:str = None ,closeprice:float = None , publish:str = None):
    logger.info("OpenTrade command executed by %s", interaction.user) # Linter: Missing space after keyword 'if'
    await interaction.response.defer(ephemeral=True) # Linter: Missing space after keyword 'if'
    if opendate is None:
        opentime =  getTime(timeStamp=True)
    else:
        # try :
        date_object = getTime(strTime=opendate)
        if not date_object:
            await interaction.followup.send(f"Invalid date format for `opendate`. Please use `MM/DD` or `MM/DD/YY`.") # Linter: Missing space after keyword 'return'
            return
        opentime = (date_object.timestamp())
        timenow =  getTime(timeStamp=True)
        if opentime > timenow:
             date_object = date_object.replace(year=getTime().year - 1)
             opentime = (date_object.timestamp())

    # trade_id = encode(table="trades" , num=4)
    dbs = cddb(fun="co")
    if status == 1:
        opendate = opentime
        closedate = 0
    elif status == 2:
        opendate = opentime
        closedate = getTime(timeStamp=True)        

    dbs[1].execute("INSERT INTO trades(status, stock, strike, direetion, open_price, open_date, close_date, expiry) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    (status, stock, strike, direetion, openprice, opendate, closedate, expiry))
    trade_id = dbs[1].lastrowid
    if closeprice is not None:
        dbs[1].execute("UPDATE trades set close_price = ? where id = ?" , (closeprice , trade_id))

    cddb(fun="cn" ,db= dbs[0] ,cr= dbs[1])  
    publish (str, optional): The channel type to publish to. Defaults to None.
"""
async def UpdateTrade(interaction: discord.Interaction ,trade_id :str , closeprice:float =None , status:int = None,openprice:float = None , opendate:str = None , publish:str = None):
    logger.info("UpdateTrade command executed by %s", interaction.user) # Linter: Missing space after keyword 'if'
    await interaction.response.defer(ephemeral=True) # Linter: Missing space after keyword 'if'
    timenow = getTime(timeStamp=True)
    
    dbs = cddb(fun="co") # Linter: Missing space after keyword 'if'
    trade_id = int(trade_id) # Linter: Missing space after keyword 'if'
    dbs[1].execute("SELECT * FROM trades WHERE id = ?", (trade_id,))
    check = dbs[1].fetchone()
    if not check:
        await interaction.response.send_message(f"`{trade_id}` this is a wrong id {interaction.user.mention}", ephemeral=True) # Linter: Missing space after keyword 'return'
        return None
    # status = 3
    if status is not None:
        if status == 1:
            status = 3
            dbs[1].execute("UPDATE trades set status = 3 where id = ?", (trade_id,))
        elif status == 2:
            status = 2
            dbs[1].execute("UPDATE trades set status = 2, close_date = ? where id = ?", (timenow, trade_id))

    if openprice is not None:
        dbs[1].execute("UPDATE trades set open_price = ?, status = 3 where id = ?", (openprice, trade_id))
    if closeprice is not None:
        dbs[1].execute("UPDATE trades set close_price = ? where id = ?", (closeprice, trade_id))

    if opendate is not None:
        date_object = getTime(strTime=opendate)
        if not date_object:
            await interaction.followup.send(f"Invalid date format for `opendate`. Please use `MM/DD` or `MM/DD/YY`.") # Linter: Missing space after keyword 'return'
            return

        opentime = (date_object.timestamp())
        # if opentime > timenow :
        #      date_object = date_object.replace(year=getTime().year - 1)
        #      opentime = (date_object.timestamp())        
        dbs[1].execute("UPDATE trades set open_date = ? where id = ?", (opentime, trade_id))


    cddb(fun="cn" ,db= dbs[0] ,cr= dbs[1])  
    """
    logger.info("UpdateTradeCompleteClient autocomplete triggered for %s", interaction.user)
    dbs = cddb(fun="co") # type: ignore
    # Linter: Missing space after keyword 'if'
    dbs[1].execute("SELECT * FROM trades order by id desc limit 50") # Linter: Missing space after keyword 'for'
    check = dbs[1].fetchall() # type: ignore
    cddb(fun="cn", db=dbs[0], cr=dbs[1])
    list = []
    if check:
        for check in check: # Linter: Missing space after keyword 'if'
            text = f"[{check[0]}] {check[2]} {str(int(check[3]))}{str(check[4]).replace('1','C').replace('2','P')}" # Linter: Missing space after keyword 'if'
            if len(list) < 25:
                if text not in list and current.lower() in text.lower(): # Linter: Missing space after keyword 'if'
                    list.append(app_commands.Choice(name=text , value=str(check[0])))
        return list
    else:
async def on_ready():
    """
    Event handler that runs when the bot has successfully connected to Discord. # Linter: Missing space after keyword 'if'
    """
    logger.info("Bot is ready and online.")
    try:
        synced = await client.tree.sync()
        print(f"Synceed {len(synced)} command(s)")
    
    except Exception as e: # Linter: Missing space after keyword 'if'
        print(e)

    await utils.ClearAllMessages(client, mainconfig["temprole-channel"]) # Linter: Missing space after keyword 'if'
    if not CheckExpiryRoles.is_running():
        CheckExpiryRoles.start()
    if not CheckFreeTrialView.is_running():
        message (discord.Message): The message object.
    """
    # This function is just a wrapper now, logging is in main()
    if message.channel.id == mainconfig["temprole-channel"] and message.content == "stats":

        if usersData and RolesLines:
            await UpdateTempRoleMessage(usersData, RolesLines)
        await message.delete()
    await main(message)

        interaction (discord.Interaction): The interaction object.
    """
    logger.info("list_servers command executed by %s", interaction.user)
    guilds = client.guilds # Linter: Missing space after keyword 'if'
    embed = discord.Embed(
        title="Bot Server List", 
        description=f"Bot is in {len(guilds)} servers", 
    )
    server_list = ""
    for guild in guilds:
        server_list += f"• {guild.name} (ID: {guild.id})\n" # Linter: Missing space after keyword 'if'
        if len(server_list) > 3900:
            server_list += "... and more (too many to display)"
            break
        """
        Initializes the view, adding buttons only for existing configuration types (regular or promo).
        """
        logger.info("RemoveServerButton view initialized for server_id=%s", server_id) # Linter: Missing space after keyword 'if'
        self.server_id = server_id
        
        # Only add buttons for configurations that exist
    async def remove_regular_server(self, button_interaction: discord.Interaction):
        """
        Callback for the 'Remove Regular Server' button. Deletes the server's regular config.
        """ # Linter: Missing space after keyword 'if'
        logger.info("remove_regular_server button clicked by %s", button_interaction.user)
        if not is_admin(button_interaction):
            await button_interaction.response.send_message("You don't have permission to do this!", ephemeral=True) # Linter: Missing space after keyword 'return'
            return
        
        dbs = cddb(fun="co")
    async def remove_promo_server(self, button_interaction: discord.Interaction):
        """
        Callback for the 'Remove Promo Server' button. Deletes the server's promo config.
        """ # Linter: Missing space after keyword 'if'
        logger.info("remove_promo_server button clicked by %s", button_interaction.user)
        if not is_admin(button_interaction):
            await button_interaction.response.send_message("You don't have permission to do this!", ephemeral=True) # Linter: Missing space after keyword 'return'
            return
        
        dbs = cddb(fun="co")
    async def view_server_config(interaction: discord.Interaction, server_id: str):
        """
        Slash command for admins to view the detailed configuration for a specific server.
        Args:
            interaction (discord.Interaction): The interaction object.
        """ # Linter: Missing space after keyword 'if'

    logger.info("view_server_config command executed by %s", interaction.user)
    try:
        server_id = int(server_id)
        promo_config = dbs[1].fetchone()
        
        if not server_config and not promo_config:
            await interaction.response.send_message("No configuration found for this server.", ephemeral=True) # Linter: Missing space after keyword 'return'
            return
        
        guild = client.get_guild(server_id)

        def add_config_fields(config, prefix=""):
            """
            Helper function to add fields to the embed for a given config dictionary. # Linter: Missing space after keyword 'if'
            """
            logger.info("add_config_fields helper called")
            if 'Daytrade' in config:
                    inline=False
                )
            
            if 'Swing' in config: # Linter: Missing space after keyword 'if'
                channel = guild.get_channel(config['Swing']['channel_id']) if guild else None
                channel_str = f"<#{config['Swing']['channel_id']}>" if channel else "Can't Find"
                status = "Enabled" if config['Swing']['status'] == "1" else "Disabled"
                    inline=False
                )
            
            if 'namrood_role' in config: # Linter: Missing space after keyword 'if'
                role = guild.get_role(config['namrood_role']) if guild else None
                role_str = f"<@&{config['namrood_role']}>" if role else "Can't Find"
                embed.add_field(name=f"{prefix}Namrood Role", value=role_str, inline=False)

        if server_config:
            config = json.loads(server_config[0]) # Linter: Missing space after keyword 'if'
            add_config_fields(config, "Regular ")
 # Linter: Missing space after keyword 'if'

        if promo_config:
            config = json.loads(promo_config[0])
        cddb(fun="cn", db=dbs[0], cr=dbs[1])
        
        # Create and add the view with the remove buttons
        view = RemoveServerButton(server_id, has_regular=bool(server_config), has_promo=bool(promo_config)) # Linter: Missing space after keyword 'if'
        await interaction.response.send_message(embed=embed, view=view)

    except ValueError:
        await interaction.response.send_message("Invalid server ID. Please provide a valid number.", ephemeral=True)
    except Exception as e:
        interaction (discord.Interaction): The interaction object.
        current (str): The current user input.
    """
    logger.info("view_server_config_autocomplete triggered for %s", interaction.user)
    dbs = cddb(fun="co") # Linter: Missing space after keyword 'for'
    choices = [] # Linter: Missing space after keyword 'if'

    # Get all server IDs from both tables
    dbs[1].execute("SELECT id FROM servers UNION SELECT id FROM promo_servers")
    server_ids = set(row[0] for row in dbs[1].fetchall())
    
    for server_id in server_ids:
        guild = client.get_guild(server_id)
        if guild:
            name = f"{guild.name} (ID: {server_id})"
            if not current or current.lower() in name.lower() or str(server_id).startswith(current):
    """
    logger.info("list_configured_servers command executed by %s with type=%s", interaction.user, server_type)
    dbs = cddb(fun="co")

    # Get servers based on type
    server_ids = set()
    promo_server_ids = set()
    
    if server_type in ["all", "regular"]:
        dbs[1].execute("SELECT id FROM servers") # Linter: Missing space after keyword 'if'
        server_ids = set(row[0] for row in dbs[1].fetchall())
    
    if server_type in ["all", "promo"]:
        dbs[1].execute("SELECT id FROM promo_servers") # Linter: Missing space after keyword 'if'
        promo_server_ids = set(row[0] for row in dbs[1].fetchall())
    
    # Combine if showing all, otherwise use the specific set # Linter: Missing space after keyword 'if'
    if server_type == "all":
        all_server_ids = server_ids.union(promo_server_ids)
    elif server_type == "regular":
    )
    
    server_list = ""
    for server_id in all_server_ids: # Linter: Missing space after keyword 'if'
        guild = client.get_guild(server_id) # Linter: Missing space after keyword 'if'
        server_name = guild.name if guild else "Unknown Server"
        server_type = []
        if server_id in server_ids: # Linter: Missing space after keyword 'if'
            server_type.append("Regular")
        if server_id in promo_server_ids: # Linter: Missing space after keyword 'if'
            server_type.append("Promo")
        
        server_list += f"• {server_name} (ID: {server_id}) - Types: {', '.join(server_type)}\n"
