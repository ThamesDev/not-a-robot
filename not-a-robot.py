# A bot for the folks over on the John Mulaney Discord server!

# TODO: forward message from user to mods, add mod list and enable mods to add more, server interface, Mulaney quotes,
#       user blacklist, bug reporting

from math import remainder
from discord import channel
from dotenv import load_dotenv
import os, sys, traceback
import discord as dc
from discord.ext import commands
from random import choice

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

initial_extensions = ['cogs.fun']

bot = commands.Bot(command_prefix='$')

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    guild = dc.utils.find(lambda g: g.name == GUILD, bot.guilds)

    print(f'{bot.user} has connected to the following server:\n'
          f'{guild.name} (id: {guild.id})')
    
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    send_channel = bot.get_channel(850642371318513684)
    game=dc.Game(name='Modding the server!', type=1, url='http://www.johnmulaney.com/')

    await bot.change_presence(status=dc.Status.idle, activity=game)
    await send_channel.send("NotARobot is online!")

@bot.event
async def on_member_join(member):
    guild = dc.utils.find(lambda g: g.name == GUILD, bot.guilds)
    channel = bot.get_channel(850634285975076904)
    await channel.send(
        f'Hi {member.name}, welcome to the John Mulaney Discord server!'
        f'You\'ll have tons of fun talking about Mulaney with {len(guild.members)}'
        f'more people! To prove, _prove_ you\'re not a robot, just check out the #rules and then jump into #main-chat!'
    )

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

bot.run(TOKEN, bot=True, reconnect=True)
