# A bot for the folks over on the John Mulaney Discord server!

# TODO: This contains some unnecessary imports
from math import remainder
from discord.ext.commands.errors import ConversionError, NoEntryPointError
import numpy as np

import discord as dc
from discord import channel, file, guild, user
from discord.abc import User
from discord.ext import commands

from dotenv import load_dotenv
import os, sys, traceback
from random import choice

import network as nw
network = nw.NeuralNetwork()
import json
import time

# END OF IMPORTS
# BEGINNING OF BOT SETUP

def get_prefix(bot, message):
    prefixes = ['$'] # This is expandable (hence the list)
    return commands.when_mentioned_or(*prefixes)(bot, message)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

initial_extensions = ['cogs.fun', 'cogs.admin']

intents = dc.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=get_prefix, intents=intents)

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

message_ctx = 'unknown'

guilds = ''
for i, guild in bot.guilds:
    guilds += str(i + 1) + ". " + str(guild.name) + '\n'

guild: dc.Guild
prev_messager: dc.User = None
time_tracker = time.time()

def chat(message: dc.Message):
    sentence = message.content
    result = network.classify(sentence)
    try:
        result_tag = result[0][0]
        intents = network.training_data['intents']
    
        for intent in intents:
            if intent['tag'] == result_tag:
                response_tag = intent

        return response_tag
    except IndexError:
        if message.content != '1':
            with open('unknown.json') as file:
                unknown = json.load(file)
            sentence = sentence.lower()
            if sentence in unknown:
                unknown[sentence] += 1
            else:
                unknown[sentence] = 1
            unknown = {k: v for k, v in sorted(unknown.items(), key=lambda item: item[1], reverse=True)}
            with open('unknown.json', 'w') as file:
                json.dump(unknown, file, indent=4, sort_keys=False)
            print("saved unknown sentence to: unknown.json")
        return None

message_ctx = 'unknown'
guilds = ''

current_guild: dc.Guild
prev_messager: dc.User = None
time_tracker = time.time()


@bot.event
async def on_ready():
    global guilds
    print(f'{bot.user} is online!')
    game=dc.Game(name='Modding the server!', type=1, url='http://www.johnmulaney.com/')

    await bot.change_presence(status=dc.Status.online, activity=game)
    if len(bot.guilds) == 1:
        guilds = '1. ' + bot.guilds[0].name
    else:
        for i, guild in bot.guilds:
            guilds += str(i + 1) + ". " + str(guild.name) + '\n'

@bot.event
async def on_member_join(ctx, member):
    guild = ctx.guild
    channel = bot.get_channel(850634285975076904)
    await channel.send(
        f'Hi {member.name}, welcome to the John Mulaney Discord server!'
        f'You\'ll have tons of fun talking about Mulaney with {len(guild.members)}'
        f'more people! To prove, _prove_ you\'re not a robot, just check out the #rules and then jump into #main-chat!'
    )

@bot.event
async def on_message(message: dc.Message):
    if message.guild == None:
        global message_ctx
        global current_guild
        global guilds
        global prev_messager
        global time_tracker

        response_tag = chat(message)
        print(message.author)
        print(message_ctx)

        if time.time() - time_tracker > 60:
            prev_messager = None
            message_ctx = 'unknown'

        if message.author != prev_messager and prev_messager != None:
            await message.author.send("Sorry, I'm having a conversation with someone else right now, but check back in a minute!")
            return

        if message.author == bot.user:
            return

        if response_tag == None and message_ctx != 'choose_server' and message_ctx != 'send_dm' and message.guild == None:
            await message.author.send("Sorry, I don't know what that means, but my creator will help me learn!")
            message_ctx = 'unknown'
            prev_messager = message.author
            time_tracker = time.time()
            return

        if message_ctx == 'send_dm':
            print(current_guild)
            admins = []
            blacklist = open("blacklist.txt").read().splitlines()

            for member in current_guild.members:
                for role in member.roles:
                    if role.name == "administrator" or role.name == "owner":
                        admins.append(member)
                        
            if message.author != bot.user and str(message.content)[0] != '$':
                if str(message.author) in blacklist:
                    await message.author.send("You have been added to the blacklist. You cannot send a DM to the admin team!")
                    prev_messager = None
                    return
                await message.author.send("Sending DM...")
                # for admin in admins:
                #     await admin.send(f'User {message.author} sent this message to the admin team: {message.content}')
                #     await admin.send(f'If you want to blacklist this user, simply type\n```\n$blacklist @User\n```\nin the server, replacing that with the user\'s username')
                await message.author.send("DM sent!")
                await message.author.send("You can dismiss me for other people to use by saying bye!")
            return
        elif message_ctx == 'choose_server':
            try:
                chosen_number = int(message.content) - 1
            except ValueError:
                await message.author.send(f'{message.content} is not a valid integer...')
                message_ctx = 'unknown'
                return
            try:
                chosen_guild = bot.guilds[chosen_number]
            except IndexError:
                await message.author.send(f'{message.content} wasn\'t one of the options...')
                message_ctx = 'unknown'
                return
            current_guild = dc.utils.find(lambda g: g == chosen_guild, bot.guilds)
            await message.author.send("What should the content of the message be?")
            message_ctx = 'send_dm'
            time_tracker = time.time()
            return
        
        if response_tag['tag'] == 'dm':
            await message.author.send("Which server's admins would you like to DM? (please enter a number)")
            await message.author.send(guilds)
            message_ctx = 'choose_server'
            prev_messager = message.author
            time_tracker = time.time()
            return
        
        response = np.random.choice(response_tag['responses'])
        await message.author.send(response)
        message_ctx = response_tag['tag']
        if response_tag['tag'] == 'farewell':
            prev_messager = None
        else:
            prev_messager = message.author
    await bot.process_commands(message)
        

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

bot.run(TOKEN, bot=True, reconnect=True)
