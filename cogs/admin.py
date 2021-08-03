import discord as dc
from discord import member
import discord
from discord.ext import commands
from discord.ext.commands.errors import MemberNotFound
from dotenv import load_dotenv
from os import getenv

from discord.ext.commands import bot

load_dotenv()
GUILD = getenv('DISCORD_GUILD')

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='blacklist', aliases=['Blacklist'], help='Blacklist a user from being able to DM the admins')
    async def blacklist(self, ctx, member: dc.Member=None):
        is_admin = False
        guild = dc.utils.find(lambda g: g.name == GUILD, self.bot.guilds)

        if member == None:
            await ctx.send("Error: you must select a user to blacklist!\nThe syntax is\n```\n$blacklist @User\n```")
            return

        print(member)
        
        for role in ctx.author.roles:
            if role.name == "administrator" or role.name == "owner":
                is_admin = True
        if is_admin:  
            if member in guild.members:
                await ctx.send("Blacklisting user... (don't worry this is just a test)")

    @blacklist.error
    async def kick_error(self, ctx: commands.Context, error: commands.CommandError):
        print("At least this is running...")
        if isinstance(error, commands.MemberNotFound):
            print("An exception has occured!")
            await ctx.send("Error: guild member not found!")

def setup(bot):
    bot.add_cog(Admin(bot))
