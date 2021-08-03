# A bot for the folks over on the John Mulaney Discord server!

# TODO: forward message from user to mods, add mod list and enable mods to add more, server interface, Mulaney quotes,
#       user blacklist, bug reporting

from discord import channel
from dotenv import load_dotenv
import os
import discord as dc
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = dc.Client()

@client.event
async def on_ready():
    guild = dc.utils.find(lambda g: g.name == GUILD, client.guilds)

    print(f'{client.user} has connected to the following server:\n'
          f'{guild.name} (id: {guild.id})')

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    send_channel = client.get_channel(850642371318513684)
    await send_channel.send("Test message")

@client.event
async def on_member_join(member):
    await member.create_dm()
    guild = dc.utils.find(lambda g: g.name == GUILD, client.guilds)
    channel = client.get_channel(850634285975076904)
    await channel.send(
        f'Hi {member.name}, welcome to the John Mulaney Discord server! You\'ll have tons of fun talking about Mulaney with {len(guild.members)} more people! To prove, _prove_ you\'re not a robot, just check out the #rules and then jump into #main-chat!'
    )

client.run(TOKEN)
