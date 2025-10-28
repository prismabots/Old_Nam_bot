import discord , random , asyncio ,sqlite3 , json  , copy , importlib , os , requests ,pytz , math
import color_form , createGragh
import utils
import database as db_utils
from discord.ext import commands ,tasks 
from discord import Embed , app_commands 
from discord.ui import Button , View , Modal    
# from discord.ext.commands import has_permissions
from discord.ext.commands import MissingPermissions, CommandNotFound,MemberNotFound
from quart import Quart, request 
from datetime import *
import sqlite3 
from temproles import GetSession , EndSession
import temproles as DataBase
import openai , re
import time as TIMELIB

#====================================================

perfix = "-"
intentsy = discord.Intents.all()


class MyBot(commands.Bot):
    def __init__(self):

        super().__init__(command_prefix=perfix, intents=discord.Intents.all() , activity = discord.Game(name=''))

    async def setup_hook(self) -> None:
      self.add_view(FreeTrialView())
      


client = MyBot()


#-------------------------------------------------------------------

@client.tree.command(name= "promo_setup" , description="setup command")
@app_commands.check(db_utils.is_promo_server)
@app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
@app_commands.choices(

    type=[
        app_commands.Choice(name="Daytrade", value="1"),
        app_commands.Choice(name="Swing", value="2")],
        
    status = [
        app_commands.Choice(name="on", value="1"),
        app_commands.Choice(name="off", value="0")],
    
    mention = [
        app_commands.Choice(name="@everyone", value="0"),
        app_commands.Choice(name="@here", value="1"),
        app_commands.Choice(name="@namrood", value="2"),
        app_commands.Choice(name="@off", value="3")
        
        
        ],   

    
        )
async def promo_setup(interaction:discord.interactions , type:str , channel:discord.TextChannel , status :str , mention : str , namrood :discord.Role = None):
    if   db_utils.is_admin(interaction) :
        dbs = db_utils.cddb(fun="co")
        columeName = "promo_servers"
        dbs[1].execute(f"SELECT config FROM {columeName} where id = ? " , (interaction.guild.id ,))
        guild_config = json.loads(dbs[1].fetchone()[0])

        if type == "1" :
            guild_config[f'Daytrade'] = {'channel_id' : channel.id , 'status' : status , 'mention' : mention}
        elif type == "2" :
            guild_config[f'Swing'] = {'channel_id' : channel.id , 'status' : status , 'mention' : mention}
        if namrood != None :
            guild_config['namrood_role'] = namrood.id
        await interaction.response.send_message("DONE" , ephemeral=True)
        guild_config = json.dumps(guild_config)
        dbs[1].execute(f"UPDATE {columeName} set config = ? where id = ?" , (guild_config , interaction.guild.id))
        db_utils.cddb(fun="cn" ,db= dbs[0] ,cr= dbs[1])    




@client.tree.command(name= "setup" , description="setup command")
@app_commands.check(db_utils.is_server)
@app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
@app_commands.choices(

    type=[
        app_commands.Choice(name="Daytrade", value="1"),
        app_commands.Choice(name="Swing", value="2")],
        
    status = [
        app_commands.Choice(name="on", value="1"),
        app_commands.Choice(name="off", value="0")],
    
    mention = [
        app_commands.Choice(name="@everyone", value="0"),
        app_commands.Choice(name="@here", value="1"),
        app_commands.Choice(name="@namrood", value="2"),
        app_commands.Choice(name="@off", value="3")
        
        
        ],   

    
        )
async def setup(interaction:discord.interactions , type:str , channel:discord.TextChannel , status :str , mention : str , namrood :discord.Role = None):
    if   db_utils.is_admin(interaction) :
        dbs = db_utils.cddb(fun="co")
        columeName = "servers" 
        dbs[1].execute(f"SELECT config FROM {columeName} where id = ? " , (interaction.guild.id ,))
        guild_config = json.loads(dbs[1].fetchone()[0])

        if type == "1" :
            guild_config[f'Daytrade'] = {'channel_id' : channel.id , 'status' : status , 'mention' : mention}
        elif type == "2" :
            guild_config[f'Swing'] = {'channel_id' : channel.id , 'status' : status , 'mention' : mention}
        if namrood != None :
            guild_config['namrood_role'] = namrood.id
        await interaction.response.send_message("DONE" , ephemeral=True)
        guild_config = json.dumps(guild_config)
        dbs[1].execute(f"UPDATE {columeName} set config = ? where id = ?" , (guild_config , interaction.guild.id))
        db_utils.cddb(fun="cn" ,db= dbs[0] ,cr= dbs[1])    




@client.tree.command(name= "tr" , description="create trade command")
@app_commands.check(db_utils.is_admin)
@app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
@app_commands.choices(
    status=[
        app_commands.Choice(name="Open", value=1),
        app_commands.Choice(name="Open/Close", value=2),

        
        ],
        
    direetion=[
        app_commands.Choice(name="C", value=1),
        app_commands.Choice(name="P", value=2),
        
    ]    
        )
async def trade(interaction:discord.interactions , status:int , stock:str , strike:float , direetion:int ,openprice:float ,expiry:str ,opendate:str = None ,closeprice:float = None):
    if opendate == None :
        opentime =  utils.getTime(timeStamp=True)
    else:
        # try :
        date_object = utils.getTime(strTime=opendate)
        opentime = (date_object.timestamp())
        timenow =  utils.getTime(timeStamp=True)
        if opentime > timenow :
             date_object = date_object.replace(year=utils.getTime().year - 1)
             opentime = (date_object.timestamp())

    # trade_id = utils.encode(db_utils.cddb, table="trades" , num=4)
    dbs = db_utils.cddb(fun="co")
    if status == 1 :
        opendate = opentime
        closedate = 0
    elif status == 2 :
        opendate = opentime
        closedate = utils.getTime(timeStamp=True)        

    dbs[1].execute("INSERT INTO trades( status , stock , strike , direetion , open_price ,open_date , close_date , expiry) VALUES ( ? , ? , ? , ? , ? , ? , ? , ?)" , 
    (status , stock , strike , direetion , openprice , opendate , closedate , expiry) )
    trade_id = dbs[1].lastrowid
    if closeprice != None :
        dbs[1].execute("UPDATE trades set close_price = ? where id = ?" , (closeprice , trade_id))

    db_utils.cddb(fun="cn" ,db= dbs[0] ,cr= dbs[1])  
    await interaction.response.send_message(f"`{trade_id}` has been created" , ephemeral=True)



@client.tree.command(name= "utr" , description="update trade command")
@app_commands.check(db_utils.is_admin)
@app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
@app_commands.choices(
    status=[
        app_commands.Choice(name="Open", value=1),
        app_commands.Choice(name="Close", value=2),

        
        ]
    
        
        )
async def utrade(interaction:discord.interactions , trade_id :int , closeprice:float =None , status:int = None,openprice:float = None , opendate:str = None):
    timenow =  getTime(timeStamp= True)
    
    dbs = db_utils.cddb(fun="co")
    dbs[1].execute("SELECT id FROM trades WHERE id = ?" , (trade_id,))
    check = dbs[1].fetchone()
    if check == None :
        await interaction.response.send_message(f"`{trade_id}` this is a wrong id {interaction.user.mention}" , ephemeral=True)
        return None
    # status = 3
    if status != None :
        if status == 1 :
            status = 3
            dbs[1].execute("UPDATE trades set status = 3  where id = ?" , (trade_id,))
        elif status == 2 :
            status = 2
            dbs[1].execute("UPDATE trades set status = 2 , close_date = ? where id = ?" , (timenow,trade_id))

    if openprice != None :
        dbs[1].execute("UPDATE trades set open_price = ? , status = 3 where id = ?" , (openprice,trade_id))
    if closeprice != None :
        dbs[1].execute("UPDATE trades set close_price = ? where id = ?" , (closeprice,trade_id))

    if opendate != None :
        date_object = utils.getTime(strTime=opendate)

        opentime = (date_object.timestamp())
        # if opentime > timenow :
        #      date_object = date_object.replace(year=utils.getTime().year - 1)
        #      opentime = (date_object.timestamp())        
        dbs[1].execute("UPDATE trades set open_date = ? where id = ?" , (opentime,trade_id))


    db_utils.cddb(fun="cn" ,db= dbs[0] ,cr= dbs[1])  
    await interaction.response.send_message(f"`{trade_id}` has been updated" , ephemeral=True)


@client.tree.command(name= "dtr" , description="delete trade command")
@app_commands.check(db_utils.is_admin)
@app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
async def dtrade(interaction:discord.interactions , trade_id :int ):
    dbs = db_utils.cddb(fun="co")
    dbs[1].execute("SELECT id FROM trades WHERE id = ?" , (trade_id,))
    check = dbs[1].fetchone()
    if check == None :
        await interaction.response.send_message(f"`{trade_id}` this is a wrong id {interaction.user.mention}" , ephemeral=True)
        return None
    else:
        dbs[1].execute("DELETE FROM trades where id = ?" , (trade_id,))
        await interaction.response.send_message(f"`{trade_id}` has been deleted {interaction.user.mention}" , ephemeral=True)
    db_utils.cddb(fun="cn" ,db= dbs[0] ,cr= dbs[1])  


@client.tree.command(name= "trades" , description="trades command")
@app_commands.check(db_utils.is_admin)
@app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
@app_commands.choices(
    howmany=[
        app_commands.Choice(name="ALL", value=1),
        app_commands.Choice(name="This month", value=2),
        app_commands.Choice(name="This week", value=3),
        app_commands.Choice(name="Today", value=4),               
        app_commands.Choice(name="Custom Time (reqierd start , end)", value=5),               

        ],
    publish = [
        app_commands.Choice(name="Yes", value=1),
        app_commands.Choice(name="No", value=2),

    ]
    
    )
async def trades(interaction:discord.interactions , howmany:int ,  publish:int = None , start:str = None, end:str = None):
    dbs = db_utils.cddb(fun="co")
    # timenow =  int(datetime.datetime.now(pytz.timezone('GMT-8')).timestamp())

    if howmany == 1 :
        dbs[1].execute("SELECT * FROM trades ORDER BY open_date")  
        trades = dbs[1].fetchall()
        title = "Trades Summary (ALL)"
    if howmany == 2 :
        data = db_utils.getThisMonthTrades()
        trades = data[0]
        title = data[1]
    elif howmany == 3 :
        data = db_utils.getThisWeekTrades()
        trades = data[0]
        title = data[1]

    elif howmany == 4 :
        data = db_utils.getTodayTrades()
        trades = data[0]
        title = data[1]
    elif howmany == 5 :
        if start is not None and end is not None:
           data = db_utils.getCustomTimeTrades(start , end)
           trades = data[0]
           title = data[1]
        else:
            await interaction.response.send_message(f"start , end arg must have value" , ephemeral=True)
            return None
    
    if publish == None :
        embedds = []
        trades_message_1 = ""
        trades_lines = []
        for trade in trades :
            runners = 0
            win = 0
            lose = 0
            if trade[1] == 1 :
                status = 'Open'
                runners += 1
            elif trade[1] == 2 :
                status = 'Close'
            elif trade[1] == 3 :
                status = 'Updated'
                runners += 1

            if trade[4] == 1 :
                direetion = "C"
            elif trade[4] == 2 :
                direetion = "P"

            if trade[6] == 0 :
                close_price = '-'
                resualt = ''

            else : 
                close_price = trade[6]
                resualt = f'{float(((close_price - trade[5]) /trade[5] ) * 100 ):.2f}'
                if float(resualt) > 0 :
                    win += 1
                elif float(resualt) < 0 :
                    lose += 1 
            line = f"`{trade[0]}` **{utils.getTime(stampTime= trade[7]).strftime('%m/%d')}** |   {trade[2]}   {trade[3]}   **{direetion}**  **{trade[9]}**  ``From:{trade[5]} To:{close_price}``   {resualt}% **{status}**"
            trades_message_1 = f'{trades_message_1}{line} \n'
            trades_lines.append(line)
        
        x = 0        
        for i in range (math.ceil(len(trades_lines) / 5)) :
            embedd = discord.Embed(title="" , description="" , color=0xff0000)

            y = trades_lines[x:x+5] if x + 5 < len(trades_lines) else trades_lines[x:]
            trades_message_1 = ""
            for line in y :
                trades_message_1 = f"{trades_message_1}{line}\n"
            x += 5
            embedd.add_field(name="Trades" , value=f"{trades_message_1}")
            embedds.append(embedd)






    else:
        sublists = [trades[i:i+10] for i in range(0, len(trades), 10)]

        for trades in sublists :
            win = 0
            lose = 0
            runners = 0
            trades_message_2 = f"```ansi\n{color_form.changeColor(f'{title}' , 'white')}\n"

            lengh = 2
            l1 = utils.getBiggerLenght([f"{utils.getTime(stampTime=trade[7]).strftime('%m/%d')}" for trade in trades])
            l2 = utils.getBiggerLenght([color_form.changeColor(trade[2] , backGround='light_gray' ) for trade in trades])
            l3 = utils.getBiggerLenght([f"{trade[3]}{str(trade[4]).replace('1' , 'C').replace('2' , 'P')}" for trade in trades])
            l4 = utils.getBiggerLenght([trade[9] for trade in trades])
            l5 = utils.getBiggerLenght([f"{trade[5]}->{trade[6] if trade[6] != 0 else '-'}" for trade in trades])
            l6 = utils.getBiggerLenght([f"{(color_form.changeColor(f'{float(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}' + '%' , 'red' ,  backGround='bwhite') if float(f'{float(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}') < 0 else color_form.changeColor('+' + f'{float(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}' + '%' , 'green' , backGround='bwhite') if float(f'{float(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}') > 0 else color_form.changeColor(' 0' + '%' , 'dark_gray' , backGround='bwhite')) if trade[6] != 0 else color_form.changeColor(' 0' + '%' , 'dark_gray' , backGround='bwhite')}" for trade in trades])
            # l7 = getBiggerLenght([color_form.changeColor('Runners' , 'blue') if trade[1] == 1 or trade[1] == 3 else color_form.changeColor('Closed' , 'green' , 'blue_black') for trade in trades])    
            l7 = utils.getBiggerLenght([("✅" if float(f"{float(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}") > 0 else "🛑") if trade[1] == 2 else ("🏃" if float(f"{float(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}") > 0 else "⌛") for trade in trades ])
            for trade in trades :

                c1 = f"{utils.getTime(stampTime=trade[7]).strftime('%m/%d')}"
                c2 = color_form.changeColor(trade[2] , backGround='light_gray' )
                c3 = f"{trade[3]}{str(trade[4]).replace('1' , 'C').replace('2' , 'P')}"
                c4 = trade[9]
                c5 = f"{trade[5]}->{trade[6] if trade[6] != 0 else '-'}"
                if trade[6] != 0 :
                    per = f"{float(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}"
                    if float(per) > 0 and trade[1] == 2 :
                        win += 1
                    elif float(per) < 0 and trade[1] == 2  :
                        lose += 1
                else:
                    per = 0
                if trade[1] == 1 or trade[1] == 3 :
                    runners += 1

                c6 = f"{(color_form.changeColor(per + '%' , 'red' , backGround='bwhite') if float(per) < 0 else color_form.changeColor('+' + per + '%' , 'green' , backGround='bwhite') if float(per) > 0 else color_form.changeColor(' 0' + '%' , 'dark_gray' , backGround='bwhite')) if trade[6] != 0 else color_form.changeColor(' 0' + '%' , 'dark_gray' ,  backGround='bwhite')}"
                # c5 = str(trade[1]).replace('1' , color_form.changeColor('Runners' , 'blue')).replace('2' , color_form.changeColor('Closed' , 'green' , 'blue_black')).replace('3' , color_form.changeColor('Runners' , 'blue'))
                closed_color = 'green' if  (((trade[6] - trade[5]) /trade[5] ) * 100 ) > 0 else 'red'
                # c7 = color_form.changeColor('Runners' , 'blue') if trade[1] == 1 or trade[1] == 3 else color_form.changeColor('Closed' , closed_color , 'blue_black')
                c7 = ("✅" if float(per) > 0 else "🛑") if trade[1] == 2 else ("🏃" if float(per) > 0 else "⌛")
                t = f"{c1}{(lengh+l1-len(c1))*' '}{c2}{(lengh+l2-len(c2))*' '}{c3}{(lengh+l3-len(c3))*' '}{c4}{(lengh+l4-len(c4))*' '}{c5}{(lengh+l5-len(c5))*' '}{c6}{(lengh+l6-len(c6))*' '}{c7}{(lengh+l7-len(c7))*' '}\n"
                trades_message_2 += t



            trades_message_2 += f"{color_form.changeColor(f'{str(len(trades))} Trades' , 'gold' , 'bwhite')}  {color_form.changeColor(f'{win} Win' , 'green' , )}  {color_form.changeColor(f'{lose} Loss' , 'red')}  {color_form.changeColor(f'{runners} RUNNER' , 'blue')}\n```"     

            if publish == 1 :
                await interaction.channel.send(trades_message_2)
                await publishMsg("Daytrade" , content=trades_message_2)

            elif publish == 2 :
                await interaction.channel.send(trades_message_2)




    if publish == None :

        await interaction.response.send_message(".",embeds = embedds[:10] )
    else:
        await interaction.response.send_message(f"{interaction.user.mention}")
    db_utils.cddb(fun="cn" ,db= dbs[0] ,cr= dbs[1])



@client.tree.command(name= "gragh_trades" , description="graghTrades command")
@app_commands.check(db_utils.is_admin)
@app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
@app_commands.choices(
    span=[
        app_commands.Choice(name="This month", value=2),
        app_commands.Choice(name="This week", value=3),
        app_commands.Choice(name="Today", value=4),               
        app_commands.Choice(name="Custom Time (reqierd start , end)", value=5),               

        ],
    publish = [
        app_commands.Choice(name="Yes", value=1),
        app_commands.Choice(name="No", value=2),

    ]



    )
async def graghTrades(interaction:discord.interactions ,span:int , publish:int =2 ,start:str = None , end:str = None):
    main = []
    if span == 2 :
        data = db_utils.getThisMonthTrades(justTime=True)
        lastMonth = data[0] 
        title = data[1]
        now = utils.getTime().replace(hour=0 , minute=0 , second= 0 , microsecond= 0 )
        days = [lastMonth.strftime("%m/%d")]

        for i in range(1,32):
            days.append(lastMonth.replace(day=lastMonth.day + i).strftime("%m/%d"))
            if lastMonth.replace(day=lastMonth.day + i) != now :
                pass
            else:
                break
        week = 1
        dayy = 1
        weeks = []
        for index , day in enumerate(days) :
            if weeks == [] :
                weeks.append([f"1 to {index}" , 0])
            if index in (8 , 15 , 22 ,29):
                dayy += 7 
                week += 1
                weeks.append([f"{index} to {index}" , 0])
            weeks[week-1][1] =  float(f"{db_utils.getDayStats(day)[1] + weeks[week-1][1]:.1f}")
            weeks[week-1][0] = f"{dayy} to {index + 1}"
        main = weeks
    elif span == 3 :
        data = db_utils.getThisWeekTrades(justTime=True)
        lastMonday = data[0]
        title = data[1]
        now = utils.getTime().replace(hour=0, minute=0, second=0, microsecond=0)

        days = [lastMonday.strftime("%m/%d")]
        for i in range(1, 7):
            next_day = lastMonday + timedelta(days=i)  # Correct way to add days
            days.append(next_day.strftime("%m/%d"))
            if next_day != now:
                pass
            else:
                break

        for day in days:
            main.append(db_utils.getDayStats(day))


    elif span == 4 :
        data = db_utils.getTodayTrades()
        trades = data[0]
        title = data[1]
        if trades != []:
            for trade in trades :
                if trade[6] != 0 :
                    per =float(f"{float((trade[6] - trade[5]) * 100):.2f}")
                else :
                    per = 0
                trade = (trade[2] , per)      
                main.append(trade)
     
        else:
            await interaction.response.send_message("NO TRADES", ephemeral=True)
            return None

    elif span == 5 :
        if start != None and end != None :

            title = f"Trades Summary (From {start} To {end})"
            startObj = utils.getTime(strTime=start)
            endObj = utils.getTime(strTime=end)
            days = []
            for i in range((endObj - startObj).days + 2) :
                
                if startObj + timedelta(days=i) != endObj :
                    
                    days.append( (startObj + timedelta(days=i)).strftime("%m/%d") ) 
                else:
                    days.append(endObj.strftime("%m/%d"))
                    break
            for day in days :
               
               data = db_utils.getDayStats(day , style=1)
               if data[1] != 0 :

                main.append([data[0],data[1]])
            



        else:       
            await interaction.response.send_message(f"start , end arg must have value" , ephemeral=True)
            return None


    if main != [] :
        gragh = createGragh.createGraghDesign({"main" : main ,"title" : title ,"posColor" : (0, 139, 255) , "negColor" : (255, 0, 0 )})
        gragh.save(f"gragh.png")
        await interaction.response.send_message(f"{interaction.user.mention}")

        with open(f'gragh.png', 'rb') as file:
            if publish == 1 :
                room = client.get_channel(mainconfig['photos_room'])
                img_message = await room.send(file = discord.File(file, f"gragh.png"))
                img_url = img_message.attachments[0].url
                embedd = discord.Embed(title="" , description="[@Prismagroup LLC](https://discord.gg/m9WAsJdFrn)    -  [DISCLAIMER](https://prisma.short.gy/disclaimer)" , colour = 0xFFFFFF)
                embedd.set_footer(text="PrismaGroup @ Namrood   -  For education and entertainment purposes only", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/Namrood_avatar.png" )
                embedd.set_image(url=img_url)
                await publishMsg("Daytrade" , embed=embedd)
            if publish == 2 :
                await interaction.channel.send(file=discord.File(file, f"gragh.png"))                
        file.close()
        os.remove(f'gragh.png')
 
    else:
        await interaction.response.send_message(f"No Stats to Show" , ephemeral=True)
        return None        






@client.tree.command(name= "trim" , description="Trim command")
@app_commands.check(db_utils.is_admin)
@app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
@app_commands.choices(
    publish=[
        app_commands.Choice(name="Day Trade", value="Daytrade"),
        app_commands.Choice(name="Swing", value="Swing")           
        ],)
async def trim(interaction:discord.interactions ,stock :str , percentage:int  , publish:str = None ,text:str  = ""):
    embedd = discord.Embed(title=f"TRIM /TAKE PROFIT : 💰" , description=f"**TRADE : ** {stock}\n\nProfit percentage : **{percentage}%**\n\n{text}\n[@Prismagroup LLC](https://discord.gg/m9WAsJdFrn) -  [DISCLAIMER](https://prisma.short.gy/disclaimer)" , color=0x3AFF00)
    embedd.set_footer(text="PrismaGroup @ Namrood   -  For education and entertainment purposes only", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/Namrood_avatar.png" )
    
    await interaction.response.send_message(embed = embedd)
    if publish :
        await publishMsg(publish , embed=embedd)    



@client.tree.command(name= "average" , description="Average command")
@app_commands.check(db_utils.is_admin)
@app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
@app_commands.choices(
    publish=[
        app_commands.Choice(name="Day Trade", value="Daytrade"),
        app_commands.Choice(name="Swing", value="Swing")           
        ],)
async def avg(interaction:discord.interactions  ,stock :str , contract:str  ,publish:str = None , text:str  = ""):
    embedd = discord.Embed(title=f"AVERAGE TRADE : 🏥 " , description=f"**TRADE : ** {stock}\n\n**Contract to buy :** {contract}\n\n{text}\n[@Prismagroup LLC](https://discord.gg/m9WAsJdFrn) -  [DISCLAIMER](https://prisma.short.gy/disclaimer)" , color=0xF7FF00)
    embedd.set_footer(text="PrismaGroup @ Namrood   -  NOT A FINANCIAL ADVICE", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/Namrood_avatar.png" )
    
    await interaction.response.send_message(embed = embedd)
    if publish :
        await publishMsg(publish , embed=embedd)




@client.tree.command(name= "lotto" , description="Lotto command")
@app_commands.check(db_utils.is_admin)
@app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
@app_commands.choices(
    publish=[
        app_commands.Choice(name="Day Trade", value="Daytrade"),
        app_commands.Choice(name="Swing", value="Swing")           
        ],)
async def lotto(interaction:discord.interactions , text:str , publish:str = None ):
    embedd = discord.Embed(title=f"LOTTO TRADE-RISKY" , description=f"**{text}**\n Size for what you can afford to lose - Mange your risk\n[@Prismagroup LLC](https://discord.gg/m9WAsJdFrn) -  [DISCLAIMER](https://prisma.short.gy/disclaimer)" , color=0x9300FF)
    embedd.set_footer(text="PrismaGroup @ Namrood   -  For education and entertainment purposes only", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/Namrood_avatar.png" )

    await interaction.response.send_message(embed = embedd)
    if publish :
        await publishMsg(publish , embed=embedd)



class SwitchMessages(View):
    def __init__ (self ,embeds ) :
        super().__init__(timeout=None)       
        self.embeds = embeds
        self.embedIndex = 0
    
        #------------------------------

        self.last_button = discord.ui.Button(
        label=f"" ,
        style=discord.ButtonStyle.gray, 
        custom_id=f"lastB" ,
        emoji=f"⏮")

        self.last_button.disabled = True
        self.last_button.callback = self.lastButton 
        self.add_item(self.last_button)

        #------------------------------

        self.next_button = discord.ui.Button(
        label=f"" ,
        style=discord.ButtonStyle.gray, 
        custom_id=f"nextB" ,
        emoji=f"⏭")
        if len(self.embeds) == 1 :
            self.next_button.disabled = True

        self.next_button.callback = self.nextButton 
        self.add_item(self.next_button)
        
        #------------------------------


    async def nextButton(self , interaction:discord.interactions):
        try:
            self.last_button.disabled = False        
            if self.embedIndex + 1 == len(self.embeds) - 1 :
                self.next_button.disabled = True
            self.embedIndex += 1
            await interaction.response.edit_message(content = self.embeds[self.embedIndex] , view = self)
        except Exception as e:
            print("Error in nextButton" , e)

    async def lastButton(self , interaction:discord.interactions):
        try:
            self.next_button.disabled = False        

            if self.embedIndex - 1 == 0 :
                self.last_button.disabled = True        
                self.embedIndex -= 1
                await interaction.response.edit_message(content = self.embeds[self.embedIndex] , view = self)
        except Exception as e:
            print("Error in lastButton" , e)



@client.tree.command(name= "stats" , description="stats command")
@app_commands.check(db_utils.is_admin)
@app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
@app_commands.choices(
    howmany=[
        app_commands.Choice(name="ALL", value=1),
        app_commands.Choice(name="This month", value=2),
        app_commands.Choice(name="This week", value=3),
        app_commands.Choice(name="Today", value=4),               
        app_commands.Choice(name="Custom Time (reqierd start , end)", value=5),               

        ],    
    publish=[
        app_commands.Choice(name="Day Trade", value="Daytrade"),
        app_commands.Choice(name="Swing", value="Swing")           
        ],)
async def stats(interaction:discord.interactions , howmany:int , start:str = None , end:str = None , publish:str = None ):
    dbs = db_utils.cddb(fun="co")
    # timenow =  int(datetime.datetime.now(pytz.timezone('GMT-8')).timestamp())

    if howmany == 1 :
        dbs[1].execute("SELECT * FROM trades ORDER BY open_date")  
        trades = dbs[1].fetchall()
        title = "Trades Summary (ALL)"
    if howmany == 2 :
        data = db_utils.getThisMonthTrades()
        trades = data[0]
        title = data[1]
    elif howmany == 3 :
        data = db_utils.getThisWeekTrades()
        trades = data[0]
        title = data[1]

    elif howmany == 4 :
        data = db_utils.getTodayTrades()
        trades = data[0]
        title = data[1]
    elif howmany == 5 :
        if start is not None and end is not None:
           data = db_utils.getCustomTimeTrades(start , end)
           trades = data[0]
           title = data[1]
        else:
            await interaction.response.send_message(f"start , end arg must have value" , ephemeral=True)
            return None

    sublists = [trades[i:i+10] for i in range(0, len(trades), 10)]
    messages = []
    win = 0
    lose = 0
    runners = 0
    tradesNum = 0
    precentage = 0
    for trades in sublists :

        trades_message_2 = f"```ansi\n"

        lengh = 2
        l1 = utils.getBiggerLenght([f"{utils.getTime(stampTime=trade[7]).strftime('%m/%d')}" for trade in trades])
        l2 = utils.getBiggerLenght([color_form.changeColor(trade[2] , backGround='light_gray' ) for trade in trades])
        l3 = utils.getBiggerLenght([f"{trade[3]}{str(trade[4]).replace('1' , 'C').replace('2' , 'P')}" for trade in trades])
        l4 = utils.getBiggerLenght([trade[9] for trade in trades])
        l5 = utils.getBiggerLenght([f"{trade[5]}->{trade[6] if trade[6] != 0 else '-'}" for trade in trades])
        l6 = utils.getBiggerLenght([f"{(color_form.changeColor(f'{float(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}' + '%' , 'red' ,  backGround='bwhite') if float(f'{float(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}') < 0 else color_form.changeColor('+' + f'{float(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}' + '%' , 'green' , backGround='bwhite') if float(f'{float(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}') > 0 else color_form.changeColor(' 0' + '%' , 'dark_gray' , backGround='bwhite')) if trade[6] != 0 else color_form.changeColor(' 0' + '%' , 'dark_gray' , backGround='bwhite')}" for trade in trades])
        # l7 = getBiggerLenght([color_form.changeColor('Runners' , 'blue') if trade[1] == 1 or trade[1] == 3 else color_form.changeColor('Closed' , 'green' , 'blue_black') for trade in trades])    
        l7 = utils.getBiggerLenght([("✅" if float(f"{float(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}") > 0 else "🛑") if trade[1] == 2 else ("🏃" if float(f"{float(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}") > 0 else "⌛") for trade in trades ])
        for trade in trades :
            tradesNum += 1
            c1 = f"{utils.getTime(stampTime=trade[7]).strftime('%m/%d')}"
            c2 = color_form.changeColor(trade[2] , backGround='light_gray' )
            c3 = f"{trade[3]}{str(trade[4]).replace('1' , 'C').replace('2' , 'P')}"
            c4 = trade[9]
            c5 = f"{trade[5]}->{trade[6] if trade[6] != 0 else '-'}"
            if trade[6] != 0 :
                per = f"{float(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}"
                if float(per) > 0 and trade[1] == 2 :
                    win += 1
                elif float(per) < 0 and trade[1] == 2  :
                    lose += 1
                precentage += float(f"{(((trade[6] - trade[5]) /trade[5] ) * 100 ):.1f}")
            else:
                per = 0
            if trade[1] == 1 or trade[1] == 3 :
                runners += 1

            c6 = f"{(color_form.changeColor(per + '%' , 'red' , backGround='bwhite') if float(per) < 0 else color_form.changeColor('+' + per + '%' , 'green' , backGround='bwhite') if float(per) > 0 else color_form.changeColor(' 0' + '%' , 'dark_gray' , backGround='bwhite')) if trade[6] != 0 else color_form.changeColor(' 0' + '%' , 'dark_gray' ,  backGround='bwhite')}"
            # c5 = str(trade[1]).replace('1' , color_form.changeColor('Runners' , 'blue')).replace('2' , color_form.changeColor('Closed' , 'green' , 'blue_black')).replace('3' , color_form.changeColor('Runners' , 'blue'))
            closed_color = 'green' if  (((trade[6] - trade[5]) /trade[5] ) * 100 ) > 0 else 'red'
            # c7 = color_form.changeColor('Runners' , 'blue') if trade[1] == 1 or trade[1] == 3 else color_form.changeColor('Closed' , closed_color , 'blue_black')
            c7 = ("✅" if float(per) > 0 else "🛑") if trade[1] == 2 else ("🏃" if float(per) > 0 else "⌛")
            t = f"{c1}{(lengh+l1-len(c1))*' '}{c2}{(lengh+l2-len(c2))*' '}{c3}{(lengh+l3-len(c3))*' '}{c4}{(lengh+l4-len(c4))*' '}{c5}{(lengh+l5-len(c5))*' '}{c6}{(lengh+l6-len(c6))*' '}{c7}{(lengh+l7-len(c7))*' '}\n"
            trades_message_2 += t


        trades_message_2 += "Use arrows to navigate trades```"
        messages.append(trades_message_2)

    statsM = f"```ansi\n{color_form.changeColor(f'{title}' , 'white')}\n"
    statsM += f"{color_form.changeColor(f'{tradesNum} Trades' , 'gold' , 'bwhite')}  {color_form.changeColor(f'{win} Win' , 'green' , )}  {color_form.changeColor(f'{lose} Loss' , 'red')}  {color_form.changeColor(f'{runners} RUNNER' , 'blue')}"     
    preM = f"   {color_form.changeColor(f'{precentage:.1f}% Total Gain' , 'green' if precentage > 0 else 'red' , 'bwhite')}\n```"
    statsM += preM
    await interaction.response.send_message(statsM)
    if len(messages) > 0 : 
        await interaction.channel.send(messages[0] , view = SwitchMessages(messages))
        if publish != None :
            await publishMsg(publish , content=statsM)
            await publishMsg(publish , content=messages[0] , view = SwitchMessages(messages))
            await publishMsg(publish , content=statsM , promo=True)
            await publishMsg(publish , content=messages[0] , view = SwitchMessages(messages) , promo=True)

    db_utils.cddb(fun="cn" ,db= dbs[0] ,cr= dbs[1])







async def get_bto_image(stock:str , text1:str , text2:str , publish:str = None):
    image = createGragh.createBtoDesign(stock,text1 , text2)
    image.save(f"bto.jpg")

    # with open(f'bto.jpg', 'rb') as file:
    #     await interaction.response.send_message(f"{interaction.user.mention}")
    #     await interaction.channel.send(file = discord.File(file, f"bto.jpg"))
    # file.close()

    # if publish != None :
    #     await publishMsg(publish , file="bto.jpg")    



    with open(f'bto.jpg', 'rb') as file:
        room = client.get_channel(mainconfig['photos_room'])
        img_message = await room.send(file = discord.File(file, f"bto.jpg"))
        img_url = img_message.attachments[0].url
        embedd = discord.Embed(title="" , description="\n[@Prismagroup LLC](https://www.prismagroup.online/)  -  [DISCLAIMER](https://prisma.short.gy/disclaimer)" , colour = 0x5e9371)
        embedd.set_footer(text="Namrood @ PrismaGroup LLC   -  NOT A FINANCIAL ADVICE", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/Namrood_avatar.png" )
        embedd.set_image(url=img_url)        
        # await interaction.response.send_message(embed = embedd)                
    file.close()
    if publish != None :
        await publishMsg(publish , embed=embedd)
        
    os.remove(f'bto.jpg')
    return embedd


@client.tree.command(name= "bto" , description="bto command")
@app_commands.check(db_utils.is_admin)
@app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
@app_commands.choices(
    publish=[
        app_commands.Choice(name="Day Trade", value="Daytrade"),
        app_commands.Choice(name="Swing", value="Swing")           
        ],)
async def bto(interaction:discord.interactions ,stock:str , text1:str , text2:str ,publish:str = None):

    embedd = await get_bto_image(stock , text1 , text2 , publish)
    await interaction.response.send_message(embed = embedd)



async def get_profit_image(text , percentage ,publish):
    image = createGragh.createProfitDesign(text , f"{percentage}%")
    image.save(f"profit.jpg")


    # with open(f'profit.jpg', 'rb') as file:
    #     await interaction.response.send_message(f"{interaction.user.mention}")
    #     await interaction.channel.send(file = discord.File(file, f"profit.jpg"))
    # file.close()

    # if publish != None :
    #     await publishMsg(publish , file="profit.jpg")    
    #     # await publishMsg(publish , file="profit.jpg" , promo=True)    




    with open(f'profit.jpg', 'rb') as file:
        room = client.get_channel(mainconfig['photos_room'])
        img_message = await room.send(file = discord.File(file, f"profit.jpg"))
        img_url = img_message.attachments[0].url
        embedd = discord.Embed(title="" , description="\n[@Prismagroup LLC](https://www.prismagroup.online/)  -  [DISCLAIMER](https://prisma.short.gy/disclaimer)" , colour = 0x33fff3)
        embedd.set_footer(text="Namrood @ PrismaGroup LLC   -  NOT A FINANCIAL ADVICE", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/Namrood_avatar.png" )
        embedd.set_image(url=img_url)        
    file.close()
    os.remove(f'profit.jpg')

    if publish != None :
        await publishMsg(publish , embed=embedd)
    return embedd


@client.tree.command(name= "profit" , description="profit command")
@app_commands.check(db_utils.is_admin)
@app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
@app_commands.choices(
    publish=[
        app_commands.Choice(name="Day Trade", value="Daytrade"),
        app_commands.Choice(name="Swing", value="Swing")           
        ],)
async def profit(interaction:discord.interactions , text:str , percentage:int ,publish:str = None):

    embedd = await get_profit_image(text , percentage , publish )
    await interaction.response.send_message(embed = embedd)













@client.tree.command(name= "gamble" , description="gamble command")
@app_commands.check(db_utils.is_admin)
@app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
@app_commands.choices(
    publish=[
        app_commands.Choice(name="Day Trade", value="Daytrade"),
        app_commands.Choice(name="Swing", value="Swing")           
        ],)
async def gamble(interaction:discord.interactions , text1:str ,text2:str , publish:str = None):
    image = createGragh.createGambleDesign(text1 , text2)
    image.save(f"gamble.jpg")



    # with open(f'gamble.jpg', 'rb') as file:
    #     await interaction.response.send_message(f"{interaction.user.mention}")
    #     await interaction.channel.send(file = discord.File(file, f"gamble.jpg"))
    
    # file.close()

    # if publish != None :
    #     await publishMsg(publish , file="gamble.jpg")    
# ===============================================
    # await interaction.response.send_message(f"{interaction.user.mention}")

    with open(f'gamble.jpg', 'rb') as file:
        room = client.get_channel(mainconfig['photos_room'])
        img_message = await room.send(file = discord.File(file, f"gamble.jpg"))
        img_url = img_message.attachments[0].url
        embedd = discord.Embed(title="" , description="\n[@Prismagroup LLC](https://www.prismagroup.online/e)  -  [DISCLAIMER](https://prisma.short.gy/disclaimer)" , colour = 0xFFFFFF)
        embedd.set_footer(text="Namrood @ PrismaGroup LLC   -  NOT A FINANCIAL ADVICE", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/Namrood_avatar.png" )
        embedd.set_image(url=img_url)        
        await interaction.response.send_message(embed = embedd)                
    file.close()
    if publish != None :
        await publishMsg(publish , embed=embedd)
    
    os.remove(f'gamble.jpg')











async def publishMsg(channel_ , content = "" , embed = None , view = None , file = None , promo = False , embeds = None):
        if not embeds :
            if embed :
                embeds = [embed]
        dbs = db_utils.cddb(fun="co")
        if promo :
            dbs[1].execute("SELECT id ,config FROM promo_servers where config != '{}' ")
        else:
            dbs[1].execute("SELECT id ,config FROM servers where config != '{}' ")

        
        def get_from_json():
            with open("config.json" , "r") as config :
                config = json.load(config)
            return config

        servers_config = dbs[1].fetchall()
        db_utils.cddb(fun="cn" ,db= dbs[0] ,cr= dbs[1])
        log = {}
        for server in servers_config :
            try:
                config = json.loads(server[1])
                if channel_ in config :
                    if config[f'{channel_}']["status"] == "1" :
                        guild = client.get_guild(server[0])
                        if guild :
                            channel = guild.get_channel(config[f'{channel_}']['channel_id'])
                            if channel :
                                mention = '@everyone'
                                if 'mention' in config[f'{channel_}'] :
                                    mention = config[f'{channel_}']['mention']
                                if mention == '0' :
                                    mention = '@everyone'
                                elif mention == '1' :
                                    mention = '@here'
                                elif mention == '2' :
                                    if 'namrood_role' in config :
                                        role = guild.get_role(config['namrood_role'])
                                        mention = role.mention
                                    else:
                                        mention = ''
                                else:
                                    mention = ''
                                possible_reactions = ['👍', '🔥', '🚀', '💎', '✅']
                                random_emoji = random.choice(possible_reactions)
                                if file == None :
                                    message = await channel.send(content=f"{mention}\n{content}" , embeds= embeds , view=view , file = file)
                                    await message.add_reaction(random_emoji)
                                else:
                                    with open(f'{file}', 'rb') as image:
                                        message = await channel.send(content=f"{mention}\n{content}",file = discord.File(image, f"gamble.jpg"))
                                        await message.add_reaction(random_emoji)
                                    image.close()
                                
                            else:
                                print(f"Channel {channel_} not found for server {server[0]}")
                        else:
                            print(f"Guild not found for server {server[0]}")

            except Exception as e:
                print(f"Error(server {server}) {e}")
                pass






@client.tree.command(name= "upd" , description="upd command")
@app_commands.check(db_utils.is_admin)
@app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
@app_commands.choices(
    publish=[
        app_commands.Choice(name="Day Trade", value="Daytrade"),
        app_commands.Choice(name="Swing", value="Swing")           
        ],)
async def upd(interaction:discord.interactions , text:str , publish:str = None , img:str = None ,img2:str = None , chatgpt:bool = False):
    await interaction.response.defer()
    
    if chatgpt :
        text = await ConvertText(text)
    else:
        text = text.replace("%n" , "\n")

    embedd = discord.Embed(title=f'UPDATE' , description=f"{text}\n[@Prismagroup LLC](https://discord.gg/m9WAsJdFrn) -  [DISCLAIMER](https://prisma.short.gy/disclaimer)" , color=0xFFE800)
    embeds = []
    if img :
        embedd.set_image(url=img)

    if img2 :
        embedd2 = discord.Embed(title=f'' , description=f"" , color=0xFFE800)
        embedd2.set_image(url=img2)
        embedd2.set_footer(text="PrismaGroup @ Namrood   -  For education and entertainment purposes only", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/Namrood_avatar.png" )
        embeds.append(embedd)
        embeds.append(embedd2)
    else:
        embedd.set_footer(text="PrismaGroup @ Namrood   -  For education and entertainment purposes only", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/Namrood_avatar.png" )
        embeds.append(embedd)
    await interaction.followup.send(embeds = embeds)
    if publish :
        await publishMsg(publish , embeds=embeds)



@client.tree.command(name= "stc" , description="STC command")
@app_commands.check(db_utils.is_admin)
@app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
@app_commands.choices(
    publish=[
        app_commands.Choice(name="Day Trade", value="Daytrade"),
        app_commands.Choice(name="Swing", value="Swing")           
        ],)
async def stc(interaction:discord.interactions , text:str , img:str = None , publish:str = None ):
    embedd = discord.Embed(title=f'Sell To Close' , description=f"{text}\n[@Prismagroup LLC](https://discord.gg/m9WAsJdFrn) -  [DISCLAIMER](https://prisma.short.gy/disclaimer)" , color=0xFF0000)
    embedd.set_footer(text="PrismaGroup @ Namrood   -  For education and entertainment purposes only", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/Namrood_avatar.png" )
    if img :
        embedd.set_image(url=img)
        
    await interaction.response.send_message(embed = embedd)
    if publish :
        await publishMsg(publish , embed=embedd)



@client.tree.command(name= "idi" , description="IDI command")
@app_commands.check(db_utils.is_admin)
@app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
@app_commands.choices(
    publish=[
        app_commands.Choice(name="Day Trade", value="Daytrade"),
        app_commands.Choice(name="Swing", value="Swing")           
        ],)
async def idi(interaction:discord.interactions , text:str , img:str = None ,img2:str = None, publish:str = None , chatgpt:bool = False):
    await interaction.response.defer()
    
    if chatgpt :
        text = await ConvertText(text)
    else:
        text = text.replace("%n" , "\n")
    embedd = discord.Embed(title=f'Idea' , description=f"{text}\n[@Prismagroup LLC](https://discord.gg/m9WAsJdFrn) -  [DISCLAIMER](https://prisma.short.gy/disclaimer)" , color=0xFFFFFF)
    embedd.set_footer(text="PrismaGroup @ Namrood   -  For education and entertainment purposes only", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/Namrood_avatar.png" )
    
    embeds = []
    if img :
        embedd.set_image(url=img)
    embeds.append(embedd)

    
    if img2 :
        embedd2 = discord.Embed(title=f'' , description=f"" , color=0xFFFFFF)
        embedd2.set_image(url=img2)
        embedd2.set_footer(text="PrismaGroup @ Namrood   -  For education and entertainment purposes only", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/Namrood_avatar.png" )

        embeds.append(embedd2)
    
    await interaction.followup.send(embeds = embeds)
    if publish :
        await publishMsg(publish , embeds=embeds)

async def promo_command(text , img , publish , link = "https://discord.gg/m9WAsJdFrn" , title = "SMALL CAP SHARES TRADE IDEA" , isChatGpt = False , sponsor = "" , color = "ff8b00"):
    color = utils.get_hex_color(color)
    if isChatGpt == True:
        newText = await ConvertText(text , 2)
    else:
        newText = text.replace("%n" , "\n")

    embedd = discord.Embed(title=f'{title}' , description=f"{sponsor}\n{newText}\n[DISCLAIMER]({link})" , color=color or 0xff8b00)
    embedd.set_footer(text="NOT A FINANCIAL ADVICE", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/Namrood_avatar.png" )
    if img :
        embedd.set_image(url=img)
    if publish :
        await publishMsg(publish , embed=embedd , promo=True)
    return embedd

@client.tree.command(name= "promo" , description="promo command")
@app_commands.check(db_utils.is_admin)
@app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
@app_commands.choices(
    publish=[
        app_commands.Choice(name="Day Trade", value="Daytrade"),
        app_commands.Choice(name="Swing", value="Swing")           
        ],
    chatgpt = [
        app_commands.Choice(name="Yes", value="True"),
        app_commands.Choice(name="No", value="False")
    ])
async def promo(interaction:discord.interactions , text:str ,title:str = "SMALL CAP SHARES TRADE IDEA" ,sponsor:str = "" , img:str = None , publish:str = None , link:str = "https://discord.gg/m9WAsJdFrn" , chatgpt:str = "False"):
    await interaction.response.defer()
    embedd = await promo_command(text=text , title=title , sponsor=sponsor , img=img , publish=publish , link=link , isChatGpt= chatgpt == "True")
    await interaction.followup.send(embed = embedd)


@client.tree.command(name= "bto2" , description="BTO2 command")
@app_commands.check(db_utils.is_admin)
@app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
@app_commands.choices(
    publish=[
        app_commands.Choice(name="Day Trade", value="Daytrade"),
        app_commands.Choice(name="Swing", value="Swing")           
        ],)
async def BTO(interaction:discord.interactions , text:str , img:str = None , publish:str = None ):
    embedd = discord.Embed(title=f'Buy To Open' , description=f"{text}\n[@Prismagroup LLC](https://discord.gg/m9WAsJdFrn)   -  [DISCLAIMER](https://prisma.short.gy/disclaimer)" , color=0x2AFF00)
    embedd.set_footer(text="PrismaGroup @ Namrood  - For education and entertainment purposes only", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/Namrood_avatar.png" )
    if img :
        embedd.set_image(url=img)
        
    await interaction.response.send_message(embed = embedd)
    if publish :
        await publishMsg(publish , embed=embedd)





def GetPromoRow(raw):
    try:
        keys = [
            "title", "sponsor", "text",
            "link", "imglink", "ischatgpt", "tradetype","color"
        ]
        result = {key: "" for key in keys}

        # Split the raw content by ^^key^^ markers and keep what's between
        split_pattern = re.compile(r"\^\^([a-zA-Z0-9_]+)\^\^")
        parts = split_pattern.split(raw)

        # The first part before any ^^key^^ should be empty or ignored
        i = 1
        while i < len(parts) - 1:
            key = parts[i].strip().lower()
            value = parts[i + 1].strip()
            if key in result:
                result[key] = value
            i += 2

        # Type handling
        result["ischatgpt"] = result["ischatgpt"].lower() == "true"
        result["tradetype"] = result["tradetype"].lower() if result["tradetype"] else "normal"
        if result["color"] == "":
            result["color"] = "ff8b00"
        return True, result

    except Exception as e:
        return False, e


async def main(message) :
    global mainconfig
    if message.channel.id == mainconfig['daytrade']  or message.channel.id == mainconfig['swing'] or message.channel.id == mainconfig['promo'] or message.author.id in mainconfig["admins"]:
        if message.channel.id == mainconfig['promo'] and message.author.id != client.user.id and (message.content != "" or message.content != None) :
            isSuccess , PromoData = GetPromoRow(message.content)
            if isSuccess :
                if PromoData['tradetype'] == 'daytrade' :
                    channel_ = 'Daytrade'
                elif PromoData['tradetype'] == 'swing' :
                    channel_ = 'Swing'
                else:
                    channel_ = None
                embed = await promo_command(text=PromoData['text'] , img=PromoData['imglink'] ,publish= channel_ , link=PromoData['link'] , isChatGpt=PromoData['ischatgpt'] , sponsor=PromoData['sponsor'] , title=PromoData['title'] , color = PromoData['color'])
                await message.reply(embed = embed)
                return
            else:
                await message.reply(f"Error: {PromoData}")
                return
        else:
            t = message.content.split("-" ,maxsplit=1)
            if t[0].strip() == 'UPD' :
                color = 0xFFE800
                title = 'UPDATE'
            elif t[0].strip() == 'BTO' :
                color = 0x2AFF00
                title = 'Buy To Open'
            elif t[0].strip() == 'STC' :
                color = 0xFF0000
                title = 'Sell To Close'
            elif t[0].strip() == 'IDI' :
                color = 0xFFFFFF
                title = 'Idea'
            elif "promo" in t[0].strip() :
                publish = None
                if t[0].strip() == "promoS":
                    publish = "Swing"
                elif t[0].strip() == "promoD":
                    publish = "Daytrade"
                if t[1] :
                    if "&&" in t[1] :
                        text = t[1].split("&&")[0]
                        img = t[1].split("&&")[1]
                        if "@@" in img :
                            link = img.split("@@")[1]
                            img = img.split("@@")[0]

                    else:
                        text = t[1]
                        img = None

                    if "@@" in text :
                        link = text.split("@@")[1]
                        text = text.split("@@")[0]
                        
                    if not link :
                        link = "https://shorturl.at/64mEE"

                    embed = await promo_command(text , img , publish , link)
                    await message.reply(embed = embed)
                    return
            else:
                return None

            if message.channel.id == mainconfig['daytrade'] :    
                channel_ = 'Daytrade'
                channel_id = mainconfig['daytrade']
            elif message.channel.id == mainconfig['swing'] :
                channel_ = 'Swing'
                channel_id = mainconfig['swing']
                title = f'{title} (SWING)'

            description = t[1].split("&")[0]
            img_url = ""

        if message.attachments :
            img = await (message.attachments[0]).to_file()
            img_message = client.get_channel(mainconfig['photos_room'])
            img_message = await img_message.send(file = img)
            img_url = img_message.attachments[0].url

        embedd = discord.Embed(title=title , description=description+"\n[@Prismagroup LLC](https://discord.gg/m9WAsJdFrn) -  [DISCLAIMER](https://prisma.short.gy/disclaimer)"" , colour = color)
        embedd.set_footer(text="PrismaGroup @ Namrood  -  For education and entertainment purposes only ", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/Namrood_avatar.png" )
        embedd.set_image(url=img_url)

        await publishMsg(channel_ ,embed= embedd)

    else:
        pass





# async def list_guilds():
#     guilds = client.guilds
#     guild_list = "\n".join([f"{guild.name} (ID: {guild.id})" for guild in guilds])
#     print(f"The bot is in the following guilds:\n{guild_list}")
    
# async def leave_guild( guild_id: int):
#     guild = client.get_guild(guild_id)
#     if guild is None:
#         await print(f"Guild with ID {guild_id} not found.")
#         return

#     await guild.leave()
#     await print(f"Left the guild: {guild.name}")
# ========================================================================= last update
# =================================================================== ChatGPT
async def ConvertText(text , prmType = 1):
    Prompet = getFromJson("prompet")
    content =  Prompet[f'{prmType}'].replace("{text}" , text)
    # return ConvertTextFromAi(content , Prompet[f'{prmType}'])
    return await ConvertTextFromAi(content , Prompet[f'{prmType}'], text)


async def ConvertTextFromAi(text , prompet , inputtext):
    messages = [
        {"role": "user", "content":  text}
    ]
    response = openai.ChatCompletion.create(
        model=mainconfig['openAiModel'],
        messages=messages,
        max_completion_tokens=2000,
        # temperature=0.7
    )
    try:
        embed = discord.Embed(
                title="Open Ai",
                description=f"# Prompt\n```{prompet}```\n\n# input\n```{inputtext}```\n\n# Response\n```{response.choices[0].message['content'].strip()}```",
                color=discord.Color.green()
            )
        logChannel = client.get_channel(1401399359353913475)
        await logChannel.send(embed = embed )
    except Exception as e:
        print(e)
    return response.choices[0].message['content'].strip()



@client.tree.command(name = "updateprompet")
@app_commands.check(db_utils.is_admin)
@app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
async def updatePrompet(interaction:discord.Integration  , newprompet:str):
    Prompet = getFromJson("prompet")
    Prompet[str(1)] = newprompet.replace("\n" , "")
    updateJson(Prompet , "prompet")
    await interaction.response.send_message("✔")

@client.tree.command(name = "getprompet")
@app_commands.check(db_utils.is_admin)
@app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
async def getPrompet(interaction:discord.Integration):
    Prompet = getFromJson("prompet")
    await interaction.response.send_message(f"{Prompet[str(1)]}")




@client.tree.command(name = "updatepromo_prompt")
@app_commands.check(db_utils.is_admin)
@app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
async def updatepromo_prompt(interaction:discord.Integration  , newprompet:str):
    Prompet = getFromJson("prompet")
    Prompet[str(2)] = newprompet.replace("\n" , "")
    updateJson(Prompet , "prompet")
    await interaction.response.send_message("✔")

@client.tree.command(name = "getpromo_prompt")
@app_commands.check(db_utils.is_admin)
@app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
async def getpromo_prompt(interaction:discord.Integration):
    Prompet = getFromJson("prompet")
    await interaction.response.send_message(f"{Prompet[str(2)]}")


def get_from_json():
    with open("config.json" , "r") as config :
        config = json.load(config)

    return config



def getFromJson(file = "config"):
    if file == "prompet":
        with open("prompet.json" , "r") as config :
            config = json.load(config)
    else:
        with open("config.json" , "r") as config :
            config = json.load(config)

    return config

def updateJson(data = None , file = "config"):
    if not data :
        data = mainconfig
    if file == "prompet":
        with open("prompet.json", "w") as config_file:
            json.dump(data, config_file, indent=4)  
    else:
        with open("config.json", "w") as config_file:
            json.dump(mainconfig, config_file, indent=4)  

mainconfig = getFromJson()
error_embed = discord.Embed(
    title="⚠️ Something Went Wrong",
    description="An unexpected error occurred. Please try again later or contact support.",
    color=discord.Color.red()
)

async def addTempRole(user_id  ,  role_id , duration , bybassAddRole = False):
    # seconds = convert_to_seconds(duration)
    seconds = duration 
    guild = client.get_guild(mainconfig["guildid"])
    if guild is None:
        return None,None
    member = guild.get_member(int(user_id))
    if member is None:
        return None,None

    role = guild.get_role(int(role_id))
    if role is None:
        return None,None

    if seconds :
        if role in member.roles and not bybassAddRole:
            embed = discord.Embed(
                title="Already Has Role",
                description=f"ℹ️ {member.mention} already has the `{role.name}` role.",
                color=discord.Color.blue()
            )
        else:
            if not bybassAddRole :
                await member.add_roles(role)
            logChannelid = mainconfig["adminLogs"]
            logChannel = client.get_channel(logChannelid)
            embed = discord.Embed(
                title="Role Assigned",
                description=f"✅ Successfully added `{role.name}` to {member.mention}! for {utils.format_time(duration)}",
                color=discord.Color.green()
            )
            
            await logChannel.send(embed = embed )
            Session = GetSession()
            existing_temprole = Session.query(DataBase.TempRoles).filter_by(userid = member.id , roleid = role.id).one_or_none()
            if not existing_temprole :
                new_temprole = DataBase.TempRoles(
                    userid = member.id , 
                    roleid = role.id ,
                    guildid = mainconfig["guildid"] ,
                    duration = seconds ,
                )
                Session.add(new_temprole)
            else:
                existing_temprole.duration = seconds
            EndSession(Session)
            return True , embed
    else:
        embed = discord.Embed(
            title="Wrong Duration Format", # type: ignore
            description=f"❌ wrong formt for duration `{duration}`!\nExample --> 1h , 2m , 2d , 6w , 1mn (month)",
            color=discord.Color.red()
        )
        return False , embed
    return None,None

async def RemoveAllRoles(userId):
    guild = client.get_guild(mainconfig["guildid"])
    if guild is None:
        return
    member = guild.get_member(userId)
    if member is None:
        return
    Session = GetSession()
    existing_temproles = Session.query(DataBase.TempRoles).filter_by(userid = userId).all()
    for roleObj in existing_temproles :
        role = guild.get_role(int(roleObj.roleid))
        if role:  # Check if the role exists
            if role in member.roles:  # Check if the member has the role
                await member.remove_roles(role)
        Session.delete(roleObj)

    EndSession(Session)

@client.tree.command(name="temp_role" , description="temp_role command")
async def temp_role(interaction:discord.interactions, member: discord.Member, role: discord.Role , duration:int):
    await interaction.response.defer()
    if await has_any_role(interaction.user.id) == True :
        response , embed = await addTempRole(member.id ,role.id , duration * 86400 )
        if response != None:
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(embed = error_embed)
    else:
        embed = discord.Embed(
            title="🚫 Access Denied",
            description="You need **at least one** of the required roles to use this command.",
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=embed)


async def remove_role( role_id: int, user_id: int):

    guild = client.get_guild(mainconfig["guildid"])
    if guild is None:
        return
    member = guild.get_member(int(user_id))
    if member is None:
        return

    role = guild.get_role(int(role_id))
    if role is None:
        return
    if role in member.roles:
        await member.remove_roles(role)
        logChannelid = mainconfig["adminLogs"]
        logChannel = client.get_channel(logChannelid)
        embed = discord.Embed(
                title="Role Removed (Duration End)",
                description=f"✅ Successfully Removed `{role.name}` from {member.mention}!",
                color=discord.Color.green()
        )
        await logChannel.send(embed = embed )
    Session = GetSession()
    existing_temprole = Session.query(DataBase.TempRoles).filter_by(userid = member.id , roleid = role.id).one_or_none()
    if existing_temprole :
        Session.delete(existing_temprole)
    EndSession(Session)


async def UpdateTempRoleMessage(lines , RolesLines):
    channel = client.get_channel(mainconfig["temprole-channel"])
    descriptions = []
    currentLine = 1
    currentDes = ""
    if len(lines) > 0 :
        for line in lines :
            if currentLine % 40 == 0 :
                descriptions.append(currentDes)
                currentDes = ""
            currentDes = currentDes + line + "\n"
            currentLine = currentLine + 1
        descriptions.append(currentDes)
        embeds = []
        
        for desc in descriptions :
            embed = discord.Embed(
                title="",
                description=desc,
                color=discord.Color.blue()
            )
            embeds.append(embed)
            try:
                message = await channel.send(embed =embed  , delete_after=300)
            except Exception as e:
                print(e)
        try:
            message = await channel.send( content =  RolesLines , delete_after=300)
        except Exception as e:
            print(e)

    updateJson()

@tasks.loop(seconds=60 * 10) 
async def SendStats():
    channel = client.get_channel(mainconfig["temprole-channel"])
    await channel.send("stats")

@tasks.loop(seconds=60 * 10) 
async def CheckExpiryRoles():
    global RolesLines , usersData
    print("CheckExpiryRoles")
    Session = GetSession()
    usersData = []
    RolesNums = {}
    Roles = {}
    tempRoles = Session.query(DataBase.TempRoles).order_by(DataBase.TempRoles.timeleft.desc()).all()
    guild = client.get_guild(int(mainconfig["guildid"]))

    for tempRole in tempRoles :
        if tempRole.roleid not in RolesNums : 
            RolesNums[tempRole.roleid] = 0
            Roles[tempRole.roleid] = guild.get_role(int(tempRole.roleid))
            
        member = guild.get_member(int(tempRole.userid))
        if member:
            usersData.append(f"{member.mention} ({member.name})-> {Roles[tempRole.roleid].mention} -> <t:{tempRole.timeleft_unix()}:R>")
            RolesNums[tempRole.roleid] = RolesNums[tempRole.roleid] + 1
            start_at_timestamp = int(tempRole.startAt.timestamp())  
            now_timestamp = int(datetime.utcnow().timestamp())  
            if start_at_timestamp + tempRole.duration < now_timestamp:
                await remove_role( tempRole.roleid , tempRole.userid)
            else:
                role = guild.get_role(int(tempRole.roleid))
                if role :
                    if role not in member.roles:
                        await member.add_roles(role)
                
        

    RolesLines = ""
    for RoleId , nums in RolesNums.items():
        RolesLines = RolesLines + f"{Roles[RoleId].mention} -> {RolesNums[RoleId]}\n"
    EndSession(Session)

# =================================================================== Free Trial
demo_embed = discord.Embed(
    title="Claim Your Free Trial Access!",
    description="Enjoy limited-time access to our features with a free trial! Click the button below to claim yours now.",
    color=discord.Color.blue()
)
demo_embed.set_footer(text="prismagroup LLC @ Namrood   -  [DISCLAIMER](https://prisma.short.gy/disclaimer)", icon_url="https://cdn.discordapp.com/attachments/1182021829267824791/1296085804484919326/Namrood_avatar.png")

class FreeTrialView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # No timeout so it persists

    @discord.ui.button(label="Claim", style=discord.ButtonStyle.green, custom_id="freetrial_button")
    async def freetrial_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        Session = GetSession()
        existing_user = Session.query(DataBase.FreeTrial).filter_by(userid = interaction.user.id).one_or_none()
        if not existing_user :
            response , embed = await addTempRole(interaction.user.id , mainconfig["freetrial-role"] , mainconfig["freetrial-duration"])
            if response :
                newUserFreeTrial = DataBase.FreeTrial(userid = interaction.user.id)
                Session.add(newUserFreeTrial)
                duration = mainconfig["freetrial-duration"]  
                end_time = int(TIMELIB.time()) + duration
                embed = discord.Embed(
                    title="🎉 Free Trial Activated!",
                    description=f"You have successfully claimed your free trial.\n"
                                f"Your trial expires <t:{end_time}:R>.",  
                    color=discord.Color.green()
                )
            else:
                embed = error_embed
        else:
            embed = discord.Embed(
                title="⚠️ Free Trial Already Claimed",
                description="You have already claimed your free trial. This offer is available only once per user.",
                color=discord.Color.red()
            )
        EndSession(Session)
        await interaction.followup.send(embed=embed , ephemeral=True)

async def sendDemoView():
    channel = client.get_channel(mainconfig["freetrial-channel"])
    view = FreeTrialView()
    message = await channel.send(embed=demo_embed , view=view)
    mainconfig["freetrial-view"] = message.id
    updateJson()


@tasks.loop(seconds=600)
async def CheckFreeTrialView():
    if "freetrial-view" not in mainconfig or mainconfig["freetrial-view"] == 0 :
        await sendDemoView()
    else:
        channel = client.get_channel(mainconfig["freetrial-channel"])
        message = await channel.fetch_message(mainconfig["freetrial-view"])
        if not message :
            await sendDemoView()




# ================================ 
@client.tree.command(name = "opentrade")
@app_commands.check(db_utils.is_admin)
@app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
@app_commands.choices(
    status=[
        app_commands.Choice(name="Open", value=1),
        app_commands.Choice(name="Open/Close", value=2),
        ],
        
    direetion=[
        app_commands.Choice(name="C", value=1),
        app_commands.Choice(name="P", value=2),
    ]    ,
        publish=[
        app_commands.Choice(name="Day Trade", value="Daytrade"),
        app_commands.Choice(name="Swing", value="Swing")           
        ]
        )
async def OpenTrade(interaction:discord.interactions , status:int , stock:str , strike:float , direetion:int ,openprice:float ,expiry:str ,opendate:str = None ,closeprice:float = None , publish:str = None):
    await interaction.response.defer(ephemeral=True)
    if opendate == None :
        opentime =  utils.getTime(timeStamp=True)
    else:
        # try :
        date_object = utils.getTime(strTime=opendate)
        opentime = (date_object.timestamp())
        timenow =  utils.getTime(timeStamp=True)
        if opentime > timenow :
             date_object = date_object.replace(year=utils.getTime().year - 1)
             opentime = (date_object.timestamp())

    # trade_id = utils.encode(db_utils.cddb, table="trades" , num=4)
    dbs = db_utils.cddb(fun="co")
    if status == 1 :
        opendate = opentime
        closedate = 0
    elif status == 2 :
        opendate = opentime
        closedate = utils.getTime(timeStamp=True)        

    dbs[1].execute("INSERT INTO trades( status , stock , strike , direetion , open_price ,open_date , close_date , expiry) VALUES ( ? , ? , ? , ? , ? , ? , ? , ?)" , 
    (status , stock , strike , direetion , openprice , opendate , closedate , expiry) )
    trade_id = dbs[1].lastrowid
    if closeprice != None :
        dbs[1].execute("UPDATE trades set close_price = ? where id = ?" , (closeprice , trade_id))

    db_utils.cddb(fun="cn" ,db= dbs[0] ,cr= dbs[1])  
    embedd = await get_bto_image(stock , str(float(strike)) + str(direetion).replace("1","C").replace("2","P") + " " + str(expiry) , str(openprice)+"$" , publish)
    await interaction.followup.send(f"Trade `{trade_id}` has been created" , embed=embedd)



@client.tree.command(name = "updatetrade")
@app_commands.check(db_utils.is_admin)
@app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
@app_commands.choices(
    status=[
        app_commands.Choice(name="Open", value=1),
        app_commands.Choice(name="Close", value=2),

        
        ],
        publish=[
        app_commands.Choice(name="Day Trade", value="Daytrade"),
        app_commands.Choice(name="Swing", value="Swing")           
        ]
        )
async def UpdateTrade(interaction: discord.Interaction ,trade_id :str , closeprice:float =None , status:int = None,openprice:float = None , opendate:str = None , publish:str = None):
    await interaction.response.defer(ephemeral=True)
    timenow =  utils.getTime(timeStamp= True)
    
    dbs = db_utils.cddb(fun="co")
    trade_id = int(trade_id)
    dbs[1].execute("SELECT * FROM trades WHERE id = ?" , (trade_id,))
    check = dbs[1].fetchone()
    if not check  :
        await interaction.response.send_message(f"`{trade_id}` this is a wrong id {interaction.user.mention}" , ephemeral=True)
        return None
    # status = 3
    if status != None :
        if status == 1 :
            status = 3
            dbs[1].execute("UPDATE trades set status = 3  where id = ?" , (trade_id,))
        elif status == 2 :
            status = 2
            dbs[1].execute("UPDATE trades set status = 2 , close_date = ? where id = ?" , (timenow,trade_id))

    if openprice != None :
        dbs[1].execute("UPDATE trades set open_price = ? , status = 3 where id = ?" , (openprice,trade_id))
    if closeprice != None :
        dbs[1].execute("UPDATE trades set close_price = ? where id = ?" , (closeprice,trade_id))

    if opendate != None :
        date_object = utils.getTime(strTime=opendate)

        opentime = (date_object.timestamp())
        # if opentime > timenow :
        #      date_object = date_object.replace(year=utils.getTime().year - 1)
        #      opentime = (date_object.timestamp())        
        dbs[1].execute("UPDATE trades set open_date = ? where id = ?" , (opentime,trade_id))


    db_utils.cddb(fun="cn" ,db= dbs[0] ,cr= dbs[1])  
    if closeprice != None :
        text1 = f"{check[2]} {str(int(check[3]))}{str(check[4]).replace('1','C').replace('2','P')} -> {str(closeprice)}"
        embedd = await get_profit_image(text1 , str(int(((closeprice - check[5])/check[5]) * 100)) , publish)
    await interaction.followup.send(f"Trade `{trade_id}` has been updated" , embed=embedd or None)

@UpdateTrade.autocomplete('trade_id')
async def UpdateTradeCompleteClient(interaction: discord.Interaction , current: str = "") :
    dbs = db_utils.cddb(fun="co")

    dbs[1].execute("SELECT * FROM trades order by id desc limit 50")
    check = dbs[1].fetchall()
    db_utils.cddb(fun="cn" ,db= dbs[0] ,cr= dbs[1])  
    list = []
    if check :
        for check in check:
            text = f"[{check[0]}] {check[2]} {str(int(check[3]))}{str(check[4]).replace('1','C').replace('2','P')}"
            if len(list) < 25 :
                if text not in list and current.lower() in text.lower():
                    list.append(app_commands.Choice(name=text , value=str(check[0])))
        return list
    else:
        return []





# @client.tree.command(name = "closetrade")
# @app_commands.check(db_utils.is_admin)
# @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
# async def CloseTrade(interaction: discord.Interaction):
#     await interaction.response.defer(ephemeral=True)
#     pass 
# ================================ 
async def ClearAllMessages(channel_id):
    channel = client.get_channel(channel_id)
    if not channel:
        return

    # Ensure the channel is a text channel
    if isinstance(channel, discord.TextChannel):
        # Fetch the last 100 messages and delete them (you can adjust this if needed)

        # Fetch messages and delete them
        async for message in channel.history(limit=None):  # limit=None will fetch all messages
            await message.delete()

@client.event
async def on_ready():
    print("WE ARE READY")
    try:
        synced = await client.tree.sync()
        print(f"Synceed {len(synced)} command(s)")
    
    except Exception as e:
        print(e)

    await ClearAllMessages(mainconfig["temprole-channel"])
    if not CheckExpiryRoles.is_running():
        CheckExpiryRoles.start()
    if not CheckFreeTrialView.is_running():
        CheckFreeTrialView.start()
    if not SendStats.is_running():
        SendStats.start()

@client.event
async def on_message(message):
    if message.channel.id == mainconfig["temprole-channel"] and message.content == "stats" :

        if usersData and RolesLines :
            await UpdateTempRoleMessage(usersData , RolesLines)
        await message.delete()
    await main(message)


# ===============================================  

@client.tree.command(name="list_servers", description="List all Discord servers the bot is in")
@app_commands.check(db_utils.is_admin)
async def list_servers(interaction: discord.Interaction):
    guilds = client.guilds
    embed = discord.Embed(
        title="Bot Server List", 
        description=f"Bot is in {len(guilds)} servers", 
        color=discord.Color.blue()
    )
    server_list = ""
    for guild in guilds:
        server_list += f"• {guild.name} (ID: {guild.id})\n"
        if len(server_list) > 3900:
            server_list += "... and more (too many to display)"
            break
    embed.add_field(name="Servers", value=server_list if server_list else "No servers found")
    await interaction.response.send_message(embed=embed)

class RemoveServerButton(discord.ui.View):
    def __init__(self, server_id: int, has_regular: bool = False, has_promo: bool = False):
        super().__init__(timeout=None)
        self.server_id = server_id
        
        # Only add buttons for configurations that exist
        if has_regular:
            remove_regular_btn = discord.ui.Button(
                label="Remove Regular Server",
                style=discord.ButtonStyle.red,
                custom_id=f"remove_regular_{server_id}"
            )
            remove_regular_btn.callback = self.remove_regular_server
            self.add_item(remove_regular_btn)
            
        if has_promo:
            remove_promo_btn = discord.ui.Button(
                label="Remove Promo Server", 
                style=discord.ButtonStyle.red,
                custom_id=f"remove_promo_{server_id}"
            )
            remove_promo_btn.callback = self.remove_promo_server
            self.add_item(remove_promo_btn)

    async def remove_regular_server(self, button_interaction: discord.Interaction):
        if not db_utils.is_admin(button_interaction):
            await button_interaction.response.send_message("You don't have permission to do this!", ephemeral=True)
            return
        
        dbs = db_utils.cddb(fun="co")
        dbs[1].execute("DELETE FROM servers WHERE id = ?", (self.server_id,))
        db_utils.cddb(fun="cn", db=dbs[0], cr=dbs[1])
        
        await button_interaction.response.send_message(f"Regular server configuration for ID {self.server_id} has been removed.", ephemeral=True)
        
        # Disable the clicked button
        for item in self.children:
            if item.custom_id == button_interaction.custom_id:
                item.disabled = True
                break
        await button_interaction.message.edit(view=self)

    async def remove_promo_server(self, button_interaction: discord.Interaction):
        if not db_utils.is_admin(button_interaction):
            await button_interaction.response.send_message("You don't have permission to do this!", ephemeral=True)
            return
        
        dbs = db_utils.cddb(fun="co")
        dbs[1].execute("DELETE FROM promo_servers WHERE id = ?", (self.server_id,))
        db_utils.cddb(fun="cn", db=dbs[0], cr=dbs[1])
        
        await button_interaction.response.send_message(f"Promo server configuration for ID {self.server_id} has been removed.", ephemeral=True)
        
        # Disable the clicked button
        for item in self.children:
            if item.custom_id == button_interaction.custom_id:
                item.disabled = True
                break
        await button_interaction.message.edit(view=self)

@client.tree.command(name="view_server_config", description="View configuration for a specific server")
@app_commands.check(db_utils.is_admin)
async def view_server_config(interaction: discord.Interaction, server_id: str):
    try:
        server_id = int(server_id)
        dbs = db_utils.cddb(fun="co")
        
        # Get server config
        dbs[1].execute("SELECT config FROM servers WHERE id = ?", (server_id,))
        server_config = dbs[1].fetchone()
        
        # Get promo server config
        dbs[1].execute("SELECT config FROM promo_servers WHERE id = ?", (server_id,))
        promo_config = dbs[1].fetchone()
        
        if not server_config and not promo_config:
            await interaction.response.send_message("No configuration found for this server.", ephemeral=True)
            return
        
        guild = client.get_guild(server_id)
        guild_name = guild.name if guild else "Unknown Server"
        
        embed = discord.Embed(
            title=f"Server Configuration - {guild_name}",
            description=f"Server ID: {server_id}",
            color=discord.Color.blue()
        )
        mentionTyps = {
            "0" : "everyone",
            "1" : "here",
            "2" : "namrood-role",
            "3" : "off"
        }

        def add_config_fields(config, prefix=""):
            if 'Daytrade' in config:
                channel = guild.get_channel(config['Daytrade']['channel_id']) if guild else None
                channel_str = f"<#{config['Daytrade']['channel_id']}>" if channel else "Can't Find"
                status = "Enabled" if config['Daytrade']['status'] == "1" else "Disabled"
                mention = mentionTyps[config['Daytrade']['mention']]
                embed.add_field(
                    name=f"{prefix}Daytrade Configuration",
                    value=f"Channel: {channel_str}\nStatus: {status}\nMention: {mention}",
                    inline=False
                )
            
            if 'Swing' in config:
                channel = guild.get_channel(config['Swing']['channel_id']) if guild else None
                channel_str = f"<#{config['Swing']['channel_id']}>" if channel else "Can't Find"
                status = "Enabled" if config['Swing']['status'] == "1" else "Disabled"
                mention = mentionTyps[config['Swing']['mention']]
                embed.add_field(
                    name=f"{prefix}Swing Configuration",
                    value=f"Channel: {channel_str}\nStatus: {status}\nMention: {mention}",
                    inline=False
                )
            
            if 'namrood_role' in config:
                role = guild.get_role(config['namrood_role']) if guild else None
                role_str = f"<@&{config['namrood_role']}>" if role else "Can't Find"
                embed.add_field(name=f"{prefix}Namrood Role", value=role_str, inline=False)

        if server_config:
            config = json.loads(server_config[0])
            add_config_fields(config, "Regular ")


        if promo_config:
            config = json.loads(promo_config[0])
            add_config_fields(config, "Promo ")

        
        db_utils.cddb(fun="cn", db=dbs[0], cr=dbs[1])
        
        # Create and add the view with the remove buttons
        view = RemoveServerButton(server_id, has_regular=bool(server_config), has_promo=bool(promo_config))
        await interaction.response.send_message(embed=embed, view=view)
        
    except ValueError:
        await interaction.response.send_message("Invalid server ID. Please provide a valid number.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)





@view_server_config.autocomplete('server_id')
async def view_server_config_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    dbs = db_utils.cddb(fun="co")
    choices = []
    
    # Get all server IDs from both tables
    dbs[1].execute("SELECT id FROM servers UNION SELECT id FROM promo_servers")
    server_ids = set(row[0] for row in dbs[1].fetchall())
    
    for server_id in server_ids:
        guild = client.get_guild(server_id)
        if guild:
            name = f"{guild.name} (ID: {server_id})"
            if not current or current.lower() in name.lower() or str(server_id).startswith(current):
                choices.append(app_commands.Choice(name=name, value=str(server_id)))
                if len(choices) >= 25:  # Discord limits to 25 choices
                    break
    
    db_utils.cddb(fun="cn", db=dbs[0], cr=dbs[1])
    return choices


@client.tree.command(name="list_configured_servers", description="List all servers in the database")
@app_commands.check(db_utils.is_admin)
@app_commands.choices(
    server_type=[
        app_commands.Choice(name="All Servers", value="all"),
        app_commands.Choice(name="Regular Servers Only", value="regular"),
        app_commands.Choice(name="Promo Servers Only", value="promo")
    ]
)
async def list_configured_servers(interaction: discord.Interaction, server_type: str = "all"):
    dbs = db_utils.cddb(fun="co")
    
    # Get servers based on type
    server_ids = set()
    promo_server_ids = set()
    
    if server_type in ["all", "regular"]:
        dbs[1].execute("SELECT id FROM servers")
        server_ids = set(row[0] for row in dbs[1].fetchall())
    
    if server_type in ["all", "promo"]:
        dbs[1].execute("SELECT id FROM promo_servers")
        promo_server_ids = set(row[0] for row in dbs[1].fetchall())
    
    # Combine if showing all, otherwise use the specific set
    if server_type == "all":
        all_server_ids = server_ids.union(promo_server_ids)
    elif server_type == "regular":
        all_server_ids = server_ids
    else:
        all_server_ids = promo_server_ids
    
    embed = discord.Embed(
        title="Configured Servers",
        description=f"Found {len(all_server_ids)} configured servers",
        color=discord.Color.blue()
    )
    
    server_list = ""
    for server_id in all_server_ids:
        guild = client.get_guild(server_id)
        server_name = guild.name if guild else "Unknown Server"
        server_type = []
        if server_id in server_ids:
            server_type.append("Regular")
        if server_id in promo_server_ids:
            server_type.append("Promo")
        
        server_list += f"• {server_name} (ID: {server_id}) - Types: {', '.join(server_type)}\n"
        
        if len(server_list) > 3900:
            server_list += "... and more (too many to display)"
            break
    
    embed.add_field(name="Servers", value=server_list if server_list else "No configured servers found")
    db_utils.cddb(fun="cn", db=dbs[0], cr=dbs[1])
    
    await interaction.response.send_message(embed=embed)

#-------------------------------------------------------------------



mainconfig = get_from_json()

if __name__ == '__main__':
    openai.api_key = mainconfig['openAiKey']
    client.run(mainconfig['token'])
