import os
import discord
from keep_alive import keep_alive
import logging
from discord.ext import commands,tasks
from random import randint, choice
from googletrans import Translator
from replit import db
from cogs import update
from datetime import datetime,timedelta
import pytz
from math import floor

my_secret = os.environ['token']

logging.basicConfig(level=logging.INFO)

client = commands.Bot(command_prefix='z!')
client.remove_command("help")

admin='351239431102922752'

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Game(name="z!help"))

@client.event
async def on_message(message):
    if message.author==client.user:
        return
    content=message.content
    if "@zl385" in content or "<@905985060346408961>" in content or "@zl835#5913" in content or "<@!905985060346408961>" in content:
        await message.channel.send('Hello. I am zl835, your friendly neighbourhood multipurpose bot. Not to be confused with my creator, zl385.')
    else:
        await client.process_commands(message)

@client.command()
async def help(ctx):
    ctxprefix=str(ctx.message.content)[0:2]
    embed1=discord.Embed(title='Help',description=f'Command prefix: {(ctxprefix)}')
    embed1.set_footer(text='Made by zl385#9363. Page 1')
    embed1.add_field(
        name='List of commands',
        value=f"`{ctxprefix}help` - shows this message.\
        \n`{ctxprefix}blackjack <bet> (alias: bj)` - play a game of blackjack. Hit: Draw a card. Stand: Stop the game. Get a higher value than the bot to win twice the bet. Go over 21 and you lose the bet. Get exactly 21 to win triple the bet. if bet is 0 you get free points if you win. \
        \n`{ctxprefix}tr <destination language code> <message>` - translates a message to the specified language.\
        \n`{ctxprefix}create` - creates a profile if there isn't one.\
        \n`{ctxprefix}leaderboard (alias: lb)` - shows the points leaderboard.\
        \n`{ctxprefix}ping` - shows the latency.\
        \n`{ctxprefix}profile (alias: p)` - shows your profile.\
        \n`{ctxprefix}dice <bet>` - play a game of dice. if you roll higher than the bot, you win 10x the bet. if you roll lower than the bot, you lose the bet.\
        \n`{ctxprefix}invite` - use this command to invite the bot to your server!\
        \n`{ctxprefix}magic_8ball` - ask the magic 8ball a question.\
        \n`{ctxprefix}send <message>` - send a message through the bot in the current channel."
    )
    embed2=discord.Embed()
    embed2.set_footer(text='Made by zl385#9363. Page 2')
    embed2.add_field(
        name='List of commands (cont.)',
        value=f"`{ctxprefix}coinflip <bet> (alias: cf)` - flips a coin. guess correctly to win double the bet. guess wrong and you lose the bet.\
        \n`{ctxprefix}now` - shows the date and time."
    )
    await ctx.send(embed=embed1)
    await ctx.send(embed=embed2)

@client.command(name='ping')
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms.')

@client.command(aliases=['bj'])
async def blackjack(ctx, bet):
    ctxprefix=str(ctx.message.content)[0:2]
    placeholder=0
    zero=False
    player_cards=[]
    player_view=[]
    bot_cards=[]
    bot_view_end=[]
    bot_view=[]
    cmds=['hit','stand']
    author_id=str(ctx.author.id)
    def check(m):
        if m.author == ctx.author:
            return True
        return False
    try:
        points=db[author_id]["points"]
    except:
        await ctx.send(f'**Create an accound first by doing `{ctxprefix}create`**')
        return 
    if str(bet)=='all':
        bet=points
    elif str(bet)=='half':
        bet=int(points/2)
    elif bet.isdigit()==True:
        bet=int(bet)
    else:
        await ctx.send('Invalid bet.')
        return
    if bet > points:
        await ctx.send("You don't have that much points!")
        return
    elif bet==0:
        bet=100
        zero=True
    for i in range(4):
        placeholder=randint(1,13) 
        if i < 2:
            if placeholder>10:
                player_cards.append(10)
                if placeholder==11:
                    player_view+='J'
                elif placeholder==12:
                    player_view+='Q'
                else:
                    player_view+='K'
            elif placeholder==1:
                player_cards.append(1)
                player_view+='A'
            else:
                player_cards.append(placeholder)
                player_view.append(placeholder)
        else:
            if placeholder>10:
                bot_cards.append(10)
                if placeholder==11:
                    bot_view_end+='J'
                elif placeholder==12:
                    bot_view_end+='Q'
                else:
                    bot_view_end+='K'
            elif placeholder==1:
                bot_cards.append(1)
                bot_view_end+='A'
            else:
                bot_cards.append(placeholder)
                bot_view_end.append(placeholder)
    bot_view.append(bot_view_end[0])
    bot_view += ['???']
    embed=discord.Embed(title=f"{ctx.author.name}'s blackjack game", description=f"**{ctx.author.name} --- {player_view} --- {sum(player_cards)}\nDealer --- {bot_view} --- ???**")
    await ctx.send(embed=embed)
    if sum(player_cards)==21:
        embed=discord.Embed(
                title=f"{ctx.author.name}'s blackjack game",
                description=f"**Blackjack!\
                \n{ctx.author.name} --- {player_view} --- {sum(player_cards)}\
                \nDealer --- {bot_view_end} --- {sum(bot_cards)}\
                \nCongrats, you won {bet*2} points!**"
            )
        await ctx.send(embed=embed)
        update(author_id, "points", db[author_id]["points"]+{bet*2})
        return
    elif sum(bot_cards)==21:
        embed=discord.Embed(
                title=f"{ctx.author.name}'s blackjack game",
                description=f"**Dealer blackjack.\
                \n{ctx.author.name} --- {player_view} --- {sum(player_cards)}\
                \nDealer --- {bot_view_end} --- {sum(bot_cards)}\
                \nRip you lost {bet*2} points.**"
            )
        await ctx.send(embed=embed)
        update(author_id, "points", db[author_id]["points"]-bet*2)
        if zero==True:
            update(author_id, "points", db[author_id]["points"]+bet*2)
        return
    while True:
        embed=discord.Embed(title=f"{ctx.author.name}'s blackjack game")
        await ctx.send('**Hit/Stand? **')
        msg=await client.wait_for('message', check=check)
        cmd=msg.content.lower()
        while cmd not in cmds:
            await ctx.send('**Invalid command. Hit/Stand?**')
            msg=await client.wait_for('message', check=check)
            cmd=msg.content.lower()
        if cmd == 'hit':
            placeholder=randint(1,13)
            if placeholder>10:
                player_cards.append(10)
                if placeholder==11:
                    player_view+='J'
                elif placeholder==12:
                    player_view+='Q'
                else:
                    player_view+='K'
            elif placeholder==1:
                player_cards.append(1)
                player_view+='A'
            else:
                player_cards.append(placeholder)
                player_view.append(placeholder)
            if sum(bot_cards)<17:
                placeholder=randint(1, 13)
                if placeholder>10:
                    bot_cards.append(10)
                    if placeholder==11:
                        bot_view_end+='J'
                    elif placeholder==12:
                        bot_view_end+='Q'
                    else:
                        bot_view_end+='K'
                elif placeholder==1:
                    bot_cards.append(1)
                    bot_view_end+='A'
                else:
                    bot_cards.append(placeholder)
                    bot_view_end.append(placeholder)
        elif cmd=='stand':
            if sum(bot_cards)<17:
                placeholder=randint(1, 13)
                if placeholder>10:
                    bot_cards.append(10)
                    if placeholder==11:
                        bot_view_end+='J'
                    elif placeholder==12:
                        bot_view_end+='Q'
                    else:
                        bot_view_end+='K'
                elif placeholder==1:
                    bot_cards.append(1)
                    bot_view_end+='A'
                else:
                    bot_cards.append(placeholder)
                    bot_view_end.append(placeholder)
            if sum(player_cards)==21:
                embed=discord.Embed(
                    title=f"{ctx.author.name}'s blackjack game",
                    description=f"**Blackjack!\
                    \n{ctx.author.name} --- {player_view} --- {sum(player_cards)}\
                    \nDealer --- {bot_view_end} --- {sum(bot_cards)}\
                    \nCongrats, you won {bet*2} points!**"
                    )
                await ctx.send(embed=embed)
                update(author_id, "points", db[author_id]["points"]+bet*2)
                return
            elif sum(bot_cards)==21:
                embed=discord.Embed(
                    title=f"{ctx.author.name}'s blackjack game",
                    description=f"**Dealer blackjack\
                    \n{ctx.author.name} --- {player_view} --- {sum(player_cards)}\
                    \nDealer --- {bot_view_end} --- {sum(bot_cards)}\
                    \nRip you lost {bet*2} points**"
                    )
                await ctx.send(embed=embed)
                update(author_id, "points", db[author_id]["points"]-bet*2)
                if zero==True:
                    update(author_id, "points", db[author_id]["points"]+bet*2)
                return
            elif sum(bot_cards)>21:
                embed=discord.Embed(
                title=f"{ctx.author.name}'s blackjack game",
                description=f"**Dealer bust\
                \n{ctx.author.name} --- {player_view} --- {sum(player_cards)}\
                \nDealer --- {bot_view_end} --- {sum(bot_cards)}\
                \nCongrats, you won {bet} points!**"
                )
                await ctx.send(embed=embed)
                update(author_id, "points", db[author_id]["points"]+bet)
                return
            elif sum(player_cards)>sum(bot_cards):
                embed=discord.Embed(
                    title=f"{ctx.author.name}'s blackjack game",
                    description=f"**{ctx.author.name} --- {player_view} --- {sum(player_cards)}\
                \nDealer --- {bot_view_end} --- {sum(bot_cards)}\
                \nCongrats, you won {bet} points!**"
                )
                await ctx.send(embed=embed)
                update(author_id, "points", db[author_id]["points"]+bet)
                return
            elif sum(player_cards)<sum(bot_cards):
                embed=discord.Embed(
                    title=f"{ctx.author.name}'s blackjack game",
                    description=f"**{ctx.author.name} --- {player_view} --- {sum(player_cards)}\
                \nDealer --- {bot_view_end} --- {sum(bot_cards)}\
                \nRip you lost {bet} points.**"
                )
                await ctx.send(embed=embed)
                update(author_id, "points", db[author_id]["points"]-bet)
                if zero==True:
                    update(author_id, "points", db[author_id]["points"]+bet)
                return
            elif sum(player_cards)==sum(bot_cards):
                embed=discord.Embed(
                    title=f"{ctx.author.name}'s blackjack game",
                    description=f"**{ctx.author.name} --- {player_view} --- {sum(player_cards)}\
                \nDealer --- {bot_view_end} --- {sum(bot_cards)}\
                \nDraw.**"
                )
                await ctx.send(embed=embed)
                return
        if sum(player_cards)==21:
            embed=discord.Embed(
                title=f"{ctx.author.name}'s blackjack game",
                description=f"**Blackjack!\
                \n{ctx.author.name} --- {player_view} --- {sum(player_cards)}\
                \nDealer --- {bot_view_end} --- {sum(bot_cards)}\
                \nCongrats, you won {bet*2} points!**"
                )
            await ctx.send(embed=embed)
            update(author_id, "points", db[author_id]["points"]+bet*2)
            return
        elif sum(bot_cards)==21:
            embed=discord.Embed(
                title=f"{ctx.author.name}'s blackjack game",
                description=f"**Dealer blackjack\
                \n{ctx.author.name} --- {player_view} --- {sum(player_cards)}\
                \nDealer --- {bot_view_end} --- {sum(bot_cards)}\
                \nRip you lost {bet*2} points.**"
                )
            await ctx.send(embed=embed)
            update(author_id, "points", db[author_id]["points"]-bet*2)
            if zero==True:
                update(author_id, "points", db[author_id]["points"]+bet*2)
            return
        elif sum(bot_cards)>21:
            embed=discord.Embed(
                title=f"{ctx.author.name}'s blackjack game",
                description=f"**Dealer bust\
                \n{ctx.author.name} --- {player_view} --- {sum(player_cards)}\
                \nDealer --- {bot_view_end} --- {sum(bot_cards)}\
                \nCongrats, you won {bet} points!**"
                )
            await ctx.send(embed=embed)
            update(author_id, "points", db[author_id]["points"]+bet)
            return
        elif sum(player_cards)>21:
            embed=discord.Embed(
                title=f"{ctx.author.name}'s blackjack game",
                description=f"**Player bust\
                \n{ctx.author.name} --- {player_view} --- {sum(player_cards)}\
                \nDealer --- {bot_view_end} --- {sum(bot_cards)}\
                \nRip you lost {bet} points.**"
                )
            await ctx.send(embed=embed)
            update(author_id, "points", db[author_id]["points"]-bet)
            if zero==True:
                update(author_id, "points", db[author_id]["points"]+bet)
            return
        embed=discord.Embed(
            title=f"{ctx.author.name}'s blackjack game",
            description=f'**{ctx.author.name} --- {player_view} --- {sum(player_cards)}\nDealer --- {bot_view} --- ???**'
            )
        await ctx.send(embed=embed)

@client.command(aliases=['tr'])
async def translate(ctx,lang,*msg):
    translator=Translator()
    msg=' '.join(msg)
    translation=translator.translate(msg,dest=lang)
    language=translator.detect(msg).lang
    embed=discord.Embed(title='', description=translation.text,colour=ctx.author.top_role.colour)
    embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
    embed.set_footer(text=f"Translated from {language}")
    await ctx.send(embed=embed)

@tasks.loop(seconds=1.0)
async def remove_negative():
    for i in db:
        points=db[i]["points"]
        if points<0:
            update(i, "points", 0)

@client.command()
async def create(ctx):
    author_id=str(ctx.author.id)
    try:
        points=db[author_id]["points"]
        await ctx.send('You already have a profile.')
    except KeyError:
        await ctx.send('__**Creating profile...**__')
        db[author_id]={
            "name": ctx.author.name,
            "points": 0
        }
        await ctx.send('__**Profile created!**__')

@client.command()
async def list_db(ctx):
    if str(ctx.author.id) in admin:
        for i in db:
            await ctx.send(db[i])

@client.command()
async def clear_db(ctx):
    if str(ctx.author.id) in admin:
        for i in db:
            del db[i]
        await ctx.send('Database cleared')

@client.command(aliases=['p'])
async def profile(ctx):
    author_id=str(ctx.author.id)
    ctxprefix=str(ctx.message.content)[0:2]
    try:
        name=db[author_id]["name"]
        points=db[author_id]["points"]
        embed=discord.Embed(title=f"{name}'s Profile", description=f"Points: {points}")
        await ctx.send(embed=embed)
    except KeyError:
        await ctx.send(f"Profile not found. Please create one with {ctxprefix}create")

@client.command(aliases=['lb'])
async def leaderboard(ctx):
    names=[]
    points=[]
    count=0
    for i in db:
        names.append(db[i]["name"])
        points.append(db[i]["points"])
    embed=discord.Embed(title='Leaderboard')
    for i in range(len(names)):
	    count+=1
	    index = points.index(max(points))
	    embed.add_field(name=f"**{count} - {names[index]}**",
		                value=f"__{points[index]}__",
		                inline=False)
	    points.pop(index)
	    names.pop(index)
    await ctx.send(embed=embed)

@client.command()
async def dice(ctx,bet):
    author_id=str(ctx.author.id)
    ctxprefix=str(ctx.message.content)[0:2]
    try:
        points=db[author_id]["points"]
    except:
        await ctx.send(f'**Create an accound first by doing `{ctxprefix}create`**')
        return
    if str(bet)=='all':
        bet=points
    elif str(bet)=='half':
        bet=int(points/2)
    elif bet.isdigit()==True:
        bet=int(bet)
    else:
        await ctx.send('Invalid bet.')
        return
    if bet > points:
        await ctx.send("You don't have that much points!")
    else:
        bot_dice=randint(1,6)
        player_dice=randint(1,6)
        if bot_dice<player_dice:
            embed=discord.Embed(
                title=f"{ctx.author.name}'s dice game",
                description=f"**{ctx.author.name} rolled {player_dice}\
                \nzl835 rolled {bot_dice}\
                \nCongrats you won {bet*10} points!**"
                )
            update(author_id, "points", db[author_id]["points"]+bet*9)
        elif bot_dice>player_dice:
            embed=discord.Embed(
                title=f"{ctx.author.name}'s dice game",
                description=f"**{ctx.author.name} rolled {player_dice}\
                \nzl835 rolled {bot_dice}\
                \nRip you lost {bet} points.**"
                )
            update(author_id, "points", db[author_id]["points"]-bet)
        elif bot_dice==player_dice:
            embed=discord.Embed(
                title=f"{ctx.author.name}'s dice game",
                description=f"**{ctx.author.name} rolled {player_dice}\
                \nzl835 rolled {bot_dice}\
                \nDraw. Bet returned.**"
                )
        await ctx.send(embed=embed)

@client.command()
async def add(ctx,id,amt):
    if str(ctx.author.id) in admin:
        author_id=id
        amt=int(amt)
        try:
            points=db[author_id]["points"]
        except:
            await ctx.send('**ID not found.**')
            return
        update(author_id, "points", db[author_id]["points"]+amt)
        await ctx.send('Points added')
    else:
        await ctx.send("You can't do this peasent.")

@client.command()
async def send(ctx, *text):
    text=' '.join(text)
    await ctx.send(text)
    await ctx.message.delete()

@client.command()
async def invite(ctx):
    text="https://discord.com/api/oauth2/authorize?client_id=905985060346408961&permissions=8&scope=bot"
    await ctx.send(f'Use this link to invite me! {text}')
    
@client.command()
async def magic_8ball(ctx):
    responses=["Yes.", "No.", "Are you dumb???", "No shit...", "When you grow a braincell, yes.", "Bruh.", "No you idiot.", "Only God can help you there.", "Do dogs talk?", "Obviously... even a blind man can see it.", "Yea sure.",  "Stop asking me stupid questions.", "I doubt it.", "As surely as 1+1=3", "This ain't worth the processor cycles.", "Uh whatever."]
    await ctx.send(choice(responses))

@client.command(aliases=["cf"])
async def coinflip(ctx, bet):
    def check(m):
        if m.author == ctx.author:
            return True
        return False
    author_id=str(ctx.author.id)
    ctxprefix=str(ctx.message.content)[0:2]
    possibilities=['heads', 'tails', 'side']
    try:
        points=db[author_id]["points"]
    except:
        await ctx.send(f'**Create an accound first by doing `{ctxprefix}create`**')
        return
    if str(bet)=='all':
        bet=points
    elif str(bet)=='half':
        bet=int(points/2)
    elif bet.isdigit()==True:
        bet=int(bet)
    else:
        await ctx.send('Invalid bet.')
        return
    if bet > points:
        await ctx.send("You don't have that much points!")
    else:
        number=randint(0,1000)
        result=''
        if number==0:
            result=possibilities[2]
        else:
            result=possibilities[number%2]
        await ctx.send("Heads or Tails?")
        msg=await client.wait_for('message', check=check)
        cmd=msg.content.lower()
        if cmd==result:
            embed=discord.Embed(
                title=f"{ctx.author.name}'s coinflip game",
                description=f"**Coin landed on {result}!\
                \nYou won {bet} points!**"
                )
            update(author_id, "points", db[author_id]["points"]+bet)
        elif result=='side':
            embed=discord.Embed(
                title=f"{ctx.author.name}'s coinflip game",
                description=f"**Coin landed on {result}!\
                \nYou lost {bet*100} points!**"
                )
            update(author_id, "points", db[author_id]["points"]-bet*100)
        else:
            embed=discord.Embed(
                title=f"{ctx.author.name}'s coinflip game",
                description=f"**Coin landed on {result}!\
                \nYou lost {bet} points!**"
                )
            update(author_id, "points", db[author_id]["points"]-bet)
        await ctx.send(embed=embed)

@client.command()
async def now(ctx):
    tz = pytz.timezone('Asia/Singapore')
    current_datetime=datetime.now(tz)
    d=current_datetime.day
    m=current_datetime.month
    y=current_datetime.year
    H=current_datetime.hour
    M=current_datetime.minute
    S=current_datetime.second
    embed=discord.Embed(
        title="Current Date and Time",
        description=""
    )
    embed.add_field(
        name="Date",
        value=f"{d}/{m}/{y}"
    )
    embed.add_field(
        name="Time",
        value=f"{H}:{M}:{S}"
    )
    await ctx.send(embed=embed)

@tasks.loop(seconds=1.0)
async def daily_interest():
    current_time=datetime.now()
    target_time=datetime(current_time.year, current_time.month, current_time.day) + timedelta(days = 1)
    time_diff=(target_time-current_time).total_seconds()
    if time_diff<1 or time_diff>86399: 
        for i in db:
            points=floor((db[i]["points"])*1.1)
            update(i, "points", points)

@client.command()
async def addall(ctx, points):
    points=int(points)
    for i in db:
        update(i, "points", db[i]["points"]+points)
    await ctx.send("FREE POINTS FOR EVERYONE!!!")


remove_negative.start()  
daily_interest.start()
keep_alive()
client.run(my_secret)    