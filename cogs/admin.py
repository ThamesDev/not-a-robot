import discord as dc
from discord import member
import discord
from discord.ext import commands
from discord.ext.commands.errors import MemberNotFound
from dotenv import load_dotenv
from os import getenv, write

from discord.ext.commands import bot

load_dotenv()
GUILD = getenv('DISCORD_GUILD')

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='blacklist', aliases=['Blacklist'], help='Blacklist a user from being able to DM the admins')
    async def blacklist(self, ctx: commands.Context, member: dc.Member=None):
        is_admin = False
        guild = dc.utils.find(lambda g: g.name == GUILD, self.bot.guilds)

        if member == None:
            await ctx.send("Error: you must select a user to blacklist!\nThe syntax is\n```\n$blacklist @User\n```")
            return
        
        for role in ctx.author.roles:
            if role.name == "administrator" or role.name == "owner":
                is_admin = True
        if is_admin:  
            if member in guild.members:
                await ctx.send("Blacklisting user...")
                with open('blacklist.txt', 'a') as f:
                    f.write(str(member))
                    f.write('\n')
                await ctx.send("User added to blacklist.")

    @blacklist.error
    async def kick_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MemberNotFound):
            print("Error: a handled exception has occured!")
            await ctx.send("Error: guild member not found!")

    @commands.command(name='whitelist', aliases=['Whitelist'], help='Un-blacklist a user so they can DM the admins again')
    async def whitelist(self, ctx: commands.Context, member: dc.Member=None):
        is_admin = False
        guild = dc.utils.find(lambda g: g.name == GUILD, self.bot.guilds)

        if member == None:
            await ctx.send("Error: you must select a user to whitelist!\nThe syntax is\n```\n$whitelist @User\n```")
            return
        
        for role in ctx.author.roles:
            if role.name == "administrator" or role.name == "owner":
                is_admin = True
        if is_admin:  
            if member in guild.members:
                await ctx.send("Whitelisting user...")
                
                read_blacklist = open('blacklist.txt', 'r')
                lines = read_blacklist.readlines()
                read_blacklist.close()

                write_blacklist = open('blacklist.txt', 'w')

                for line in lines:
                    if line.strip('\n') != str(member):
                        write_blacklist.write(line)
                write_blacklist.close()
                
                await ctx.send("User removed from blacklist.")

    @whitelist.error
    async def kick_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MemberNotFound):
            print("Error: a handled exception has occured!")
            await ctx.send("Error: guild member not found!")

def setup(bot):
    bot.add_cog(Admin(bot))
