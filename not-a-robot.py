# A bot for the folks over on the John Mulaney Discord server!

# TODO: forward message from user to mods, add mod list and enable mods to add more, server interface, Mulaney quotes,
#       user blacklist, bug reporting

from dotenv import load_dotenv
import os
import discord as dc

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = dc.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
