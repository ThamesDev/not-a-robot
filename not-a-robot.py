# A bot for the folks over on the John Mulaney Discord server!

# TODO: forward message from user to mods, add mod list and enable mods to add more, server interface, Mulaney quotes,
#       user blacklist, bug reporting

from discord import channel
from dotenv import load_dotenv
import os
import discord as dc
from discord.ext import commands
from random import choice

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
    await send_channel.send("NotARobot is online!")

@client.event
async def on_member_join(member):
    await member.create_dm()
    guild = dc.utils.find(lambda g: g.name == GUILD, client.guilds)
    channel = client.get_channel(850634285975076904)
    await channel.send(
        f'Hi {member.name}, welcome to the John Mulaney Discord server!'
        f'You\'ll have tons of fun talking about Mulaney with {len(guild.members)}'
        f'more people! To prove, _prove_ you\'re not a robot, just check out the #rules and then jump into #main-chat!'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    mulaney_quotes = [
        'I was always the squarest person in the cool room, and alternatively, sometimes the weirder person at the mainstream table.',
        'Things have to be funny first, and if they want to have a point, that’s awesome.',
        'I have a lot of stories about being a kid because it was the last time I was interesting.',
        'You can do good work simply staying up all night and eating nothing but junk food, but probably not in the long term.',
        'I’m a very lucky person. I’m an idiot, and I’ve shoveled through life rather nicely so far, so I don’t feel like I deserve good treatment.'
        'All my money is in a savings account. My dad has explained the stock market to me maybe 75 times. I still don’t understand it.',
        'I like making fun of myself a lot. I like being made fun of, too. I’ve always enjoyed it. There’s just something really, really funny about someone tearing into me.',
        'You all have a relative who is an expert even though they really don’t know what they’re talking about.',
        'I can’t listen to any new songs. Because every new song is about how tonight is the night and we only have tonight. That is such 19-year-old horseshit. I want to write songs for people in their 30s called ‘Tonight’s no good. How about wednesday? Oh, you’re in Dallas Wednesday? Let’s not see each other for eight months and it doesn’t matter at all.‘',
        'I like when things are crazy. Something good comes out of exhaustion.',
        'You remember being 12, when you’re like, ‘No one look at me or I’ll kill myself.‘',
        'You’re like the kid at the sleepover who, after midnight, is like, ‘It’s tomorrow now.’ Get out of here with your technicalities. Just because you’re accurate doesn’t mean you’re interesting.',
        'It’s important to remember that life is a joke and that outlook grants a lot of perspective, but I don’t think comedy should change and become political due to other things. It should just laugh at that cosmic joke that life is all the time.',
        'I wish I could go tell 12-year-old me like I don’t worry that you just fainted in front of all the girls, one day you’ll be able to make this into an episode of TV.',
        'My vibe is like, hey you could probably pour soup in my lap and I’ll apologize to you.',
        'You have the moral backbone of a chocolate éclair.',
        'Now, I don’t know if you’ve been following the news, but I’ve been keeping my ears open and it seems like everyone everywhere is super mad about everything all the time.',
        'You can’t always see both sides of the story. Eventually, you have to pick a side and stick with it. No more equivocating. You have to commit.',
        '13-year-olds are the meanest people in the world. They terrify me to this because 8th graders will make fun of you but in an accurate way. They will get to the thing that you don’t like about you.',
        'College was like a four-year game show called ‘Do my friends hate me or do I just need to go to sleep?’',
        'We started chanting, McDonald’s, McDonald’s, McDonald’s! And my dad pulled into the drive thru, and we started cheering and then he ordered one black coffee for himself and kept driving.',
        'I don’t look older, I just look worse.',
        'Why do people shush animals? They just go ‘Shhh, hey, shhh.’ They’ve never spoken.',
        'In terms of instant relief, cancelling plans is like heroin.',
        'If it’s something very, very funny but possibly controversial, if it’s truly funny, then it’s worth doing. Things aren’t worth doing for the sake of being controversial.'
    ]

    if message.content == '$mulaney':
        response = choice(mulaney_quotes)
        print(f'Outputting message {response}')
        await message.channel.send(response)
    elif message.content == 'raise-exception':
        raise dc.DiscordException

@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

client.run(TOKEN)
