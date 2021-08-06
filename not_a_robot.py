# A bot for the folks over on the John Mulaney Discord server!

# TODO: This contains some unnecessary imports
from math import remainder
from discord import channel, file, guild, user
from discord.abc import User
from dotenv import load_dotenv
import os, sys, traceback
import discord as dc
from discord.ext import commands
from random import choice
import network as nw
import json
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy as np
import time

# END OF IMPORTS
# BEGINNING OF NEURAL NETWORK SETUP

with open('intents.json') as json_data:
    training_data = json.load(json_data)

words = []
classes = []
documents = []
ignore_words = ['?', '\'', '!', '.', ',', 'to', 'a', 'the']

for intent in training_data['intents']:
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)

        words.extend(w)
        documents.append((w, intent['tag']))

        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

classes = sorted(list(set(classes)))

print (len(documents), "documents", documents)
print (len(classes), "classes", classes)
print (len(words), "unique stemmed words", words)

training = []
output = []

output_empty = [0] * len(classes)

for doc in documents:
    bag = []
    pattern_words = doc[0]
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)
    
    training.append(bag)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    output.append(output_row)

X = np.array(training)
y = np.array(output)

network = nw.NeuralNetwork()
start_time = time.time()

overwrite = False

if not overwrite:
    with open(network.synapse_file) as data_file: 
        synapse = json.load(data_file) 
        synapse_0 = np.asarray(synapse['synapse0']) 
        synapse_1 = np.asarray(synapse['synapse1'])

network.train(X, y, hidden_neurons=20, alpha=0.1, epochs=100000, dropout=False, dropout_percent=0.2, overwrite=overwrite, synapse_0=synapse_0, synapse_1=synapse_1)

if overwrite:
    elapsed_time = time.time() - start_time
    print("processing time:", elapsed_time, "seconds")
    with open(network.synapse_file) as data_file: 
        synapse = json.load(data_file) 
        synapse_0 = np.asarray(synapse['synapse0']) 
        synapse_1 = np.asarray(synapse['synapse1'])

while True:
    sentence = input("> ")
    result = network.classify(sentence)
    try:
        result_tag = result[0][0]
        intents = training_data['intents']
    
        for intent in intents:
            if intent['tag'] == result_tag:
                response_tag = intent

        response = np.random.choice(response_tag['responses'])
        print(response)

        if response_tag['tag'] == 'farewell':
            break
    except IndexError:
        print("I'm not sure what that means...")
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

# END OF NEURAL NETWORK SETUP
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

@bot.event
async def on_ready():
    # guild = dc.utils.find(lambda g: g.name == GUILD, bot.guilds)
    print(f'{bot.user} is online!')
    
    # members = ', '.join([member.name for member in guild.members])
    # print(f'Guild Members:\n{members}')
    # send_channel = bot.get_channel(850642371318513684)
    game=dc.Game(name='Modding the server!', type=1, url='http://www.johnmulaney.com/')

    await bot.change_presence(status=dc.Status.online, activity=game)
    # await send_channel.send("NotARobot is online!")

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
    # network = nw.NeuralNetwork()
    admins = []
    blacklist = open("blacklist.txt").read().splitlines()

    guild = dc.utils.find(lambda g: g.name == GUILD, bot.guilds)
    for member in guild.members:
        for role in member.roles:
            if role.name == "administrator" or role.name == "owner":
                admins.append(member)
                
    if message.guild is None and message.author != bot.user and str(message.content)[0] != '$':
        if str(message.author) in blacklist:
            await message.author.send("You have been added to the blacklist. You cannot send a DM to the admin team!")
            return
        await message.author.send("Sending DM...")
        for admin in admins:
            await admin.send(f'User {message.author} sent this message to the admin team: {message.content}')
            await admin.send(f'If you want to blacklist this user, simply type\n```\n$blacklist @User\n```\nin the server, replacing that with the user\'s username')
        await message.author.send("DM sent!")
    await bot.process_commands(message)
        

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

bot.run(TOKEN, bot=True, reconnect=True)
