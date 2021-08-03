import discord as dc
from discord.ext import commands
from random import choice

from discord.ext.commands import bot

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='mulaney', aliases=['Mulaney'], help='Responds with a random John Mulaney quote!')
    async def mulaney_gen(self, ctx):
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

        response = choice(mulaney_quotes)
        await ctx.send(response)

def setup(bot):
    bot.add_cog(Fun(bot))
