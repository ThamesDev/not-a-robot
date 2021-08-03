# import discord as dc
# from discord import member
# from discord.ext import commands
# from dotenv import load_dotenv
# from os import getenv

# from discord.ext.commands import bot

# load_dotenv()
# GUILD = getenv('DISCORD_GUILD')

# class Admin(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
    
#     @commands.command(name='blacklist', aliases=[' blacklist', 'Blacklist', ' Blacklist'], help='Blacklist a user from being able to DM the admins')
#     async def blacklist(ctx, user: dc.member=None):
#         is_admin = False
#         guild = dc.utils.find(lambda g: g.name == GUILD, bot.guilds)

#         for role in user.roles:
#             if role.name == "administrator" or role.name == "owner":
#                 is_admin = True
#         if is_admin:
#             if user == None:
#                 await ctx.send("Error: you must select a user to blacklist")
#             elif not (user in guild.members):
#                 await ctx.send("Error: that member doesn't exist in this server")
#             else:
#                 await ctx.send("Blacklisting user... (don't worry this is just a test)")

# def setup(bot):
#     bot.add_cog(Admin(bot))
