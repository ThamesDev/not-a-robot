# A bot for the folks over on the John Mulaney Discord server!

# TODO: forward message from user to mods, add mod list and enable mods to add more, server interface, Mulaney quotes,
#       user blacklist, bug reporting

from dotenv import load_dotenv
import os
import discord as dc

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = dc.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(f'{client.user} has connected to the following server:\n'
          f'{guild.name} (id: {guild.id})')

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


client.run(TOKEN)
