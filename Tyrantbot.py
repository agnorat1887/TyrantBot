import discord
from discord.ext import commands
from datetime import datetime, timedelta
import random
from asyncio import sleep
import numpy

import sys

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='?', intents=intents)

startdate = datetime.utcnow() - timedelta(hours=5)
print(startdate)

bot.count  = 19
bot.word = ""
bot.date = (startdate - timedelta(hours=startdate.hour, minutes=startdate.minute, seconds=startdate.second, microseconds=startdate.microsecond)) + timedelta(days = 1)

def round_date(dat):
    dat = (dat - timedelta(hours=dat.hour, minutes=dat.minute, seconds=dat.second, microseconds=dat.microsecond)) + timedelta(days=1)
    return dat

def utcToEst(dat):
    return dat - timedelta(hours=5)

def checkOwnerOrInsurgent(user):
    if user.id == user.guild.owner.id:
        return True
    elif user.id == 809265750220210206:
        return True
    else:
        return False

def oddsEquation(x):
    if x >=28:
        return .99
    odd = 5*(((x+.5)**(1/3)-1)/((x+.5)**(1/100)))
    return odd/10

async def adds(ctx, val):
    bot.count += val
    await ctx.channel.send(f"Comrades, the glorious leader had added {val} messages. We have {bot.count+1} in reserves!")

@bot.event
async def on_ready():
    print("Bot is ready to bot it up")
    print("Start bot date: ", bot.date)


@bot.event
async def on_message(message):
    print(bot.count)
    if message.author.bot:
        return

    elif message.content == "?reserve":
        await message.channel.send(f"Comrades, we have {bot.count+1} messages in reserve")
        return

    elif message.content == "!dc" or message.content == "!rand":
        return

    if(utcToEst(message.created_at) > bot.date):
        bot.date = round_date(message.created_at)
        bot.count = 20

    if bot.count > 0  and not (checkOwnerOrInsurgent(message.author)):
        bot.count -= 1
    

    elif bot.count == 0 and not (checkOwnerOrInsurgent(message.author)):
        bot.count -= 1
        await message.channel.send(f"WE ARE OUT OF MESSAGES!!! WE CANT SEND ANYMORE TODAY @everyone")
        await ussr(bot.get_channel(788161516843171840))                       #Play russia here

    elif bot.count < 0 and bot.count > -6 and not (checkOwnerOrInsurgent(message.author)):
        bot.count -= 1
        await message.channel.send(f"DO NOT PANIC. WE ARE OUT OF MESSAGES. COMMUNISM WILL ENSURE WE WILL HAVE MORE TOMORROW @everyone")
        await message.delete()

    elif bot.count ==-6 and not (checkOwnerOrInsurgent(message.author)):
        bot.count -=1
        await message.channel.send(f"@everyone WARNING! COUP DETECTED! PREPARING TO SEND OUT SOVIET HAMMERS!!!")
        await message.delete()
    
    elif bot.count < -6 and not (checkOwnerOrInsurgent(message.author)):
        await message.author.kick(reason="PARTCIPATED IN THE COUP")
        await message.channel.send(f"@everyone {message.author.name} WAS DETECTED IN THE COUP. THEY HAVE MET THE SOVIET HAMMER.")
        await message.delete()

    
    if (bot.count+1) % 5 == 0 and not (checkOwnerOrInsurgent(message.author)) and bot.count>-1:
        if bot.count == 0:
            bot.count -= 1
            return
            
        await message.channel.send(f"ALERT!!!  We only have {bot.count+1} messages in reserve! @everyone")


    await bot.process_commands(message)

async def ussr(channel):
    voice_channel = channel
    channel = None
    if voice_channel != None:
        channel = voice_channel.name
        vc = await voice_channel.connect()
        song = discord.FFmpegOpusAudio(source="ussr.mp3")
        vc.play(song)
        while vc.is_playing():
            await sleep(1)
        await vc.disconnect()

@bot.command(pass_context = True)
async def count(ctx, args):
    server = ctx.guild
    if(server.owner.name == ctx.author.name):
        channel = ctx.channel
        bot.count = int(args) - 1
        await channel.send(f"Comrades, the TYRANT gave us enough to have {bot.count+1} messages")
    else:
        await ctx.author.kick(reason = "YOU HAVE BEEN CAUGHT TRYING TO INFILTRATE THE TYRANTS RESERVES")
        await ctx.channel.send((f"@{ctx.author.name} WAS CAUGHT TRYING TO INFILTRATE THE TYRANTS RESERVES"))

@bot.command(pass_context = True)
async def add(ctx, *, args=None):
    try:
        if(ctx.author.id == 809265750220210206):
            roll = -1
            if args is None:
                odds = oddsEquation(1)
                roll = numpy.random.choice(numpy.arange(0, 2), p=[odds, 1-odds])                                   #run the odds here
            else:
                odds = oddsEquation(int(args))
                roll = numpy.random.choice(numpy.arange(0, 2), p=[odds, 1-odds])
            
            if roll == 0:
                await ctx.author.kick(reason="YOU HAVE BEEN CAUGHT TRYING TO INFILTRATE THE TYRANTS RESERVES")
                await ctx.channel.send((f"@{ctx.author.name} WAS CAUGHT TRYING TO INFILTRATE THE TYRANTS RESERVES"))
                return
            elif roll == 1:
                await adds(ctx, int(args))
                return
            else:
                ctx.channel.send("AN ERROR HAS OCCURED")
                return

        if args is None:
            await adds(ctx, 1)
        elif(checkOwnerOrInsurgent(ctx.author)):
                await adds(ctx, int(args))
        else:
            await ctx.author.kick(reason="YOU HAVE BEEN CAUGHT TRYING TO INFILTRATE THE TYRANTS RESERVES")
            await ctx.channel.send((f"@{ctx.author.name} WAS CAUGHT TRYING TO INFILTRATE THE TYRANTS RESERVES"))

    except ValueError:
        await ctx.channel.send("Please enter a whole number")
        return
@bot.command(pass_context = True)
async def roll(ctx, *, args):
    args = args.split()
    server = ctx.guild

    if(server.owner.name == ctx.author.name):
        role_name=(args[0])
        role_id = server.roles[0]
        for role in server.roles:
            if role_name.lower() == role.name.lower():
                role_id = role
                break
        else:
            await ctx.channel.send(f"{role_name} does not exist")
            return
        bot.word = args[1]
        members = role_id.members
        for member in members:                          #Remove any bots from the members list
            if member.bot:
                members.remove(member)

        await members[random.randint(0, len(members)-1)].send(f"The email is: theinsurgent42069@gmail.com\nThis is the secret word for the bot: {bot.word}\nPlease send a DM WITH THE INFILTRATOR ACCOUNT to the tyrant to confirm everything is working as intended")

    else:
        await ctx.author.kick(reason = "YOU HAVE BEEN CAUGHT TRYING TO INFILTRATE THE INFILTRATOR")
        await ctx.channel.send((f"@{ctx.author.name} WAS CAUGHT TRYING TO INFILTRATE THE INFILTRATOR"))
        return

bot.run(str(sys.argv[1]), bot=True)